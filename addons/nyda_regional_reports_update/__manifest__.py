# -*- coding: utf-8 -*-
{
    'name': "nyda_regional_reports_update",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/voucher_applications_report.xml',
        'report/voucher_applications_template.xml',
        'report/voucher_assessments_conducted_report.xml',
        'report/voucher_assessments_conducted_template.xml',
        'report/voucher_assessments_scheduled_report.xml',
        'report/voucher_assessments_scheduled_template.xml',
        'report/multiple_vouchers_report.xml',
        'report/multiple_vouchers_template.xml',
        'report/voucher_issuance_report_report.xml',
        'report/voucher_issuance_template.xml',
        'report/voucher_expired_voucher_report.xml',
        'report/voucher_expired_voucher_template.xml',
        'report/voucher_beneficiaries_supported_report.xml',
        'report/voucher_beneficiaries_supported_template.xml',
        'report/reissued_vouchers_report.xml',
        'report/reissued_vouchers_template.xml',
        'report/voucher_jobs_created_report.xml',
        'report/voucher_jobs_created_template.xml',
        'views/views.xml',
        'views/templates.xml',
        'wizard/voucher_application_wizard_view.xml',
        'wizard/voucher_assessments_conducted_wizard_view.xml',
        'wizard/voucher_assessments_scheduled_wizard_view.xml',
        'wizard/voucher_issuance_wizard_view.xml',
        'wizard/multiple_vouchers_wizard_view.xml',
        'wizard/voucher_beneficiaries_supported_wizard_view.xml',
        'wizard/voucher_expired_voucher_wizard_view.xml',
        'wizard/reissued_voucher_wizard_view.xml',
        'wizard/voucher_jobs_created_wizard_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}