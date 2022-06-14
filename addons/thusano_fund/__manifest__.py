# -*- coding: utf-8 -*-
{
    'name': "thusano_fund",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "MoyaTech",
    'website': "http://www.moyetech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website','client_management'],
    'application': True,

    # always loaded
    'data': [
        'security/thusano_group.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/ngp_npo_template.xml',
        'views/templates.xml',
        'wizard/thusano_report_wizard_view.xml',
        'views/thusano_reject_view.xml',
        'views/assets.xml',
        
        
        #'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/thusano_mail_template.xml',
        'reports/thusano_report.xml',
        'reports/thusano_report_template.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}