# -*- coding: utf-8 -*-
{
    'name': "performance_management",

    'summary': """
        Keeping track of employee's performance""",

    'description': """
        This module's purpose is to keep track of employee's performance.
        First by finding an agreement with the employee of what's expected, this is done
        with the line manager. Thereafter the monitoring phase begins and employee's are then scored
        based on the wotrk they have done and how well they did it. 
    """,

    'author': "Tadiwa Muguta",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','document','hr','mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/performancemanagement.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}