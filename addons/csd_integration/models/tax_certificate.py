# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class Tax(models.Model):
    _name = 'tax.certificate'
    _description = "Supplier Tax Certificate"
    _rec_name = "IncomeTaxNumber"
    
    IsRegistered = fields.Char("IsRegistered")
    IsActive = fields.Char("IsActive")
    IncomeTaxNumber = fields.Char("IncomeTaxNumber")
    IsVATVendor = fields.Char("IsVATVendor")
    IncomeTaxVendor = fields.Char("IncomeTaxVendor")
    PAYENumber = fields.Char("PAYENumber")
    VATNumber = fields.Char("VATNumber")
    IsValidCertificate = fields.Char("IsValidCertificate")
    ValidationResponse = fields.Text("ValidationResponse")
    LastVerficationDate = fields.Char("LastVerficationDate")
    EditDate = fields.Char("EditDate")
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x