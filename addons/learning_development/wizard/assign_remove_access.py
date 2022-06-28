# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class AssignRemoveAccess(models.TransientModel):
    _name = "assign.remove.access"
    _description = "Assign Remove Access"

    @api.multi
    def default_group(self):
        group = self.env['res.groups'].sudo().search(
            [('id', '=', self.env.ref('learning_development.group_learn_dev_admin').id)])
        if group:
            print ("\n\n\n\n\n\n Group ", group)
            return group.id

    @api.multi
    def default_nyda_group(self):
        nyda_group = self.env['res.groups'].sudo().search(
            [('id', '=', self.env.ref('monitoring_and_evaluation.group_nyda_employees').id)])
        if nyda_group:
            print ("\n\n\n\n\n\n Group ", nyda_group)
            return nyda_group

    assign_group_id = fields.Many2one('res.groups', string="Group will be assigned/removed",
                                      default=lambda self: self.default_group())
    group_id = fields.Many2one('res.groups', string="Assign/Remove Group For",
                               default=lambda self: self.default_nyda_group())

    def assign_group(self):
        if self.assign_group_id and self.group_id:
            if self.group_id.users:
                for user in self.group_id.users:
                    if self.assign_group_id.id not in user.groups_id.ids:
                        user.write({
                            'groups_id': [(4, self.assign_group_id.id)]
                        })

    def remove_group(self):
        if self.assign_group_id and self.group_id:
            if self.group_id.users:
                for user in self.group_id.users:
                    if self.assign_group_id.id in user.groups_id.ids:
                        user.write({
                            'groups_id': [(3, self.assign_group_id.id)]
                        })
