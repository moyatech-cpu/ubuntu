# -*- coding: utf-8 -*-
{
    'name': 'Risk Management',

    'summary': """
       Risk Management module.
    """,

    'description': """
      This module consists of all configurations and flow for organisational risk management .
    """,

    'sequence': 6,
    'author': 'MOYATECH',
    'website': 'http://www.moyatech.co.za',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base', 'mail', 'strategy_and_planning', 'hr','web_notify','client_management'],
    'application': True,
    'data': [
        'security/risk_groups.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/mail_templates.xml',
        'wizard/wiz_risk_reporting_comment_view.xml',
        'views/risk_management_views.xml',
        'views/risk_compliance_views.xml',
        'views/risk_insurance_views.xml',
        'views/loss_damage_assets_views.xml',
        'views/particular_claims_view.xml',
        'views/insurance_excess_view.xml',
        'views/recovery_view.xml',
        'views/risk_report_views.xml',
        'wizard/report_wiz.xml',
        'views/res_config_settings_views.xml',
        'views/enterprise_risk_views.xml',
    ],
}
