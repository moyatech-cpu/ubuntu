# -*- coding: utf-8 -*-
{
    'name': "BMT Pitching Training Attendance",

    'summary': """
        You can manage different types of training""",

    'description': """
        You can manage training like sales pitch training, co-operative governance training, digital
        skills training, life skills training, job preparedness training,BMT Training, Short Skills
        training, Leanership Programme, Apprenticeship Programme.
    """,

    'author': "Techultra Solutions",
    'website': "http://www.techultrasolutions.com",
    'category': 'Training',
    'version': '11.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'nyda_risk_management', 'product', 'client_management', 'mentorship', 'web_digital_sign'],
    # , 'openeducat_admission','openeducat_facility'

    # always loaded
    'data': [
        
        'views/bmt_pitching_view.xml',
        'report/report_bus_mgmt_attendance_register.xml',
        'report/attendance_report.xml',
    ],
}
