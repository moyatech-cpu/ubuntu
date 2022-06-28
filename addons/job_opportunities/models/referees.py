# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Referees(models.Model):
    _name = 'referees'
    _description = 'Referees'

    organisation = fields.Char(string="Organisation")
    job_title_id = fields.Many2one('hr.job', string="Job Title")
    telephone = fields.Char(string="Telephone")
    mobile = fields.Char(string="Mobile")
    jobs_database_id = fields.Many2one('jobs.database', string="Jobs Database")