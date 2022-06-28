from odoo import api, fields, models

class UsmoAftercare(models.Model):
    _name = 'usmo.aftercare'

    FinanceAmount = fields.Char(string='Finance Amount')
    FinancerBranch = fields.Char(string='Financer Branch')
    FinancerText = fields.Char(string='Financer Text')
    FinancerType = fields.Char(string='Financer Type')
    Followup1By = fields.Char(string='Followup 1 By')
    Followup1DT = fields.Char(string='Followup 1 DT')
    Followup1DateOfContact = fields.Char(string='Followup 1 Date Of Contact')
    Followup1Notes = fields.Char(string='Followup 1 Notes')
    Followup1StateOfBusiness = fields.Char(string='Followup 1 State Of Business')
    Followup1TypeOfContact = fields.Char(string='Followup 1 Type Of Contact')
    Followup2By = fields.Char(string='Followup 2 By')
    Followup2DT = fields.Char(string='Followup 2 DT')
    Followup2DateOfContact = fields.Char(string='Followup 2 Date Of Contact')
    Followup2Notes = fields.Char(string='Followup 2 Notes')
    Followup2StateOfBusiness = fields.Char(string='Followup 2 State Of Business')
    Followup2TypeOfContact = fields.Char(string='Followup 2 Type Of Contact')
    Voucher = fields.Char(string='Voucher')