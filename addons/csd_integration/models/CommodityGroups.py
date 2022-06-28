# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class CommodityGroup(models.Model):
    _name = 'commodity.group'
    _description = "Commodity Group"
    _rec_name = "Name"
    
    IsActive = fields.Char("IsActive")
    
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    CommodityGroupID = fields.Char("CommodityGroupID")
    Name = fields.Char("Name")
    Description = fields.Char("Description")
    NationWide = fields.Char("NationWide")
    Field1 = fields.Char("Field1")
    CreatedDate = fields.Char("CreatedDate")
    EditDate = fields.Char("EditDate")
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x
    