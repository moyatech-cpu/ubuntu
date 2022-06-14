# -*- coding: utf-8 -*-

{
    'name': 'Client Management',

    'summary': """
       Client Management has Registration Form for Youth Enquiry and Partner Enquiry
    """,

    'description': """
      Customer/Client can submit Register/Enquiry Form and as per enquiry Product and Service team attends to the enquiry
    """,

    'sequence': 5,
    'author': 'Moyatech',
    'website' : 'http://www.moyatech.co.za',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base', 'website', 'mail', 'portal', 'sms_email'],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'security/client_security.xml',
        'security/enquiry_rule.xml',
        'data/data.xml',
        'data/res_data.xml',
        'data/mail_templates.xml',
        'data/enquiry_sequence.xml',
        'wizard/team_wiz.xml',
        'views/assets.xml',
        'views/register_templates.xml',
        'views/res_views.xml',
        'views/youth_enquiry_views.xml',
        'views/partner_enquiry_views.xml',
    ],
}
