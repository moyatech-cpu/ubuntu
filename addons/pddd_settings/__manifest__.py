# -*- coding: utf-8 -*-
{
    'name': "PDDD Administration",

    'summary': """
        PDDD Administration Settings
        -Admin access rights to Client Management, Jobs and Opportunities, Training, BMT Training, Grant and Voucher
        -Manage users within PDDD department only
        """,

    'description': """
        PDDD Administration Settings
        This module defines PDDD Administrator user group that is responsible for maintaining access to all users within the PDDD modules,
        namely Client Management, Jobs and Opportunities, Training, BMT Training, Grant and Voucher. This user will also have access to
        all changes (states) or updates to the above mentioned modules.
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}