# coding=utf-8
{
    'name': 'Request For Quotation',

    'summary': """
       SCM Request for Quotation module for making the purchase process for the organisation.
    """,

    'description': """
      SCM Request for Quotation module for making the purchase process for the organisation.
    """,

    'sequence': 5,
    'author': 'Moyatech',
    'website' : 'http://www.moyatech.co.za',
    'category': 'Finance - SCM',
    'version': '0.1',
    'depends': ['purchase_requisition'],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'security/scm_user_groups.xml',
        'security/scm_record_rules.xml',
        'views/scm_rfq_main.xml',
        'views/vendor_management.xml',
        'wizard/recommendation_review_reject_reason.xml',

        'report/purchase_reports.xml',
        'report/purchase_quotation_templates.xml',
        
        'data/scm_rfq_sequence.xml',
        'data/mail_template_data.xml',        
    ],
}
