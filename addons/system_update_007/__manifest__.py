# -*- coding: utf-8 -*-
{
    'name': "system_update_007",

    'summary': """
        Module to add the cancel and reinstate button""",

    'description': """
        Allow users to cancel and reinstate applications
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'System Updates',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','bmt_training'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/cancel_bmt_application_view.xml',
        'views/cancel_pitch_training_view.xml',
        'views/cancel_business_mgmt_training_view.xml',
        'views/cancel_sales_pitch_training_view.xml',
        'views/cancel_coop_governance_training_view.xml',
        'views/templates.xml',
        'wizard/cancel_bmt_application_wizard_view.xml',
        'wizard/cancel_business_mgmt_training_wizard_view.xml',
        'wizard/cancel_pitch_training_wizard_view.xml',
        'wizard/cancel_sales_pitch_wizard_view.xml',
        'wizard/cancel_coop_governance_training_wizard_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}