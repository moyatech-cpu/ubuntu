# coding=utf-8
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
from lxml import etree

_logger = logging.getLogger(__name__)

class BudgetReallocationManagement(models.Model):
    """ Budget Reallocation Model """
    _name           = 'budget.reallocation'
    #_inherit        = ['mail.thread', 'mail.activity.mixin']
    _description    ='facilitates the memo approval process for reallocations of funds'

    @api.multi
    def default_employee_id(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.id

    employee_id     = fields.Many2one('hr.employee', string="Requester", related_sudo=False, default=lambda self: self.default_employee_id())
    department_id   = fields.Many2one('hr.department', string="Department", related="employee_id.department_id")
    designation     = fields.Many2one('hr.job', string="Designation", related="employee_id.job_id")
    
    state           = fields.Selection([
                                        ('new', 'New'),
                                        ('internal_review', 'Internal Review'),
                                        ('1st_review', '1st Review'),
                                        ('2nd_review', '2nd Review'),
                                        ('final_review', 'Final Review'),
                                        ('rejected', 'Rejected'),
                                        ], 'Status', default='new', index=True, required=True, readonly=True, copy=False, track_visibility='always') 
    name            = fields.Char('Name')
    description     = fields.Text('Description')
    reject_reason   = fields.Text(string='Reject Reason')
    color           = fields.Integer(string='Color Index', default=4)
    active          = fields.Boolean(default=True)

    @api.multi
    def action_proceed(self):
        self.write({'state': 'internal_review'})

    @api.multi
    def action_internal_review(self):
        self.write({'state': 'internal_review'})
        
    @api.multi
    def action_1st_review(self):
        self.write({'state': '1st_review'})
        
    @api.multi
    def action_2nd_review(self):
        self.write({'state': '2nd_review'})

    @api.multi
    def action_final_review(self):
        self.write({'state': 'final_review'})
        
        
    def action_reject_reallocation(self):
        return {
            'name': _('Reject Reason'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('nyda_budget_management.budget_reject_reason_form').id,
            'res_model': 'budget.reallocation',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
        }        