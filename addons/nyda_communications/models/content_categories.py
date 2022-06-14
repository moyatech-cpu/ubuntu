# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import  _
from datetime import date, datetime
from odoo.exceptions import UserError

class ContentCategories(models.Model):
    
    _name = "content.categories"
    _description = "content request categories"
    _rec_name = 'category_name'
    
    category_name = fields.Char('Category')
    sub_category_id = fields.Many2one('content.sub.categories', string="Sub Categories")
    category_officer = fields.Many2one('hr.employee', string="Category Manager")
    category_description = fields.Char('Category Description')
    
    @api.multi
    def get_category_officer_email(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.category_officer.id)])
        if employee:
            return employee.id