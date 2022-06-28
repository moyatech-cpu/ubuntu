# coding=utf-8
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, exceptions, fields, models, _
import logging

class AddressID(models.Model):
    """ Model to inherit/extend the voucher application """
    _name = 'address.id'
    _rec_name = 'address'
    
    type = fields.Selection([('primary','PRIMARY'),('secondary','SECONDARY')],default='primary',string="Type")
    contact = fields.Char("Contact")
    address = fields.Char("Address Line 1")
    address2 = fields.Char("Address Line 2")
    city = fields.Char("City")
    state = fields.Many2one('res.country.state')
    zip = fields.Char("ZipCode")
    country = fields.Many2one('res.country')

class CustomerAccount(models.Model):
    """ Model to inherit/extend the voucher application """
    _inherit = 'account.account'
    _rec_name = 'name'
    
    description = fields.Text("Description")
    cash_account = fields.Selection([('checkbook','Checkbook'),('customer','Customer')],string="Cash Account")
    #accounts = fields.One2many('account.account','checkbook_id',string='Accounts')
    
class Customer(models.Model):
    """ Model to inherit/extend the voucher application """
    _inherit = 'res.partner'
    
    customer_id = fields.Char("Customer ID") #sequence
    name = fields.Char('Name')
    surname = fields.Char('Surname')
    description = fields.Text("Description")
    statement_name = fields.Char('Statement Name')
    
    
    is_finance = fields.Boolean("Is Finance User")
    role = fields.Selection([('debtor','Debtor'),('creditor','Creditor')],string='Customer Type')
    
    address_id = fields.Many2many('address.id','rel_partner_address', 'customer_id', 'type', string='Address ID')
    #contact = fields.Char("Contact",related='address_id.contact')
    #address = fields.Char("Address Line 1",related='address_id.address')
    #address2 = fields.Char("Address Line 2",related='address_id.address2')
    #city = fields.Char("Address",related='address_id.city')
    #state = fields.Many2one('res.country.state',related='address_id.state')
    #zip = fields.Char("ZipCode",related='address_id.zip')
    #country = fields.Many2one('res.country',related='address_id.country')
    
    phone1 = fields.Char('Phone 1')
    phone2 = fields.Char('Phone 2')
    phone3 = fields.Char('Phone 3')
    fax = fields.Char('Fax')
    comment1 = fields.Char('Comment')
    comment2 = fields.Char('Comment 2')
    
    trade_discount = fields.Float('Trade discount')
    payment_term = fields.Selection([('immediate','Immediate'),('fifteen','15 days'),('thirty','30 days')],string='Payment Term')
    discount_grace_period = fields.Integer('Discount grace period')
    due_date_grace_period = fields.Integer('Due date grace period')
    price_level = fields.Char('Price level')
    priority = fields.Selection([('low','Low'),('medium','Medium'),('high','High')],string='Priority')
    ship_to_address = fields.Many2one('address.id',string='Ship to')
    bill_to = fields.Char('Bill to')
    statement_to = fields.Char('Statement to')
    sales_person_id = fields.Many2one('res.users',string='Sales person ID')
    type = fields.Char('Type')
    region = fields.Char('Region')
    
    customer_accounts = fields.Many2many('account.account','rel_partner_mutliple_accounts', 'customer_id', 'code',string='Customer Accounts')
    
    #New Fields
    
    customer_number = fields.Char('Customer Number')
    account_number = fields.Char("Accounts Receivable Account Number")
    sales_account = fields.Char("Sales Account Number")
    total_cash_received_LTD = fields.Char('Total Cash Received LTD')
    
    '''@api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        if values:
            values['customer_id'] = self.env['ir.sequence'].next_by_code('customer.id')
        record_obj = super(Customer, self).create(values)
        return record_obj'''