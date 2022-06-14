# coding=utf-8
import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from lxml import etree
from odoo.http import request
from odoo.tools.misc import ustr


class MeetingDashboard(models.Model):
    """Meeting Dashboard model."""
    _name = "meeting.dashboard"
    _rec_name = "name"
    _description = "Meeting Dashboard"

    name = fields.Char(string="Title")

    @api.model
    def get_booking_data(self):
        cancelled_bookings = self.env['meeting.room.booking'].sudo().search([('state', '=', 'cancelled')])
        history_bookings = self.env['meeting.room.booking'].sudo().search([('type', '=', 'history')])
        confirmed_bookings = self.env['meeting.room.booking'].sudo().search([('state', '=', 'booked')])
        upcoming_bookings = self.env['meeting.room.booking'].sudo().search([('type', '=', 'upcoming')])
        rescheduled_bookings = self.env['meeting.room.booking'].sudo().search([('rescheduled_room', '=', True)])
        booking_list = []
        for bookings in upcoming_bookings:
            booking_dict = {
                'name': bookings.name,
                'user': bookings.user_id.name,
                'start_date': bookings.meeting_date,
                'end_date': bookings.meeting_end_time,
                'room_name': bookings.meeting_room_id.name,
                'id': bookings.id
            }
            booking_list.append(booking_dict)
        room_wise_bookings = self.env['meeting.room'].sudo().search([])
        room_wise_booking_list = []
        for room_bookings in room_wise_bookings:
            booked_rooms = 0
            cancelled_rooms = 0
            for single_rec in room_bookings.meeting_room_booking_ids:
                if single_rec.state == 'booked':
                    booked_rooms += 1
                elif single_rec.state == 'cancelled':
                    cancelled_rooms += 1
            room_wise_booking_dict = {
                'name': room_bookings.name,
                'total_booked': booked_rooms,
                'total_cancelled': cancelled_rooms,
                'id': room_bookings.id
            }
            room_wise_booking_list.append(room_wise_booking_dict)
        data = {
            'total_cancelled_bookings': len(cancelled_bookings),
            'total_history_bookings': len(history_bookings),
            'total_confirmed_bookings': len(confirmed_bookings),
            'total_upcoming_bookings': len(upcoming_bookings),
            'total_rescheduled_bookings': len(rescheduled_bookings),
            'upcoming_booking_records': booking_list,
            'single_rooms': room_wise_booking_list,
            'uid': self.env.user.id,
        }
        return data
