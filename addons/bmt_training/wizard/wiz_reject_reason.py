# -*- coding: utf-8 -*-

from odoo import models, fields


class WizReportRejectComment(models.Model):
    _name = 'wiz.reject.reason'
    _description = "Wizard Reject Reason"

    comment = fields.Text(string="Comment")

    def action_button_reject(self):
        self.ensure_one()
        training_id = self.env['technical.training.apprenticeship'].browse(self._context.get('active_id'))
        curr_user_id = self.env.user.id or False
        vals = {'reject_reason': self.comment}
        if self._context.get('reject_head_office',False):
            vals.update({
                'state': 'placed_at_company',
                'head_office_user_id': curr_user_id
            })
        if self._context.get('reject_site_visitor', False):
            vals.update({
                'state': 'site_visit_reject',
                'site_visit_user_id': curr_user_id
            })
        if self._context.get('nyda_reject', False):
            vals.update({
                'state': 'service_provider_submit',
                'nyda_user_id': curr_user_id
            })
        if self._context.get('reject_poc', False):
            vals.update({
                'state': 'pc_reject',
                'pcr_user_id': curr_user_id
            })
        training_id.write(vals)