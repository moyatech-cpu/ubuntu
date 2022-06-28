# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_facilitator  = fields.Boolean(string="Is Facilitator")
    #x_services        = fields.Many2many('business.development.assistance',relation='x_business_development_assistance_res_partner_rel',
    #                                   column1='res_partner_id',column2='business_development_assistance_id',string="Services")
    x_service_rating  = fields.Integer(String="Service Rating")
    x_province        = fields.Many2one('res.country.state', string="Province")
    x_branch_id       = fields.Many2one('res.branch', string="Province")
    

