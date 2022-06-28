# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class Accreditation(models.Model):
    _name = 'accreditation.model'
    _description = "Commodity Group"
    _rec_name = "AccreditationID"
    
    IsActive = fields.Char("IsActive")
    
    
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    AccreditationID = fields.Char("AccreditationID")
    AccreditationNumber = fields.Char("AccreditationNumber")
    Description = fields.Char("Description")
    RegistrationDate = fields.Char("RegistrationDate")
    ExpiryDate = fields.Char("ExpiryDate")
    IsVerified = fields.Char("IsVerified")
    LastVerificationDate = fields.Char("LastVerificationDate")
    StatusCode = fields.Char("StatusCode")
    CreatedDate = fields.Char("CreatedDate")
    EditDate = fields.Char("EditDate")
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier Details")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x
    