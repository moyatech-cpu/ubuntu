# coding=utf-8

from odoo import api, fields, models, _
from odoo import http
from datetime import date, datetime


class Region(models.Model):
    """ Model to register all the applications for grant. """
    _name = 'res.region'
    _description = 'Region'
    
    name = fields.Char(string="Region Name")
    region_manager = fields.Many2one('res.users','Region Manager')
    user = fields.Many2one('res.users')
    branches = fields.One2many('res.branch','region_id',relation='rel_branches_region_view',compute="_compute_service_provider_vouchers",readonly=True,store=False,copy=False,
                               string="Assigned branches")
    
    @api.depends("user")
    def _compute_service_provider_vouchers(self):
        recordset = self.env["res.branch"].sudo().search([('region_id','=',self.id)])
        self.branches = recordset
        
class Branch(models.Model):
    """ Model to register all the applications for grant. """
    _inherit = 'res.branch'
    
    region_id = fields.Many2one('res.region',string="Region")

class Users(models.Model):
    """ Model to register all the applications for grant. """
    _inherit = 'res.users'
    
    is_regional_user = fields.Boolean(string="Is Regional User")
    