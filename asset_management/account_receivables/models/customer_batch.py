# coding=utf-8
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.safe_eval import safe_eval
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

import logging

_logger = logging.getLogger(__name__)
# mapping invoice type to refund type

class CustomerBatch(models.Model):
    _name = 'customer.batch.entry'
    _rec_name = 'batch_id'
    
    batch_id = fields.Char("Batch ID") #service provider
    comment = fields.Text("Description")
    
    posting_date = fields.Date('Posting Date')
    date_due = fields.Date('Due Date')
    source = fields.Many2one('res.partner')
    customer_id = fields.Many2one('res.partner',compute="service_provider_select")
    account_id = fields.Many2one('account.account',related="source.property_account_receivable_id")
    trade_discount = fields.Float('Trade Discount',related="customer_id.trade_discount")
    last_posting_date = fields.Date('Last Date Posted')
    
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    
    journal_ids = fields.One2many('account.move', 'batch_id',string="Journal Entries")
    journal_line_ids = fields.One2many('account.move.line','batch_id',string="Journal Entries")
    
    #controls
    transactions_control = fields.Integer("Trn Control")
    batch_control = fields.Monetary('Batch Total Control')
    
    #actual 
    
    transactions_actual = fields.Integer("Trn Actual",compute="compute_voucher_value")
    batch_actual = fields.Monetary('Batch Total Actual',compute="compute_voucher_value")
    control = fields.Boolean("Control")
    invoice_status = fields.Selection([
            ('draft','Draft'),
            ('review','Review'),
            ('approve','Approved'),
            ('reject','Rejected'),
            ('posted', 'Posted'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled')],
        default='draft', string="Batch State")
    
    approvalUser = fields.Many2one('res.users', string='Approved by')
    last_update_user = fields.Many2one('res.users', string='Last updated by')
    approval_date = fields.Date('Approval Date')
    
    transactions = fields.One2many('account.invoice', 'cust_batch_id',string="Transactions")
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        record_obj = super(CustomerBatch, self).create(values)
        record_obj.batch_id = record_obj.source.name
        return record_obj
    
    @api.multi
    def write(self, values):
        record_obj = super(CustomerBatch, self).write(values)
        '''inv_counter = 1
        for rec in self.transactions:
            if not rec.inv_identifier:
                string_number = str(inv_counter)
                rec.inv_identifier = "SLS"+string_number.zfill(7)
            inv_counter += 1'''
                
        return self.env.ref('account_receivables.action_report_cust_batch_entry').report_action(self)
    
        return record_obj
    
    @api.multi
    @api.depends('source')
    @api.onchange('source')
    def service_provider_select(self):
        customer_id = self.env['res.partner'].sudo().search([('id','=',self.source.id)])
        for each in customer_id:
            self.customer_id = each.id
        
    @api.multi
    @api.depends('transactions')
    @api.onchange('transactions')
    def compute_voucher_value(self):
        sum = 0.0
        for inv in self.transactions:
            inv.batch_id = self.id
            inv.partner_id = self.source
            inv.discount = self.trade_discount
            sum = sum + inv.amount_total
                            
        self.batch_actual = sum
        self.transactions_actual = len(self.transactions)
        if self.transactions_actual >= self.transactions_control or self.batch_actual >= self.batch_control:
            self.control = True
        else:
            self.control = False
            self.last_update_user = self.env.user.id
        res = {}
        if self.transactions_actual > self.transactions_control:
            
            res = {'warning': {
                'title': _('Warning'),
                'message': _('Actual Transactions limit reached transactions control')
            }}
            if res:
                return res
            
        if self.batch_actual > self.batch_control:
            
            res = {'warning': {
                'title': _('Warning'),
                'message': _('Actual Batch Total limit reached Batch Control')
            }}
            if res:
                return res
            
    @api.multi
    def set_review(self):
        res = {}
        if self.transactions_actual > self.transactions_control:
            res = {'Warning': {
                'title': _('Warning'),
                'message': _('Actual Transactions limit reached transactions control')
            }}
            if res:
                return res
            
        if self.batch_actual > self.batch_control:
            res = {'warning': {
                'title': _('Warning'),
                'message': _('Actual Batch Total limit reached Batch Control')
            }}
            if res:
                return res
        
        self.invoice_status = 'review'
        self.approvalUser = self.env.user.id
        #populate journal entries
        journals = []
        jids = []
        for inv in self.transactions:
            inv.date_due = self.date_due
            inv.action_invoice_open()
            if inv.move_id:
                journals.append(inv.move_id.id)
        
        self.journal_ids = [(6, 0, journals)]
        
        if self.journal_ids:       
            for inv in self.journal_ids:
                if inv.line_ids:
                    for line in inv.line_ids:
                        jids.append(line.id)
            self.journal_line_ids = [(6, 0, jids)]
        
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoices have been successfully moved to open status."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }
        
    @api.multi
    def set_approve_reject(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Review Batch',
            'res_model': 'customer.batch.review',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def set_post(self):
        for inv in self.transactions:
            inv.state = 'posted'
        
        self.invoice_status = 'posted'
        self.last_posting_date = date.today()
        self.posting_date = date.today()
        return self.env.ref('account_receivables.action_cust_general_post_journal_entry').report_action(self)
        #return self.env.ref('account_receivables.action_report_batch_entry').report_action(self)
    
    def sales_journal(self):
        return self.env.ref('account_receivables.action_report_cust_batch_entry').report_action(self)
    
    @api.multi
    def get_batch_entries(self):
        system_time = datetime.now()
        create_date = self.create_date
        create_user = self.env.user.name
        batch_id = self.batch_id
        posting_date = self.posting_date
        comment = self.comment
        transactions_actual = self.transactions_actual
        transactions_control = self.transactions_control
        batch_actual = self.batch_actual
        batch_control = self.batch_control
        state = self.invoice_status
        approvalUser = self.approvalUser.name
        approval_date = self.approval_date
        
        debit_totals = 0
        credit_totals = 0
        applied_distribution_ids = []
        
        total_invoices_amount = 0
        total_write_off = 0
        total_discounts = 0
        total_unapplied_amount = 0
        total_applied_ = 0
        
        dictionairy = []
        dict_custom = {}
        vouchers = {}
        final_list = []
        ledger_data = []
        for sv in self.transactions:
            for invoice in sv:
                temp_ledger = []
                move_id = invoice.move_id
                if move_id:
                    for line in move_id.line_ids:
                        debit_totals =debit_totals+ line.debit
                        credit_totals = credit_totals+ line.credit
                        ledger = {
                         'code': line.account_id.code, 
                         'account_id': line.account_id.code+" "+line.account_id.name + " " +line.name,
                         'type': line.account_id.user_type_id.name,
                         'debit': line.debit,
                         'credit': line.credit,
                         
                        }
                        ledger_data.append(ledger)
                        temp_ledger.append(ledger)
                    
                vdata = {
                         'number': invoice.number, 
                         'date_invoice': invoice.date_invoice,
                         'due_date': invoice.date_due,
                         'parnter_id': invoice.partner_id.name,
                         'name': invoice.partner_id.name,
                         'sales_person': "",
                         'amount_total_signed': invoice.amount_total_signed,
                         #'write_off': "0.00",
                         'discount': invoice.discount * invoice.sales_amount,
                         'ledger_data':temp_ledger,
                         #'unapplied': invoice.amount_total_signed - (invoice.amount_total_signed * invoice.percentage),
                         }
                       
                final_list.append(vdata)
                app_data = {
                         'type': invoice.number, 
                         'inv_name': invoice.number,
                         'date_inv': invoice.date_invoice,
                         'discount_amount': invoice.discount_amount,
                         'write_off_amount': "0.00",
                         'amount_applied': invoice.amount_total_signed,
                        }
                applied_distribution_ids.append(app_data)
                total_invoices_amount = total_invoices_amount + invoice.amount_total_signed
                total_discounts = total_discounts+invoice.discount * invoice.sales_amount
                total_unapplied_amount = total_unapplied_amount+invoice.amount_total_signed - (invoice.amount_total_signed * invoice.percentage)
                total_applied_ = total_applied_+invoice.amount_total_signed
        dict_custom = {
                'system_time':system_time, 
                'create_user':create_user,
                'create_date':create_date,
                'batch_id':batch_id,
                'posting_date':posting_date,
                'comment':comment,
                'transactions_actual':transactions_actual,
                'transactions_control':transactions_control,
                'batch_actual':batch_actual,
                'batch_control':batch_control,
                'state':state,
                'approval_date':approval_date,
                'approvalUser':approvalUser,
                'invoice_status':self.invoice_status,
                'invoice_ids':final_list,
                'ledger_ids':ledger_data,
                'applied_distribution_ids':applied_distribution_ids,
                'total_invoices_amount':total_invoices_amount,
                'total_discounts':total_discounts,
                'total_unapplied_amount':total_unapplied_amount,
                'total_write_off':total_write_off,
                
                'discount_total':total_discounts,
                'write_off_total':total_write_off,
                'total_applied':total_applied_,
                'debit_totals':debit_totals,
                'credit_totals':credit_totals,
            }
        
        return dict_custom
        
    @api.multi
    def set_paid(self):
        for inv in self.transactions:
            inv.state = 'paid'
        
        self.invoice_status = 'paid'

    @api.multi
    def set_cancel(self):
        self.invoice_status = 'cancel'

    def general_post(self):
        return self.env.ref('account_receivables.action_cust_general_post_journal_entry').report_action(self)
    
    @api.multi
    def get_general_post_journal(self):
        system_time = datetime.now()
        create_date = self.create_date
        create_user = self.env.user.name
        batch_id = self.batch_id
        posting_date = self.posting_date
        comment = self.comment
        transactions_actual = self.transactions_actual
        transactions_control = self.transactions_control
        batch_actual = self.batch_actual
        batch_control = self.batch_control
        state = self.invoice_status
        approvalUser = self.approvalUser.name
        approval_date = self.approval_date
        total_entries = len(self.journal_ids)
        applied_distribution_ids = []
        
        total_invoices_amount = 0
        total_write_off = 0
        total_discounts = 0
        total_unapplied_amount = 0
        total_applied_ = 0
        
        dictionairy = []
        dict_custom = {}
        vouchers = {}
        final_list = []
        ledger_data = []
        for invoice in self.journal_ids:
            temp_ledger = []
            debit_totals = 0
            credit_totals = 0
            distributions = 0
            for line in invoice.line_ids:
                debit_totals = debit_totals + line.debit
                credit_totals = credit_totals+ line.credit
                distributions= distributions +1
                ledger = {
                         'code': line.account_id.code, 
                         'account_id': line.account_id.code+" "+line.account_id.name + " " +line.name,
                         'type': line.account_id.user_type_id.name,
                         'debit': line.debit,
                         'credit': line.credit,
                         
                }
                ledger_data.append(ledger)
                temp_ledger.append(ledger)
                    
            vdata = {
                         'jid': invoice.id, 
                         'journal_id': invoice.journal_id.name,
                         'date': invoice.date,
                         'reverse_date': "",    #invoice.reverse_date,
                         'name': invoice.name,
                         'reference': invoice.ref,
                         'audit_trail_code': "",#invoice.audit_trail_code,
                         #'write_off': "0.00",
                         'rev_audit_trail_code': "", #invoice.discount * invoice.sales_amount,
                         'ledger_data':temp_ledger,
                         'debit_totals':debit_totals,
                         'credit_totals':credit_totals,
                         'total_distributions':distributions,
                         #'unapplied': invoice.amount_total_signed - (invoice.amount_total_signed * invoice.percentage),
            }
                       
            final_list.append(vdata)
            
        dict_custom = {
                'system_time':system_time, 
                'create_user':create_user,
                'create_date':create_date,
                'batch_id':batch_id,
                'posting_date':posting_date,
                'comment':comment,
                'transactions_actual':transactions_actual,
                'transactions_control':transactions_control,
                'batch_actual':batch_actual,
                'batch_control':batch_control,
                'state':state,
                'approval_date':approval_date,
                'approvalUser':approvalUser,
                'invoice_status':self.invoice_status,
                'invoice_ids':final_list,
                'ledger_ids':ledger_data,
                #'applied_distribution_ids':applied_distribution_ids,
                #'total_invoices_amount':total_invoices_amount,
                #'total_discounts':total_discounts,
                #'total_unapplied_amount':total_unapplied_amount,
                #'total_write_off':total_write_off,
                'total_entries': str(total_entries),
                #'discount_total':total_discounts,
                #'write_off_total':total_write_off,
                #'total_applied':total_applied_,
                #'debit_totals':debit_totals,
                #'credit_totals':credit_totals,
            }
        
        return dict_custom

