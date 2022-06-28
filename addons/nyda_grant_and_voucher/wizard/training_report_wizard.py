# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class TrainingReportWizard(models.TransientModel):
    """Training Report Wizard"""
    _name = "training.report.wizard"
    _description = 'Training Report Wizard'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    intervention_type = fields.Selection(
        [('job_preparedness', 'Job Preparedness'), ('life_skills', 'Life Skills'),
         ('sales_pitch', 'Sales Pitch'), ('bbbee', 'BBBEE'),('bmt_training','BMT Training'),
         ('sales_pitch_bbbee', 'Sales Pitch/BBBEE'), ('digital_skills', 'Digital Skills'),
         ('coop_gov','Co-operative Governance')],
        string="Intervention Type")
    branch_id = fields.Many2one('res.branch', string="Branch")
    report_type = fields.Selection(
        [('training', 'Training'), ('branch', 'branch'), ('training_schedule', 'Training Schedule')],
        string="Report Type")


    def get_training_data(self):
        converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        type = ''
        rep_type = ''
        training_list = []
        rep_print_type = ''
        # training_data = ''
        if self.report_type == 'training':
            if self.intervention_type == 'sales_pitch_bbbee':
                type = 'Sales Pitch/BBBEE Training'
                rep_type = 'sb'
                rep_print_type = 'training'
                training_data = self.env['sales.pitch.training'].search(
                    [('intervention_type', '=', self.intervention_type)])
            elif self.intervention_type == 'life_skills':
                type = 'Life Skills Training'
                rep_type = 'all'
                rep_print_type = 'training'
                training_data = self.env['sales.pitch.training'].search(
                    [('intervention_type', '=', self.intervention_type)])
            elif self.intervention_type == 'sales_pitch':
                type = 'Sales Pitch Training'
                rep_type = 'all'
                rep_print_type = 'training'
                training_data = self.env['sales.pitch.training'].search(
                    [('intervention_type', '=', self.intervention_type)])
            elif self.intervention_type == 'bbbee':
                type = 'BBBEE Training'
                rep_type = 'all'
                rep_print_type = 'training'
                training_data = self.env['sales.pitch.training'].search(
                    [('intervention_type', '=', self.intervention_type)])
            elif self.intervention_type == 'digital_skills':
                type = 'Digital Skills Training'
                rep_type = 'all'
                rep_print_type = 'training'
                training_data = self.env['sales.pitch.training'].search(
                    [('intervention_type', '=', self.intervention_type)])
            elif self.intervention_type == 'job_preparedness':
                type = 'Job Preparedness Training'
                rep_type = 'all'
                rep_print_type = 'training'
                training_data = self.env['sales.pitch.training'].search(
                    [('intervention_type', '=', self.intervention_type)])
            elif self.intervention_type == 'bmt_training':
                type = 'BMT Training'
                rep_type = 'bmt'
                rep_print_type = 'training'
                training_data = self.env['business.mgmt.training'].search([])
            elif self.intervention_type == 'coop_gov':
                type = 'Co-operative Governance Training'
                rep_type = 'all'
                rep_print_type = 'training'
                training_data = self.env['cooperative.governance.training'].search([])
        elif self.report_type == 'branch':
            training_data = []
            sp_branch_data = self.env['sales.pitch.training'].search([('branch_id', '=', self.branch_id.id)])
            bmt_data = self.env['business.mgmt.training'].search([('branch_id', '=', self.branch_id.id)])
            coop_data = self.env['cooperative.governance.training'].search([('branch_id', '=', self.branch_id.id)])
            for sp in sp_branch_data:
                training_data.append(sp)
            for bmt in bmt_data:
                training_data.append(bmt)
            for coop in coop_data:
                training_data.append(coop)
            type = self.branch_id.name
            rep_type = 'all'
            rep_print_type = 'branch'
        if training_data:
            for training_check_date in training_data:
                if self.intervention_type == 'bmt_training' or str(training_check_date).split("(")[
                    0] == 'business.mgmt.training':
                    check_date = datetime.strptime(
                        datetime.strftime(datetime.strptime(training_check_date.start_date, '%Y-%m-%d %H:%M:%S'),
                                          '%Y-%m-%d'), '%Y-%m-%d')
                else:
                    check_date = datetime.strptime(
                        datetime.strftime(datetime.strptime(training_check_date.start_date, '%Y-%m-%d'),
                                          '%Y-%m-%d'), '%Y-%m-%d')
                if converted_start_date <= check_date <= converted_end_date:
                    training_list.append(training_check_date)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'type': type,
                'training': training_list, 'rep_type': rep_type, 'rep_print_type': rep_print_type}

    def get_training_schedule_data(self):
        sales_pitch_bbbee_list = []
        life_skills_training_list = []
        sales_pitch_training_list = []
        bbbee_training_list = []
        digital_skills_training_list = []
        job_preparedness_training_list = []
        bmt_training_training_list = []
        coop_gov_training_list = []
        converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        sales_pitch_bbbee_data = self.env['sales.pitch.training'].search(
            [('intervention_type', '=', 'sales_pitch_bbbee'), ('branch_id', '=', self.branch_id.id)])
        life_skills_training_data = self.env['sales.pitch.training'].search(
            [('intervention_type', '=', 'life_skills'), ('branch_id', '=', self.branch_id.id)])
        sales_pitch_training_data = self.env['sales.pitch.training'].search(
                [('intervention_type', '=', 'sales_pitch'), ('branch_id', '=', self.branch_id.id)])
        bbbee_training_data = self.env['sales.pitch.training'].search(
                [('intervention_type', '=', 'bbbee'), ('branch_id', '=', self.branch_id.id)])
        digital_skills_training_data = self.env['sales.pitch.training'].search(
                    [('intervention_type', '=', 'digital_skills'), ('branch_id', '=', self.branch_id.id)])
        job_preparedness_training_data = self.env['sales.pitch.training'].search(
            [('intervention_type', '=', 'job_preparedness'), ('branch_id', '=', self.branch_id.id)])
        bmt_training_training_data = self.env['business.mgmt.training'].search([('branch_id', '=', self.branch_id.id)])
        coop_gov_training_data = self.env['cooperative.governance.training'].search(
            [('branch_id', '=', self.branch_id.id)])
        for training_check_date in sales_pitch_bbbee_data:
            check_date = datetime.strptime(training_check_date.start_date, '%Y-%m-%d')
            if converted_start_date <= check_date <= converted_end_date:
                sales_pitch_bbbee_list.append(training_check_date)
        for training_check_date in life_skills_training_data:
            check_date = datetime.strptime(training_check_date.start_date, '%Y-%m-%d')
            if converted_start_date <= check_date <= converted_end_date:
                life_skills_training_list.append(training_check_date)
        for training_check_date in sales_pitch_training_data:
            check_date = datetime.strptime(training_check_date.start_date, '%Y-%m-%d')
            if converted_start_date <= check_date <= converted_end_date:
                sales_pitch_training_list.append(training_check_date)
        for training_check_date in bbbee_training_data:
            check_date = datetime.strptime(training_check_date.start_date, '%Y-%m-%d')
            if converted_start_date <= check_date <= converted_end_date:
                bbbee_training_list.append(training_check_date)
        for training_check_date in digital_skills_training_data:
            check_date = datetime.strptime(training_check_date.start_date, '%Y-%m-%d')
            if converted_start_date <= check_date <= converted_end_date:
                digital_skills_training_list.append(training_check_date)
        for training_check_date in job_preparedness_training_data:
            check_date = datetime.strptime(training_check_date.start_date, '%Y-%m-%d')
            if converted_start_date <= check_date <= converted_end_date:
                job_preparedness_training_list.append(training_check_date)
        for training_check_date in bmt_training_training_data:
            check_date = datetime.strptime(
                datetime.strftime(datetime.strptime(training_check_date.start_date, '%Y-%m-%d %H:%M:%S'),
                                  '%Y-%m-%d'), '%Y-%m-%d')
            if converted_start_date <= check_date <= converted_end_date:
                bmt_training_training_list.append(training_check_date)
        for training_check_date in coop_gov_training_data:
            check_date = datetime.strptime(training_check_date.start_date, '%Y-%m-%d')
            if converted_start_date <= check_date <= converted_end_date:
                coop_gov_training_list.append(training_check_date)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': self.branch_id.name,
                'sale_pitch': sales_pitch_training_list, 'bbbee': bbbee_training_list,
                'sales_pitch_bbbee': sales_pitch_bbbee_list, 'life_skills': life_skills_training_list,
                'digital_skills': digital_skills_training_list, 'job_preparedness': job_preparedness_training_list,
                'bmt': bmt_training_training_list, 'coop_gov': coop_gov_training_list}

    def get_training_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            elif self.report_type in ['training', 'branch']:
                return self.env.ref('bmt_training.action_report_training').report_action(self)
            elif self.report_type in ['training_schedule']:
                return self.env.ref('bmt_training.action_report_training_schedule').report_action(self)