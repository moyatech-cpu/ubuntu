# coding=utf-8
import datetime

from odoo import api, fields, models, _


class WizardAgreementMentor(models.TransientModel):
    """ Wizard for mentor to accept Mentorship agreement. """
    _name = "wizard.agreement.mentor"
    _description = " Wizard for mentor to accept Mentorship. "

    def accepted_by_mentor(self):
        """ Add user signature to current mentorship agreement. """
        agreement_id = self.env['mentorship.agreement'].search([('id', '=', self._context.get('active_id'))])
        vals = {
            'mentor_sign': agreement_id.mentor_id.signature,
            'mentor_sign_date': datetime.date.today(),
            'signed_by_mentor': True,
            'state': 'mentor_signed'
        }
        if agreement_id.signed_by_mentee:
            vals.update({'state': 'accepted',
                         'date_of_engagement': datetime.date.today()
                         })
        agreement_id.write(vals)
        return True
