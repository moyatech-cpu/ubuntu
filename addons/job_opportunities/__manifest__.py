# -*- coding: utf-8 -*-
{
    'name': "Jobs Opportunities",

    'summary': """
        Job Posting, Applying Jobs""",

    'description': """
        Long description of module's purpose
    """,

    'author': "MOYATECH",
    'website': "http://www.moyatech.co.za",

    'category': 'Jobs',
    'version': '11.0',

    # any module necessary for this one to work correctly
    'depends': ['base','client_management', 'web_digital_sign', 'hr', 'website'],

    # always loaded
    'data': [
        'demo/demo.xml',
        'demo/mail_template.xml',
        'security/ir.model.access.csv',
        'views/opp_provider_view.xml',
        'views/job_location_view.xml',
        'views/jobs_database_views.xml',
        'views/job_database_register_template.xml',
        'views/career_template.xml',
        'views/service_provider_template.xml',
        'views/matric_results_view.xml',
        'views/ter_high_education_view.xml',
        'views/comp_skills_view.xml',
        'views/organisations_view.xml',
        'views/referees_view.xml',
        'views/assets_modifier.xml',
        'views/opportunities_view.xml',
        'views/industry_sector_view.xml',
        'views/degree_view.xml',
        'views/application_view.xml',
        'wizard/jobs_report_wizard.xml',
        'report/jobs_report_template.xml',
        'report/jobs_report.xml',
    ],
}