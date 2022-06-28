# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime, date
from odoo.exceptions import UserError


class AftercareReportWizard(models.TransientModel):
    """Aftercare Report Wizard"""
    _name = "aftercare.report.wizard"
    _description = 'Aftercare Report Wizard'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    all_branch = fields.Boolean(string="All Branch")
    branch_id = fields.Many2one('res.branch', string="Branch")

    @api.onchange('branch_id')
    def onchange_branch(self):
        if self.branch_id:
            self.all_branch = False

    @api.onchange('all_branch')
    def onchange_all_branch(self):
        if self.all_branch:
            self.branch_id = False

    def get_aftercare_data(self):
        voucher_list = []
        final_list = []
        branch = ''
        print("\n\n\n ", self.start_date, self.end_date)
        sdate = datetime.strptime(
            datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%m-%d-%Y %H:%M:%S'), '%m-%d-%Y %H:%M:%S')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%m-%d-%Y %H:%M:%S'),
                                  '%m-%d-%Y %H:%M:%S')
        if self.branch_id:
            branch = self.branch_id.name
            ac_data = self.env['after.care'].sudo().search(
                [('financerbranch', '=', self.branch_id.id), ('after_care', '=', 'voucher_ac')])
            voucher_list.append(ac_data)
        elif self.all_branch:
            branch = 'All Branch'
            branches = self.env['res.branch'].sudo().search([])
            for bid in branches:
                vouchers = self.env['after.care'].sudo().search(
                    [('financerbranch', '=', bid.id), ('after_care', '=', 'voucher_ac')])
                if len(vouchers) >= 1:
                    voucher_list.append(vouchers)
        val_type = 'number'
        for sac in voucher_list:
            jobs = 0
            total = 0
            if len(sac) == 1:
                cdate = datetime.strptime(sac.create_date, '%Y-%m-%d %H:%M:%S')
                if sdate <= cdate and edate >= cdate:
                    vdata = {'name': sac.financerbranch.name, 'total': len(sac), 'jobs': sac.jobs_created}
                    final_list.append(vdata)
            elif len(sac) >= 2:
                for ac in sac:
                    cdate = datetime.strptime(ac.create_date, '%Y-%m-%d %H:%M:%S')
                    if sdate <= cdate and edate >= cdate:
                        name = ac.financerbranch.name
                        jobs += ac.jobs_created
                        total += 1
                vdata = {'name': name, 'total': total, 'jobs': jobs}
                final_list.append(vdata)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch, 'value_type': val_type,
                'vouchers': final_list}

    def get_aftercare_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_aftercaree').report_action(self)
