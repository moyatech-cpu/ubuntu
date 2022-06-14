# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class TicketReportWizard(models.TransientModel):
    """Ticket Report Wizard"""
    _name = "ticket.report.wizard"
    _description = 'Ticket Report Wizard'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def get_ticket_logging_report(self):
        ticket_list = []
        converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        tickets = self.env['helpdesk_lite.ticket'].search([])
        for ticket_check_date in tickets:
            check_date = datetime.strptime(
                datetime.strftime(datetime.strptime(ticket_check_date.create_date, '%Y-%m-%d %H:%M:%S'),
                                  '%Y-%m-%d'), '%Y-%m-%d')
            if converted_start_date <= check_date <= converted_end_date:
                ticket_list.append(ticket_check_date)
        return {'start_date': self.start_date,'end_date': self.end_date, 'tickets': ticket_list}

    def get_ticketing_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('facility.action_report_ticket').report_action(self)
