# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError
import base64
from odoo.exceptions import ValidationError
#import holidays


class Course(models.Model):
    _name = 'course'
    _description = 'Course'

    name = fields.Char(string="Name")


class BmtParticipants(models.Model):
    _name = 'bmt.participants'
    _rec_name = 'participant_id'
    _description = 'BMT Participants'

    participant_id = fields.Many2one('youth.enquiry', string="Beneficiary")
    surname = fields.Char(string="Surname")
    related_participant_id = fields.Many2one('res.users', string="Related Participant",
                                             related="participant_id.user_id")
    dob = fields.Date(string="Date Of birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    area = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Rural area - Villages'),
         ('rural-area-farms', 'Rural area - Farms'), ('informa-settlement', 'Informa settlement')],
        string="Geographic Location")
    is_disabled = fields.Boolean(string="Is Disabled")
    race = fields.Selection(
        [('african', 'African'), ('asian', 'Asian'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Race")
    mobile = fields.Char(string="Contact Number")
    business_mgmt_training_id = fields.Many2one('business.mgmt.training', string="Business Management Training")
    signature_day_one = fields.Binary(string="Signature Day 1")
    signature_day_one_date = fields.Datetime(string="Signature Day 1 Date")
    day_one = fields.Boolean(string="Day 1 Att.")
    signature_day_second = fields.Binary(string="Signature Day 2")
    signature_day_second_date = fields.Datetime(string="Signature Day 2 Date")
    day_two = fields.Boolean(string="Day 2 Att.")
    signature_day_three = fields.Binary(string="Signature Day 3")
    signature_day_three_date = fields.Datetime(string="Signature Day 3 Date")
    day_three = fields.Boolean(string="Day 3 Att.")
    signature_day_four= fields.Binary(string="Signature Day 4")
    signature_day_four_date = fields.Datetime(string="Signature Day 4 Date")
    day_four = fields.Boolean(string="Day 4 Att.")
    signature_day_five = fields.Binary(string="Signature Day 5")
    signature_day_five_date = fields.Datetime(string="Signature Day 5 Date")
    day_five = fields.Boolean(string="Day 5 Att.")
    attended_full_training = fields.Integer(string="Attended 80% Training")
    bmt_training_app_id = fields.Many2one('bmt.training.application', string="BMT Training Application")
    state = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Rejected')], string="Status")
    coop_gov_id = fields.Many2one('cooperative.governance.training', string="Co-operative Governance")
    is_certi = fields.Boolean(string="Certificate Uploaded")
    training_type = fields.Selection(
        [('gyb', 'GYBI - 3 days'),('syb', 'SYB - 5 days'),
         ('iyb_one', 'IYB 1 - 5 days'),
         ('iyb_two', 'IYB 2 - 5 days'), ('syb_coops', 'SYB/Co-ops - 3 days')],
        string="Course", related="business_mgmt_training_id.training_type")

    @api.multi
    def do_confirm(self):
        """ Confermation Done """
        self.state = 'confirm'
        return

    @api.multi
    def do_reject(self):
        """ Reject Done """
        self.state = 'reject'
        return

    @api.onchange('day_one','day_two','day_three','day_four','day_five')
    def onchange_sign(self):
        lec = 0
        if self.day_one:
            lec += 1
        if self.day_two:
            lec += 1
        if self.day_three:
            lec += 1
        if self.day_four:
            lec += 1
        if self.day_five:
            lec += 1
        self.attended_full_training = lec

    @api.onchange('participant_id')
    def onchange_participant_id(self):
        self.gender = self.participant_id.gender
        self.area = self.participant_id.geographic_location
        self.mobile = self.participant_id.cell_phone_number
        self.race = self.participant_id.population_group
        self.surname = self.participant_id.surname


class BusinessMgmtTraining(models.Model):
    _name = 'business.mgmt.training'
    _description = 'Business Management Training'

    branch_id = fields.Many2one('res.branch', string="Branch")
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date", compute="onchange_date")
    state = fields.Selection([('start_training', 'Start Training'), ('end_training', 'End Training'),
                               ('start_pitching_training', 'Start Pitching Training'),('coordinator_review', 'Coordinator Review'),
                               ('bm_review', 'Branch Manager Review'),('ho_admin_review', 'HO Admin Review'),
                               ('ho_manager_review', 'HO Manager Review'),('completed', 'Completed')
                               ], string="State")
    intervention_type = fields.Selection(
        [('bmt_training', 'BMT Training')], string="Intervention Type", default="bmt_training")
    bmt_participants_ids = fields.One2many('bmt.participants', 'business_mgmt_training_id', string="BMT Participants",
                                           copy=False)
    municipality = fields.Many2one('res.municipality', string="Municipality")
    product_id = fields.Many2one('product.template', string="Product")
    course_id = fields.Many2one('course', string="Course")
    facilitator_id = fields.Many2one('res.users', string="Trainer", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_trainer").id)], default=lambda self:self.add_trainer())
    venue = fields.Char(string="Venue")
    catering = fields.Char(string="Catering")
    pdd_training_id = fields.Many2one('pddd.training', string="Pdd Training")
    training_type = fields.Selection(
        [('gyb', 'GYBI - 3 days'),('syb', 'SYB - 5 days'),
         ('iyb_one', 'IYB 1 - 5 days'),
         ('iyb_two', 'IYB 2 - 5 days'), ('syb_coops', 'SYB/Co-ops - 5 days')],
        string="Course")
    training_type_kanban = fields.Char(string="Training type", compute="check_training_type")
    total_no_attended = fields.Integer(string="Total No. Attended", compute="total_attandees")
    total_youth = fields.Integer(string="Total No. Attended", related="total_no_attended")
    services_coordinator_name = fields.Many2one('res.users', string="Services Co-ordinator")
    services_coordinator_signature = fields.Binary(string="Services Co-ordinator Signature")
    no_of_males_attended = fields.Integer(string="No.of Males Attended", compute="male_female_disabled_attendess")
    no_of_males = fields.Integer(string="No.of Males", related="no_of_males_attended")
    no_of_females_attended = fields.Integer(string="No.of Females Attended", compute="male_female_disabled_attendess")
    no_of_females = fields.Integer(string="No.of Males", related="no_of_females_attended")
    no_of_rural_participants = fields.Integer(string="No. of Rural Participants", compute="rural_urban_disabled_attendess")
    no_of_asian_participants = fields.Integer(string="No. of Asian Participants", compute="race_attandees")
    no_of_urban_participants = fields.Integer(string="No. of Urban Participants", compute="rural_urban_disabled_attendess")
    no_of_disabled_participants = fields.Integer(string="No. of Disabled Participants", compute="male_female_disabled_attendess")
    no_of_african_participants = fields.Integer(string="No. of African Participants", compute="race_attandees")
    no_of_coloured_participants = fields.Integer(string="No. of Coloured Participants", compute="race_attandees")
    no_of_indian_participants = fields.Integer(string="No. of Indian Participants", compute="race_attandees")
    no_of_white_participants = fields.Integer(string="No. of White Participants", compute="race_attandees")
    facilitator_signature = fields.Binary(string="Facilitator Signature")
    date_of_facilitator_signature = fields.Datetime(string="Date Of Facilitator Signature")
    pitching_mail_sent = fields.Boolean(string="Pitching Mail Sent")
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    bmt_pitching_id = fields.Many2one('business.mgmt.training.pitching', string="Business Managemnet Training Pitching")
    name = fields.Char(string="Batch")
    title = fields.Char(string="Title")
    training_type_id = fields.Many2one('pddd.type.training', string="Training Type")
    total_participants = fields.Integer(string="Total Participants", compute="calculate_participants")
    max_attendees = fields.Integer(string="Max Attendees",default='1')
    coordinator_review_id = fields.Many2one('res.users', string="Coordinator", domain=lambda self: [
                                            ("groups_id", "=", self.env.ref("client_management.group_coordinator").id)])
    coordinator_rejection = fields.Text(string="Coordinator Rejection Reason")
    branch_manager_id = fields.Many2one('res.users', string="Branch Manager", domain=lambda self: [
                                            ("groups_id", "=", self.env.ref("client_management.group_branch_manager").id)])
    branch_manager_rejection = fields.Text(string="Branch Manager Rejection Reason")
    ho_admin_id = fields.Many2one('res.users', string="Head Office Admin", domain=lambda self: [
                                            ("groups_id", "=", self.env.ref("bmt_training.group_ho_admin").id)])
    ho_admin_rejection = fields.Text(string="HO Admin Rejection Reason")
    ho_manager_id = fields.Many2one('res.users', string="Head Office Manager", domain=lambda self: [
                                            ("groups_id", "=", self.env.ref("bmt_training.group_ho_manager").id)])
    ho_manager_rejection = fields.Text(string="HO Manager Rejection Reason")
    # Reporting
    trainer_submitted_report = fields.Selection([('yes','Yes'), ('no','No')], string="Trainer Submitted Report")
    coordinator_approved = fields.Selection([('yes','Yes'), ('no','No')], string="Coordinator Approved Report")
    coordinator_rejected = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Coordinator Rejected Report")
    bm_approved = fields.Selection([('yes','Yes'), ('no','No')], string="Branch Manager Approved Report")
    bm_rejected = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Branch Manager Rejected Report")
    ho_admin_approved = fields.Selection([('yes','Yes'), ('no','No')], string="HO Admin Approved Report")
    ho_admin_rejected = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="HO Admin Rejected Report")
    ho_manager_approved = fields.Selection([('yes','Yes'), ('no','No')], string="HO Manager Approved Report")
    ho_manager_rejected = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="HO Manager Rejected Report")
    is_certi_generated = fields.Boolean(string="Is Certificates Generated")
    pitching_start_date = fields.Datetime(string="Pitching Start Date")
    pitching_end_date = fields.Datetime(string="Pitching End Date")

    def add_trainer(self):
        if self.env.user.id in self.env.ref('bmt_training.group_trainer').users.ids:
            return self.env.user.id

    @api.onchange('training_type')
    def change_title(self):
        if self.training_type:
            if self.training_type == 'syb':
                self.title = "START YOUR BUSINESS TRAINING"
            elif self.training_type == 'gyb':
                self.title = "GENERATE YOUR BUSINESS IDEA"
            elif self.training_type == 'iyb_one':
                self.title = "IMPROVE YOUR BUSINESS - 1"
            elif self.training_type == 'iyb_two':
                self.title = "IMPROVE YOUR BUSINESS - 2"
            elif self.training_type == 'syb_coops':
                self.title = "CO-OPERATIVE GOVERNANCE TRAINING & START YOUR BUSINESS TRAINING"

    @api.onchange('facilitator_id')
    def onchange_facilitator(self):
        if self.facilitator_id:
            trainer = self.env['link.trainer'].sudo().search([('trainer_id', '=', self.facilitator_id.id)])
            print ("Trainer ", trainer)
            self.branch_id = self.facilitator_id.branch_id
            if trainer:
                self.coordinator_review_id = trainer.coordinator_id
                self.branch_manager_id = trainer.branch_manager_id
                self.ho_admin_id = trainer.head_office_admin_id
                self.ho_manager_id = trainer.head_office_manager_id

    def generate_certificate(self):
        for rec in self.bmt_participants_ids:
            if rec.attended_full_training >= 3 and rec.state == 'confirm':
                pdf = self.env.ref('bmt_training.action_bmt_participants_without_pitching').render_qweb_pdf(rec.ids)
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
                rec.participant_id.sudo().write({
                    'bmt_training_certificate': attachment.datas,
                    'bmt_training_certificate_name': attachment.datas_fname,
                    'bmt_certi_upload_date': datetime.now(),
                    'training_type': self.training_type

                })
                rec.is_certi = True
                attachment.unlink()
        self.is_certi_generated = True

    def generate_coops_certificate(self):
        for rec in self.bmt_participants_ids:
            # return self.env.ref('bmt_training.action_coops_certificate').report_action(rec)
            if rec.attended_full_training >= 4 and rec.coop_gov_id.id:
                pdf = self.env.ref('bmt_training.action_coops_certificate').render_qweb_pdf(rec.ids)
                b64_pdf = base64.b64encode(pdf[0])
                attachment_name = rec.participant_id.name + " Co-op BMT Certificate"
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
                rec.participant_id.sudo().write({
                    'coop_bmt_training_certificate': attachment.datas,
                    'coop_bmt_training_certificate_name': attachment.datas_fname,
                    'coop_bmt_certi_upload_date': datetime.now()

                })
                rec.is_certi = True
                attachment.unlink()
        self.is_certi_generated = True

    @api.constrains('start_date', 'pitching_end_date', 'pitching_start_date')
    @api.one
    def _check_date(self):
        start_date = ''
        end_date= ''
        pstart_date= ''
        pend_date= ''
        ns_sa_holidays= ''
        ne_sa_holidays= ''
        ps_sa_holidays= ''
        pe_sa_holidays= ''
        if self.start_date:
            start_date = datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S')
            ns_sa_holidays = holidays.ZA(years=start_date.year).items()
        if self.end_date:
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d %H:%M:%S')
            ne_sa_holidays = holidays.ZA(years=end_date.year).items()
        if self.pitching_start_date:
            pstart_date = datetime.strptime(self.pitching_start_date, '%Y-%m-%d %H:%M:%S')
            ps_sa_holidays = holidays.ZA(years=pstart_date.year).items()
        if self.pitching_end_date:
            pend_date = datetime.strptime(self.pitching_end_date, '%Y-%m-%d %H:%M:%S')
            pe_sa_holidays = holidays.ZA(years=pend_date.year).items()
        if self.start_date:
            if start_date.weekday() == 5 or start_date.weekday() == 6:
                raise ValidationError(_("You cannot select the weekend dates or holidays !!"))
            for cdate in ns_sa_holidays:
                if start_date.date() in cdate:
                    raise ValidationError(_("You cannot select the holidays for pitching start date!!"))
        if end_date and pstart_date:
            if end_date > pstart_date:
                raise ValidationError(_("Pitching Start Date cannot be greater than End Date !!"))
        if pend_date and pstart_date:
            if datetime.now() > pstart_date:
                raise ValidationError(_("Date has been passed, please select another date !!"))
            if pstart_date > pend_date:
                raise ValidationError(_("Pitching End Date cannot be greater than Pitching Start Date !!"))
        if self.pitching_start_date:
            if pstart_date.weekday() == 5 or pstart_date.weekday() == 6:
                raise ValidationError(_("You cannot select the weekend dates for pitching start date!!"))
            for cdate in ps_sa_holidays:
                if pstart_date.date() in cdate:
                    raise ValidationError(_("You cannot select the holidays for pitching start date!!"))
        if self.pitching_end_date:
            if pend_date.weekday() == 5 or pend_date.weekday() == 6:
                raise ValidationError(_("You cannot select the weekend dates for pitching end date!!"))
            for cdate in pe_sa_holidays:
                if pend_date.date() in cdate:
                    raise ValidationError(_("You cannot select the holidays for pitching end date!!"))
        if self.pitching_start_date and self.pitching_end_date:
            count = 0
            diff = pend_date - pstart_date
            for i in range(diff.days + 1):
                day = pstart_date + timedelta(days=i)
                if day.weekday() == 5:
                    count += 1
                elif day.weekday() == 6:
                    count += 1
            total_days = diff.days - count
            if not 1 >= total_days and not total_days <= 4:
                raise ValidationError(_("Pitching Date duration should be minimum 2 days and maximum 5 days !!"))
            elif total_days == 0:
                raise ValidationError(_("Pitching Date duration should be minimum 2 days and maximum 5 days !!"))

    @api.model
    def create(self, vals):
        res = super(BusinessMgmtTraining, self).create(vals)
        # if res.intervention_type == 'bmt_training':
        #     ref_number = self.env['ir.sequence'].next_by_code('bmt_code') or _('New')
        #     res.name = ref_number
        if res.training_type == 'gyb':
            ref_number = self.env['ir.sequence'].next_by_code('gyb_code') or _('New')
            res.name = ref_number
        elif res.training_type == 'syb':
            ref_number = self.env['ir.sequence'].next_by_code('syb_code') or _('New')
            res.name = ref_number
        elif res.training_type == 'iyb_one':
            ref_number = self.env['ir.sequence'].next_by_code('iyb_one_code') or _('New')
            res.name = ref_number
        elif res.training_type == 'iyb_two':
            ref_number = self.env['ir.sequence'].next_by_code('iyb_two_code') or _('New')
            res.name = ref_number
        elif res.training_type == 'syb_coops':
            ref_number = self.env['ir.sequence'].next_by_code('syb_coops_code') or _('New')
            res.name = ref_number
        return res

    @api.depends('training_type')
    def check_training_type(self):
        for res in self:
            if res.training_type == 'syb':
                res.training_type_kanban = 'SYB - 5 days'
            elif res.training_type == 'gyb':
                res.training_type_kanban = 'GYB - 3 days'
            elif res.training_type == 'iyb_one':
                res.training_type_kanban = 'IYB 1 - 5 days'
            elif res.training_type == 'iyb_two':
                res.training_type_kanban = 'IYB 2 - 5 days'
            elif res.training_type == 'syb_coops':
                res.training_type_kanban = 'SYB/Co-ops - 5 days'

    @api.depends('bmt_participants_ids')
    def calculate_participants(self):
        for res in self:
            count_len = len(res.bmt_participants_ids)
            res.total_participants = count_len

    def apply_for_training(self):
        for rec in self:
            if rec.state == False:
                current_user_youth_id = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.env.user.id)])
                bmt_participants_id = self.env['bmt.participants'].sudo().search(
                    [('participant_id', '=', current_user_youth_id.id)])
                if not bmt_participants_id:
                    all_ben_users = self.env.ref('client_management.group_branch_beneficiary').users.ids
                    all_trainers_users = self.env.ref('bmt_training.group_trainer').users.ids
                    if not self.env.user.id in all_ben_users and not self.env.user.id in all_trainers_users:
                        raise UserError(_("Only beneficiaries or trainers can apply to this course !!"))
                    elif self.env.user.id in all_ben_users:
                        youth = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.env.user.id)])
                        bmt_participants = self.env['bmt.participants'].sudo().create({
                            'participant_id': youth.id,
                            'gender': youth.gender,
                            'area': youth.geographic_location,
                            'race': youth.population_group,
                            'physical_address': youth.physical_address,
                            'mobile': youth.cell_phone_number,
                            'business_mgmt_training_id': rec.id
                        })
                    elif self.env.user.id in all_trainers_users:
                        action = {
                            'type': 'ir.actions.act_window',
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_model': 'business.mgmt.training',
                            'target': 'current',
                            'res_id': rec.id,
                            'flags': {'initial_mode': 'edit'},
                            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
                        }
                        return action
                else:
                    raise UserError(_("You can only apply to one training at a time !!"))
            else:
                raise UserError(_("You cannot apply for these training as batch is confirmed !!"))

    def view_edit_training(self):
        for record in self:
            action = {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'business.mgmt.training',
                'target': 'current',
                'res_id': record.id,
                'flags': {'initial_mode': 'edit'},
                'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
            }
            return action


    @api.model
    def get_bus_mgmt_data(self):
        single_attendees = []
        for attendees in self.bmt_participants_ids:
            single_attendees.append(attendees)
        return single_attendees

    @api.multi
    def get_attendance_register(self):
        return self.env.ref('bmt_training.action_report_bus_gov_attendance_register').report_action(self)

    def start_bmt_training(self):
        self.state = 'start_training'

    def end_bmt_training(self):
        self.state = 'end_training'

    def submit_report(self):
        if datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S") > datetime.now():
            raise ValidationError(_("You cannot submit report before the end date !!"))
        if not self.bmt_pitching_id and self.training_type in ['syb','iyb_one','iyb_two']:
            raise ValidationError(_("Please create Pitching Training before submitting report !!"))
        self.state = 'coordinator_review'
        self.trainer_submitted_report = 'yes'
        self.coordinator_approved = False
        self.coordinator_rejected = False
        self.coordinator_rejection = False
        self.bm_approved = False
        self.bm_rejected = False
        self.branch_manager_rejection = False
        self.ho_admin_approved = False
        self.ho_admin_rejected = False
        self.ho_admin_rejection = False
        self.ho_manager_approved = False
        self.ho_manager_rejected = False
        self.ho_manager_rejection = False
        mail_template = self.env.ref('bmt_training.bmt_training_email_template')
        mail_template.send_mail(self.id, force_send=True,
                                email_values={
                                    'email_from': self.env.user.login,
                                    'email_to': self.coordinator_review_id.login
                                })

    def approved_by_coordinator(self):
        self.state = 'bm_review'
        self.coordinator_approved = 'yes'
        self.coordinator_rejected = 'no'
        self.coordinator_rejection = False
        self.bm_approved = False
        self.bm_rejected = False
        self.branch_manager_rejection = False
        self.ho_admin_approved = False
        self.ho_admin_rejected = False
        self.ho_admin_rejection = False
        self.ho_manager_approved = False
        self.ho_manager_rejected = False
        self.ho_manager_rejection = False
        mail_template = self.env.ref('bmt_training.bmt_training_email_template')
        mail_template.send_mail(self.id, force_send=True,
                                email_values={
                                    'email_from': self.env.user.login,
                                    'email_to': self.branch_manager_id.login
                                })

    def approved_by_branch_manager(self):
        self.state = 'ho_admin_review'
        self.bm_approved = 'yes'
        self.bm_rejected = 'no'
        self.branch_manager_rejection = False
        self.ho_admin_approved = False
        self.ho_admin_rejected = False
        self.ho_admin_rejection = False
        self.ho_manager_approved = False
        self.ho_manager_rejected = False
        self.ho_manager_rejection = False
        mail_template = self.env.ref('bmt_training.bmt_training_email_template')
        mail_template.send_mail(self.id, force_send=True,
                                email_values={
                                    'email_from': self.env.user.login,
                                    'email_to': self.ho_admin_id.login
                                })

    def approved_by_ho_admin(self):
        self.state = 'ho_manager_review'
        self.ho_admin_approved = 'yes'
        self.ho_admin_rejected = 'no'
        self.ho_admin_rejection = False
        self.ho_manager_approved = False
        self.ho_manager_rejected = False
        self.ho_manager_rejection = False
        mail_template = self.env.ref('bmt_training.bmt_training_email_template')
        mail_template.send_mail(self.id, force_send=True,
                                email_values={
                                    'email_from': self.env.user.login,
                                    'email_to': self.ho_manager_id.login
                                })

    def approved_by_ho_manager(self):
        self.ho_manager_approved = 'yes'
        self.ho_manager_rejected = 'no'
        self.ho_manager_rejection = False
        self.state = 'completed'

    def start_pitch_training(self):
        if self.bmt_pitching_id:
            raise UserError(_("Pitching is already created !!"))
        pitching = self.env['business.mgmt.training.pitching'].create({
            'pitching_date': datetime.now(),
            'facilitator_id': self.facilitator_id.id,
            'branch_id': self.branch_id.id,
            'business_mgmt_training_id': self.id,
            'start_date': datetime.strptime(self.pitching_start_date, '%Y-%m-%d %H:%M:%S'),
            'end_date': datetime.strptime(self.pitching_end_date, '%Y-%m-%d %H:%M:%S'),
            'name': "Participant Pitching Session of " + self.name
        })
        for participants in self.bmt_participants_ids:
            if participants.attended_full_training >= 4:
                if participants.dob:
                    final_dob = datetime.strptime(participants.dob, "%Y-%m-%d")
                else:
                    final_dob = ''
                pitching_participants = self.env['bmt.pitching.participants'].create({
                    'participant_id': participants.participant_id.id,
                    'related_participant_id': participants.related_participant_id.id,
                    'dob': final_dob,
                    'gender': participants.gender,
                    'area': participants.area,
                    'is_disabled': participants.is_disabled,
                    'race': participants.race,
                    'mobile': participants.mobile,
                    'business_mgmt_training_pitching_id': pitching.id
                })
        self.bmt_pitching_id = pitching.id
        action = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'business.mgmt.training.pitching',
            'target': 'current',
            'res_id': pitching.id,
        }
        return action

    def send_pitching_mail(self):
        pitching_mail_rec = self.env['business.mgmt.training'].search(
            [('pitching_mail_sent', '=', False), ('training_type', 'in', ['syb', 'iyb_one', 'iyb_two'])])
        mail_template_id = self.env.ref('bmt_training.pitching_email_template')
        for rec in pitching_mail_rec:
            mail_template_id.send_mail(rec.id, force_send=True,
                      email_values={
                          'email_to': rec.facilitator_id.email
                      })
            rec.pitching_mail_sent = True

    def total_attandees(self):
        for rec in self:
            rec.total_no_attended = len(self.env['bmt.participants'].search([('business_mgmt_training_id', '=', rec.id)]))

    def rural_urban_disabled_attendess(self):
        for rec in self:
            bmt_parti_obj = self.env['bmt.participants']
            rec.no_of_rural_participants = bmt_parti_obj.search_count([('business_mgmt_training_id', '=', rec.id), ('area', '=', 'rural')])
            rec.no_of_urban_participants = bmt_parti_obj.search_count([('business_mgmt_training_id', '=', rec.id), ('area', '=', 'urban')])

    def male_female_disabled_attendess(self):
        for rec in self:
            bmt_parti_obj = self.env['bmt.participants']
            rec.no_of_disabled_participants = bmt_parti_obj.search_count([('business_mgmt_training_id', '=', rec.id), ('is_disabled', '=', True)])
            rec.no_of_males_attended = bmt_parti_obj.search_count([('business_mgmt_training_id', '=', rec.id), ('gender', '=', 'male')])
            rec.no_of_females_attended = bmt_parti_obj.search_count([('business_mgmt_training_id', '=', rec.id), ('gender', '=', 'female')])

    def race_attandees(self):
        for rec in self:
            indian_attendess = self.env['bmt.participants'].search(
                [('business_mgmt_training_id', '=', rec.id), ('race', '=', 'indian')])
            asian_attendess = self.env['bmt.participants'].search(
                [('business_mgmt_training_id', '=', rec.id), ('race', '=', 'asian')])
            african_attendess = self.env['bmt.participants'].search(
                [('business_mgmt_training_id', '=', rec.id), ('race', '=', 'african')])
            white_attendess = self.env['bmt.participants'].search(
                [('business_mgmt_training_id', '=', rec.id), ('race', '=', 'white')])
            coloured_attendess = self.env['bmt.participants'].search(
                [('business_mgmt_training_id', '=', rec.id), ('race', '=', 'coloured')])
            rec.no_of_indian_participants = len(indian_attendess)
            rec.no_of_white_participants = len(white_attendess)
            rec.no_of_coloured_participants = len(coloured_attendess)
            rec.no_of_african_participants = len(african_attendess)
            rec.no_of_asian_participants = len(asian_attendess)

    # @api.onchange('start_date', 'end_date', 'training_type')
    # def onchange_date(self):
    #     if  self.start_date and self.end_date and self.training_type:
    #         start_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
    #         end_date = datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
    #         diff = end_date.date() - start_date.date()
    #         if end_date <= start_date:
    #             raise UserError(_("End Date should not be greater than start date."))
    #         if self.training_type == 'syb_iyb' or self.training_type == 'gyb_co_gov':
    #             if not diff.days == 4:
    #                 self.end_date = False
    #         elif self.training_type == 'gyb_only':
    #             if not diff.days == 2:
    #                 self.end_date = False

    @api.depends('start_date')
    def onchange_date(self):
        for res in self:
            if res.start_date:
                start_date = datetime.strptime(res.start_date, "%Y-%m-%d %H:%M:%S")
                sat = 0
                sun = 0
                holiday_count = 0
                sa_holidays = holidays.ZA(years = start_date.year).items()
                if res.training_type in ['syb', 'iyb_one', 'iyb_two', 'syb_coops']:
                    end_date = start_date + timedelta(days=4)
                    diff = end_date - start_date
                    for i in range(diff.days + 1):
                        day = start_date + timedelta(days=i)
                        if day.weekday() == 5:
                            sat += 1
                        elif day.weekday() == 6:
                            sun += 1
                        elif day in sa_holidays:
                            holiday_count += 1
                    if sat > 0 and sun > 0:
                        final_date = end_date + timedelta(days=(sat + sun + holiday_count))
                        res.end_date = final_date
                    elif sat > 0 and sun == 0:
                        final_date = end_date + timedelta(days=(sat + sat + holiday_count))
                        res.end_date = final_date
                    elif sat == 0 and sun > 0:
                        final_date = end_date + timedelta(days=(sun + holiday_count))
                        res.end_date = final_date
                    elif sat == 0 and sun == 0 and holiday_count > 0:
                        final_date = end_date + timedelta(days=(holiday_count))
                        res.end_date = final_date
                    else:
                        res.end_date = end_date
                elif res.training_type in ['gyb']:
                    end_date = start_date + timedelta(days=2)
                    diff = end_date - start_date
                    for i in range(diff.days + 1):
                        day = start_date + timedelta(days=i)
                        if day.weekday() == 5:
                            sat += 1
                        elif day.weekday() == 6:
                            sun += 1
                        elif day in sa_holidays:
                            holiday_count += 1
                    if sat > 0 and sun > 0:
                        final_date = end_date + timedelta(days=(sat + sun + holiday_count))
                        res.end_date = final_date
                    elif sat > 0 and sun == 0:
                        final_date = end_date + timedelta(days=(sat + sat + holiday_count))
                        res.end_date = final_date
                    elif sat == 0 and sun > 0:
                        final_date = end_date + timedelta(days=(sun + holiday_count))
                        res.end_date = final_date
                    elif sat == 0 and sun == 0 and holiday_count > 0:
                        final_date = end_date + timedelta(days=(holiday_count))
                        res.end_date = final_date
                    else:
                        res.end_date = end_date

    @api.onchange('training_type')
    def onchange_training(self):
        if self.training_type:
            self.start_date = False
            self.end_date =  False
