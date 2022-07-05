# -*- coding: utf-8 -*-

from odoo import models, fields, api

class partners(models.Model):
    _name = 'nationalyouth.partnerz'

    name = fields.Char('Name')
    date = fields.Datetime('Date')
    color = fields.Integer()