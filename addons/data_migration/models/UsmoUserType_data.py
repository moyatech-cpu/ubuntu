from odoo import api, fields, models

class UsmoUserType(models.Model):
    _name= 'usmo.user.type'

    Description = fields.Char(string='Description')
    IsBranchUser = fields.Char(string='Is Branch User')