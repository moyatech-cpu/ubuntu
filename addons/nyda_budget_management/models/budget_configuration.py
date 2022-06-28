# coding=utf-8
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
from lxml import etree

_logger = logging.getLogger(__name__)
                  
class BudgetDivision(models.Model):
    """ Budget Division"""
    _name = "budget.division"
    
    code    = fields.Text('Code')
    name    = fields.Char('Name')
    dept_id = fields.Many2one('hr.department', string="Division", domain=lambda self: [("parent_id", "=", False)])

class BudgetBusinessUnit(models.Model):
    """ Budget Business Unit"""
    _name = "budget.business.unit"
    
    code                = fields.Text('Code')
    name                = fields.Char('Name')
    budget_division     = fields.Many2one('budget.division', string='Budget Division')
    business_unit_id    = fields.Many2one('hr.department', string="Business Unit", domain=lambda self: [("parent_id", "!=", False)])