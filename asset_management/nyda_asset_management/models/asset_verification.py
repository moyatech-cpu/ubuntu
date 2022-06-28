# -*- coding: utf-8 -*-

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import float_compare, float_is_zero

class AssetVerification(models.Model):
    
    _name = 'asset.verification'
    _inherit = ['mail.thread']
    _rec_name = 'serial_number'
    
    
    user_id                                     = fields.Many2one('res.users',string='Assigned to',default=lambda self: self.env.uid,index=True, track_visibility='always')
    serial_number                               = fields.Char('Serial Number')
    
    #project_task_id                             = fields.Many2one('project.task', string='Project Task ID')
    #legend_blocked                              = fields.Char(related='project_task_id.legend_blocked', string='Kanban Blocked Explanation', readonly=True, related_sudo=False)
    #legend_done                                 = fields.Char(related='project_task_id.legend_done', string='Kanban Valid Explanation', readonly=True, related_sudo=False)
    #legend_normal                               = fields.Char(related='project_task_id.legend_normal', string='Kanban Ongoing Explanation', readonly=True, related_sudo=False)
    #kanban_state                                = fields.Selection(related='project_task_id.kanban_state')
    
    asset_verification_title                    = fields.Char(string='Verification Title')
    state                                       = fields.Selection([('new', 'New'),
                                                                    ('verification','Verification'),
                                                                    ('branch_review','Branch Review'),
                                                                    ('regional_review','Regional Review'),
                                                                    ('1st_review','Senior Accountant Review'),
                                                                    ('2nd_review','Asset Manager Review'),
                                                                    ('3rd_review','Snr. Mnager Review'),
                                                                    ('completed','Completed')],
                                                                    'Status',group_expand='_expand_states', default='new')
    
    default_user                                = fields.Many2one('res.users',default=lambda self: self.env.user and self.env.user.id or False,string="Dispatcher")
    user_branch                                 = fields.Char(related="default_user.branch_id.name")
    asset_branch_id                             = fields.Many2one('res.branch', string="Branch")
    asset_verification_officer                  = fields.Many2one('hr.employee',default=lambda self: self._get_employee_id(), string="Verification Officer")
    asset_verification_start_date               = fields.Datetime(string="Starting Date")
    asset_verification_end_date                 = fields.Datetime(string="Ending Date")
    asset_verification_comments                 = fields.Text(string="Comments")
    asset_verification_branch_manager_comments  = fields.Text(string="Branch Manager Comments")
    asset_verification_snr_accountant_comments  = fields.Text(string="Snr Accountant Comments")
    asset_verification_asset_manager_comments   = fields.Text(string="Asset Manager Comments")
    asset_verification_snr_manager_comments     = fields.Text(string="Senior Manager Comments")
    asset_verification_regional_comments        = fields.Text(string="Regional Manager Comments")
    color                                       = fields.Integer(string='Color Index', default=4)
    
    def _expand_states(self, state, domain, order):
         return [key for key, val in type(self).state.selection]
    
    def _get_employee_id(self):
    # assigning the related employee of the logged in user
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id
    
    @api.onchange('state')
    def onchange_state(self):
        if self.state == 'new':
            self.color = 6 
        if self.state == 'verification':
            self.color = 1
        if self.state == 'branch_review':
            self.color = 4
        if self.state == '1st_review':
            self.color = 6
        if self.state == '2nd_review':
            self.color = 3
        if self.state == '3rd_review':
            self.color = 2
        if self.state == 'completed':
            self.color = 5
            
    @api.multi
    def asset_verification_proceed_button(self):
        for records in self:
            records.write({
                'state' : 'verification'
            })

    @api.multi
    def asset_verification_proceed_from_verification_button(self):
        for records in self:
            records.write({
                'state' : 'branch_review'
            })
            
    @api.multi
    def asset_verification_regional_manager_sign_off_button(self):
        for records in self:
            records.write({
                'state' : '1st_review'
            })
    
    @api.multi
    def branch_asset_register_button(self, values):
        """ This opens the Fixed Asset Register for a specific branch
            @return: Dictionary value for Fixed Asset Register
        """        
        return {
            'type': 'ir.actions.act_window',    
            'name': _('Branch Asset Register'),
            "views": [[False, "tree"], [False, "form"]],
            'view_id': 3685,
            'res_model': 'account.asset',
            "domain": [["location", "=", self.user_branch]],
            "context": {"create": False},
        }
        
    @api.multi
    def manager_query_button(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manager Query Comment',
            'res_model': 'asset.verification.query.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_asset_management.asset_verification_branch_mngr_query_form').id),
            'target': 'new',
        }
    
    @api.multi
    def accountant_query_button(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Accountant Query Comment',
            'res_model': 'asset.verification.query.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_asset_management.asset_verification_accountant_query_form').id),
            'target': 'new',
        }
    
    @api.multi
    def asset_mngr_query_button(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Asset Manager Query Comment',
            'res_model': 'asset.verification.query.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_asset_management.asset_verification_asset_mngr_query_form').id),
            'target': 'new',
        }
        
    @api.multi
    def snr_mngr_query_button(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Senior Manager Query Comment',
            'res_model': 'asset.verification.query.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_asset_management.asset_verification_snr_mngr_query_form').id),
            'target': 'new',
        }
    
    @api.multi
    def cfo_query_button(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'CFO Query Comment',
            'res_model': 'asset.verification.query.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_asset_management.asset_verification_cfo_query_form').id),
            'target': 'new',
        }
        
    @api.multi
    def asset_branch_mngr_sign_off_button(self):
        for records in self:
            records.write({
                'state' : 'regional_review'})
    @api.multi
    def asset_accountant_sign_off_button(self):
        for records in self:
            records.write({
                'state' : '2nd_review'})
    @api.multi
    def asset_asset_mngr_sign_off_button(self):
        for records in self:
            records.write({
                'state' : '3rd_review'})
    @api.multi
    def asset_snr_mngr_sign_off_button(self):
        for records in self:
            records.write({
                'state' : 'completed'})
        
    def asset_verfification_assign_to_me_button(self):
        self.write({'user_id': self.env.user.id})
        
    @api.model
    def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['serial_number'] = self.env['ir.sequence'].next_by_code('asset.verification')
        rec_obj = super(AssetVerification, self).create(values)
       
        return rec_obj