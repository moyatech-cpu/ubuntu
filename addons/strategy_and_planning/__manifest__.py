# -*- coding: utf-8 -*-
{
    'name': 'Strategy and Planning',

    #    'summary': """
    #       Mentorship Application Form for Youth Enquiry and Partner Enquiry
    #    """,

    #   'description': """
    #     Customer/Client can submit Application Form and as per enquiry Product and Service team attends to the Application
    #   """,

    'sequence': 6,
    'author': 'TechUltra Solutions',
    'website': 'https://www.techultrasolutions.com',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base','sms_email','hr'],

    'data': [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "data/mail_template.xml",
        "report/performance_report_export_view.xml",
        "report/divisional_execution_plan_report_view.xml",
        "report/report.xml",
        "views/strategic_plan.xml",
        "views/strategic_goals.xml",
        "views/annual_performance_plan_views.xml",
        "views/annual_performance_plan_target_views.xml",
        "views/strategic_plan_objectives.xml",
        "views/execution_targets.xml",
        # "views/report_back_view.xml",
        'views/project_plan_linkage_views.xml',
        'views/project_plan_target_views.xml',
        'views/project_plan_all_view.xml',
        'views/admin_interface_view.xml',
    ],
    'demo': [

    ],
}
