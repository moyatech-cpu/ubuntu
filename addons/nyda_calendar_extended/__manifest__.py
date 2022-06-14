# coding=utf-8
{
    'name': 'NYDA Calendar Event Extended',

    'summary': """
       Extended Calendar Event module from base to include events to all committee members at once.
    """,

    'description': """
      Extended Calendar Event module from base to include events to all committee members at once.
    """,

    'sequence': 5,
    'author': 'TechUltra Solutions',
    'website' : 'https://www.techultrasolutions.com',
    'category': 'Products',
    'version': '0.1',
    'depends': ['calendar', 'client_management'],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'views/res_modifications.xml',
        'views/calendar_inherit.xml',
    ],
}