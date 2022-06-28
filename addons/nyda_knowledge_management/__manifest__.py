# -*- coding: utf-8 -*-
{
    'name': 'Knowledge Management',

    'summary': """
       Knowledge Management module.
    """,

    'description': """
      This module consists of all configurations and flow for Knowledge Management.
    """,

    'sequence': 6,
    'author': 'TechUltra Solutions',
    'website': 'https://www.techultrasolutions.com',
    'category': 'Products',
    'version': '0.1',
    'depends': ['base','portal'],
    'application': True,

    'data': [
        'security/knowledge_groups.xml',
        'security/ir.model.access.csv',
        'views/knowledge_management_views.xml',
        'views/knowledge_management_templates.xml',
    ],
}
