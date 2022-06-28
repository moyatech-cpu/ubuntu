from odoo import api,fields,models

class AfterCare(models.Model):
    _name = 'after.care'
    _rec_name = 'voucher'

    after_care = fields.Selection([('grant_ac', 'Grant AC'), ('voucher_ac', 'Voucher AC')], string='After Care')
    financeamount = fields.Char(string='Finance Amount')
    financerbranch = fields.Many2one('res.branch', string='Finance Branch')
    financertype = fields.Many2one('financer.type', string='Financer Type')
    followup1By = fields.Many2one('hr.employee', string='First Level Follow By')
    followup1DT = fields.Date(string='First Level Follow Date')
    followup1DateOfContact = fields.Date(string='First Level Followup Date Of Contact')
    followup1Notes = fields.Text(string='First Level Followup Notes')
    followup1StateOfBusiness = fields.Many2one('followup.state.business', string='First Level Followup State Of '
                                                                                 'Business')
    followup1TypeOfContact = fields.Many2one('followup.typeof.contact', string='First Level Followup Type Of Contact')
    followup2By = fields.Many2one('hr.employee', string='Second Level Follow By')
    followup2DT = fields.Date(string='Second Level Follow Date')
    followup2DateOfContact = fields.Date(string='Second Level Followup Date Of Contact')
    followup2Notes = fields.Text(string='Second Level Followup Notes')
    followup2StateOfBusiness = fields.Many2one('followup.state.business', string='Second Level Followup State Of '
                                                                                 'Business')
    followup2TypeOfContact = fields.Many2one('followup.typeof.contact', string='Second Level Followup Type Of Contact')
    voucher = fields.Many2one('voucher.application', string='Voucher')

    jobs_created = fields.Integer(string='Jobs Created')

    voucher_beneficiary_id = fields.Many2one('youth.enquiry', string='Beneficiary', related='voucher.beneficiary_id')


class FinancerBranch(models.Model):
    _name = 'financer.branch'
    _rec_name = 'name'

    name = fields.Char(String='Name')


class FinancerType(models.Model):
    _name = 'financer.type'
    _rec_name = 'name'

    name = fields.Char(String='Name')


class FollowupStateOfBusiness(models.Model):
    _name = 'followup.state.business'
    _rec_name = 'name'

    name = fields.Char(String='Name')


class FollowupTypeOfContact(models.Model):
    _name = 'followup.typeof.contact'
    _rec_name = 'name'

    name = fields.Char(String='Name')
