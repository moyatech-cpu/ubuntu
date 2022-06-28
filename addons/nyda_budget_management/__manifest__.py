# coding=utf-8
{
    'name': 'Budget Management',

    'summary': """
       Budget Management Module
    """,

    'description': """
      Budget Management Module assists the organisation with the creation and administration of the organisational budget. 
    """,

    'sequence': 5,
    'author': 'Moyatech',
    'website' : 'http://www.moyatech.co.za',
    'category': 'Finance',
    'version': '0.1',
    'depends': ['account_budget'],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'security/budget_user_groups.xml',
        'security/budget_record_rules.xml',
        'views/budget_management.xml',
        'views/budget_reallocation.xml',
        'views/budget_configuration.xml',
        'wizard/reallocation_review_reject_reason.xml',
        'wizard/budget_report_view.xml',
        'report/budget_report.xml',
        'report/budget_report_template.xml',
        
    ],
}
