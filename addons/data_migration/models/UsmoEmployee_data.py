from odoo import api, fields, models

class UsmoEmployee(models.Model):
    _name = 'usmo.employee'

    CreatedDT = fields.Char(string='Created DT')
    Deleted = fields.Char(string='Deleted')
    EmployeeOfUser = fields.Char(string='Employee Of User')
    EmploymentEndDate = fields.Char(string='Employment End Date')
    EmploymentStartDate = fields.Char(string='Employment Start Date')
    FirstName = fields.Char(string='First Name')
    IDNumber = fields.Char(string='ID Number')
    IsDisabled = fields.Char(string='Is Disabled')
    IsMale = fields.Char(string='Is Male')
    IsRural = fields.Char(string='Is Rural')
    LastName = fields.Char(string='Last Name')
    Race = fields.Char(string='Race')
    RowGUID = fields.Char(string='Row GUID')
    TelNo = fields.Char(string='Tel No')
    TypeOfEmployment = fields.Char(string='Type Of Employment')