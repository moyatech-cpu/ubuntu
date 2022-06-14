# coding=utf-8
from twilio.rest import Client


class TwilioSMSHelper:
    """ SMS Helper class to send sms from Odoo """

    def __init__(self):
        """ Currently setting up account SID and Auth Token statically on initialization. """
        self.account_sid = ""
        self.auth_token = ""

    def send_enquiry_sms(self, data):
        """ Send sms to youth/partner once request is received. """
        message_text = "Thank you, We have received your enquiry. Use your ID no. when making a follow-up. \n Regards," \
                       " \n NYDA."
        try:
            client = Client(self.account_sid, self.auth_token)
            message = client.messages.create(body=message_text, from_=data.get('message_from'),
                                             to=data.get('message_to'))
            print(message)
        except:
            pass
        finally:
            print("Message sent.")
