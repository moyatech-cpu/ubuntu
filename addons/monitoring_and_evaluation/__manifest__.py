# -*- coding: utf-8 -*-
{
    'name': 'Monitoring and Evaluation',

    'summary': """
       Reporting against the planned targets from individual up to divisional
    """,

    # 'description': """
    #   Customer/Client can submit Register/Enquiry Form and as per enquiry Product and Service team attends to the enquiry
    # """,

    'sequence': 8,
    'author': 'TechUltra Solutions',
    'website' : 'https://www.techultrasolutions.com',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base','hr','web_digital_sign','strategy_and_planning', 'sms_email'],

    'data': [
        'security/security.xml',
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/monitoring_report_views.xml',
        'views/employee_monitoring_report_view.xml',
        'views/res_partner_view.xml',
    ],
}