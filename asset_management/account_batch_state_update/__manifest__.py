# -*- coding: utf-8 -*-
{
    'name': "Batch Asset Disposal Update",

    'summary': """
        Batch Asset Management Module 
        """,

    'description': """
        Accomodate workflows and status
        
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    'category': 'assets',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_asset_management','account_asset_batch','nyda_asset_management'],

    # always loaded
    'data': [
        'report/report.xml',
        'report/report_dep_asset_template.xml',
        'report/report_asset_transfer_template.xml',
        'report/report_asset_disposal_template.xml',
        'report/report_bcs_vsp_template.xml',
        'wizard/asset_dep_reports_views.xml',
        'wizard/asset_transfer_report_views.xml',
        'wizard/asset_disposal_report_views.xml',
        'wizard/review.xml',
        'views/batch_asset_disposal_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}