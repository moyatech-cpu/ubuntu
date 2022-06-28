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
    
class Authorization(models.Model):
    _name='creditor.authorize'
    _rec_name = 'batch_number'
    
    chequebook = fields.Many2one('account.journal',string="Bank Accounts")
    process = fields.Selection([('eft','EFT')], default='eft')
    show_statements = fields.Boolean('Show all Statements')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    total_authorized = fields.Monetary('Authorized Amount')
    statement = fields.Many2many('creditor.recon',string="Statements")
    cheque_number = fields.Char('Cheque ref')
    num_of_payments = fields.Integer('Payments')
    state = fields.Selection([('new','New'),('auth','Authorized')],default='new')
    batch_number = fields.Char('Batch number')
    partner_ids = fields.Many2many('res.partner',string="Partners")
    
    @api.multi
    @api.depends('chequebook')
    @api.onchange('chequebook')
    def compute_voucher_value(self):
        invoices = self.env['creditor.recon'].sudo().search([])
        
        #Fill up the list of captured statement
        self.statement = invoices
        
    def authorize(self):
        self.state = 'auth'
        sp = []
        for record in self:
            for each in record['statement']:
                each.authorized = True 
                sp.append(each['partner_id']['id'])
            record['partner_ids'] = [(6,0,sp)]
            
        
        return self.env.ref('account_payables.action_print_posting_journal_report').report_action(self)
    
    def create_eft(self):
        context = {'default_batch_id':self.id}
        return{
                    'type': 'ir.actions.act_window',
                    'name': 'New EFT',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'creditor.eft',
                    'views': [(self.env.ref("account_payables.views_payable_eft").id, 'form')],
                    'context': context,
                    'target': 'new',
        }
    
    @api.model
    def create(self, values):
        if values:
            values['batch_number'] = self.env['ir.sequence'].next_by_code('creditor.authorize')
            #replace lines with defaul line
            
        record_obj = super(Authorization, self).create(values)
        return record_obj
        
    @api.multi
    @api.depends('statement','chequebook')
    @api.onchange('statement','chequebook')
    def compute_voucher_value(self):
        for record in self:
            sum = 0
            c=0
            for rec in record['statement']:
                sum += rec['balance']
                c+=1
                record['cheque_number'] = rec['batch_number']
            record['total_authorized'] = sum 
            record['num_of_payments'] = c
    