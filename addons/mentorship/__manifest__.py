# -*- coding: utf-8 -*-
{
    'name': 'Mentorship',

    'summary': """
       Mentorship Application Form for Youth Enquiry and Partner Enquiry
    """,

    'description': """
      Customer/Client can submit Application Form and as per enquiry Product and Service team attends to the Application
    """,

    'sequence': 6,
    'author': 'Moyatech',
    'website': 'http://www.moyatech.co.za',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base', 'mail', 'client_management', 'web_digital_sign', 'website'],
    'application': True,

    'data': [
        'views/res_data.xml',
        'data/data.xml',
        'data/mail_templates.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'security/own_mentorship_rule.xml',
        'report/mentee_application_reports.xml',
        'report/mentee_application_form_report_views.xml',
        'report/mentor_application_form_report_view.xml',
        'report/mentorship_agreement_views.xml',
        'report/mentor_decline_views.xml',
        'wizard/wiz_agreement_mentee.xml',
        'wizard/wiz_mentor_application_signed.xml',
        'wizard/wiz_agreement_mentor.xml',
        'wizard/wiz_agreement_decline.xml',
        'wizard/wiz_application_reject.xml',
        'views/mentee_application_views.xml',
        'views/mentor_application_views.xml',
        'views/mentorship_agreement_views.xml',
        'views/assets.xml',
        'views/templates.xml',
        'views/res_users.xml',
    ],
}
