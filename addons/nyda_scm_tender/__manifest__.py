# coding=utf-8
{
    'name': 'Tender Purchasing',

    'summary': """
       SCM Tender Purchasing module for making the purchase process for the organisation.
    """,

    'description': """
      SCM Tender Purchasing module for making the purchase process for the organisation.
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
        'views/scm_tender_committee.xml',
        'views/scm_tender_main.xml',
        'views/scm_tender_evaluation.xml',

        'data/scm_tender_sequence.xml',
        'data/committees_sequence.xml',
        #'demo/demo.xml',
        
        'wizard/cancel_reject_wizard.xml',        
    ],
}
