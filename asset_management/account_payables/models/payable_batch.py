# coding=utf-8
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.safe_eval import safe_eval
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)
# mapping invoice type to refund type

class Pinvoice(models.Model):
    """ Model to inherit/extend the PO"""
    _inherit = 'account.invoice'
    
    batch_id_payables = fields.Many2one('payable.batch')
    
    @api.onchange('purchase_id')
    def purchase_order_change(self):
        for record in self:
            if not record.purchase_id:
                return {}
            if not record.partner_id:
                for rec in record.purchase_id:
                    record.partner_id = rec.partner_id.id
            
            for r in record.purchase_id:
                total = 0
                new_lines = self.env['account.invoice.line']
                for rec in r:
                    for line in rec.order_line - self.invoice_line_ids.mapped('purchase_line_id'):
                        data = self._prepare_invoice_line_from_po_line(line)
                        new_line = new_lines.new(data)
                        new_line._set_additional_fields(self)
                        new_lines += new_line
                        total += new_line.price_subtotal
                    record.invoice_line_ids += new_lines
                    record.payment_term_id = r.payment_term_id
                record.amount_total_signed += total
            self.env.context = dict(self.env.context, from_purchase_order_change=True)
            return {}
    
    '''@api.onchange('amount_total_signed')
    def amount_total_change(self):
        if self.sales_amount != 0.0:
            self.percentage = self.amount_total_signed / self.sales_amount'''
    
    @api.onchange('sales_amount','percentage')
    def amount_po_change(self):
        for record in self:
            record['amount_total_signed'] = record['percentage'] * record['sales_amount']
    
class AccountMove(models.Model):
    """ Model to inherit/extend the PO"""
    _inherit = 'account.move'
    
    batch_id_payables = fields.Many2one('payable.batch')
    
class PayablesBatch(models.Model):
    _name="payable.batch"
    _rec_name="batch_id"
    
    doc_number = fields.Char("Doc Number")
    date = fields.Date("Document Date")
    source = fields.Many2one('res.partner',string="Creditor")
    creditor_id = fields.Char(related="source.creditor_id")
    posting_date = fields.Date("Posting Date")
    batch_id = fields.Char("Batch #")
    
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    #VP19 link
    vp_link = fields.Many2one('bcs.vsp','VP19')
    gp_link = fields.Many2one('bulk.grant.disbursment','Grant Disbursement Bulk')
    receipt_num = fields.Char('Receipt Number')
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term',default=lambda self: self.env['account.payment.term'].search([('name','=','30 Net Days')]),
        readonly=True,
        help="If you use payment terms, the due date will be computed automatically at the generation "
             "of accounting entries. If you keep the payment terms and the due date empty, it means direct payment. "
             "The payment terms may compute several due dates, for example 50% now, 50% in one month.")
    total_amount = fields.Monetary("Total Amount",compute="calculate_batch_total",store=True)
    batch_ref = fields.Char("Batch ID")
    audit_trail_code_ref = fields.Char("Batch ID")
    voucher_number = fields.Char('Voucher No.')
    transactions = fields.One2many('account.invoice','batch_id_payables',string="Transactions")
    journals = fields.One2many('account.move','batch_id_payables', string="Journal Ids")
    comment = fields.Text("Description")
    state = fields.Selection([('new','New'),('posted','Posted')],default='new')
    batch_type = fields.Selection([('cons','Consolidate'),('credit','Credit Note(s) Batch'),('normal','Normal'),('voucher','Voucher Batch'),('grant','Grant Batch')],default='normal')

    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        if values:
            values['receipt_num'] = self.env['ir.sequence'].next_by_code('receipt.number.payables')
            
        record_obj = super(PayablesBatch, self).create(values)
        return record_obj
    
    
    
    @api.depends('transactions')
    @api.onchange('transactions')
    def calculate_batch_total(self):
        sum = 0
        for record in self:
            for rec in record['transactions']:
                sum += rec['amount_total_signed'] 
            record['total_amount'] = sum
        
    def populate_po_invoice(self):
        for batch in self:
            invoices = []
            invoices_detail = []
            creditors_po = self.env['purchase.order'].sudo().search([('partner_id','=',self.source.id)])
            #create invoices per PO
            for po in creditors_po:
                accounts = self.env['account.account'].sudo().search([('code','like','000-000-000-9100')])
                account_id = self.env['account.account']
                journal_id = self.env['account.journal']
                for acc in accounts:
                    account_id = acc
                journals = self.env['account.journal'].sudo().search([('name','=','Vendor Invoices')])
                for jn in journals:
                    journal_id = jn
                item_ordered = ''
                for order_line in po['order_line']:
                    item_ordered = order_line.name
                 
                invoice_id = self.env['account.invoice'].create({
                    'invoice_number_entry':po['name'],
                    'name' : po['name'],
                    'number': po['name'],
                    'date_invoice' : batch['date'],
                    'partner_id': batch['source']['id'],
                    'user_id': self.env.uid,
                    'type':'in_invoice',
                    'sales_amount':po.amount_untaxed,
                    'ivoice_item': item_ordered,
                    'account_id':account_id.id,
                    'journal_id':journal_id.id,
                    'batch_id_payables':batch['id'],
                    })
                for line in po['order_line']:
                    self.env['account.invoice.line'].create({
                            'invoice_id' : invoice_id.id,
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'account_id': journal_id.default_debit_account_id.id,
                            'price_unit': line.price_unit,
                            'quantity': line.product_qty,
                            'discount': 0.0,
                        })
                invoices_detail.append(invoice_id)
                invoices.append(invoice_id.id)
            for inv in invoices_detail:
                _logger.info("--> Partner: "+str(inv.partner_id.id)+ " PO:"+str(inv.number))
            
            batch['transactions'] = [(6,0,invoices)]
            
    
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
        
        journals=[]
        for inv in self.transactions:
            inv.action_invoice_open()
            if inv.move_id:
                inv.move_id.move_total = inv.amount_total_signed
                journals.append(inv.move_id.id)
        for rec in self:
            rec['batch_ref'] = self.env['ir.sequence'].next_by_code('audit.trail.code.payables')
            rec['audit_trail_code_ref'] = self.env['ir.sequence'].next_by_code('audit.trail.code.payables')
            rec['voucher_number'] = self.env['ir.sequence'].next_by_code('voucher.number.payables')
            
            rec['journals'] = [(6, 0, journals)]
            if rec['journals']:
                rec['state'] = 'posted'
                
            if self.type == 'normal':   
                self.env['capture.line'].create({
                        'creditor': rec['source'],
                        'doc_number': rec['doc_number'],
                        'amount': rec['total_amount'],
                        'date': rec['date'],
                    })
            else:
                for inv in rec['transactions']:
                    batch_line = self.env['capture.line'].create({
                            'creditor': inv['partner_id'],
                            'doc_number': inv['invoice_number_entry'],
                            'amount': inv['amount_total_signed'],
                            'date': inv['invoice_date'],
                        })
                    self.env['creditor.recon'].create({
                            'partner_id': inv['partner_id'],
                            'transactions': [batch_line.id],
                            'balance': inv['amount_total_signed'],
                            'date': inv['invoice_date'],
                        })
                    
            
        return self.env.ref('account_payables.action_print_posting_journal').report_action(self)
    
