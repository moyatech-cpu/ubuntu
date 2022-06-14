# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class FleetReportWizard(models.TransientModel):
    """Fleet Report Wizard"""
    _name = "fleet.report.wizard"
    _description = 'Fleet Report Wizard'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    type = fields.Selection([('booked', 'Booked'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')],
                            string="Type")

    def get_booked_fleet_report(self):
        fleet_list = []
        converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        booked_fleet = self.env['fleet.booking'].search([('state', '=', 'booked')])
        for check_date in booked_fleet:
            check_start_date = datetime.strptime(datetime.strftime(datetime.strptime(check_date.meeting_date, '%Y-%m-%d %H:%M:%S'),
                                                 '%Y-%m-%d'),'%Y-%m-%d')
            check_end_date = datetime.strptime(datetime.strftime(datetime.strptime(check_date.meeting_end_time, '%Y-%m-%d %H:%M:%S'),
                                               '%Y-%m-%d'),'%Y-%m-%d')
            if converted_start_date <= check_start_date <= converted_end_date or converted_start_date <= check_end_date <= converted_end_date:
                room_list.append(check_date)
        return {'start_date': self.start_date,'end_date': self.end_date, 'fleet': fleet_list}

    def get_approved_fleet_report(self):
        fleet_list = []
        converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        booked_fleet = self.env['fleet.booking'].search([('state', '=', 'approved')])
        for check_date in booked_fleet:
            check_start_date = datetime.strptime(datetime.strftime(datetime.strptime(check_date.meeting_date, '%Y-%m-%d %H:%M:%S'),
                                                 '%Y-%m-%d'),'%Y-%m-%d')
            check_end_date = datetime.strptime(datetime.strftime(datetime.strptime(check_date.meeting_end_time, '%Y-%m-%d %H:%M:%S'),
                                               '%Y-%m-%d'),'%Y-%m-%d')
            if converted_start_date <= check_start_date <= converted_end_date or converted_start_date <= check_end_date <= converted_end_date:
                room_list.append(check_date)
        return {'start_date': self.start_date,'end_date': self.end_date, 'fleet': fleet_list}

    def get_rejected_fleet_report(self):
        fleet_list = []
        converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        booked_fleet = self.env['fleet.booking'].search([('state', '=', 'rejected')])
        for check_date in booked_fleet:
            check_start_date = datetime.strptime(datetime.strftime(datetime.strptime(check_date.meeting_date, '%Y-%m-%d %H:%M:%S'),
                                                 '%Y-%m-%d'),'%Y-%m-%d')
            check_end_date = datetime.strptime(datetime.strftime(datetime.strptime(check_date.meeting_end_time, '%Y-%m-%d %H:%M:%S'),
                                               '%Y-%m-%d'),'%Y-%m-%d')
            if converted_start_date <= check_start_date <= converted_end_date or converted_start_date <= check_end_date <= converted_end_date:
                room_list.append(check_date)
        return {'start_date': self.start_date,'end_date': self.end_date, 'fleet': fleet_list}
        
    def get_cancelled_fleet_report(self):
        fleet_list = []
        converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        booked_fleet = self.env['fleet.booking'].search([('state', '=', 'cancelled')])
        for check_date in booked_fleet:
            check_start_date = datetime.strptime(datetime.strftime(datetime.strptime(check_date.meeting_date, '%Y-%m-%d %H:%M:%S'),
                                                 '%Y-%m-%d'),'%Y-%m-%d')
            check_end_date = datetime.strptime(datetime.strftime(datetime.strptime(check_date.meeting_end_time, '%Y-%m-%d %H:%M:%S'),
                                               '%Y-%m-%d'),'%Y-%m-%d')
            if converted_start_date <= check_start_date <= converted_end_date or converted_start_date <= check_end_date <= converted_end_date:
                room_list.append(check_date)
        return {'start_date': self.start_date,'end_date': self.end_date, 'fleet': fleet_list}
        
    def get_fleet_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            elif self.type:
                if self.type == 'booked':
                    return self.env.ref('facility.action_report_booked_fleet').report_action(self)
                elif self.type == 'approved':
                    return self.env.ref('facility.action_report_approved_fleet').report_action(self)
                elif self.type == 'rejected':
                    return self.env.ref('facility.action_report_rejected_fleet').report_action(self)                
                elif self.type == 'cancelled':
                    return self.env.ref('facility.action_report_cancelled_fleet').report_action(self)
                else:
                    raise UserError(_("Report type not stipulated"))    
    