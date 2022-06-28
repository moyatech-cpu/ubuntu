# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
import base64


class BmtParticipantsPitching(models.Model):
    _name = 'bmt.pitching.participants'
    _rec_name = 'participant_id'
    _description = 'BMT Pitching Participants'

    participant_id = fields.Many2one('youth.enquiry', string="Benificiary")
    related_participant_id = fields.Many2one('res.users', string="Related Participant",
                                             related="participant_id.user_id")
    dob = fields.Date(string="Date Of birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    is_disabled = fields.Boolean(string="Is Disabled")
    race = fields.Selection([('asian', 'Asian'), ('african', 'African'), ('indian', 'Indian'), ('coloured', 'Coloured'),
                             ('white', 'White')], string="Race")
    mobile = fields.Char(string="Contact Number")
    business_mgmt_training_pitching_id = fields.Many2one('business.mgmt.training.pitching',
                                                         string="Business Management Training Pitching")
    area = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Rural area - Villages'),
         ('rural-area-farms', 'Rural area - Farms'), ('informa-settlement', 'Informa settlement')],
        string="Geographic Location")
    attended_full_training = fields.Boolean(string="Attended Full Training")
    sign_date = fields.Datetime(string="Signature Date")
    signature = fields.Binary(string="Signature")
    is_certi = fields.Boolean(string="Certificate Uploaded")

class BusinessMgmtTrainingPitching(models.Model):
    _name = 'business.mgmt.training.pitching'
    _rec_name = 'name'
    _description = 'Business Management Training Pitching'

    branch_id = fields.Many2one('res.branch', string="Branch")
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

    # @api.model
    def add_report(self):
        for rec in self.pitching_participants_ids:
            if rec.attended_full_training and not rec.is_certi:
                pdf = self.env.ref('bmt_training.action_bmt_certificate').render_qweb_pdf(rec.ids)
                b64_pdf = base64.b64encode(pdf[0])
                attachment_name = rec.participant_id.name + " BMT Certificate"
                attachment = self.env['ir.attachment'].create({
                    'name': attachment_name,
                    'type': 'binary',
                    'datas': b64_pdf,
                    'datas_fname': attachment_name + '.pdf',
                    'store_fname': attachment_name,
                    'res_model': rec._name,
                    'res_id': rec.id,
                    'mimetype': 'application/x-pdf'
                })
                self.env['bmt.certificate'].sudo().create({
                    'bmt_training_certificate': attachment.datas,
                    'bmt_training_certificate_name': attachment.datas_fname,
                    'bmt_certi_upload_date': datetime.now(),
                    'training_type': self.business_mgmt_training_id.training_type,
                    'youth_id': rec.participant_id.id,
                    'bmt_id': rec.business_mgmt_training_pitching_id.business_mgmt_training_id.id
                })
                # rec.participant_id.sudo().write({
                #     'bmt_training_certificate': attachment.datas,
                #     'bmt_training_certificate_name': attachment.datas_fname,
                #     'bmt_certi_upload_date': datetime.now(),
                #     'training_type': self.business_mgmt_training_id.training_type
                # })
                rec.is_certi = True
                attachment.unlink()

    def end_pitch_training(self):
        if not self.end_date:
            raise UserError(_("Please enter end date !!"))
        self.state = 'end_pitching_training'

    def start_pitch_training(self):
        self.state = 'start_pitching_training'

    # @api.onchange('start_date', 'end_date')
    # def onchange_date(self):
    #     if self.start_date and self.end_date:
    #         start_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
    #         end_date = datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
    #         if end_date <= start_date:
    #             self.end_date = False
    #             raise UserError(_("End Date should not be greater than start date."))
