# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Agreement(models.Model):
    _name = 'performancemanagement.agreement'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(
        string="Title"
        )
    agreement_start = fields.Date(
        string="Agreement Start", 
        default=fields.Date.today
        )
    agreement_end = fields.Date(
        string="Agreement End"
        )
    monitoring_start = fields.Date(
        string="Monitoring Start"
        )
    monitoring_end = fields.Date(
        string="Monitoring End"
        )
    description = fields.Html()
    color = fields.Integer()
    state = fields.Selection(
        [
            ('new', 'NEW'),
            ('review', 'REVIEW'),
            ('performance dialogue', 'PERFORMANCE DIALOGUE'),
            ('performance contract', 'PERFORMANCE CONTRACT'),
            ('completed', 'COMPLETED')
        ],
        string='Status',
        readonly=True,
        group_expand='_expand_states',
        default='new'
        )

    def action_to_lm(self):
        self.state = 'review'

    def action_to_dia(self):
        self.state = 'performance dialogue'

    def action_to_con(self):
        self.state = 'performance contract'

    def action_completed(self):
        self.state = 'completed'

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]
    