# -*- coding: utf-8 -*-
{
    'name': "Voucher Vendor Management",

    'summary': """
        Asisst business unit to manage vendors that are registered to provide services to successfull youth applicants.
        """,

    'description': """
        Asisst business unit to manage vendors that are registered to provide services to successfull youth applicants.
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
}