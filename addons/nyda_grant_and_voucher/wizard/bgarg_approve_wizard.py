from odoo import fields, api, models

from datetime import date

class BGARGApproveWizard(models.TransientModel):
    _name = 'bgarg.approve.wizard'
    _description = 'BGARC Approve Letter'


    bgarg_declaration_of_interest = fields.Binary(string='Declaration Of Interest')
    brarg_declaration_of_interest_name = fields.Char(string='File Name')
    bgarg_minutes = fields.Binary(string='Minutes')
    bgarg_minutes_name = fields.Char(string='File Name')
    bgarg_approval_letter_send_date = fields.Date(string="Date")

    @api.multi
    def bgarg_approve_submit(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        bgarg_as = grant_application.write({
            'brarg_declaration_of_interest_name': self.brarg_declaration_of_interest_name,
            'bgarg_declaration_of_interest': self.bgarg_declaration_of_interest,
            'bgarg_minutes_name': self.bgarg_minutes_name,
            'bgarg_minutes': self.bgarg_minutes,
            'bgarg_approval_letter_send_date': self.bgarg_approval_letter_send_date,
            'x_bgarg_approval_letter_name': self.x_bgarg_approval_letter_name,
            'x_bgarg_approval_letter': self.x_bgarg_approval_letter,
        })
        grant_application.status = 'approved'
        return True
