from odoo import api, fields, models

class UsmoServiceType(models.Model):
    _name = 'usmo.service.type'

    Composition = fields.Char(string='Composition')
    CreatedDT = fields.Char(string='Created DT')
    DefaultValue = fields.Char(string='Default Value')
    Enabled = fields.Char(string='Enabled')
    MinimumDuration = fields.Char(string='Minimum Duration')
    RowGUID = fields.Char(string='Row GUID')
    ServiceItemID = fields.Char(string='Service Item ID')
    ServiceName = fields.Char(string='Service Name')
