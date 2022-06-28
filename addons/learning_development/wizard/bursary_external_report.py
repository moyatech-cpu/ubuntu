# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class BursaryExternalReport(models.TransientModel):
    """Bursary External Report"""
    _name = "bursary.external.report"
    _description = 'Bursary External Report'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    type = fields.Selection(
        [('bursaries', 'Bursaries'), ('ext_training', 'External Courses')],
        string="Type")
    status = fields.Selection(
        [('request', 'Requested')   , ('approve', 'Approved'),
         ('reject', 'Rejected')], string="State")

    def get_bursary_external_data(self):
        bur_ext_list = []
        converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        print ("\n\n\n")
        if self.type == 'bursaries' and self.status == 'request':
            bursary_ext_data = self.env['learning.development'].search(
                [('state', 'not in', ['bursary_app','bursary_reject']), ('type', 'in', ['bursary_request'])])
        elif self.type == 'bursaries' and self.status == 'approve':
            bursary_ext_data = self.env['learning.development'].search(
                [('state', 'in', ['bursary_app']), ('type', 'in', ['bursary_request'])])
        elif self.type == 'bursaries' and self.status == 'reject':
            bursary_ext_data = self.env['learning.development'].search(
                [('state', 'in', ['bursary_reject']), ('type', 'in', ['bursary_request'])])
        elif self.type == 'ext_training' and self.status == 'request':
            bursary_ext_data = self.env['learning.development'].search(
                [('state', 'not in', ['bursary_app','bursary_reject']), ('type', 'in', ['ext_courses'])])
        elif self.type == 'ext_training' and self.status == 'approve':
            bursary_ext_data = self.env['learning.development'].search(
                [('state', 'in', ['bursary_app']), ('type', 'in', ['ext_courses'])])
        elif self.type == 'ext_training' and self.status == 'reject':
            bursary_ext_data = self.env['learning.development'].search(
                [('state', 'in', ['bursary_reject']), ('type', 'in', ['ext_courses'])])
        if bursary_ext_data:
            for bursary_ext_data_date in bursary_ext_data:
                check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(bursary_ext_data_date.create_date, '%Y-%m-%d %H:%M:%S'),
                                      '%Y-%m-%d'), '%Y-%m-%d')
                if converted_start_date <= check_date <= converted_end_date:
                    bur_ext_list.append(bursary_ext_data_date)
        return {'start_date': self.start_date, 'end_date': self.end_date,
                'type': dict(self._fields['type'].selection).get(self.type),
                'state': dict(self._fields['status'].selection).get(self.status),
                'bur_ext_data': bur_ext_list}

    def get_training_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('learning_development.action_bursary_external_report').report_action(self)
