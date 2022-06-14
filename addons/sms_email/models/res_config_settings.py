
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    twilio_sms_default_number = fields.Char("Message From")
    twilio_account_sid = fields.Char("Account SID")
    twilio_auth_token = fields.Char("Auth Token")
    twilio_sms_default_country_code = fields.Char('Default Country Code (with "+")', default='+27')

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
        IrConfigPrmtr.set_param(
            "sms_email.twilio_sms_default_number", self.twilio_sms_default_number
        )
        IrConfigPrmtr.set_param(
            "sms_email.twilio_account_sid", self.twilio_account_sid
        )
        IrConfigPrmtr.set_param(
            "sms_email.twilio_auth_token", self.twilio_auth_token
        )
        IrConfigPrmtr.set_param(
            "sms_email.twilio_sms_default_country_code", self.twilio_sms_default_country_code
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
        twilio_sms_default_number = IrConfigPrmtr.get_param('sms_email.twilio_sms_default_number')
        twilio_account_sid = IrConfigPrmtr.get_param('sms_email.twilio_account_sid')
        twilio_auth_token = IrConfigPrmtr.get_param('sms_email.twilio_auth_token')
        twilio_sms_default_country_code = IrConfigPrmtr.get_param('sms_email.twilio_sms_default_country_code')
        res.update({
            'twilio_sms_default_number': twilio_sms_default_number,
            'twilio_account_sid': twilio_account_sid,
            'twilio_auth_token': twilio_auth_token,
            'twilio_sms_default_country_code': twilio_sms_default_country_code or '+27'
        })
        return res