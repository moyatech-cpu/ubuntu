# coding=utf-8
import base64
from odoo import api, fields, models, _
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper
from datetime import date
from odoo import modules
from odoo import http


class PitchAndPolishUpdate(models.Model):
   
    _inherit = 'pitch.polish.rating'
    
    
    def get_default_file():
        with open(modules.get_module_resource('system_update_005', 'static', 'RequiredDocuments.pdf'),'rb') as f:
            return base64.b64encode(f.read())
        
    grant_required_docs = fields.Binary(default=get_default_file())
    
    
    
    @api.multi
    def btn_recommend(self):
        """ Sets state to recommended. Add logic if need anything once application is moved to recommended state. """
        attachment = {
            'name': str("GrantRequiredDocuments"),
            'datas': self.grant_required_docs,
            'datas_fname': "GrantRequiredDocuments",
            'res_model': 'pitch.polish.rating',
            'type': 'binary'
        }
        
        ir_attechment_id = self.env['ir.attachment'].create(attachment)
        
        mail_template_id = self.env.ref('nyda_grant_and_voucher.picth_and_polish_mail_template')
        active_id = self._context.get('active_id')
        preassessment_id = self.env['client.preassessment'].browse([active_id])
        for rec in self:
            if mail_template_id:

                base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                base_url += '/web/login?db={}#id={}&view_type=form&model=client.preassessment'.format(self.env.cr.dbname,
                                                                                                 preassessment_id.id)
                mail_template_id.attachment_ids = [(6,0,[])]
                mail_template_id.attachment_ids = [(4, ir_attechment_id.id)]
                mail_template_id.with_context(user=self.env.user, grant_url=base_url).send_mail(rec.id, force_send=True)
            rec.write({'state': 'recommended'})
            if preassessment_id:
                ts = TwilioSMSHelper()
                ts.send_sms({
                'message_to': preassessment_id.cell,
                'message_text': """Hello, \n Your application has been recommended has been accepted.\n You can login to system to check details."""
                })
                preassessment_id.write({'state': 'recommended'})