# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class TeritoryHigherEducation(models.Model):
    _name = 'teritory.higher.education'
    _description = 'Teritory Higher Education'

    name = fields.Char(string="Name")
    major_subjects = fields.Char(string="Major Subjects")
    teritory_year_completed = fields.Date(string="Teritory Year Completed")
    qualification_obtained = fields.Char(string="Qualification Obtained")
    attachment = fields.Binary(string="Attachment")
    attachment_name = fields.Char(string="Attachment Name")
    jobs_database_id = fields.Many2one('jobs.database', string="Jobs Database")