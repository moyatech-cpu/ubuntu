# -*- coding: utf-8 -*-


{
    'name': 'system update 13',

    'summary': """
       Voucher Module Update
    """,

    'description': """
      Voucher Re-Issuance implementation under voucher management module
    """,

    'sequence': 8,
    'author': 'TechUltra Solutions',
    'website': 'https://www.techultrasolutions.com',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base', 'nyda_grant_and_voucher'],
    'application': True,

    'data': [
        'wizard/voucher_supporting_documents.xml',

    ],
    
}
