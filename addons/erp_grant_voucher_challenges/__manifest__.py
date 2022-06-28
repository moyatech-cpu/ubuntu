# -*- coding: utf-8 -*-
{
    'name': "ERP Grant Challenges",

    'summary': """
        Module to update grant / voucher
        """,

    'description': """
        Module to update grant voucher challenges
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    'category': 'system_updates',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','nyda_grant_and_voucher','client_management','system_update_005'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/applications_report_wizard.xml',
        'report/report.xml',
        'report/report_grant_app_report_template.xml',
        'views/date_update_internal_report_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}