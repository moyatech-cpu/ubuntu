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
    _inherit = 'customer.batch.entry'
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
    
    