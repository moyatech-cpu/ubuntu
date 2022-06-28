# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper
from odoo.exceptions import UserError, Warning
from datetime import datetime

class BmtTrainingApplicationInherit(models.Model):
    _inherit = 'bmt.training.application'

    client_preassessments_id = fields.Many2one('client.preassessment', string="Nearest Branch")

    @api.model
    def create(self, vals):
        rec = super(BmtTrainingApplicationInherit, self).create(vals)
        active_id = self._context.get('active_id')
        pich_and_police_id = self.env['pitch.polish.rating'].browse([active_id])
        if pich_and_police_id.client_preassessment_id:
            ts = TwilioSMSHelper()
            ts.send_sms({
            'message_to': pich_and_police_id.client_preassessment_id.cell,
            'message_text': """Hello, \n Your application has been Referred Apllication has been accepted.\n You can login to system to check details."""
            })
            rec.write({'client_preassessments_id': pich_and_police_id.client_preassessment_id.id or False})
        return rec
