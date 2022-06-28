# -*- coding: utf-8 -*-
{
    'name': "NYDA Accounting Receivables",

    'summary': """
        Accounting Receivables Module""",

    'description': """
        NYDA custom module for Accounting Receivables Management. This module includes additional fields to customer details, invoices and coveres additional functionality for batch processing of invoices.
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'products',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','purchase','website', 'mail', 'portal', 'sms_email'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/cust_review_views.xml',
        'wizard/final_review.xml',
        'wizard/transaction_enquiry_views.xml',
        'wizard/customer_summary_views.xml',
        'views/receivable_views.xml',
        'data/sequence.xml',
        'wizard/review.xml',
        'views/customer_views.xml',
        'views/customer_batch_views.xml',
        'report/report.xml',
        'report/report_trans_enq_template.xml',
        'report/report_batch_entry_template.xml',
        'report/report_invoice_template.xml',
        'report/report_general_post_journal_template.xml',
        'report/report_cash_receipt_journal_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}