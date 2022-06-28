# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
import base64


class BusinessMgmtTrainingPitching(models.Model):
    _inherit = 'business.mgmt.training.pitching'
    _description = 'Business Management Training Pitching'

    '''branch_id = fields.Many2one('res.branch', string="Branch")
    start_date = fields.Datetime(string="Training Start Date", related="pitching_date")
    end_date = fields.Datetime(string="Training End Date", related="pitching_date")
    pitching_date = fields.Datetime(string="Pitching Date")
    pitching_venue = fields.Char(string="Pitching Venue")
    facilitator_id = fields.Many2one('res.users', string="Facilitator")
    business_mgmt_training_id = fields.Many2one('business.mgmt.training', string="Business Management Training")
    state = fields.Selection(
        [('start_pitching_training', 'Start Pitching Training'), ('end_pitching_training', 'End Pitching Training')],
        string="State")
    pitching_participants_ids = fields.One2many('bmt.pitching.participants', 'business_mgmt_training_pitching_id', string="BMT Pitching Participants")
    facilitator_signature = fields.Binary(string="Facilitator Signature")
    date_of_facilitator_signature = fields.Datetime(string="Date Of Facilitator Signature")
    name = fields.Char(string="Name")
'''
    total_no_attended = fields.Integer(string="Total No. Attended", compute="total_attandees")
    
    def total_attandees(self):
        for rec in self:
            rec.total_no_attended = len(self.env['bmt.pitching.participants'].search([('business_mgmt_training_pitching_id', '=', rec.id)]))

    @api.multi
    def get_attendance_register(self):
        return self.env.ref('system_update_12.action_bmt_pitching_attendance').report_action(self)

    
    @api.model
    def get_bus_mgmt_data(self):
        single_attendees = []
        for attendees in self.pitching_participants_ids:
            single_attendees.append(attendees)
        return single_attendees
    
