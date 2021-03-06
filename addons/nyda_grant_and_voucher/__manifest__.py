# -*- coding: utf-8 -*-


{
    'name': 'Grant and Voucher',

    'summary': """
       Grant and Voucher is provide link between beneficiary and service provider.
    """,

    'description': """
      Service provider/Mentor can submit oppotunity and according BOA link beneficiary to Service provider/Mentor and upload a linkage
      report also Monitoring and Evaluate the both Service provider and Beneficiary
    """,

    'sequence': 8,
    'author': 'Moyatech',
    'website': 'http://www.moyatech.co.za',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base', 'client_management', 'mail', 'mentorship', 'hr', 'bmt_training', 'market_linkage'],
    'application': True,

    'data': [
        'security/grant_voucher_security.xml',
        'security/ir.model.access.csv',
        'security/enquiry_rule.xml',
        'wizard/sent_rejection_letter.xml',
        'wizard/approve_letter.xml',
        'wizard/refer_to_correctrion_wiz_view.xml',
        'wizard/deligence_wiz.xml',
        'wizard/ict_wiz.xml',
        'wizard/inspect_wiz.xml',
        'wizard/bdo_reject_wiz.xml',
        'wizard/investment_uploaded_view.xml',
        'wizard/schedule_appointment_wizard.xml',
        'wizard/select_service_provider_wizard.xml',
        'wizard/schedule_grant_appointment.xml',
        'wizard/work_plan_submit_wizard.xml',
        'wizard/client_approve_reject_wizard.xml',
        'wizard/assessment_report_view.xml',
        'wizard/bdo_accept_confirm_wizard.xml',
        'wizard/bm_accept_confirm_wizard.xml',
        'wizard/bsc_accept_confirm_wizard.xml',
        'wizard/edm_accept_confirm_wizard.xml',
        'wizard/qao_accept_confirm_wizard.xml',
        'wizard/bdo_rejection_reason_wizard.xml',
        'wizard/bgarg_approve_wizard.xml',
        'wizard/bm_rejection_report_wizard.xml',
        'wizard/bcs_rejection_report_wizard.xml',
        'wizard/qao_rejection_report_wizard.xml',
        'wizard/edm_rejection_report_wizard.xml',
        'wizard/disbursement_pack_view.xml',
        'wizard/proof_of_payment.xml',
        'wizard/submit_product_wiz.xml',
        'wizard/voucher_pop_wiz.xml',
        'wizard/post_disbursement_wiz.xml',
        'wizard/rejection_reason_view.xml',
        'wizard/refer_to_hogac_view.xml',
        'wizard/any_query_view.xml',
        'wizard/letter_sent_view.xml',
        'wizard/cancel_voucher_wiz_view.xml',
        'wizard/attendance_register.xml',
        'wizard/voucher_supporting_documents.xml',
        'views/any_query_record_view.xml',
        'data/grant_data.xml',
        'data/mail_templates.xml',
        'data/data.xml',
        'data/sequence.xml',
        'views/assets.xml',
        'views/pre_assesment_veiw.xml',
        'views/preassessment_templates.xml',
        'views/voucher_templates.xml',
        'views/grant_application.xml',
        'views/voucher_application.xml',
        'views/voucher_isurance_view.xml',
        'views/voucher_assessment_view.xml',
        'wizard/grant_status_report.xml',
        'wizard/users_report_wizard.xml',
        'wizard/aftercare_report_wizard.xml',
        'wizard/grant_report_wizard_view.xml',
        'wizard/all_voucher_search_view.xml',
        'views/grant_templates.xml',
        'views/templates.xml',
        'views/pitch_polish_rating_view.xml',
        'views/investment_memo.xml',
        'views/aftercare_view.xml',
        'views/business_development_assistance.xml',
        'views/partner_enquiry_inherit.xml',
        'wizard/recomendation_note_voucher.xml',
        'wizard/reject_reason_pcbc.xml',
        'wizard/query_pcbc_view.xml',
        # 'wizard/voucher_status_report.xml',
        'wizard/voucher_status_report.xml',
        'reports/grant_report.xml',
        'reports/grant_report_template.xml',
        'reports/report.xml',
        'reports/investment_memo_card.xml',
        'reports/users_report.xml',
        'reports/users_report_template.xml',
        'reports/status_bdo_report.xml',
        'reports/status_bdo_template.xml',
        'reports/status_branch_template.xml',
        'reports/status_client_template.xml',
        'reports/status_disable_template.xml',
        'reports/status_gender_template.xml',
        'reports/status_race_template.xml',
        'reports/status_rural_urban_template.xml',
        'reports/status_aftercare_report.xml',
        'reports/status_branch_cons_template.xml',
        'reports/status_sp_report.xml',
        'reports/status_service_template.xml',
        'reports/voucher_assessment_template.xml',
        'reports/voucher_assessment_report.xml',
        'reports/report_assessment_appointment.xml',
        'reports/report_assessment_conducted.xml',
        # 'reports/report_grant.xml',
        'reports/report_status_aftercares.xml',
        'reports/report_status_bdo.xml',
        'reports/report_status_branch_cons_grant.xml',
        'reports/report_status_branch_cons.xml',
        'reports/report_status_branch_grant.xml',
        'reports/report_status_branch.xml',
        'reports/report_status_client_applications.xml',
        'reports/report_status_client.xml',
        'reports/report_status_disable.xml',
        'reports/report_status_gender.xml',
        'reports/report_status_race.xml',
        'reports/report_status_rural_urban.xml',
        'reports/report_status_service.xml',
        'reports/report_status_sp.xml',
        'reports/report_va.xml',
        'reports/report_voucher_beneficiaires.xml',
        'reports/report_voucher_expired.xml',
        'reports/report_voucher_issuance_multiple.xml',
        'reports/report_voucher_jobs_created.xml',
        'reports/report_voucher_payment_tracking.xml',
        'reports/report_voucher_payments.xml',
        'reports/report_voucher_redemptions.xml',
        'reports/report_voucher_reissued.xml',
        'reports/report_voucher_service_provider_query.xml',
        'reports/report_voucher_service_provider.xml',
        'reports/report_voucher_service_ratings.xml',

    ],
    'qweb': ['static/src/xml/thresholds_grant.xml'],
}
