# -*- coding: utf-8 -*-
{
    'name': "Facility Management",

    'summary': """
        This covers service desk requests, fleet management, surveys and inventory management.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "MOYATECH",
    'website': "http://www.moyatech.co.za",

    'category': 'Facility',
    'version': '11.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'helpdesk_lite', 'survey', 'stock', 'fleet','maintenance', 'strategy_and_planning'],

    # always loaded
    'data': [
        'data/demo.xml',
        'data/mail_template.xml',
        'security/ir.model.access.csv',
        'views/kanban_template.xml',
        'views/meeting_room_booking_view.xml',
        'views/fleet_booking_view.xml',
        'views/fleet_booking_dashboard_template.xml',
        'views/meeting_room_view.xml',
        'views/inherit_helpdesk_ticket_form_view.xml',
        'views/booking_dashboard_template.xml',
        'views/inherit_helpdesk_stage_form.xml',
        'views/compliments_suggestion_view.xml',
        'report/booking_report_template.xml',
        'report/booking_report.xml',
        'report/ticketing_report_template.xml',
        'report/ticketing_report.xml',
        'wizard/report_wizard_template.xml',
        'wizard/ticket_report_wizard.xml',
        'wizard/rate_service_wizard.xml',
        'views/ticket_dashbaord_template.xml',
        'views/helpdesk_category_view.xml',
        'views/supporting_function_template.xml',
        
        'wizard/fleet_report_wizard_template.xml',
        'report/fleet_booking_report_template.xml',
        'report/fleet_booking_report.xml'        
    ],
    'qweb': [
        "static/src/xml/dashboard_tickets.xml",
        "static/src/xml/dashboard_tickets_end_user.xml",
        "static/src/xml/dashboard_meeting_rooms.xml",
        "static/src/xml/fleet_booking_dashboard.xml",
    ],
    'post_init_hook': 'post_init_hook',
}