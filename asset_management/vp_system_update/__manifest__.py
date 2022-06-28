# -*- coding: utf-8 -*-
{
    'name': "VP19 System update",

    'summary': """
        Module to update grant / voucher
        """,

    'description': """
        Module to update grant voucher
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    'category': 'system_updates',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','nyda_grant_and_voucher','client_management','account','purchase','website', 'mail', 'portal', 'sms_email'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'data/mail_templates.xml',
        'security/security.xml',
        'wizard/edm_query_view.xml',
        #'wizard/disbursement_pack_view.xml',
        'report/report.xml',
        'report/report_sp_list_template.xml',
        #'report/report_bulk_grant_template.xml',
        'report/report_process_flow_template.xml',
        'report/report_internal_audit_template.xml',
        'views/bcs_vsp_views.xml',
        #'views/bulk_grant_views.xml',
        'views/date_update_internal_report_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}