'''class JournalBatch(models.Model):
    _name="journal.batch"
    _rec_name="batch_id"
    
    batch_id = fields.Char("Batch #")
    date = fields.Date("Date")
    reference = fields.Char('Rereference')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    
    #transactions = fields.One2many('account.move','journal_batch_id',string="Journal Ids")
    credit_total = fields.Monetary('Credit R')
    debit_total = fields.Monetary('Debit R')
    total_control = fields.Monetary('Total')
    line_count = fields.Integer("Line count")
    gl_report = fields.Binary(compute='generate_report_file')
    gl_report_fn = fields.Char('GL',default='GL Report')
    
    def generate_report_file(self):
        temp = False
        for record in self:
            pdf = self.env.ref('account_payables.action_general_posting_journal').sudo().render_qweb_pdf([record['id']])[0]
            record['gl_report'] = base64.b64encode(pdf)
            temp = base64.b64encode(pdf)
        return temp
    
    
    def print_gl_report(self):
        return self.env.ref('account_payables.action_general_posting_journal').report_action(self)
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        if values:
            values['batch_id'] = self.env['ir.sequence'].next_by_code('audit.trail.code')
            
        record_obj = super(JournalBatch, self).create(values)
        return record_obj
    
    @api.depends('transactions')
    @api.onchange('transactions')
    def calculate_batch_total(self):
        for record in self:
            sum_cr = 0.0
            sum_db = 0.0
            c = 0
            for rec in record['transactions']:
                for line in rec['line_ids']:
                    sum_db += line['debit']
                    sum_cr += line['credit']
                    c+=1
            record['credit_total'] = sum_cr 
            record['debit_total'] = sum_db
            record['total_control'] = sum_cr + sum_db
            record['line_count'] = c
            
            
    def post_journals(self):
        for record in self:
            for rec in record['transactions']:
                rec.post()
        return self.env.ref('account_payables.action_general_posting_journal').report_action(self)
    '''
    
    