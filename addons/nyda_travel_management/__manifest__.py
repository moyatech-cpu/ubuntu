# coding=utf-8
{
    'name': 'Travel Management',

    'summary': """
       Travel Management Module
    """,

    'description': """
      Travel Management Module assists the organisation with the processing and administration of employee travel arrangements. 
    """,

    'sequence': 5,
    'author': 'Moyatech',
    'website' : 'http://www.moyatech.co.za',
    'category': 'Administration',
    'version': '0.1',
    #'depends': ['product'],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'security/scm_user_groups.xml',
        'security/scm_travel_record_rules.xml',
        'views/travel_management.xml',
        #'views/vendor_management.xml',
        'wizard/travel_request_report_view.xml',
        #'wizard/travel_purchase_order_report_view.xml',
        
        'report/travel_purchase_order_report.xml',
        'report/travel_purchase_order_report_template.xml',
        'report/travel_request_report_template.xml',
        'report/travel_request_report.xml'        
    ],
}
