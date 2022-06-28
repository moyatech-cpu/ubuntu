# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class UsersReportWizard(models.TransientModel):
    """Users Report Wizard"""
    _name = "users.report.wizard"
    _description = 'Users Report Wizard'

    groups_id = fields.Many2one('res.groups', string="User Type")
    user_type = fields.Selection(
        [('active', 'Active Users'), ('inactive', 'Inactive Users'), ('all_users', 'All Users')],
        string="Status")
    all_users = fields.Boolean(string="All users")
    all_nyda_staff = fields.Boolean(string="All NYDA Staff")

    @api.onchange('groups_id')
    def onchange_groups(self):
        if self.groups_id:
            self.all_users = False
            self.all_nyda_staff = False

    @api.onchange('all_users')
    def onchange_all_users(self):
        if self.all_users:
            self.groups_id = False
            self.all_nyda_staff = False

    @api.onchange('all_nyda_staff')
    def onchange_all_nyda_staff(self):
        if self.all_nyda_staff:
            self.groups_id = False
            self.all_users = False

    def get_users_report(self):
        return self.env.ref('nyda_grant_and_voucher.action_report_users').report_action(self)

    def get_users_data(self):
        users_data = ''
        type = ''
        state = ''
        gname = ''
        if self.groups_id and self.user_type == 'active':
            type = self.groups_id.name
            state = 'Active Users'
            gname = self.groups_id.name
            users_data = self.env['res.users'].sudo().search([('groups_id', 'in', self.groups_id.id), ('active', '=', True)])
        elif self.groups_id and self.user_type == 'inactive':
            type = self.groups_id.name
            state = 'Inactive Users'
            gname = self.groups_id.name
            users_data = self.env['res.users'].sudo().search([('groups_id', 'in', self.groups_id.id), ('active', '=', False)])
        elif self.groups_id and self.user_type == 'all_users':
            type = self.groups_id.name
            state = 'All Users'
            gname = self.groups_id.name
            users_data = self.env['res.users'].sudo().search([('groups_id', 'in', self.groups_id.id)])
        elif self.all_users and self.user_type == 'active':
            type = 'All Users'
            state = 'Active Users'
            gname = ''
            users_data = self.env['res.users'].sudo().search([('active', '=', True)])
        elif self.all_users and self.user_type == 'inactive':
            type = 'All Users'
            state = 'Inactive Users'
            gname = ''
            users_data = self.env['res.users'].sudo().search([('active', '=', False)])
        elif self.all_users and self.user_type == 'all_users':
            type = 'All Users'
            state = 'All Users'
            gname = ''
            users_data = self.env['res.users'].sudo().search([])
        elif self.all_nyda_staff and self.user_type == 'active':
            type = 'All NYDA Staff'
            state = 'Active Users'
            gname = ''
            users_data = self.env['res.users'].sudo().search([('active', '=', True)])
        elif self.all_nyda_staff and self.user_type == 'inactive':
            type = 'All NYDA Staff'
            state = 'Inactive Users'
            gname = ''
            users_data = self.env['res.users'].sudo().search([('active', '=', False)])
            return {'type': type, 'udata': users_data, 'state': state, 'group_name': gname}
        elif self.all_nyda_staff and self.user_type == 'all_users':
            type = 'All NYDA Staff'
            state = 'All Users'
            gname = ''
            users_data = self.env['res.users'].sudo().search([])
