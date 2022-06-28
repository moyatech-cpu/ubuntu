# -*- coding: utf-8 -*-

{
    'name': 'Data Migration',

    'summary': """
       Voucher data migration.
    """,

    'description': """
      Voucher data migration.
    """,

    'sequence': 8,
    'author': 'TechUltra Solutions',
    'website': 'https://www.techultrasolutions.com',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base'],
    'application': True,
    'data': [
        'views/UmsoVoucher_data_view.xml',
        'views/UmsoVoucherStatus_data_view.xml',
        'views/UsmoAftercare_data_view.xml',
        'views/UsmoAssessment_data_view.xml',
        'views/UsmoBusinessPartner_data_view.xml',
        'views/UsmoEmployee_data_view.xml',
        'views/UsmoFIle_data_view.xml',
        'views/UsmoFinancerType_data_view.xml',
        'views/UsmoServiceType_data_view.xml',
        'views/USmoUserService_data_view.xml',
        'views/UsmoUserType_data_view.xml',
        'views/UsmoVoucherQuery_data_view.xml',
        'views/UsmoVoucherReassign_data_view.xml',
    ],
    'qweb': [],
}
