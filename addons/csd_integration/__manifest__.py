# -*- coding: utf-8 -*-
{
    'name': "CSD Integration",

    'summary': """
        CSD Services""",

    'description': """
        CSD Integration of CSD services database to the NYDA ERP database for business suppliers. 
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Integration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    #'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/csd_integration_views.xml',
        'views/csd_templates_views.xml',
        'views/address_details_view.xml',
        'views/association_details_view.xml',
        'views/bbbee_certifcate_views.xml',
        'views/banking_details_view.xml',
        'views/contact_details_views.xml',
        'views/director_detail_views.xml',
        'views/supplier_base_views.xml',
        'views/tax_certificate_views.xml',
        'views/Accreditations_views.xml',
        'views/CommodityGroups_views.xml',
        'views/industryclassifications_views.xml',
        'views/realtime_enquiry_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}