# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class Association(models.Model):
    _name = 'supplier.association'
    _description = "Association"
    _rec_name = "AssociationID"
    
    IsActive = fields.Char("IsActive")
    LastVerficationDate = fields.Char("LastVerficationDate")
    EditDate = fields.Char("EditDate")
    IsPreferred = fields.Char("IsPreferredd")
    CreatedDate = fields.Char("CreatedDate")
    
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    AssociationID = fields.Char("AssociationID")
    SupplierNumberRequestor = fields.Char("SupplierNumberRequestor")
    SupplierNumberRequested = fields.Char("SupplierNumberRequested")
    AssociationTypeCode = fields.Char("AssociationTypeCode")
    AssociationStatusTypeCode = fields.Char("AssociationStatusTypeCode")
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x