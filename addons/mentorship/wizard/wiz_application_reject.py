# coding=utf-8
from odoo import api, fields, models, _


class WizardApplicationReject(models.TransientModel):
    """ Wizard for asking result on rejecting mentor/mentee application """
    _name = "wiz.application.reject"

    reason_rejected = fields.Text("Reason for Rejection")

    def reject_application(self):
        """ Action to be performed when clicked on confirm button. """
        active_obj = self.env[self._context.get('active_model')].search(
            [('id', '=', self._context.get('active_id'))])
        active_obj.write({
            'reject_reason': self.reason_rejected,
            'state': 'reject'
        })
        mail_template_id = False
        if self._context.get('active_model') == 'mentee.application':
            mail_template_id = self.env.ref('mentorship.mentee_application_reject_mail_template')
        elif self._context.get('active_model') == 'mentor.application':
            mail_template_id = self.env.ref('mentorship.mentor_application_reject_mail_template')
        if mail_template_id:
            mail_template_id.with_context(mail_from=self.env.user.partner_id.email).\
                send_mail(active_obj.id, force_send=True)
        return True
