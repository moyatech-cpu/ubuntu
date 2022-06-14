from odoo import api, fields, models


class TwilioSms(models.Model):
    _name = 'twilio.sms'
    _rec_name = 'message_model_id'

    message_text = fields.Text(string='Message')
    # twilio_sms_default_number = fields.Char(string='From')
    # message_to = fields.Char(string='To')
    message_model_id = fields.Many2one('ir.model', string="Message Model")
    type = fields.Selection([('create', 'Creation'), ('write', 'Updating'), ('archive', 'Archiving')],
                            string="Send Message On")
