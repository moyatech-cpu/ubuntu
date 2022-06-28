# coding=utf-8
import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime,date,timedelta
from lxml import etree
from odoo.exceptions import ValidationError
from odoo.tools.misc import ustr

class CopGovMenteeParticipants(models.Model):
    """ Cooperative Governance Mentee Participants """
    _name = "cop.gov.mentee.participants"
    _rec_name = "mentee_id"
    _description = "Cooperative Governance Mentee Participants"

    mentee_id = fields.Many2one('youth.enquiry', string="Name")
    surname = fields.Char(string="Surname", related="mentee_id.surname")
    id_number = fields.Char(string="ID Number", related="mentee_id.id_number")
    mobile = fields.Char(string="Mobile", related="mentee_id.alternative_number")
    email = fields.Char(string="E-mail", related="mentee_id.email")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('not_specify', 'Not Specify')], string="Gender",
                              related="mentee_id.gender")
    is_disabled = fields.Selection([('yes','Yes'), ('no','No')], string="Is Disabled")
    area = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Rural area - Villages'),
         ('rural-area-farms', 'Rural area - Farms'), ('informa-settlement', 'Informa settlement')],
        string="Geographic Location", related="mentee_id.geographic_location")
    telephone = fields.Char(string="Telephone", related="mentee_id.cell_phone_number")
    cop_gov_training_id = fields.Many2one('cooperative.governance.training', string="Cooperative Governance Training")
    cop_gov_training_id_2 = fields.Many2one('cooperative.governance.training',
                                            string="Cooperative Governance Training 2")
    signature = fields.Binary(string="Signature")
    signed = fields.Boolean(string="Signed")
    state = fields.Selection([('confirm', 'Confirmed'), ('reject', 'Rejected')], string="State")
    race = fields.Selection(
        [('african', 'African'), ('asian', 'Asian'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Race", related="mentee_id.population_group")

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

class CooperativeGovernanceTraining(models.Model):
    """ Cooperative Governance Training """
    _name = "cooperative.governance.training"
    _rec_name = "name"
    _description = "Cooperative Governance Training"

    name = fields.Char(string="Title")
    state = fields.Selection([('new', 'New'),('start_training', 'Start Training'),
                              ('end_training', 'End Training'), ('coordinator_review', 'Coordinator Review'),
                              ('bm_review', 'Branch Manager Review'),
                              ('ho_admin_review', 'HO Admin Review'), ('ho_manager_review', 'HO Manager Review'),
                              ('completed', 'Completed')], string="State", default="new")
    trainer_id = fields.Many2one('res.users', string="Trainer", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_trainer").id)], default=lambda self:self.get_trainer())
    start_date = fields.Date('Training Start Date', default=lambda self: date.today())
    branch_id = fields.Many2one('res.branch', string="Branch")
    intervention_type = fields.Selection(
        [('job_preparedness', 'Job Preparedness'), ('life_skills', 'Life Skills'),
         ('sales_pitch_bbbee', 'Sales Pitch/BBBEE'), ('digital_skills', 'Digital Skills'), ('cooperative_governance', 'Cooperative Governance')],
        string="Intervention Type")
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

    end_date = fields.Date('Training End Date', default=lambda self:self.get_end_date())
    nyda_products = fields.Selection([('mentorship', 'Mentorship'), ('grant', 'Grant'), ('voucher', 'Voucher')],
                                     string="NYDA Products")
    participant_ids = fields.One2many('cop.gov.mentee.participants', 'cop_gov_training_id',
                                      string="Session 1  Participants")
    participant_ids_2 = fields.One2many('cop.gov.mentee.participants', 'cop_gov_training_id_2',
                                        string="Session 2 Participants")
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
    total_youth = fields.Integer(string="Total no. of youth attended", compute="calculate_participants", store=True)
    no_of_males = fields.Integer(string="No. of Males Attended", compute="calculate_participants", store=True)
    no_of_females = fields.Integer(string="No. of Females Attended", compute="calculate_participants", store=True)
    no_of_rural_participants = fields.Integer(string="No. of Rural Participants", compute="calculate_participants", store=True)
    no_of_urban_participants = fields.Integer(string="No. of Urban Participants", compute="calculate_participants", store=True)
    no_of_african_participants = fields.Integer(string="No. of African Participants", compute="calculate_participants", store=True)
    no_of_coloured_participants = fields.Integer(string="No. of Coloured Participants", compute="calculate_participants", store=True)
    no_of_indian_participants = fields.Integer(string="No. of Indian Participants", compute="calculate_participants", store=True)
    no_of_asian_participants = fields.Integer(string="No. of Asian Participants", compute="calculate_participants", store=True)
    no_of_disabled_participants = fields.Integer(string="No. of Disabled Participants", compute="calculate_participants", store=True)
    no_of_white_participants = fields.Integer(string="No. of White Participants", compute="calculate_participants", store=True)
    venue = fields.Text('Training Venue')
    bmt_id = fields.Many2one('business.mgmt.training', string="Business Management Training")

    def refer_training(self):
        if not self.bmt_id:
            raise ValidationError(_("Please select Business Management Training !!"))
        else:
            all_participants = []
            joining_participants = []
            part_count = 0
            count = 0
            add_part = True
            rem_space = 0
            for training_id in self.bmt_id.bmt_participants_ids:
                all_participants.append(training_id.participant_id)
            for training_id in self.participant_ids:
                if training_id.state == 'confirm' and training_id.signed == True:
                    part_count += 1
                    joining_participants.append(training_id)
            for training_id in self.participant_ids_2:
                if training_id.state == 'confirm' and training_id.signed == True:
                    part_count += 1
                    joining_participants.append(training_id)
            if self.bmt_id.max_attendees == 0:
                add_part = True
            else:
                rem_space = self.bmt_id.max_attendees - len(self.bmt_id.bmt_participants_ids)
                if not rem_space >= part_count:
                    add_part = False
                    raise ValidationError(_(
                        "Only " + str(rem_space) + " participant can join the training and there are " + str(
                            part_count) + " particpant so training cannot be reffered !!"))
            print ("\n\n\n\n JP ", joining_participants)
            for training_id in joining_participants:
                already_trained = 0
                other_training = self.env['bmt.participants'].sudo().search(
                    [('participant_id', '=', training_id.id), ('business_mgmt_training_id', '=', self.bmt_id.id)])
                for ot in other_training:
                    if ot.business_mgmt_training_id.training_type == 'syb_coops':
                        already_trained = 1
                # if self.bmt_id.max_attendees == 0:
                #     add_part = True
                # else:
                #     rem_space = self.bmt_id.max_attendees - len(self.bmt_id.bmt_participants_ids)
                #     if not rem_space >= part_count:
                #         add_part = False
                if add_part == True:
                    if not training_id.mentee_id in all_participants and training_id.state == 'confirm' and already_trained == 0 and training_id.signed == True:
                        attendance_data = self.env['bmt.participants'].sudo().create({
                            'participant_id': training_id.mentee_id.id,
                            'gender': training_id.gender,
                            'area': training_id.area,
                            'is_disabled': training_id.is_disabled,
                            'race': training_id.race,
                            'mobile': training_id.telephone,
                            'business_mgmt_training_id': self.bmt_id.id,
                            'coop_gov_id': self.id
                        })
                        count += 1
                else:
                    if not rem_space == 0:
                        raise ValidationError(_(
                            "Only " + str(rem_space) + " participant can join the training and there are " + str(
                                part_count) + " particpant so training cannot be reffered !!"))
                    else:
                        raise ValidationError(_("Batch is full !!"))
            if count == 0:
                raise ValidationError(_("All participants are already added !!"))

    @api.model
    def create(self, vals):
        res = super(CooperativeGovernanceTraining, self).create(vals)
        if res.intervention_type == 'cooperative_governance':
            ref_number = self.env['ir.sequence'].next_by_code('cg_code') or _('New')
            res.name = ref_number
        return res

    @api.model
    def get_end_date(self):
        return date.today() + timedelta(days=1)

    @api.constrains('end_date')
    @api.one
    def _check_number(self):
        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        days = (end_date - start_date).days
        if end_date <= start_date:
            raise ValidationError(_("End date cannot be same or smaller than start date."))
        elif days != 1:
            raise ValidationError(_('Training must be for 2 days only.'))

    @api.depends('participant_ids', 'participant_ids_2')
    def calculate_participants(self):
        for rec in self:
            males = 0
            females = 0
            rural = 0
            urban = 0
            african = 0
            asian = 0
            indian = 0
            coloured = 0
            white = 0
            disabled = 0
            #update Sep 27 22:16 2021 calculate participants
            all_participants = rec.participant_ids + rec.participant_ids_2
            unique_users = []
            unique_users_bmt = []

            for obj in all_participants:
                if obj.mentee_id.user_id in unique_users:
                    pass
                else:
                    unique_users.append(obj.mentee_id.user_id)
                    unique_users_bmt.append(obj)

            rec.total_youth = len(unique_users)

            for youth in unique_users_bmt:
                if youth.gender == 'male':
                    males += 1
                if youth.gender == 'female':
                    females += 1
                if youth.area in ['urban', 'peri-urban']:
                    urban += 1
                if youth.area in ['rural-area-villages', 'rural-area-farms']:
                    rural += 1
                if youth.race == 'african':
                    african += 1
                if youth.race == 'asian':
                    asian += 1
                if youth.race == 'indian':
                    indian += 1
                if youth.race == 'coloured':
                    coloured += 1
                if youth.race == 'white':
                    white += 1
                if youth.is_disabled == 'yes':
                    disabled += 1

            """ Old calculate participants
            rec.total_youth = len(rec.participant_ids) + len(rec.participant_ids_2)
            for single_rec in rec.participant_ids:
                if single_rec.gender == 'male':
                    males += 1
                if single_rec.gender == 'female':
                    females += 1
                if single_rec.area in ['urban', 'peri-urban']:
                    urban += 1
                if single_rec.area in ['rural-area-villages', 'rural-area-farms']:
                    rural += 1
                if single_rec.race == 'african':
                    african += 1
                if single_rec.race == 'asian':
                    asian += 1
                if single_rec.race == 'indian':
                    indian += 1
                if single_rec.race == 'coloured':
                    coloured += 1
                if single_rec.race == 'white':
                    white += 1
                if single_rec.is_disabled == 'yes':
                    disabled += 1
            for second_rec in rec.participant_ids_2:
                if second_rec.gender == 'male':
                    males += 1
                if second_rec.gender == 'female':
                    females += 1
                if second_rec.area in ['urban', 'peri-urban']:
                    urban += 1
                if second_rec.area in ['rural-area-villages', 'rural-area-farms']:
                    rural += 1
                if second_rec.race == 'african':
                    african += 1
                if second_rec.race == 'asian':
                    asian += 1
                if second_rec.race == 'indian':
                    indian += 1
                if second_rec.race == 'coloured':
                    coloured += 1
                if second_rec.race == 'white':
                    white += 1
                if second_rec.is_disabled == 'yes':
                    disabled += 1
                    """
            rec.no_of_males = males
            rec.no_of_females = females
            rec.no_of_rural_participants = rural
            rec.no_of_urban_participants = urban
            rec.no_of_african_participants = african
            rec.no_of_coloured_participants = coloured
            rec.no_of_indian_participants = indian
            rec.no_of_disabled_participants = disabled
            rec.no_of_white_participants = white
            rec.no_of_asian_participants = asian

    def submit_report(self):
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
        mail_template = self.env.ref('bmt_training.coopertive_governance_training_email_template')
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
        mail_template = self.env.ref('bmt_training.coopertive_governance_training_email_template')
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
        mail_template = self.env.ref('bmt_training.coopertive_governance_training_email_template')
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
        mail_template = self.env.ref('bmt_training.coopertive_governance_training_email_template')
        mail_template.send_mail(self.id, force_send=True,
                                email_values={
                                    'email_from': self.env.user.login,
                                    'email_to': self.ho_manager_id.login
                                })

    def view_edit_training(self):
        group_list = []
        coordinator = self.env['res.groups'].search(
            [('id', '=', self.env.ref("client_management.group_coordinator").id)])
        group_list.append(coordinator.id)
        bm = self.env['res.groups'].search(
            [('id', '=', self.env.ref("client_management.group_branch_manager").id)])
        group_list.append(bm.id)
        ho_admin = self.env['res.groups'].search(
            [('id', '=', self.env.ref("bmt_training.group_ho_admin").id)])
        group_list.append(ho_admin.id)
        ho_manager = self.env['res.groups'].search(
            [('id', '=', self.env.ref("bmt_training.group_ho_manager").id)])
        group_list.append(ho_manager.id)
        for gid in group_list:
            if gid in self.env.user.groups_id.ids:
                return True
        for record in self:
            action = {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'cooperative.governance.training',
                'target': 'current',
                'res_id': record.id,
                'flags': {'initial_mode': 'edit'},
                'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
            }
            return action

    def approved_by_ho_manager(self):
        self.ho_manager_approved = 'yes'
        self.ho_manager_rejected = 'no'
        self.ho_manager_rejection = False
        self.state = 'completed'

    @api.model
    def get_cop_gov_data(self):
        single_attendees = []
        for attendees in self.participant_ids:
            single_attendees.append(attendees)
        return single_attendees

    @api.multi
    def get_attendance_register(self):
        return self.env.ref('bmt_training.action_report_coop_gov_attendance_register').report_action(self)

    def state_accepted(self):
        self.state = 'start_training'

    def state_rejected(self):
        self.state = 'end_training'

    def get_trainer(self):
        trainer = self.env['res.groups'].search(
            [('id', '=', self.env.ref("bmt_training.group_trainer").id)])
        if trainer.id in self.env.user.groups_id.ids:
            return self.env.user.id
        else:
            return False

    @api.onchange('trainer_id')
    def get_branch(self):
        if self.trainer_id:
            self.branch_id = self.trainer_id.branch_id.id
            trainer_data = self.env['link.trainer'].sudo().search([('trainer_id', '=', self.trainer_id.id)])
            self.coordinator_review_id = trainer_data.coordinator_id.id
            self.ho_admin_id = trainer_data.head_office_admin_id.id
            self.branch_manager_id = trainer_data.branch_manager_id.id
            self.ho_manager_id = trainer_data.head_office_manager_id.id