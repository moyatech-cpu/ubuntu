# coding=utf-8
{
    'name': 'NYDA Human Resource Reports',

    'summary': """
       Human Resource Module
    """,

    'description': """
      Human Resource Module
    """,

    'sequence': 5,
    'author': 'MOYATECH',
    'website' : 'http://www.moyatech.co.za',
    'category': 'Reports',
    'version': '0.1',
    'application': True,

    'data': [
        'security/ir.model.access.csv',  

        'wizard/hr_performance_report_view.xml',
        'report/hr_performance_report_template.xml',
        'report/hr_performance_report.xml',
        
    ],
}