from odoo import api, fields, models

class UsmoFinancerType(models.Model):
    _name = 'usmo.financer.type'

    ID = fields.Char(string='ID')
    Name = fields.Char(string='Name')
