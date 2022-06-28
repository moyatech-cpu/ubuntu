# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class IndustryClassification(models.Model):
    _name = 'industry.classification'
    _description = "Industry Classification"
    _rec_name = "IndustryClassificationCode"
    #IsActive = fields.Char("IsActive")
    
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    IndustryClassificationCode = fields.Char("IndustryClassificationCode")
    PercentageRanking = fields.Char("PercentageRanking")
    CoreIndustryIndicator = fields.Char("CoreIndustryIndicator")
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x
    
    