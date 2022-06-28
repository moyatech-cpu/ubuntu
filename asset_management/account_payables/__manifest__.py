# -*- coding: utf-8 -*-
{
    'name': "Accounting Payables",

    'summary': """
        NYDA Account Payables """,

    'description': """
        Account Payables custom module for NYDA
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'products',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','purchase','website', 'mail', 'portal', 'sms_email','account_receivables','nyda_grant_and_voucher','bcs_vsp','vp_system_update'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizards/transaction_enquiry_views.xml',
        'wizards/vendor_summary_views.xml',
        'views/vendor_batch_views.xml',
        'views/payable_views.xml',
        'views/payable_batch_views.xml',
        'views/authorization.xml',
        'views/eft_window.xml',
        'views/journal_batch_views.xml',
        'views/grant_batch_views.xml',
        'views/voucher_batch_views.xml',
        'views/bulk_grant_views.xml',
        'views/credit_note_batch_views.xml',
        #'views/voucher_reconciliation.xml',
        #'views/voucher_authorization.xml',
        #'report/report_authorization_voucher_template.xml',
        'report/report.xml',
        'report/report_invoice_purchase_template.xml',
        'report/report_first_posting_journal_template.xml',
        'report/report_reconciliation_template.xml',
        'report/report_authorization_template.xml',
        'report/report_print_eftpayables_template.xml',
        'report/report_general_post_journal_template.xml',
        'wizards/disbursement_pack_view.xml',
        #'report/report_reconciliation_voucher_template.xml',
        #'report/report_print_eftpayables_v_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}