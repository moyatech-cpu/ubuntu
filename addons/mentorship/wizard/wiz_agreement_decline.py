# coding=utf-8
from odoo import api, fields, models, _


class WizardAgreementDecline(models.TransientModel):
    """ When user clicks on decline Agreement change state to Declined. """
    _name = "wizard.agreement.decline"

    def agreement_declined(self):
        """ Declined by current user so save the user in declined by field and change state to Declined. """
        agreement_id = self.env['mentorship.agreement'].search([('id', '=', self._context.get('active_id'))])
        vals = {'declined_by': self.env.user.id,
                'state': 'declined'
                }
        agreement_id.write(vals)
        return True
