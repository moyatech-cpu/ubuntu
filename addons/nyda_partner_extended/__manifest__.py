# coding=utf-8
{
    'name': 'NYDA Partner Service Rating',

    'summary': """
       Extended Partner module from base to calculate an aggregate service rating for the service provider.
    """,

    'description': """
      Extended Partner module from base to calculate an aggregate service rating for the service provider
    """,

    'sequence': 5,
    'author': 'MOYATECH',
    'website' : 'http://www.moyatech.co.za',
    'category': 'Contacts',
    'version': '0.1',
    'depends': ['contacts'],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'views/service_rating.xml',
    ],
}