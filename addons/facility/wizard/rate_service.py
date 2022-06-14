# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class RateService(models.TransientModel):
    """Rate Service"""
    _name = "rate.service"
    _description = 'Rate Service'

    type = fields.Selection([('cancel', 'Cancel'), ('solved', 'Solved')], string="Type")
    cancellation_reason = fields.Text(string="Cancellation Reason")
    description = fields.Text(string="Description")
    service_level = fields.Selection(
        [('worst', 'Worst'), ('bad', 'Bad'), ('good', 'Good'), ('best', 'Best'), ('excellent', 'Excellent'),
         ('outstanding', 'Outstanding')], string='Service Level')

    def cancel_tickets(self):
        ticket = self.env[self._context['active_model']].sudo().search([('id', '=', self._context['active_id'])])
        if ticket:
            ticket.sudo().write({
                'cancellation_reason' : self.cancellation_reason,
                'stage_id': self.env.ref('helpdesk_lite.stage_canceled').id
            })

    def submit_feedback(self):
        if not self.service_level:
            raise UserError (_("Please rate the service !!"))
        ticket = self.env[self._context['active_model']].sudo().search([('id', '=', self._context['active_id'])])
        if ticket:
            ticket.sudo().write({
                'service': self.service_level,
                'stage_id': self.env.ref('helpdesk_lite.stage_solved').id,
                'service_description': self.description
            })
