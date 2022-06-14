# -*- coding: utf-8 -*-
{
    'name': "system_update_005",

    'summary': """
        This adds cancelling and reinstating functionalities to applications on the ERP system""",

    'description': """
        This adds cancelling and reinstating functionalities to applications on the ERP system
    """,

    'author': "MoyaTech",
    'website': "http://www.moyatech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Cancel & Reinstate Buttons',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','nyda_grant_and_voucher'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/client_preassessment_update_views.xml',
        'views/grant_application_view_update.xml',
        'views/voucher_application_view_update.xml',
        'views/templates.xml',
        'wizard/grant_and_voucher_update_wizard.xml',
        'wizard/voucher_application_wizard_update.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}