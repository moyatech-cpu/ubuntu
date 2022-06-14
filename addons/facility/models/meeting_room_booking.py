# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class MeetingRoomBooking(models.Model):
    _name = 'meeting.room.booking'
    _rec_name = 'name'
    _description = "Meeting Room Booking"

    name = fields.Char(string="Description")
    booking_user_id = fields.Many2one('res.users', string="Booked By", default=lambda self: self.env.user)
    meeting_date = fields.Datetime(string="Meeting Start Date")
    meeting_end_time = fields.Datetime(string="Meeting End Date")
    state = fields.Selection([('booked', 'Booked'), ('cancelled', 'Cancelled')], string="Status")
    meeting_room_id = fields.Many2one('meeting.room', string="Meeting Room")
    type = fields.Selection([('upcoming', 'Upcoming'), ('history','History')], string="Type")
    cancellation_user_id = fields.Many2one('res.users', string="Cancellation User")
    rescheduled_room = fields.Boolean(string="Rescheduled Room")
    color = fields.Integer('Kanban Color Index')

    def _default_division(self):
        booking_user_id = self.env['divisions'].sudo().search(
            [('responsible_user', '=', self._context.get('uid'))], limit=1)
        print ("\n\n\n\n\n booking_user_id ", booking_user_id, self._context, self._context.get('uid'))
        if booking_user_id:
            return booking_user_id.id

    division_id = fields.Many2one('divisions', string="Division", default=lambda self: self.sudo()._default_division())

    def _default_job(self):
        booking_user_id = self.env['hr.employee'].sudo().search(
            [('user_id', '=', self._context.get('uid'))], limit=1)
        print ("\n\n\n\n\n booking_user_id ", booking_user_id, self._context, self._context.get('uid'))
        if booking_user_id:
            return booking_user_id.job_id.id

    position_id = fields.Many2one('hr.job', string="Position", default=lambda self: self.sudo()._default_job())

    def _default_users(self):
        ulist=[]
        facility_manager_groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('facility.facility_manager').id)]).users
        facility_officer_groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('facility.facility_officer').id)]).users
        end_user_groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('facility.end_user').id)]).users
        admin_groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('base.group_system').id)]).users
        for fm in facility_manager_groups:
            ulist.append(fm.id)
        for fo in facility_officer_groups:
            ulist.append(fo.id)
        for eu in end_user_groups:
            ulist.append(eu.id)
        for a in admin_groups:
            ulist.append(a.id)
        return [('id', 'in', ulist)]

    user_id = fields.Many2one('res.users', string="Email", domain=lambda self: self._default_users(),
                              default=lambda self: self.env.user)

    def write(self, vals):
        res = super(MeetingRoomBooking, self).write(vals)
        if self.state == 'booked':
            if 'meeting_date' in vals or 'meeting_end_time' in vals:
                facility_manager_groups = self.env['res.groups'].search(
                    [('id', '=', self.env.ref('facility.facility_manager').id)]).users.ids
                facility_officer_groups = self.env['res.groups'].search(
                    [('id', '=', self.env.ref('facility.facility_officer').id)]).users.ids
                admin_groups = self.env['res.groups'].search(
                    [('id', '=', self.env.ref('base.group_system').id)]).users.ids
                end_user_groups = self.env['res.groups'].search(
                    [('id', '=', self.env.ref('facility.end_user').id)]).users.ids
                if 'meeting_date' in vals:
                    converted_start_date = datetime.strptime(vals['meeting_date'], '%Y-%m-%d %H:%M:%S')
                else:
                    converted_start_date = datetime.strptime(self.meeting_date, '%Y-%m-%d %H:%M:%S')
                if 'meeting_end_time' in vals:
                    converted_end_date = datetime.strptime(vals['meeting_end_time'], '%Y-%m-%d %H:%M:%S')
                else:
                    converted_end_date = datetime.strptime(self.meeting_end_time, '%Y-%m-%d %H:%M:%S')
                if converted_start_date > converted_end_date or converted_start_date == converted_end_date:
                    raise UserError(_("Start date and time should not be greater than end date."))
                else:
                    other_bookings = self.search(
                        [('type', '=', 'upcoming'), ('state', '=', 'booked'), ('id', '!=', self.id),
                         ('meeting_room_id', '=', self.meeting_room_id.id)])
                    if other_bookings:
                        for other_booking in other_bookings:
                            other_converted_start_date = datetime.strptime(other_booking.meeting_date,
                                                                           '%Y-%m-%d %H:%M:%S')
                            other_converted_end_date = datetime.strptime(other_booking.meeting_end_time,
                                                                         '%Y-%m-%d %H:%M:%S')
                            if other_converted_start_date < converted_start_date < other_converted_end_date or other_converted_start_date < converted_end_date < other_converted_end_date:
                                raise UserError(_(
                                    "These room has been in these time slot by " + other_booking.user_id.name + ", so please select another timing slot."))
                            else:
                                self.rescheduled_room = True
                                if self.env.user.id in facility_manager_groups or self.env.user.id in facility_officer_groups or self.env.user.id in admin_groups:
                                    if self.user_id.id in end_user_groups:
                                        mail_template = self.env.ref('facility.meeting_room_rescheduled_email_template')
                                        mail_template.send_mail(self.id, force_send=True)
                    else:
                        self.rescheduled_room = True
                        if self.env.user.id in facility_manager_groups or self.env.user.id in facility_officer_groups or self.env.user.id in admin_groups:
                            if self.user_id.id in end_user_groups:
                                mail_template = self.env.ref('facility.meeting_room_rescheduled_email_template')
                                mail_template.send_mail(self.id, force_send=True)
        return res

    def update_bookings(self):
        bookings = self.search([('type', '=', 'upcoming')])
        for booking in bookings:
            converted_start_date = datetime.strptime(booking.meeting_date, '%Y-%m-%d %H:%M:%S')
            converted_end_date = datetime.strptime(booking.meeting_end_time, '%Y-%m-%d %H:%M:%S')
            if datetime.now() > converted_end_date and datetime.now() > converted_start_date:
                booking.type = 'history'

    @api.onchange('meeting_date', 'meeting_end_time')
    def update_type(self):
        if self.meeting_date and self.meeting_end_time:
            converted_date = datetime.strptime(self.meeting_date, '%Y-%m-%d %H:%M:%S')
            converted_end_date = datetime.strptime(self.meeting_end_time, '%Y-%m-%d %H:%M:%S')
            if datetime.now() > converted_date and datetime.now() > converted_end_date:
                self.type = 'history'
            else:
                self.type = 'upcoming'
        elif self.meeting_date or self.meeting_end_time:
            if self.meeting_date:
                converted_date = datetime.strptime(self.meeting_date, '%Y-%m-%d %H:%M:%S')
                if datetime.now() > converted_date:
                    self.type = 'history'
                else:
                    self.type = 'upcoming'
            if self.meeting_end_time:
                converted_end_date = datetime.strptime(self.meeting_end_time, '%Y-%m-%d %H:%M:%S')
                if datetime.now() > converted_end_date:
                    self.type = 'history'
                else:
                    self.type = 'upcoming'


    def book_room(self):
        converted_start_date = datetime.strptime(self.meeting_date, '%Y-%m-%d %H:%M:%S')
        converted_end_date = datetime.strptime(self.meeting_end_time, '%Y-%m-%d %H:%M:%S')
        if self.meeting_date and self.meeting_end_time:
            if datetime.now() > converted_start_date or datetime.now() > converted_end_date:
                raise UserError(_("Please check Start Date and End Date as it has been passed."))
            elif converted_start_date > converted_end_date or  converted_start_date == converted_end_date:
                raise UserError(_("Start date and time should not be greater than end date."))
            elif (converted_end_date.date() - converted_start_date.date()).days > 4:
                raise UserError(_("You are not allowed to book a room for more than 4 days in a row."))
            elif datetime.now() + timedelta(days=2) >= converted_start_date:
                raise UserError(_("Rooms should be booked before 48 hours."))
            else:
                other_bookings = self.search(
                    [('type', '=', 'upcoming'), ('state', '=', 'booked'), ('id', '!=', self.id),
                     ('meeting_room_id', '=', self.meeting_room_id.id)])
                if other_bookings:
                    for other_booking in other_bookings:
                        other_converted_start_date = datetime.strptime(other_booking.meeting_date, '%Y-%m-%d %H:%M:%S')
                        other_converted_end_date = datetime.strptime(other_booking.meeting_end_time, '%Y-%m-%d %H:%M:%S')
                        if other_converted_start_date.date() == converted_start_date.date() or other_converted_start_date.date() == converted_end_date.date() or other_converted_end_date.date() == converted_end_date.date() or other_converted_start_date.date() == converted_end_date.date() and self.user_id.id == other_booking.user_id.id:
                            raise UserError(_("You cannot book the rooms on same date"))
                        elif other_converted_start_date < converted_start_date < other_converted_end_date or other_converted_start_date < converted_end_date < other_converted_end_date:
                            raise UserError(_(
                                "These room has been in these time slot by " + other_booking.user_id.name + ", so please select another timing slot."))
                        else:
                            self.state = 'booked'
                            mail_template = self.env.ref('facility.meeting_room_email_template')
                            mail_template.send_mail(self.id, force_send=True)
                            return True
                else:
                    self.state = 'booked'
                    mail_template = self.env.ref('facility.meeting_room_email_template')
                    mail_template.send_mail(self.id, force_send=True)
                    return True
        else:
            raise UserError(_("Please enter both Start date and End date !!"))

    def cancel_room(self):
        facility_manager_groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('facility.facility_manager').id)]).users.ids
        facility_officer_groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('facility.facility_officer').id)]).users.ids
        end_user_groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('facility.end_user').id)]).users.ids
        if self.user_id.id in end_user_groups:
            if self.env.user.id in facility_manager_groups or self.env.user.id in facility_officer_groups:
                raise UserError(_("You cannot cancel the end users bookings"))
        else:
            self.state = 'cancelled'
        admin_groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('base.group_system').id)]).users.ids
        if self.env.user.id in admin_groups:
            if self.env.user.id in facility_manager_groups or self.env.user.id in facility_officer_groups or self.user_id.id in end_user_groups:
                self.cancellation_user_id = self.env.user.id
                mail_template = self.env.ref('facility.meeting_room_email_template')
                mail_template.send_mail(self.id, force_send=True)
