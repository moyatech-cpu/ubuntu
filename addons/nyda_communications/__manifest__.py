# -*- coding: utf-8 -*-
{
    'name': "nyda_communications",

    'summary': """
        Internal NYDA communications application for facilitating communication 
        in the organization""",

    'description': """
        Internal NYDA communications application for facilitating communication 
        in the organization
    """,

    'author': "MoyaTech",
    'website': "http://www.moyatech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Communication',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','client_management','hr','portal'],

    # always loaded
    'data': [
         #'security/ir.model.access.csv',
        'security/comm_user_groups.xml',
        'security/comm_record_rules.xml',
        
        'views/content_request.xml',
        'views/content_publishing.xml',
        'wizards/create_content_categories.xml',
        'wizards/create_content_subcategory.xml',
        'wizards/SM_ED_reject_content_publish_reason.xml',
        
        'data/content_request_sequence.xml',
        'data/content_publishing_sequence.xml',
        
         
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}