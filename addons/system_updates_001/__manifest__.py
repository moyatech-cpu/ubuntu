# -*- coding: utf-8 -*-
{
    'name': "System updates 001",

    'summary': """
        Module update client.preassessment & pitch.polish.rating
        """,

    'description': """
        This module will integrate additional method for reject business process within the submitted client.preassessment
        the state field is also affected by this update together with the pitch.polish.rating.
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    'category': 'system_updates',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','nyda_grant_and_voucher'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/mail_templates.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}