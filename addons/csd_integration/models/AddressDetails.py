# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class Address(models.Model):
    _name = 'address.details'
    _description = "Address Details"
    _rec_name = "AddressID"
    
    IsActive = fields.Char("IsActive")
    LastVerficationDate = fields.Char("LastVerficationDate")
    EditDate = fields.Char("EditDate")
    IsPreferred = fields.Char("IsPreferredd")
    CreatedDate = fields.Char("CreatedDate")
    
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    AddressID = fields.Char("AddressID")
    AddressTypeCode = fields.Char("AddressTypeCode")
    AddressLine1 = fields.Char("AddressLine1")
    AddressLine2 = fields.Char("AddressLine2")
    CountryCode = fields.Char("CountryCode")
    ProvinceCode = fields.Char("ProvinceCode")
    DistrictCode = fields.Char("DistrictCode")
    MunicipalityCode = fields.Char("MunicipalityCode")
    CityCode = fields.Char("CityCode")
    SuburbCode = fields.Char("SuburbCode")
    WardCode = fields.Char("WardCode")
    PostalCode = fields.Char("PostalCode")
    IsPostalAddress = fields.Char("IsPostalAddress")
    IsDeliveryAddress = fields.Char("IsDeliveryAddress")
    IsPhysicalAddress = fields.Char("IsPhysicalAddress")
    IsPaymentAddress = fields.Char("IsPaymentAddress")
    Field1 = fields.Char("Field1")
    Field2 = fields.Char("Field2")
    Field3 = fields.Char("Field3")
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x