# -*- coding: utf-8 -*-
{
    'name': "Voucher Suppliers Reports",

    'summary': """
        Retrieve Voucher Suppliers reports
        """,

    'description': """
        Retrieve all kinds of reports from voucher supplier and voucher applications data.
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    'category': 'system_updates',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','nyda_grant_and_voucher','voucher_suppliers'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'data/sequence.xml',
        'wizard/voucher_supplier_report_wizard.xml',
        'report/report.xml',
        'report/report_voucher_supplier_template.xml',
        #'views/date_update_internal_report_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}