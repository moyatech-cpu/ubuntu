# -*- coding: utf-8 -*-
{
    'name': "NYDA System",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "TechUltra SOlutiuons",
    'website': "http://www.techultrasolutions.com",

    'category': 'System',
    'version': '11.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/services_view.xml',
    ],
}