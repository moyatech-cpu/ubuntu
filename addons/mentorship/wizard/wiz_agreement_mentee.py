# coding=utf-8
import datetime
from odoo import api, fields, models, _


class WizardAgreementMentee(models.TransientModel):
    """ Wizard for mentee to accept Mentorship agreement. """
    _name = "wizard.agreement.mentee"
    _description = " Wizard for mentee to accept Mentorship. "

    def accepted_by_mentee(self):
        """ Add user signature to current mentorship agreement. """
        agreement_id = self.env['mentorship.agreement'].search([('id', '=', self._context.get('active_id'))])
        vals = {
            'mentee_sign': agreement_id.mentee_id.signature,
            'mentee_sign_date': datetime.date.today(),
            'signed_by_mentee': True,
            'state': 'mentee_signed'
        }
        if agreement_id.mentor_sign:
            vals.update({'state': 'accepted',
                         'date_of_engagement': datetime.date.today()
                         })
        agreement_id.write(vals)
        return True
