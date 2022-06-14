# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import  _
from datetime import date, datetime
from odoo.exceptions import UserError

class ContentSubCategories(models.Model):
    
    _name = "content.sub.categories"
    _description = "content request sub categories"
    _rec_name = 'sub_category_name'
    
    sub_category_name = fields.Char('Sub Category Name')
    parent_category_id = fields.One2many('content.categories','sub_category_id', string="Parent Category ID")
    sub_category_description =  fields.Char('Sub Category Description')