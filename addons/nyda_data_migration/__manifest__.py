# coding=utf-8
{
    'name': 'NYDA Data Migration Module',

    'summary': """
       Data Migration module from base to move data from legacy systems into the ERP.
    """,

    'description': """
      Data Migration module from base to move data from legacy systems into the ERP.
    """,

    'sequence': 5,
    'author': 'MOYATECH',
    'website' : 'http://www.moyatech.co.za',
    'category': 'Reports',
    'version': '0.1',
    'depends': [
        'base', 'hr',
    ],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'views/data_migration.xml',
    ],
}