# coding=utf-8
from odoo import api, fields, models, _
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper
from datetime import date

from odoo import http


class PitchPolishRating(models.Model):
    _inherit = 'pitch.polish.rating'
    _rec_name = 'branch_id'
    
    state = fields.Selection([('new', 'New'), ('recommended', 'Recommended'),('rejected','Rejected')], default='new', string="State")

    @api.multi
    def btn_reject(self):
        """ Sets state to rejected. Add logic if need anything once application is moved to rejected state. """
        mail_template_id = self.env.ref('system_updates_001.picth_and_polish_reject_template')
        active_id = self._context.get('active_id')
        preassessment_id = self.env['client.preassessment'].browse([active_id])
        for rec in self:
            if mail_template_id:

                base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                base_url += '/web/login?db={}#id={}&view_type=form&model=client.preassessment'.format(self.env.cr.dbname,
                                                                                                 preassessment_id.id)

                mail_template_id.with_context(user=self.env.user, grant_url=base_url).send_mail(rec.id, force_send=True)
            rec.write({'state': 'rejected'})
            if preassessment_id:
                preassessment_id.write({'state': 'rejected'})
                #ts = TwilioSMSHelper()
                #ts.send_sms({
                #'#message_to': preassessment_id.cell,
                #'message_text': """Hello, \n Your Client Preassessment application has been rejected.\n You can login to system to check details."""
                #})
                

class ClientPreassessment(models.Model):
    _inherit = 'client.preassessment'
    _rec_name = 'client_id'


    state = fields.Selection([('new', 'New'), ('pitch_polish', 'Pitch and Polish'),('BMT_Referred','BMT Referred'), ('recommended', 'Recommended'),('rejected', 'Rejected')],
                             default='new', string="State")
    