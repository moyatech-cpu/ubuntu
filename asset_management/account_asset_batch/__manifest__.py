# -*- coding: utf-8 -*-
{
    'name': "Batch Asset Disposal",

    'summary': """
        Batch Asset Management Module 
        """,

    'description': """
        Batch Asset Management Module that provides a soluction to batch processing of assets in a batch
        
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    'category': 'assets',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_asset_management','nyda_asset_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/batch_asset_disposal_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}