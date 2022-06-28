# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MatricResults(models.Model):
    _name = 'matric.results'
    _description = 'Matric Results'

    subject = fields.Char(string="Subject")
    level_grade = fields.Selection(
        [('level_one', 'Level 1: 0 - 30%'), ('level_two', 'Level 2: 30 - 40%'), ('level_three', 'Level 3: 40 - 50%'),
         ('level_four', 'Level 4: 50 - 60%'), ('level_five', 'Level 5: 60 - 70%'), ('level_six', 'Level 6: 70 - 80%'),
         ('level_seven', 'Level 7: 80 - 100%')],
        string="Level/Grade")
    symbol = fields.Char(string="Symbol")
    certificate = fields.Binary(string="Certificate")
    certificate_name = fields.Char(string="Certificate Name")
    jobs_database_id = fields.Many2one('jobs.database', string="Jobs Database")