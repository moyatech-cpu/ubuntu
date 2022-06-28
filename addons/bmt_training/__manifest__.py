# -*- coding: utf-8 -*-
{
    'name': "BMT Training",

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
        'data/res_data.xml',
        'security/bmt_training_security.xml',
        'security/ir.model.access.csv',
        'security/mail_template.xml',
        'views/assets_backend.xml',
        'data/data.xml',
        'data/mail_template.xml',
        'wizard/signature_wizard_view.xml',
        'wizard/wiz_reject_reason_view.xml',
        'wizard/training_rejection_view.xml',
        'wizard/tech_training_rej_view.xml',
        'views/course_view.xml',
        'views/bmt_participants_view.xml',
        'views/business_management_training_view.xml',
        'views/pddd_overall_training_veiw.xml',
        'views/bmt_pitching_participants_view.xml',
        'views/bmt_pitching_view.xml',
        'views/youth_enquiry_view.xml',
        'views/sales_pitch_training_views.xml',
        # 'views/op_admission_register_view.xml',
        'views/bmt_training_application_form.xml',
        'views/cop_gov_training.xml',
        'views/company_view.xml',
        'views/technical_training_view.xml',
        'views/technical_training_apprenticeship_view.xml',
        'views/enrolled_users_view.xml',
        'views/link_trainer_view.xml',
        'wizard/training_report_wizard.xml',
        'report/attendance_report_template.xml',
        'report/attendance_report.xml',
        'report/training_report_template.xml',
        'report/training_schedule_report_template.xml',
        'report/training_report.xml',
        'report/bmt_certificate_template.xml',
        'report/bmt_certificate.xml',
        'report/coop_certi_template.xml',
        'report/coop_certi.xml',
    ],
}
