# -*- coding: utf-8 -*-
{
    'name': "Learning Development",

    'summary': """
        Facilitates the submission of bursary and study applications processes for employees""",

    'description': """
        Facilitates the submission of bursary and study applications processes for employees
    """,

    'author': "Moyatech",
    'website': "http://www.moyatech.co.za",
    'category': 'Learning',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'client_management', 'strategy_and_planning','monitoring_and_evaluation'],

    # always loaded
    'data': [
        'security/security.xml',
        'data/data.xml',
        'security/ir.model.access.csv',
        'wizard/approve_reject_view.xml',
        'views/inherit_hr_employee.xml',
        'views/learning_development.xml',
        'views/institution_view.xml',
        'wizard/assign_remove_group.xml',
        'wizard/bursary_external_report_view.xml',
        'report/bursray_external_report_template.xml',
        'report/bursray_external_report.xml'
    ],
}