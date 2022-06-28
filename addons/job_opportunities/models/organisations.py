# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class Organisations(models.Model):
    _name = 'organisations'
    _description = 'Organisations'

    name_of_organisation = fields.Char(string="Name of organisation")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    position_held_id = fields.Many2one('hr.job', string="Position Held")
    reason_for_leaving = fields.Text(string="Reasons for leaving")
    jobs_database_id = fields.Many2one('jobs.database', string="Jobs Database")