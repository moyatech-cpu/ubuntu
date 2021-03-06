# -*- coding: utf-8 -*-
{
    'name': "system_update_008",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','nyda_grant_and_voucher','bmt_training','client_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/regional_training_data_report.xml',
        'report/regional_training_data_template.xml',
        'wizard/regional_training_report_wizard_view.xml',
        
        'wizard/regional_grant_status_report_wizard_view.xml',
        'report/regional_grant_status_template.xml',
        'report/regional_grant_status_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}