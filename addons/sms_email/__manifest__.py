# -*- coding: utf-8 -*-
{
    'name': "SMS E-mail",

    'summary': """
        Module for sending sms and emails""",

    'description': """
        Form view for Twilio sms and updated email templates
    """,

    'author': "TechUltra Solutions",
    'website': "https://www.techultrasolutions.com",

    'category': 'SMS',
    'version': '11.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','website_mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mail_template.xml',
        'views/twilio_sms_view.xml',
        'views/res_config_settings_view.xml',
    ],
}