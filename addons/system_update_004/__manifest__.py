# -*- coding: utf-8 -*-
{
    'name': "System updates 004",

    'summary': """
        Module to update grant threshold supporting documents
        """,

    'description': """
        Module to update grant threshold supporting documents
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    'category': 'system_updates',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','nyda_grant_and_voucher'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'data/mail_templates.xml',
        #'views/submit_product_wiz.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
