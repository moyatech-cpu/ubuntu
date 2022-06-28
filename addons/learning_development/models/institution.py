# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Institution(models.Model):
    _name = 'institution'
    _rec_name = 'name'
    _description = 'Institution'

    name = fields.Char(string="Name")