# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class Director(models.Model):
    _name = 'supplier.director'
    _description = "Bank Account"
    _rec_name = "DirectorID"
    
    IsActive = fields.Char("IsActive")
    LastVerficationDate = fields.Char("LastVerficationDate")
    EditDate = fields.Char("EditDate")
    IsPreferred = fields.Char("IsPreferred")
    CreatedDate = fields.Char("CreatedDate")
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    
    DirectorID = fields.Char("DirectorID")
    Name = fields.Char("Name")
    Surname = fields.Char("Surname")
    AppointmentDate = fields.Char("AppointmentDate")
    CountryTypeCode = fields.Char("CountryTypeCode")
    IDTypeCode = fields.Char("IDTypeCode")
    DirectorStatusTypeCode = fields.Char("DirectorStatusTypeCode")
    SAIDNumber = fields.Char("SAIDNumber")
    ForeignIDNumber = fields.Char("ForeignIDNumber")
    ForeignPassportNumber = fields.Char("ForeignPassportNumber")
    WorkPermitNumber = fields.Char("WorkPermitNumber")
    LastVerificationDate = fields.Char("LastVerificationDate")
    DirectorTypeCode = fields.Char("DirectorTypeCode")
    IsOwner = fields.Char("IsOwner")
    CellphoneNumber = fields.Char("CellPhoneNumber")
    EmailAddress = fields.Char("EmailAddress")
    GenderCode = fields.Char("GenderCode")
    EthnicGroupCode = fields.Char("EthnicGroupCode")
    OwnershipPercentage = fields.Char("OwnershipPercentage")
    OwnershipDemographics = fields.Char("OwnershipDemographics")
    
    SupplierFlagType = fields.Char("SupplierFlagType")
    SupplierFlagDescription = fields.Char("SupplierFlagDescription")
    SupplierFlagValue = fields.Char("SupplierFlagValue")
    SupplierFlagLastVerificationDate = fields.Char("SupplierFlagLastVerificationDate")
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x