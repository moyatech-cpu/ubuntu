# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError

class PdddOverallTraining(models.Model):
    _name = 'pddd.training'
    _rec_name = 'title'
    _description = 'Pddd Overall Training'

    states = fields.Selection([('new', 'New'), ('confirm_batch', 'Confirm Batch'), ('start_batch', 'Start Batch'),
                               ('submit_coordinator', 'Submitted to Co-ordinator'),
                               ('reject_coordinator', 'Reject Co-ordinator'), ('app_coordinator', 'Approve Co-ordinator'),
                               ('submit_branch_manager', 'Submitted to Branch Manager'),
                               ('reject_branch_manager', 'Reject Branch Manager'),
                               ('app_branch_manager', 'Approve Branch Manager'),
                               ('submit_head_office', 'Submitted to Head Office'),
                               ('reject_head_office', 'Reject Head Office'), ('app_head_office', 'Approve Head Office'),
                               ('submit_senior_manager', 'Submitted to Senior Manager'),
                               ('reject_senior_manager', 'Reject Senior Manager'),
                               ('app_senior_manager', 'Approve Senior Manager'),
                               ('submit_me_personnal', 'Submitted to M&E Personnal'),
                               ('reject_me_personnal', 'Reject M&E Personnal'),
                               ('app_me_personnal', 'Approve M&E Personnal')],
                              string="State",
                              default='new')
    title = fields.Char(string="Title")
    is_start_batch = fields.Boolean(string="Start Batch",default=False)
    training_type_id = fields.Many2one('pddd.type.training', string="Training Type")
    trainer_id = fields.Many2one('res.users', string="Trainer", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_trainer").id)])
    branch_id = fields.Many2one('res.branch', string="Branch")
    participants_ids = fields.One2many('pddd.training.participants', 'pddd_training_id', string="Participants")
    bool_count = fields.Boolean('Boolean Count')
    total_participants = fields.Integer(string="Total Participants", compute="calculate_participants")
    sales_pitch_training_id = fields.Many2one('sales.pitch.training', string="Training")
    business_mgmt_training_id = fields.Many2one('business.mgmt.training', string="Business Management Training")
    upload_report = fields.Binary(string="Upload Training report")
    file_name = fields.Char(string="File Name")
    max_count = fields.Integer(string="Max Attendees")

    def apply_for_training(self):
        all_benificiaries = []
        for rec in self:
            if rec.states == 'new':
                for participants in rec.participants_ids:
                    users = self.env['youth.enquiry'].sudo().search([('id', '=', participants.participants_id.id)]).user_id.id
                    all_benificiaries.append(users)
                all_ben_users = self.env.ref('client_management.group_branch_beneficiary').users.ids
                if not self.env.user.id in all_ben_users:
                    raise UserError(_("Only beneficiaries can apply to this course !!"))
                elif self.env.user.id in all_benificiaries:
                    raise UserError(_("You have already applied to this course !!"))
                elif len(rec.participants_ids) >= rec.max_count:
                    raise UserError(_("Batch is Full !!"))
                else:
                    youth = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.env.user.id)])
                    training_participants = self.env['pddd.training.participants'].sudo().create({
                        'participants_id': youth.id,
                        'gender': youth.gender,
                        'geographic_location': youth.geographic_location,
                        'population_group': youth.population_group,
                        'pddd_training_id': rec.id

                    })
            else:
                raise UserError(_("You cannot apply for these training as batch is confirmed !!"))

    def view_edit_training(self):
        print ("View Edit Training")
        for record in self:
            action = {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'pddd.training',
                'target': 'current',
                'res_id': record.id,
                'flags': {'initial_mode': 'edit'},
                'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
            }
            return action

    def submit_to_coordinator(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        # action_performers = self.env.ref("bmt_training.group_trainer").users
        # f_ap = set(action_performers) & set(user)
        # for ap in f_ap:
        #     ap_ids.append(ap.id)
        recepients = self.env.ref("client_management.group_coordinator").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id == self.trainer_id.id or self.env.user.id in ap_ids:
            self.states = 'submit_coordinator'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def reject_by_coordinator(self):
        # final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("client_management.group_coordinator").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        # recepients = self.env.ref("bmt_training.group_trainer").users
        # f_recepients = set(recepients) & set(user)
        # for u in f_recepients:
        #     final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'reject_coordinator'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': self.trainer_id.login
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def app_by_coordinator(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("client_management.group_coordinator").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("client_management.group_branch_manager").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'app_coordinator'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def submit_to_branch_manager(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("client_management.group_coordinator").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("client_management.group_branch_manager").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'submit_branch_manager'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def reject_by_branch_manager(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("client_management.group_branch_manager").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("client_management.group_coordinator").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'reject_branch_manager'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def app_by_branch_manager(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("client_management.group_branch_manager").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("mentorship.group_bmp").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'app_branch_manager'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def submit_to_head_office(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("client_management.group_branch_manager").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("mentorship.group_bmp").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'submit_head_office'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def reject_by_head_office(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("mentorship.group_bmp").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("client_management.group_branch_manager").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'reject_head_office'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def app_by_head_office(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("mentorship.group_bmp").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("monitoring_and_evaluation.group_senior_manager").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'app_head_office'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def submit_to_senior_manager(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("mentorship.group_bmp").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("monitoring_and_evaluation.group_senior_manager").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'submit_senior_manager'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def reject_by_senior_manager(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("mentorship.group_bmp").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("monitoring_and_evaluation.group_senior_manager").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'reject_senior_manager'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def app_by_senior_manager(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("monitoring_and_evaluation.group_senior_manager").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("monitoring_and_evaluation.group_me_personnal").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'app_senior_manager'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def submit_to_me_personnal(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("monitoring_and_evaluation.group_senior_manager").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("monitoring_and_evaluation.group_me_personnal").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'submit_me_personnal'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def reject_by_me_personnal(self):
        final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("monitoring_and_evaluation.group_me_personnal").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        recepients = self.env.ref("monitoring_and_evaluation.group_senior_manager").users
        f_recepients = set(recepients) & set(user)
        for u in f_recepients:
            final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'reject_me_personnal'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': final_users
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    def app_by_me_personnal(self):
        # final_users = ''
        ap_ids = []
        admin = self.env.ref("base.group_system").users
        for a in admin:
            ap_ids.append(a.id)
        user = self.env['res.users'].search([('branch_id', '=', self.branch_id.id)])
        action_performers = self.env.ref("monitoring_and_evaluation.group_me_personnal").users
        f_ap = set(action_performers) & set(user)
        for ap in f_ap:
            ap_ids.append(ap.id)
        # recepients = self.env.ref("monitoring_and_evaluation.group_senior_manager").users
        # f_recepients = set(recepients) & set(user)
        # for u in f_recepients:
        #     final_users += u.login + ","
        if self.env.user.id in ap_ids:
            self.states = 'app_me_personnal'
            mail_template = self.env.ref('bmt_training.overall_training_email_template')
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': self.trainer_id.login
                                    })
        else:
            raise UserError(_("You are not allowed to perform this action as this branch is not assigned to you !!"))

    @api.depends('participants_ids')
    def calculate_participants(self):
        for res in self:
            count_len = len(res.participants_ids)
            res.total_participants = count_len

    @api.multi
    @api.onchange('participants_ids')
    def _onchange_participants_ids(self):
        for res in self:
            count_len = len(res.participants_ids)
            print("Length of Participant Id==", len(res.participants_ids))
            if res.max_count != 0:
                if count_len == res.max_count:
                    self.bool_count = True
                if count_len > res.max_count:
                    raise UserError(_('Your Participants count has reached max limit. Please do not add more'))

    @api.multi
    def start_batch(self):
        """ Start Training """
        if self.participants_ids:
            for participants_id in self.participants_ids:
                if participants_id.state == False:
                    raise UserError(_('You can not start batch without all participant Confirmation.'))
        bmt_id = self.env.ref('bmt_training.pddd_type_training_1')
        sales_pitch_id = self.env.ref('bmt_training.pddd_type_training_2')
        bbbee_id = self.env.ref('bmt_training.pddd_type_training_3')
        job_preparedness_id = self.env.ref('bmt_training.pddd_type_training_4')
        sales_pitch_bbbee_id = self.env.ref('bmt_training.pddd_type_training_5')
        life_skills_id = self.env.ref('bmt_training.pddd_type_training_6')
        digital_skills_id = self.env.ref('bmt_training.pddd_type_training_7')

        if self.training_type_id.id == bmt_id.id:
            bmt_training = self.env['business.mgmt.training'].create({
                'name' : self.title,
                'facilitator_id': self.trainer_id.id,
                'branch_id':self.branch_id.id,
                'pdd_training_id':self.id,
                'training_type_id':self.training_type_id.id,
                'max_count': self.max_count
            })
            self.business_mgmt_training_id = bmt_training.id
            for participants_record in self.participants_ids:
                if participants_record.state == 'confirm':
                    data = {
                        'participant_id' : participants_record.participants_id.id ,
                        'dob' : participants_record.dob ,
                        'gender' : participants_record.gender ,
                        'area' : participants_record.geographic_location ,
                        'is_disabled' : participants_record.is_disabled ,
                        'race' : participants_record.population_group ,
                        'mobile' : participants_record.cell_phone_number ,
                        'business_mgmt_training_id' : bmt_training.id,
                    }
                    participant = self.env['bmt.participants'].create(data)
            self.states = 'start_batch'
            self.is_start_batch = True
            return {
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'business.mgmt.training',
                'res_id': bmt_training.id,
                'type': 'ir.actions.act_window',
            }
        elif self.training_type_id.id == sales_pitch_bbbee_id.id:
            sp_training = self.env['sales.pitch.training'].create({
                'name': "Training for " + self.title,
                'trainer_id': self.trainer_id.id,
                'branch_id':self.branch_id.id,
                'intervention_type': 'sales_pitch_bbbee',
                'max_count': self.max_count
            })
            self.sales_pitch_training_id = sp_training.id
            for participants_record in self.participants_ids:
                if participants_record.state == 'confirm':
                    data = {
                        'participant_id' : participants_record.participants_id.id ,
                        'dob' : participants_record.dob ,
                        'gender' : participants_record.gender ,
                        'geographic_location' : participants_record.geographic_location ,
                        'is_disabled' : participants_record.is_disabled ,
                        'race' : participants_record.population_group ,
                        'contact_number' : participants_record.cell_phone_number ,
                        'sp_training_id' : sp_training.id ,
                    }
                    participant = self.env['training.attendance'].create(data)
            self.states = 'start_batch'
            self.is_start_batch = True
            return {
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'sales.pitch.training',
                'res_id': sp_training.id,
                'type': 'ir.actions.act_window',
            }
        elif self.training_type_id.id == sales_pitch_id.id:
            sp_training = self.env['sales.pitch.training'].create({
                'name': "Training for " + self.title,
                'trainer_id': self.trainer_id.id,
                'branch_id':self.branch_id.id,
                'intervention_type': 'sales_pitch',
                'max_count': self.max_count
            })
            self.sales_pitch_training_id = sp_training.id
            for participants_record in self.participants_ids:
                if participants_record.state == 'confirm':
                    data = {
                        'participant_id' : participants_record.participants_id.id ,
                        'dob' : participants_record.dob ,
                        'gender' : participants_record.gender ,
                        'geographic_location' : participants_record.geographic_location ,
                        'is_disabled' : participants_record.is_disabled ,
                        'race' : participants_record.population_group ,
                        'contact_number' : participants_record.cell_phone_number ,
                        'sp_training_id_3' : sp_training.id ,
                    }
                    participant = self.env['training.attendance'].create(data)
            self.states = 'start_batch'
            self.is_start_batch = True
            return {
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'sales.pitch.training',
                'res_id': sp_training.id,
                'type': 'ir.actions.act_window',
            }
        elif self.training_type_id.id == bbbee_id.id:
            sp_training = self.env['sales.pitch.training'].create({
                'name': "Training for " + self.title,
                'trainer_id': self.trainer_id.id,
                'branch_id':self.branch_id.id,
                'intervention_type': 'bbbee',
                'max_count': self.max_count
            })
            self.sales_pitch_training_id = sp_training.id
            for participants_record in self.participants_ids:
                if participants_record.state == 'confirm':
                    data = {
                        'participant_id' : participants_record.participants_id.id ,
                        'dob' : participants_record.dob ,
                        'gender' : participants_record.gender ,
                        'geographic_location' : participants_record.geographic_location ,
                        'is_disabled' : participants_record.is_disabled ,
                        'race' : participants_record.population_group ,
                        'contact_number' : participants_record.cell_phone_number ,
                        'sp_training_id_3' : sp_training.id ,
                    }
                    participant = self.env['training.attendance'].create(data)
            self.states = 'start_batch'
            self.is_start_batch = True
            return {
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'sales.pitch.training',
                'res_id': sp_training.id,
                'type': 'ir.actions.act_window',
            }
        elif self.training_type_id.id == job_preparedness_id.id:
            sp_training = self.env['sales.pitch.training'].create({
                'name': "Training for " + self.title,
                'trainer_id': self.trainer_id.id,
                'branch_id':self.branch_id.id,
                'intervention_type': 'job_preparedness',
                'max_count': self.max_count
            })
            self.sales_pitch_training_id = sp_training.id
            for participants_record in self.participants_ids:
                if participants_record.state == 'confirm':
                    data = {
                        'participant_id' : participants_record.participants_id.id ,
                        'dob' : participants_record.dob ,
                        'gender' : participants_record.gender ,
                        'geographic_location' : participants_record.geographic_location ,
                        'is_disabled' : participants_record.is_disabled ,
                        'race' : participants_record.population_group ,
                        'contact_number' : participants_record.cell_phone_number ,
                        'sp_training_id_3' : sp_training.id ,
                    }
                    participant = self.env['training.attendance'].create(data)
            self.states = 'start_batch'
            self.is_start_batch = True
            return {
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'sales.pitch.training',
                'res_id': sp_training.id,
                'type': 'ir.actions.act_window',
            }
        elif self.training_type_id.id == life_skills_id.id:
            sp_training = self.env['sales.pitch.training'].create({
                'name': "Training for " + self.title,
                'trainer_id': self.trainer_id.id,
                'branch_id':self.branch_id.id,
                'intervention_type': 'life_skills',
                'max_count': self.max_count
            })
            self.sales_pitch_training_id = sp_training.id
            for participants_record in self.participants_ids:
                if participants_record.state == 'confirm':
                    data = {
                        'participant_id' : participants_record.participants_id.id ,
                        'dob' : participants_record.dob ,
                        'gender' : participants_record.gender ,
                        'geographic_location' : participants_record.geographic_location ,
                        'is_disabled' : participants_record.is_disabled ,
                        'race' : participants_record.population_group ,
                        'contact_number' : participants_record.cell_phone_number ,
                        'sp_training_id_3' : sp_training.id ,
                    }
                    participant = self.env['training.attendance'].create(data)
            self.states = 'start_batch'
            self.is_start_batch = True
            return {
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'sales.pitch.training',
                'res_id': sp_training.id,
                'type': 'ir.actions.act_window',
            }
        elif self.training_type_id.id == digital_skills_id.id:
            sp_training = self.env['sales.pitch.training'].create({
                'name': "Training for " + self.title,
                'trainer_id': self.trainer_id.id,
                'branch_id':self.branch_id.id,
                'intervention_type': 'digital_skills',
                'max_count': self.max_count
            })
            self.sales_pitch_training_id = sp_training.id
            for participants_record in self.participants_ids:
                if participants_record.state == 'confirm':
                    data = {
                        'participant_id' : participants_record.participants_id.id ,
                        'dob' : participants_record.dob ,
                        'gender' : participants_record.gender ,
                        'geographic_location' : participants_record.geographic_location ,
                        'is_disabled' : participants_record.is_disabled ,
                        'race' : participants_record.population_group ,
                        'contact_number' : participants_record.cell_phone_number ,
                        'sp_training_id_3' : sp_training.id ,
                    }
                    participant = self.env['training.attendance'].create(data)
            self.states = 'start_batch'
            self.is_start_batch = True
            return {
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'sales.pitch.training',
                'res_id': sp_training.id,
                'type': 'ir.actions.act_window',
            }

    @api.multi
    def confirm_batch(self):
        """ Confirm Training """
        self.states = 'confirm_batch'
        participants_mail = self.participants_ids
        mail_template_id = self.env.ref('bmt_training.participants_email_template')
        for rec in participants_mail:
            mail_template_id.send_mail(self.id, force_send=True,
                                       email_values={
                                           'email_to': rec.participants_id.email
                                       })
        return


class PdddTypeTraining(models.Model):
    _name = 'pddd.type.training'
    _rec_name = 'name'
    _description = 'Pddd Type Training'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")


class PdddTrainingParticipants(models.Model):
    _name = 'pddd.training.participants'

    pddd_training_id = fields.Many2one('pddd.training',string="Pddd Training")
    participants_id = fields.Many2one('youth.enquiry', string="Beneficiary")
    dob = fields.Datetime(string="Date Of birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", related="participants_id.gender")
    id_number = fields.Char('ID Number', related="participants_id.id_number")
    population_group = fields.Selection(
        [('african', 'African'), ('asian', 'Asian'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Race", related="participants_id.population_group")
    geographic_location = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Rural area - Villages'),
         ('rural-area-farms', 'Rural area - Farms'), ('informa-settlement', 'Informa settlement')],
        string="Geographic Location",related="participants_id.geographic_location")
    is_disabled = fields.Boolean(string="Is Disabled",default=False)
    cell_phone_number = fields.Char('Contact Number', related="participants_id.cell_phone_number")
    branch_id = fields.Many2one('res.branch', string="Branch")
    state = fields.Selection([('confirm', 'Confirm'), ('reject', 'Reject')],
                              string="Confirmation")
    training_state = fields.Selection(
        [('new', 'New'), ('confirm_batch', 'Confirm Batch'), ('start_batch', 'Start Batch')], string="State",
        related='pddd_training_id.states')

    @api.onchange('participants_id')
    def _onchange_participants_id(self):
        if self.id_number:
            try:
                if int(self.id_number[:2]) < 50:
                    date = "20" + self.id_number[:2] + "-" + self.id_number[2:4] + "-" + self.id_number[4:6]
                    self.dob = datetime.strptime(date, '%Y-%m-%d').date()
                else:
                    date = "19" + self.id_number[:2] + "-" + self.id_number[2:4] + "-" + self.id_number[4:6]
                    self.dob = datetime.strptime(date, '%Y-%m-%d').date()
            except Exception:
                raise UserError(_('You are not on our age group'))

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
