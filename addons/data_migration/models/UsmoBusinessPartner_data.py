from odoo import api, fields, models

class UsmoBusinessPartner(models.Model):
    _name = 'usmo.business.partner'

    Deleted = fields.Char(string='Deleted')
    FirstName = fields.Char(string='First Name')
    IDNumber = fields.Char(string='ID Number')
    IsDisabled = fields.Char(string='Is Disabled')
    IsMale = fields.Char(string='Is Male')
    IsRural = fields.Char(string='Is Rural')
    LastName = fields.Char(string='Last Name')
    PartnerOfUser = fields.Char(string='Partner Of User')
    PartnershipEndDate = fields.Char(string='Partnership End Date')
    PartnershipStartDate = fields.Char(string='Partnership Start Date')
    Race = fields.Char(string='Race')
    RowGUID = fields.Char(string='Row GUID')
    TelNo = fields.Char(string='Tel No')