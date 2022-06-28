# -*- coding: utf-8 -*-
{
    'name': 'Market Linkage',

    'summary': """
       Market Linkage is provide link between beneficiary and service provider.
    """,

    'description': """
      Service provider/Mentor can submit oppotunity and according BOA link beneficiary to Service provider/Mentor and upload a linkage
      report also Monitoring and Evaluate the both Service provider and Beneficiary
    """,

    'sequence': 8,
    'author': 'Moyatech',
    'website' : 'http://www.moyatech.co.za',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base', 'client_management', 'mail', 'mentorship'],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'security/enquiry_rule.xml',
        'data/mail_templates.xml',
        'data/data.xml',
        'wizard/beneficiary_wiz.xml',
        'wizard/linkage_report.xml',
        'wizard/project_closeout_report.xml',
        'views/assets.xml',
        'views/products_services_templates.xml',
        'views/register_opportunity_views.xml',
        'views/mkl_beneficiary_views.xml',
        'views/opportunity_match_views.xml',
        'views/res_users.xml',
    ],
}
