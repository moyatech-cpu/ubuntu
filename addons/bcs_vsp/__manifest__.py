# -*- coding: utf-8 -*-
{
    'name': "VP 19 Module",

    'summary': """
        BCS VP 19 form""",

    'description': """
        Module to fix the voucher value defect, compute voucher value on change, and add menu item for VP 19 form.
    """,

    'author': "Moyatech",
    'website': "http://erp.nyda.gov.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'products',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','nyda_grant_and_voucher'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/sequence.xml',
        'security/security.xml',
        'views/templates.xml',
        'report/report.xml',
        'report/report_bcs_vsp_template.xml',
        'views/bcs_vsp_views.xml',
        #'wizard/review.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}