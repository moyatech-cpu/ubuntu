# coding=utf-8
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
from lxml import etree

_logger = logging.getLogger(__name__)

class BudgetManagement(models.Model):
    """ Budget Management Module """
    _inherit    = 'crossovered.budget'
            
    @api.multi
    def default_name(self):
        if self.budget_type == "mid-term":
            return self.env['ir.sequence'].next_by_code('mid-term.budget.seq') or _('New')
        else:
            return self.env['ir.sequence'].next_by_code('standard.budget.seq') or _('New')            

    branch_id       = fields.Many2one('hr.employee', string="Branch", related="creating_user_id.employee_id.x_branch_id")
    department_id   = fields.Many2one('hr.employee', string="Department", related="creating_user_id.employee_id.department_id")
    state           = fields.Selection([
                                        ('draft', 'Draft'),
                                        ('cancel', 'Cancelled'),
                                        ('confirm', 'Confirmed'),
                                        ('internal_review', 'Internal Review'),
                                        ('1st_review', '1st Review'),
                                        ('2nd_review', '2nd Review'),
                                        ('3rd_review', '3rd Review'),
                                        ('validate', 'Validated'),
                                        ('adjustment', 'Adjustment'),
                                        ('adopted', 'Adopted'),
                                        ('done', 'Done'),
                                        ], 'Status', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always') 
    
    budget_balance      = fields.Float('Budget Balance')
    budget_limit        = fields.Float('Budget Limit')
    budget_request      = fields.Float('Budget Request')
    budget_type         = fields.Selection([('mid-term','Mid-Term'),('standard','Standard')], 'Budget Type')
    budget_limit        = fields.Float('Budget Limit')    
    budget_request      = fields.Float('Budget Request')    
    executive_comments  = fields.Text('Executive Comments')    
    manager_comments    = fields.Text('Manager Comments')    
    officer_comments    = fields.Text('Officer Comments')    
    sm_comments         = fields.Text('SM Comments')    
    total_spent         = fields.Float('Total Spent')

    @api.multi
    def action_budget_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_budget_confirm(self):
        self.write({'state': 'confirm'})
        
    @api.multi
    def action_budget_internal_review(self):
        self.write({'state': 'internal_review'})
        
    @api.multi
    def action_budget_1st_review(self):
        self.write({'state': '1st_review'})

    @api.multi
    def action_budget_2nd_review(self):
        self.write({'state': '2nd_review'})

    @api.multi
    def action_budget_3rd_review(self):
        self.write({'state': '3rd_review'})
                        
    @api.multi
    def action_budget_validate(self):
        self.write({'state': 'validate'})

    @api.multi
    def action_budget_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_budget_done(self):
        self.write({'state': 'done'})

    @api.multi
    def action_budget_adjustment(self):
        self.write({'state': 'adjustment'})
        
class BudgetLineManagement(models.Model):
    """ Budget Line Management Module """
    _inherit    = 'crossovered.budget.lines'

    adjustment_amount           = fields.Float('Adjustment Amount')
    final_amount                = fields.Float('Final Amount')
    payment_interval            = fields.Selection([('Once-Off','Once-Off'), 
                                            ('Quarterly','Quarterly'), 
                                            ('Monthly','Monthly')],'Payment Interval')
    period                      = fields.Float('Period')    
    planned_amount_y2           = fields.Float('Planned Amount Year 2')
    planned_amount_y3           = fields.Float('Planned Amount Year 3')
    
    @api.onchange('adjustment_amount')
    def _onchange_adjustment_amount(self):
        for line in self:
            if line.adjustment_amount:
                line.final_amount = (line.planned_amount + line.adjustment_amount)
            
    @api.multi
    def _compute_percentage(self):
        for line in self:
            if line.theoritical_amount != 0.00:
                line.percentage = float((line.practical_amount or 0.0) / line.theoritical_amount) * 100
            else:
                line.percentage = 0.00      
                
class BudgetObjective(models.Model):
    """ Budget Objective"""
    _name = "budget.objective"
    
    name        = fields.Char('Name')
    description = fields.Text('Description')
                    
                
class AccountBudgetPostInherit(models.Model):
    """ Budget Line Management Module """
    _inherit = "account.budget.post"
    
    code   = fields.Char('Code')                    
    
class BudgetAnalyticAccount(models.Model):
    """ GL Account"""
    _inherit = "account.analytic.account"
    
    is_ledger           = fields.Boolean('Is Ledger')
    division_id         = fields.Many2one('budget.division', string="Division", domain=lambda self: [("parent_id", "=", False)])
    business_unit_id    = fields.Many2one('budget.business.unit', string="Business Unit", domain=lambda self: [("parent_id", "!=", False)])
    product_id          = fields.Many2one('product.template', string="Product")
    objective_id        = fields.Many2one('budget.objective', string="Budget Objective")
    account_id          = fields.Many2one('account.account', string="Account") 
    
class ProductExtend(models.Model):
    """ Model to inherit/extend the product.template model """
    _inherit    = 'product.template'
    
    product_class   = fields.Selection([('budget','Budget'),('po','Purchase Order'),('sales','Sales')], 'Product Classification')
        