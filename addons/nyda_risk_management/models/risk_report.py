# -*- coding: utf-8 -*-

from odoo import api, fields, models


class RiskReport(models.Model):
    """ User can add supporting document to the risk report. """
    _name = "risk.report"
    _rec_name = "risk_id"
    _description = "Risk Report Submit"

    state = fields.Selection([('new', 'New'), ('approve', 'Approve'), ('reject', 'Reject')],
                             default='new', string="State")
    employee_id = fields.Many2one('hr.employee',string="Employee")
    risk_id = fields.Many2one('risk.management',string="Name")
    report_doc = fields.Binary('Report')
    store_report_name = fields.Char("Report Name")
    p_o_e_doc = fields.Binary('Portfolio of evidence.')
    store_p_o_e_name = fields.Char("POE Name")

    @api.multi
    def action_approve(self):
        """ Function for processing Risk Report record for approve. """
        template_id = self.env.ref('nyda_risk_management.email_template_risk_report_approve')
        if template_id:
            template_id.send_mail(self.id, force_send=True)
        return self.write({
            'state': 'approve'
        })

    @api.multi
    def action_reject(self):
        """ Function for processing Risk Report record for reject. """
        template_id = self.env.ref('nyda_risk_management.email_template_risk_report_reject')
        if template_id:
            template_id.send_mail(self.id, force_send=True)
        return self.write({
            'state': 'reject'
        })