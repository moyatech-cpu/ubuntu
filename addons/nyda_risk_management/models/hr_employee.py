# -*- coding: utf-8 -*-

from odoo import api, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, vals):
        res = super(HrEmployee, self).create(vals)
        #group_id = self.env.ref('nyda_risk_management.risk_manager')
        #for user in group_id.users:
        #    user.notify_info(res.name+" Employee Created.", title="Notification", sticky=True)
        return res