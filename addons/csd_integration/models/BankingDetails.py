# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class BankAccount(models.Model):
    _name = 'bank.account'
    _description = "Bank Account"
    _rec_name = "BankAccountID"
    
    IsActive = fields.Char("IsActive")
    LastVerficationDate = fields.Char("LastVerficationDate")
    EditDate = fields.Char("EditDate")
    IsPreferred = fields.Char("IsPreferred")
    CreatedDate = fields.Char("CreatedDate")
    
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    BankAccountID = fields.Char("BankAccountID")
    IsForeignBankAccount = fields.Char("IsForeignBankAccount")
    AccountHolder = fields.Char("AccountHolder")
    BankAccountTypeCode = fields.Char("BankAccountTypeCode")
    BankName = fields.Char("BankName")
    BankCode = fields.Char("BankCode")
    BranchName = fields.Char("BranchName")
    BranchNumber = fields.Char("BranchNumber")
    AccountNumber = fields.Char("AccountNumber")
    BankAccountStatusCode = fields.Char("BankAccountStatusCode")
    BankAccountVerificationDate = fields.Char("BankAccountVerificationDate")
    AddressLine1 = fields.Char("AddressLine1")
    AddressLine2 = fields.Char("AddressLine2")
    CountryCode = fields.Char("CountryCode")
    ZipCode = fields.Char("ZipCode")
    FirstName = fields.Char("FirstName")
    Initials = fields.Char("Initials")
    LastName = fields.Char("LastName")
    Title = fields.Char("Title")
    IsIdentifierLinkedAtBank = fields.Char("IsIdentifierLinkedAtBank")
    IsSharedFundingAccount = fields.Char("IsSharedFundingAccount")
    FundingContacts = fields.Char("FundingContacts")
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x