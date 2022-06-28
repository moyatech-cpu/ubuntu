# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date,datetime
from odoo.exceptions import UserError

class Application(models.Model):
    _name = 'application'
    _description = 'Application'

    name = fields.Char(string="Subject / Application Name")
    applicant_name = fields.Char(string="Applicant's Name")
    email = fields.Char(string="Email", related="contact_id.email")
    phone = fields.Char(string="Phone",related="contact_id.cell_phone_number")
    opportunity_id = fields.Many2one('opportunities', string="Applied Job")
    stage = fields.Selection(
        [('new', 'New'), ('shortlisted', 'Shortlisted'), ('placed', 'Placed'), ('not_placed', 'Not Placed')],
        string="Stage", default="new")
    medium = fields.Char(string="Medium")
    source = fields.Selection([('newspaper', 'News Paper'), ('website', 'Website'), ('job_portal', 'Job Portal')],
                              string="Source")
    appreciation = fields.Selection([('normal', 'Normal'), ('good', 'Good'), ('best', 'Best')], string="Appreciation")
    official_responsible_id = fields.Many2one('res.users', string="Responsible", domain=lambda self: [
        ('groups_id', '=', self.env.ref('job_opportunities.job_officer').id)],
                                              related="opportunity_id.official_responsible_id")
    contact_id = fields.Many2one('youth.enquiry', string="Contact")
    applied_user_id = fields.Many2one('res.users', string="Applied By User", related="contact_id.user_id")
    mobile = fields.Char(string="Mobile",related="contact_id.alternative_number")
    degree_id = fields.Many2one('degree', string="Degree")
    referred_by = fields.Char(string="Referred By")
    description = fields.Text(string="Application Summary")
    department_id = fields.Many2one('hr.department', string="Department")
    jobs_training = fields.Boolean(string="Jobs Training")
    resume = fields.Binary(string="Resume")
    resume_name = fields.Char(string="Resume Name")

    @api.onchange('contact_id')
    def onchange_contact(self):
         if self.contact_id:
             self.name = self.contact_id.name.capitalize() + "'s Application"
             self.applicant_name = self.contact_id.name.capitalize()

    def shortlist_ben(self):
        if self.opportunity_id.active == False:
            raise UserError(_("This position has been closed !!"))
        elif self.opportunity_id.position_available > self.opportunity_id.position_left:
            self.stage = 'shortlisted'
        else:
            raise UserError(_("No position left for this post !!"))

    def placed_ben(self):
        if self.opportunity_id:
            if self.opportunity_id.active == False:
                raise UserError(_("This position has been closed !!"))
            elif self.opportunity_id.position_available > self.opportunity_id.position_left:
                self.opportunity_id.position_left += 1
                self.stage = 'placed'
            else:
                raise UserError(_("No position left for this post !!"))

    def not_placed_ben(self):
        self.stage = 'not_placed'

class Degree(models.Model):
    _name = 'degree'
    _description = 'Degree'

    name = fields.Char(string="Name")