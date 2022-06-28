from odoo import api, fields, models

class USmoUserService(models.Model):
    _name = 'usmo.user.service'

    RowGUID = fields.Char(string='Row GUID')
    ServiceType = fields.Char(string='Service Type')
    ServiceUser = fields.Char(string='Service User')