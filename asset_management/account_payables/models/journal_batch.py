# coding=utf-8
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.safe_eval import safe_eval
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.tools.float_utils import float_compare
import base64

import logging

_logger = logging.getLogger(__name__)
# mapping invoice type to refund type

class PayablesBatch(models.Model):
    _inherit='payable.batch'
    
    #journal_batch_id = fields.Many2one('journal.batch',string="GL")
    gl_report = fields.Binary()
    gl_report_fn = fields.Char('GL',default='GL Report.pdf')
    
    def generate_report_file(self):
        temp = False
        for record in self:
            pdf = self.env.ref('account_payables.action_general_posting_journal').sudo().render_qweb_pdf([record['id']])[0]
            record['gl_report'] = base64.b64encode(pdf)
            temp = base64.b64encode(pdf)
        return temp

    def print_gl_report(self):
        return self.env.ref('account_payables.action_general_posting_journal').report_action(self)
    
    def post_journal(self):
        #if lines re empty
        for invoice in self.transactions:
            if not invoice.invoice_line_ids:
                type_id = self.env['account.account.type'].sudo().search([('name','=','Expenses')])
                products = self.env['product.product'].sudo().search([('name','=','Generic')])
                accounts = self.env['account.account'].sudo().search([('user_type_id','=',type_id.id)])
                
                for s in accounts:
                    acc_single = s
                
                default_lines = self.env['account.invoice.line'].create({ 'product_id': products.id,
                                                             'name':'VENDOR PAYMENT',
                                                             'account_id': acc_single.id,
                                                             'price_unit':invoice.amount_total_signed,
                                                             'quantity':1})

                invoice.invoice_line_ids = [(4,default_lines.id)]
        #===============================
        line_totals = 0
        move_totals = 0
        journals=[]
        for inv in self.transactions:
            inv.action_invoice_open()
            if inv.move_id:
                inv.move_id.move_total = inv.amount_total_signed
                move_totals+=1
                for line_record in inv.move_id.line_ids:
                    line_totals+=1
                journals.append(inv.move_id.id)
                
        for rec in self:
            rec['batch_ref'] = self.env['ir.sequence'].next_by_code('audit.trail.code.payables')
            rec['audit_trail_code_ref'] = self.env['ir.sequence'].next_by_code('audit.trail.code.payables')
            rec['voucher_number'] = self.env['ir.sequence'].next_by_code('voucher.number.payables')
            
            rec['journals'] = [(6, 0, journals)]
            if rec['journals']:
                rec['state'] = 'posted'
                
        if self.batch_type == 'normal':   
            self.env['capture.line'].create({
                    'creditor': self.source.id,
                    'doc_number': self.doc_number,
                    'amount': self.total_amount,
                    'date': self.date,
                })
        else:
            partner_id = 0
            date_v = 0
            for invoice in rec['transactions']:
                partner_id = invoice['partner_id']['id']
                date_v = invoice['date_invoice']
                break
            b_lines = []
            for inv in rec['transactions']:
                if partner_id == inv['partner_id']['id']:
                    batch_line = self.env['capture.line'].create({
                            'creditor': inv['partner_id']['id'],
                            'doc_number': inv['invoice_number_entry'],
                            'amount': inv['amount_total_signed'],
                            'date': inv['date_invoice'],
                        })
                    b_lines.append(batch_line.id)
                else:
                    partner_id = inv['partner_id']['id']
                    self.env['creditor.recon'].create({
                        'partner_id': inv['partner_id']['id'],
                        'transactions': [(6,0,b_lines)],
                        'balance': 0.0,
                        'statement_date': inv['date_invoice'],
                    })
                    b_lines = []
                
            self.env['creditor.recon'].create({
                    'partner_id': partner_id,
                    'partner_id': partner_id,
                    'transactions': [(6,0,b_lines)],
                    'balance': 0.0,
                    'statement_date': date_v,
                })
        
        self.gl_report = self.generate_report_file()
        
        return self.env.ref('account_payables.action_print_posting_journal').report_action(self)
    
class AccountMoveLine(models.Model):
    """ Model to inherit/extend the PO"""
    _inherit = 'account.move.line'
    
    date = fields.Date('Date')

class AccountMove(models.Model):
    """ Model to inherit/extend the PO"""
    _inherit = 'account.move'
    
    jid = fields.Char('Audit Trail Code')
    move_total = fields.Float('Total')
    batch_id = fields.Char("Batch #")
    type_journal = fields.Selection([('batch','Batch'),('entry','Journal Entry')],default='entry')
    date = fields.Date("Date")
    credit_total = fields.Monetary('Credit R')
    debit_total = fields.Monetary('Debit R')
    total_control = fields.Monetary('Total')
    line_count = fields.Integer("Line count")
    gl_report = fields.Binary(compute='generate_report_file')
    gl_report_fn = fields.Char('GL',default='GL Report')
    
    '''@api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        if values:
            values['jid'] = self.env['ir.sequence'].next_by_code('audit.trail.code.journal')
            values['batch_id'] = self.env['ir.sequence'].next_by_code('audit.trail.code')
            
        record_obj = super(AccountMove, self).create(values)
        return record_obj'''
    
    @api.multi
    @api.onchange('line_ids')
    @api.depends('line_ids')
    def calculate_batch_total(self):
        sum = 0
        sum_cr = 0.0
        sum_db = 0.0
        c = 0
        for record in self:
            for rec in record['line_ids']:
                sum+=rec['credit']
                sum_db += rec['debit']
                sum_cr += rec['credit']
                c+=1
            record['move_total'] = sum
            record['credit_total'] = sum_cr 
            record['debit_total'] = sum_db
            record['total_control'] = sum_cr + sum_db
            record['line_count'] = c
    
    '''def generate_report_file(self):
        temp = False
        for record in self:
            pdf = self.env.ref('account_payables.action_general_posting_journal').sudo().render_qweb_pdf([record['id']])[0]
            record['gl_report'] = base64.b64encode(pdf)
            temp = base64.b64encode(pdf)
        return temp
    
    
    def print_gl_report(self):
        return self.env.ref('account_payables.action_general_posting_journal').report_action(self)'''
        
    
    