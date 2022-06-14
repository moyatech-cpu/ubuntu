# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class RiskInsurance(models.Model):
    """ Main model for risk management. """
    _name = "risk.insurance"
    _description = "This model consist of basic structure to Insurance for the Risk"

    name = fields.Char('Risk Insurance')
    details = fields.Text('Details')
    user_id = fields.Many2one('hr.employee', string="Resposible Person")
    risk_id = fields.Many2one('risk.management', string="Risk")
    plan_id = fields.Many2one('strategic.plan', string="Plan", related="risk_id.plan_id")
    attachment_id = fields.Binary(string='POE Attachment')
    state = fields.Selection([('draft', 'New'), ('confirm', 'Confirm'), ('reject', 'Reject')],
                             default='draft', string="State")
    responsible_user_id = fields.Many2one('res.users', string="Responsible")
    date = fields.Date(string="Date")

    @api.multi
    def button_confirm_insurence(self):
        for ins in self:
            ins.write({
                'state': 'confirm',
                'responsible_user_id': self.env.user.id,
                'date': datetime.now().date()
            })

    @api.multi
    def button_reject_insurence(self):
        for ins in self:
            ins.write({
                'state': 'reject',
                'responsible_user_id': self.env.user.id,
                'date': datetime.now().date()
            })
