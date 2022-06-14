# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class MeetingRoom(models.Model):
    _name = 'meeting.room'
    _rec_name = 'name'
    _description= 'Meeting Room'

    name = fields.Char(string="Name")
    meeting_room_booking_ids = fields.One2many('meeting.room.booking', 'meeting_room_id', string="Meeting Room Booking")
    room_location = fields.Text(string="Room Location")
