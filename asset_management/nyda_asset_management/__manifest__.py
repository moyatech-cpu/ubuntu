# -*- coding: utf-8 -*-
{
    'name': "Asset Management",

    'summary': """
        Asset management application for managing the life circle of assets within the organization""",

    'description': """
        Asset management application for managing the life circle of assets within the organization,
        includes  a fixed asset register,depreciation calculations, asset verification,transfer and disposals.
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Assets',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','account_asset_management','client_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/asset_disposal_sequence.xml',
        'data/asset_id_sequences.xml',
        'data/asset_transfer_sequence.xml',
        'data/asset_verification_sequence.xml',
        'security/asset_management_user_groups.xml',
        'views/asset_verification_views.xml',
        'views/asset_register_views.xml',
        'views/asset_transfer_views.xml',
        'views/asset_disposal_views.xml',
        'views/account_asset_profile.xml',
        #'views/templates.xml',
        'wizards/asset_verification_query_comment_views.xml',
        'wizards/asset_transfer_reject_reasons_views.xml',
    ],
    # only loaded in demonstration mode

}