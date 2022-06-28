# coding=utf-8
import datetime

from odoo import api, fields, models, _


class WizardMentorApplicationSigned(models.TransientModel):
    """ Wizard for mentor to accept Mentorship agreement. """
    _name = "wizard.mentor.application.signed"
    _description = " Wizard for mentor to accept Mentorship. "

    signed_agreement = fields.Binary("Signed Agreement")

    def accepted_by_mentor(self):
        """ Add user signature to current mentorship agreement. """
        application_id = self.env['mentor.application'].search([('id', '=', self._context.get('active_id'))])
        mail_template_id = self.env.ref('mentorship.mentor_application_accept_mail_template')
        if mail_template_id:
            mail_template_id.with_context(mail_from=self.env.user.partner_id.email). \
                send_mail(application_id.id, force_send=True)
        vals = {
            'signed_agreement': self.signed_agreement,
            'state': 'accepted'
        }
        application_id.write(vals)
        return True


class WizardBGARGReviewUpload(models.TransientModel):
    """ Wizard for mentor to accept Mentorship agreement. """
    _name = "wizard.bgarg.review.upload"
    _description = " Wizard for mentor to accept Mentorship. "

    bgarg_minutes = fields.Binary("BGARG Minutes")

    def accepted_by_mentor(self):
        """ Add user signature to current mentorship agreement. """
        application_id = self.env['mentor.application'].search([('id', '=', self._context.get('active_id'))])
        vals = {
            'bgarg_minutes': self.bgarg_minutes,
            'state': 'bgarg_review'
        }
        application_id.write(vals)
        return True

class WizardRecommendationUpload(models.TransientModel):
    """ Wizard for mentor to accept Mentorship agreement. """
    _name = "wizard.recommendation.upload"
    _description = " Wizard for Recommendation. "

    recommendation_char = fields.Text("Recommendation")

    def accepted_recommendation_char(self):
        """ Add user signature to current mentorship agreement. """
        application_id = self.env['mentor.application'].search([('id', '=', self._context.get('active_id'))])
        mail_template_id = self.env.ref('mentorship.mentor_application_recommended_mail_template')
        if mail_template_id:
            mail_template_id.with_context(mail_from=self.env.user.partner_id.email). \
                send_mail(application_id.id, force_send=True)
        vals = {
            'recommendation_char': self.recommendation_char,
            'state': 'recommended'
        }
        application_id.write(vals)
        return True
