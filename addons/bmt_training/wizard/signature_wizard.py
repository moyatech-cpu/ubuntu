# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class AttendanceSignature(models.TransientModel):
    _name = "attendance.signature"
    _description = "Attendance Signature"

    signature = fields.Binary(string="Signature")
    day = fields.Selection([('day_one', 'Day 1'), ('day_two', 'Day 2'), ('day_three', 'Day 3'), ('day_four', 'Day 4'),
                            ('day_five', 'Day 5')], string="Day")
    signature_date = fields.Datetime(string="Signature Date", default=datetime.today())
    bmt_participants_id = fields.Many2one('bmt.participants', string="BMT Participants")
    bmt_pitching_participants_id = fields.Many2one('bmt.pitching.participants', string="BMT Pitching Participants")

    def save_signature(self):
        if self.bmt_participants_id:
            if self.day == 'day_one':
                if self.bmt_participants_id.day_one:
                    raise UserError(_("Attendance for this day has already done !!"))
                else:
                    self.bmt_participants_id.signature_day_one = self.signature
                    self.bmt_participants_id.signature_day_one_date = self.signature_date
                    self.bmt_participants_id.day_one = True
                    lec = 0
                    if self.bmt_participants_id.day_one:
                        lec += 1
                    if self.bmt_participants_id.day_two:
                        lec += 1
                    if self.bmt_participants_id.day_three:
                        lec += 1
                    if self.bmt_participants_id.day_four:
                        lec += 1
                    if self.bmt_participants_id.day_five:
                        lec += 1
                    self.bmt_participants_id.attended_full_training = lec
            if self.day == 'day_two':
                if self.bmt_participants_id.day_two:
                    raise UserError(_("Attendance for this day has already done !!"))
                else:
                    self.bmt_participants_id.signature_day_second = self.signature
                    self.bmt_participants_id.signature_day_second_date = self.signature_date
                    self.bmt_participants_id.day_two = True
                    lec = 0
                    if self.bmt_participants_id.day_one:
                        lec += 1
                    if self.bmt_participants_id.day_two:
                        lec += 1
                    if self.bmt_participants_id.day_three:
                        lec += 1
                    if self.bmt_participants_id.day_four:
                        lec += 1
                    if self.bmt_participants_id.day_five:
                        lec += 1
                    self.bmt_participants_id.attended_full_training = lec
            if self.day == 'day_three':
                if self.bmt_participants_id.day_three:
                    raise UserError(_("Attendance for this day has already done !!"))
                else:
                    self.bmt_participants_id.signature_day_three = self.signature
                    self.bmt_participants_id.signature_day_three_date = self.signature_date
                    self.bmt_participants_id.day_three = True
                    lec = 0
                    if self.bmt_participants_id.day_one:
                        lec += 1
                    if self.bmt_participants_id.day_two:
                        lec += 1
                    if self.bmt_participants_id.day_three:
                        lec += 1
                    if self.bmt_participants_id.day_four:
                        lec += 1
                    if self.bmt_participants_id.day_five:
                        lec += 1
                    self.bmt_participants_id.attended_full_training = lec
            if self.day == 'day_four':
                if self.bmt_participants_id.training_type in ['gyb','syb_coops']:
                    raise UserError(_("You are not able to fill attendance for day 4 in this course !!"))
                elif self.bmt_participants_id.day_four:
                    raise UserError(_("Attendance for this day has already done !!"))
                else:
                    self.bmt_participants_id.signature_day_four = self.signature
                    self.bmt_participants_id.signature_day_four_date = self.signature_date
                    self.bmt_participants_id.day_four = True
                    lec = 0
                    if self.bmt_participants_id.day_one:
                        lec += 1
                    if self.bmt_participants_id.day_two:
                        lec += 1
                    if self.bmt_participants_id.day_three:
                        lec += 1
                    if self.bmt_participants_id.day_four:
                        lec += 1
                    if self.bmt_participants_id.day_five:
                        lec += 1
                    self.bmt_participants_id.attended_full_training = lec
            if self.day == 'day_five':
                if self.bmt_participants_id.training_type in ['gyb', 'syb_coops']:
                    raise UserError(_("You are not able to fill attendance for day 5 in this course !!"))
                elif self.bmt_participants_id.day_five:
                    raise UserError(_("Attendance for this day has already done !!"))
                else:
                    self.bmt_participants_id.signature_day_five = self.signature
                    self.bmt_participants_id.signature_day_five_date = self.signature_date
                    self.bmt_participants_id.day_five = True
                    lec = 0
                    if self.bmt_participants_id.day_one:
                        lec += 1
                    if self.bmt_participants_id.day_two:
                        lec += 1
                    if self.bmt_participants_id.day_three:
                        lec += 1
                    if self.bmt_participants_id.day_four:
                        lec += 1
                    if self.bmt_participants_id.day_five:
                        lec += 1
                    self.bmt_participants_id.attended_full_training = lec
        elif self.bmt_pitching_participants_id:
            print ("\n\n\n\n\n\n")
            print ("self.bmt_pitching_participants_id ",self.bmt_pitching_participants_id)
            if self.bmt_pitching_participants_id.attended_full_training:
                raise UserError(_("Attendance has already done !!"))
            else:
                self.bmt_pitching_participants_id.signature = self.signature
                self.bmt_pitching_participants_id.sign_date = self.signature_date
                self.bmt_pitching_participants_id.attended_full_training= True