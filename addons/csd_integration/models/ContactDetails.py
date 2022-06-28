# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class Contact(models.Model):
    _name = 'contact.detail'
    _description = "Contact Details"
    
    IsActive = fields.Char("IsActive")
    LastVerficationDate = fields.Char("LastVerficationDate")
    EditDate = fields.Char("EditDate")
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    ContactID = fields.Char("ContactID")
    ContactTypeCode = fields.Char("ContactTypeCode")
    IsPreferred = fields.Char("IsPreferred")
    Name = fields.Char("Name")
    Surname = fields.Char("Surname")
    IdentificationTypeCode = fields.Char("IdentityTypeCode")
    SAIDNumber = fields.Char("SAIDNumber")
    ForeignIDNumber = fields.Char("ForeignIDNumber")
    ForeignPassportNumber = fields.Char("ForeignPassportNumber")
    WorkPermitNumber = fields.Char("WorkPermitNumber")
    PreferCellphone = fields.Char("PreferCellphone")
    PreferEmail = fields.Char("PreferEmail")
    PreferFax = fields.Char("PreferFax")
    PreferPostal = fields.Char("PreferPostal")
    PreferSMS = fields.Char("PreferSMS")
    PreferTelephone = fields.Char("PreferTelephone")
    EmailAddress = fields.Char("EmailAddress")
    CellphoneNumber = fields.Char("CellphoneNumber")
    FaxNumber = fields.Char("FaxNumber")
    TelephoneNumber = fields.Char("TelephoneNumber")
    TollFreeNumber = fields.Char("TollFreeNumber")
    WebsiteAddress = fields.Char("WebsiteAddress")
    FundingPartnerLegalName = fields.Char("FundingPartnerLegalName")
    CSDUser = fields.Char("CSDUser")
    CreatedDate = fields.Char("CreatedDate")
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x