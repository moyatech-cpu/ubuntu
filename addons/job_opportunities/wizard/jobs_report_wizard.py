# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class JobsReportWizard(models.TransientModel):
    """Jobs Report Wizard"""
    _name = "jobs.report.wizard"
    _description = 'Jobs Report Wizard'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    branch_id = fields.Many2one('res.branch', string="Branch")
    report_type = fields.Selection([('jobs', 'Jobs'), ('branch', 'Branch')],string="Report Type")
    job_id = fields.Many2one('opportunities', string="Job")

    def get_jobs_data(self):
        converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        name = ''
        rep_type = ''
        jobs_list = []
        jobs_data = ''
        report = ''
        male = 0
        female = 0
        african = 0
        asian = 0
        indian = 0
        white = 0
        coloured = 0
        if self.report_type == 'jobs':
            name = self.job_id.name
            rep_type = 'Jobs Report'
            report = 'jobs'
            if self.job_id:
                jobs_data = self.env['opportunities'].search([('id', '=', self.job_id.id)])
        elif self.report_type == 'branch':
            name = self.branch_id.name
            rep_type = 'Branch Report'
            report = 'branch'
            if self.branch_id:
                jobs_data = self.env['opportunities'].search([('branch_id', '=', self.branch_id.id)])
        if jobs_data:
            for apps in jobs_data:
                for jobs_check_date in apps.opp_applicant_ids:
                    if jobs_check_date.stage == 'placed':
                        check_date = datetime.strptime(
                            datetime.strftime(datetime.strptime(jobs_check_date.create_date, '%Y-%m-%d %H:%M:%S'),
                                              '%Y-%m-%d'), '%Y-%m-%d')
                        if converted_start_date <= check_date <= converted_end_date:
                            jobs_list.append(jobs_check_date)
                            if report == 'branch':
                                if jobs_check_date.contact_id.gender == 'male':
                                    male += 1
                                elif jobs_check_date.contact_id.gender == 'female':
                                    female += 1
                                if jobs_check_date.contact_id.population_group == 'african':
                                    african += 1
                                elif jobs_check_date.contact_id.population_group == 'asian':
                                    asian += 1
                                elif jobs_check_date.contact_id.population_group == 'indian':
                                    indian += 1
                                elif jobs_check_date.contact_id.population_group == 'coloured':
                                    coloured += 1
                                elif jobs_check_date.contact_id.population_group == 'white':
                                    white += 1
        return {'start_date': self.start_date, 'end_date': self.end_date, 'type': name,
                'jobs': jobs_list, 'rep_type': rep_type, 'report': report, 'male': male, 'female': female,
                'african': african, 'asian': asian, 'indian': indian, 'white': white, 'coloured': coloured}

    def get_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            elif self.report_type in ['jobs', 'branch']:
                return self.env.ref('job_opportunities.action_report_job').report_action(self)
            # elif self.report_type in ['training_schedule']:
            #     return self.env.ref('bmt_training.action_report_training_schedule').report_action(self)