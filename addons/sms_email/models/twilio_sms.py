# coding=utf-8
from twilio.rest import Client
from odoo.http import request


class TwilioSMSHelper:
    """ SMS Helper class to send sms from Odoo """

    def __init__(self):
        """ Currently setting up account SID and Auth Token statically on initialization. """
        sms = request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if sms.twilio_account_sid and sms.twilio_auth_token and sms.twilio_sms_default_number:
            self.twilio_account_sid = sms.twilio_account_sid
            self.twilio_auth_token = sms.twilio_auth_token
            self.default_number = sms.twilio_sms_default_number
        else:
            self.twilio_account_sid = ''
            self.twilio_auth_token = ''
            self.default_number = '+13613362334'

    def send_enquiry_sms(self, data):
        """ Send sms to youth/partner once request is received. """
        try:
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            message = client.messages.create(body=data.get('message_text'), from_=self.default_number,
                                             to=data.get('message_to'))
            print(message)
        except:
            print("Message not Sent.")
        finally:
            pass
            print("Message sent.")

    def send_sms(self, data):
        """ Send sms to provided details in data. """
        try:
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            client.messages.create(from_=data.get('twilio_sms_default_number') or self.default_number,
                                   to=data.get('message_to'),
                                   body=data.get('message_text')
                                   )
        except:
            pass
        finally:
            pass
