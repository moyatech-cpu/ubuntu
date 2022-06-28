# coding=utf-8
import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from lxml import etree
from odoo.http import request
from odoo.tools.misc import ustr


class FleetDashboard(models.Model):
    """Fleet Dashboard model."""
    _name = "fleet.dashboard"
    _rec_name = "name"
    _description = "Fleet Dashboard"

    name = fields.Char(string="Title")

    @api.model
    def get_booking_data(self):
        
        rejected_bookings       = self.env['fleet.booking'].sudo().search([('state', '=', 'rejected')])
        history_bookings        = self.env['fleet.booking'].sudo().search([('type', '=', 'history')])
        submitted_bookings      = self.env['fleet.booking'].sudo().search([('state', '=', 'booked')])
        approved_bookings       = self.env['fleet.booking'].sudo().search([('state', '=', 'approved')])
        upcoming_bookings       = self.env['fleet.booking'].search([('type', '=', 'upcoming')])
        rescheduled_bookings    = self.env['fleet.booking'].sudo().search([('rescheduled_vehicle', '=', True)])
        booking_list = []
        
        for bookings in upcoming_bookings:
            booking_dict = {
                'name': bookings.name,
                'user': bookings.user_id.name,
                'start_date': bookings.booking_date,
                'end_date': bookings.booking_end_time,
                'room_name': bookings.vehicle_id.name,
                'id': bookings.id
            }
            booking_list.append(booking_dict)
        fleet_wise_bookings = self.env['fleet.vehicle'].sudo().search([])
        fleet_wise_booking_list = []
        
        for fleet_booking in fleet_wise_bookings:
            booked_fleet    = 0
            cancelled_fleet = 0
            
            bookings = self.env['fleet.booking'].sudo().search([('vehicle_id','=',fleet_booking.id)])
            
            for booking in bookings:
                if booking.state == 'booked':
                    booked_fleet += 1
                elif booking.state == 'cancelled':
                    cancelled_fleet += 1
            
            fleet_wise_booking_dict = {
                'name': fleet_booking.name,
                'total_booked': booked_fleet,
                'total_cancelled': cancelled_fleet,
                'id': fleet_booking.id
            }
            fleet_wise_booking_list.append(fleet_wise_booking_dict)
        
        data = {
            'total_rejected_bookings': len(rejected_bookings),
            'total_approved_bookings': len(approved_bookings),
            'total_history_bookings': len(history_bookings),
            'total_submitted_bookings': len(submitted_bookings),
            'total_upcoming_bookings': len(upcoming_bookings),
            'total_rescheduled_bookings': len(rescheduled_bookings),
            'upcoming_booking_records': booking_list,
            'single_fleet': fleet_wise_booking_list,
            'uid': self.env.user.id,
        }
        return data
