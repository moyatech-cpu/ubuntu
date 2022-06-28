# -*- coding: utf-8 -*-
{
    'name': "System updates 006",

    'summary': """
        Module to add field for region
        """,

    'description': """
        Module to add field for region for regional support
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    'category': 'system_updates',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','client_management','mentorship'],

    # always loaded
    'data': [
        'views/branch_view_inherit.xml',
        'views/users_view_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
