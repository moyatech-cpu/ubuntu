# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date,datetime
from odoo.exceptions import UserError

class Opportunities(models.Model):
    _name = 'opportunities'
    _description = 'Opportunities'

    name = fields.Char(string="Jobs/Opportunity Title")
    job_location_id = fields.Char(string="Job Location")
    official_responsible_id = fields.Many2one('res.users', string="Official Responsible", domain=lambda self: [
        ('groups_id', '=', self.env.ref('job_opportunities.job_officer').id)])
    position_available = fields.Integer(string="Position Available")
    position_left = fields.Integer(string="Position Left")
    description = fields.Text(string="Description")
    app_closing_date = fields.Date(string="Closing Date for Applications")
    job_level = fields.Selection([('senior', 'Senior'), ('intermediate', 'Intermediate'), ('junior', 'Junior')],
                                 string="Job Level")
    required_qualification = fields.Char(string="Required Qualification")
    required_experience = fields.Char(string="Required Experience")
    description_role = fields.Text(string="Description Role")
    points = fields.Text(string="Points you'd like us to note / Special Requirements")
    aff_act_req = fields.Text(string="Affirmative Action Requirements")
    prop_can_start_date = fields.Date(string="Proposed Candidate Start Date")
    emp_type = fields.Selection(
        [('apprenticeship', 'Apprenticeship'), ('contract', 'Contract'), ('learnership', 'Learnership'),
         ('internship', 'Internship'), ('perm', 'Perm'), ('temp', 'Temp')], string="Employment Type")
    stipend_per_month = fields.Char(string="Stipend Per Month")
    salary_per_month = fields.Char(string="Salary Per Month")
    province_id = fields.Many2one('res.country.state',string="Province")
    ind_sector_id = fields.Many2one('industry.sector', string="Industry Sector")
    active = fields.Boolean(string="Active", default=True)
    branch_id = fields.Many2one('res.branch', string="Branch")
    opp_applicant_ids = fields.One2many('application', 'opportunity_id', string="Applicants")
    
    legacy_district = fields.Char(string="Legacy District")
    legacy_creation_date = fields.Datetime(string="Legacy Creation Date")
    legacy_employment_type = fields.Char(string="Legacy Employment Type")
    legacy_service_provider = fields.Char(string="Legacy Service Provider")

    @api.model
    def create(self, values):
        res= super(Opportunities, self).create(values)
        print ("\n\n\n\n res ", res)
        opp_mail = self.env.ref('job_opportunities.new_opp_email_template')
        if opp_mail:
            all_mails = ''
            for mail in self.env['jobs.database'].sudo().search([('active', '=', True)]):
                if mail.email:
                    if len(all_mails) == 0:
                        all_mails += mail.email
                    else:
                        all_mails += "," + mail.email
            opp_mail.send_mail(res.id, force_send=True,
                               email_values={
                                            'email_from': 'darshil.tus@gmail.com',
                                            'email_to': all_mails
                                        })
        return res

    def doc_opportunity(self):
        for rec in self:
            return {
                'name': "Documents",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'application',
                'domain': [('opportunity_id', '=', rec.id)],
                'context': {'default_opportunity_id': rec.id},
                'view_id': self.env.ref('job_opportunities.application_doc_tree_view').id,
            }

    def rec_opportunity(self):
        for rec in self:
            return {
                'name': "Recruited Beneficiaries",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'application',
                'domain': [('stage', '=', 'placed'), ('opportunity_id', '=', rec.id)],
                'context': {'default_stage': 'placed','default_opportunity_id': rec.id}
            }

    def apps_opportunity(self):
        for rec in self:
            return {
                'name': "Applications",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'application',
                'domain': [('opportunity_id', '=', rec.id)],
                'context': {'default_opportunity_id': rec.id}
            }

    #@api.constrains('app_closing_date')
    @api.one
    def _check_date(self):
        if self.app_closing_date:
            close_date = datetime.strptime(self.app_closing_date, "%Y-%m-%d")
            if datetime.now() >= close_date:
                raise UserError(_("Application close date has passed"))

class JobLocation(models.Model):
    _name = 'job.location'
    _description = 'Job Location'

    name = fields.Char(string="Title")

class IndustrySector(models.Model):
    _name = 'industry.sector'
    _description = 'Industry Sector'

    name = fields.Char(string="Title")