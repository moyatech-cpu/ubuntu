# coding=utf-8
import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree
from odoo.tools.misc import ustr


class SalesPitchTraining(models.Model):
    """ Sales pitch Training model to provide proper details for particular details. """
    _name = "sales.pitch.training"
    _rec_name = "name"
    _description = "Sales pitch Training"

    name = fields.Char(string="Title")
    state = fields.Selection([('new', 'New'), ('start_training', 'Start Training'), ('end_training', 'End Training'),
                              ('coordinator_review', 'Coordinator Review'), ('bm_review', 'Branch Manager Review'),
                              ('ho_admin_review', 'HO Admin Review'), ('ho_manager_review', 'HO Manager Review'),
                              ('completed', 'Completed')], string="State", default='new')
    trainer_id = fields.Many2one('res.users', string="Trainer", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_trainer").id)], default=lambda self:self.get_trainer())
    start_date = fields.Date('Training Start Date', default=lambda today: datetime.date.today())
    end_date = fields.Date('Training End Date', default=lambda self:self.get_end_date())
    venue = fields.Text('Training Venue')
    branch_id = fields.Many2one('res.branch', string="Branch")
    facilitator = fields.Char(string="Facilitator")
    municipality = fields.Many2one('res.municipality', string="Municipality")
    intervention_type = fields.Selection(
        [('job_preparedness', 'Job Preparedness'), ('life_skills', 'Life Skills'),
         ('sales_pitch_bbbee', 'Sales Pitch/BBBEE'), ('digital_skills', 'Digital Skills'),
         ('sales_pitch', 'Sales Pitch'), ('bbbee', 'BBBEE')],
        string="Intervention Type")
    total_youth = fields.Integer(string="Total no. of youth attended", compute="calculate_participants", store=True)
    no_of_males = fields.Integer(string="No. of Males Attended", compute="calculate_participants", store=True)
    no_of_females = fields.Integer(string="No. of Females Attended", compute="calculate_participants", store=True)
    no_of_rural_participants = fields.Integer(string="No. of Rural Participants", compute="calculate_participants", store=True)
    no_of_urban_participants = fields.Integer(string="No. of Urban Participants", compute="calculate_participants", store=True)
    no_of_african_participants = fields.Integer(string="No. of African Participants", compute="calculate_participants", store=True)
    no_of_coloured_participants = fields.Integer(string="No. of Coloured Participants", compute="calculate_participants", store=True)
    no_of_indian_participants = fields.Integer(string="No. of Indian Participants", compute="calculate_participants", store=True)
    no_of_disabled_participants = fields.Integer(string="No. of Disabled Participants", compute="calculate_participants", store=True)
    no_of_white_participants = fields.Integer(string="No. of White Participants", compute="calculate_participants", store=True)
    no_of_asian_participants = fields.Integer(string="No. of Asian Participants", compute="calculate_participants", store=True)
    session_1_title = fields.Char('Session 1')
    session_1_details = fields.Text('Details')
    session_1_attendee_ids = fields.One2many('training.attendance', 'sp_training_id' ,'Attendance')
    session_2_title = fields.Char('Session 2')
    session_2_details = fields.Text('Details')
    session_2_attendee_ids = fields.One2many('training.attendance', 'sp_training_id_2' ,'Attendance')
    session_3_attendee_ids = fields.One2many('training.attendance', 'sp_training_id_3', 'Attendance')
    service_coordinator_name = fields.Char(string="Service Co-ordinator Name")
    service_coordinator_signature = fields.Binary(string="Service Co-ordinator Signature")
    facilitator_signature = fields.Binary(string="Facilitator Signature")
    facilitator_date = fields.Datetime(string="Facilitator Date")
    total_participants_jld = fields.Integer(string="Total Participants", compute="calculate_participants_jld")
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
    max_count = fields.Integer(string="Max Attendees", default='1')
    sales_pitch_training_id = fields.Many2one('sales.pitch.training', string="Sales Pitch Training")
    bbbee_training_id = fields.Many2one('sales.pitch.training', string="BBBEE Training")
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

    def refer_participants(self):
        if self.intervention_type == 'sales_pitch':
            if not self.bbbee_training_id:
                raise ValidationError(_("Please select BBBEE Training"))
            else:
                all_participants = []
                part_count = 0
                count = 0
                add_part = True
                rem_space = 0
                for training_id in self.bbbee_training_id.session_3_attendee_ids:
                    all_participants.append(training_id.participant_id)
                for training_id in self.session_3_attendee_ids:
                    if training_id.state == 'confirm' and training_id.signature_done == True:
                        part_count += 1
                if self.bbbee_training_id.max_count == 0:
                    add_part = True
                else:
                    rem_space = self.bbbee_training_id.max_count - len(self.bbbee_training_id.session_3_attendee_ids)
                    if not rem_space >= part_count:
                        add_part = False
                        raise ValidationError(_(
                            "Only " + str(
                                rem_space) + " participant can join the training and there are " + str(
                                part_count) + " particpant so training cannot be reffered !!"))
                for training_id in self.session_3_attendee_ids:
                    already_trained = 0
                    other_training = self.env['training.attendance'].sudo().search(
                        [('participant_id', '=', training_id.participant_id.id), ('sp_training_id_3', '!=', False)])
                    for ot in other_training:
                        if ot.sp_training_id_3.intervention_type == 'bbbee':
                            already_trained = 1
                    # if self.bbbee_training_id.max_count == 0:
                    #     add_part = True
                    # else:
                    #     rem_space = self.bbbee_training_id.max_count - len(self.bbbee_training_id.session_3_attendee_ids)
                    #     if not rem_space >= part_count:
                    #         add_part = False
                    if add_part == True:
                        if not training_id.participant_id in all_participants and training_id.state == 'confirm' and already_trained == 0 and training_id.signature_done == True:
                            attendance_data = self.env['training.attendance'].sudo().create({
                                'participant_id': training_id.participant_id.id,
                                'dob': training_id.dob,
                                'gender': training_id.gender,
                                'geographic_location': training_id.geographic_location,
                                'is_disabled': training_id.is_disabled,
                                'race': training_id.race,
                                'physical_address': training_id.physical_address,
                                'contact_number': training_id.contact_number,
                                'sp_training_id_3': self.bbbee_training_id.id
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
        elif self.intervention_type == 'bbbee':
            if not self.sales_pitch_training_id:
                raise ValidationError(_("Please select Sales Pitch Training"))
            else:
                all_participants = []
                part_count = 0
                count = 0
                add_part = True
                rem_space = 0
                for training_id in self.sales_pitch_training_id.session_3_attendee_ids:
                    all_participants.append(training_id.participant_id)
                for training_id in self.session_3_attendee_ids:
                    if training_id.state == 'confirm' and training_id.signature_done == True:
                        part_count += 1
                if self.sales_pitch_training_id.max_count == 0:
                    add_part = True
                else:
                    rem_space = self.sales_pitch_training_id.max_count - len(self.sales_pitch_training_id.session_3_attendee_ids)
                    if not rem_space >= part_count:
                        add_part = False
                        raise ValidationError(_(
                            "Only " + str(
                                rem_space) + " participant can join the training and there are " + str(
                                part_count) + " particpant so training cannot be reffered !!"))
                for training_id in self.session_3_attendee_ids:
                    already_trained = 0
                    other_training = self.env['training.attendance'].sudo().search(
                        [('participant_id', '=', training_id.participant_id.id), ('sp_training_id_3', '!=', False)])
                    for ot in other_training:
                        if ot.sp_training_id_3.intervention_type == 'sales_pitch':
                            already_trained = 1
                    # if self.bbbee_training_id.max_count == 0:
                    #     add_part = True
                    # else:
                    #     rem_space = self.bbbee_training_id.max_count - len(self.bbbee_training_id.session_3_attendee_ids)
                    #     if not rem_space >= part_count:
                    #         add_part = False
                    if add_part == True:
                        if not training_id.participant_id in all_participants and training_id.state == 'confirm' and already_trained == 0:
                            attendance_data = self.env['training.attendance'].sudo().create({
                                'participant_id': training_id.participant_id.id,
                                'dob': training_id.dob,
                                'gender': training_id.gender,
                                'geographic_location': training_id.geographic_location,
                                'is_disabled': training_id.is_disabled,
                                'race': training_id.race,
                                'physical_address': training_id.physical_address,
                                'contact_number': training_id.contact_number,
                                'sp_training_id_3': self.sales_pitch_training_id.id
                            })
                            count += 1
                        else:
                            if not rem_space == 0:
                                raise ValidationError(_(
                                    "Only " + str(
                                        rem_space) + " participant can join the training and there are " + str(
                                        part_count) + " particpant so training cannot be reffered !!"))
                            else:
                                raise ValidationError(_("Batch is full !!"))
                if count == 0:
                    raise ValidationError(_("All participants are already added !!"))

    @api.constrains('end_date')
    @api.one
    def _check_date(self):
        start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
        if end_date and start_date:
            if self.intervention_type in ['sales_pitch', 'bbbee']:
                if end_date < start_date:
                    raise ValidationError(_("End date cannot be same or smaller than start date."))
                elif start_date != end_date:
                    raise ValidationError(_('Training must be for 1 day only.'))
            elif self.intervention_type in ['digital_skills']:
                if end_date < start_date:
                    raise ValidationError(_("End date cannot be same or smaller than start date."))

    @api.constrains('trainer_id')
    @api.one
    def _check_trainer(self):
        if self.trainer_id:
            print (self.trainer_id, self.env.user, self.env.user.branch_id, self.trainer_id.branch_id)
            all_trainers = self.env.ref('bmt_training.group_trainer').users.ids
            if self.env.user.id in all_trainers:
                if self.env.user.id != self.trainer_id.id:
                    raise ValidationError(_("You cannot change the trainer !!"))
                if self.env.user.branch_id.id != self.trainer_id.branch_id.id:
                    raise ValidationError(_("You cannot change your branch !!"))

    @api.model
    def create(self, vals):
        res = super(SalesPitchTraining, self).create(vals)
        if res.intervention_type == 'sales_pitch_bbbee':
            ref_number = self.env['ir.sequence'].next_by_code('sb_code') or _('New')
            res.name = ref_number
        elif res.intervention_type == 'sales_pitch':
            ref_number = self.env['ir.sequence'].next_by_code('sp_code') or _('New')
            res.name = ref_number
        elif res.intervention_type == 'bbbee':
            ref_number = self.env['ir.sequence'].next_by_code('be_code') or _('New')
            res.name = ref_number
        elif res.intervention_type == 'job_preparedness':
            ref_number = self.env['ir.sequence'].next_by_code('jp_code') or _('New')
            res.name = ref_number
        elif res.intervention_type == 'life_skills':
            ref_number = self.env['ir.sequence'].next_by_code('ls_code') or _('New')
            res.name = ref_number
        elif res.intervention_type == 'digital_skills':
            ref_number = self.env['ir.sequence'].next_by_code('ds_code') or _('New')
            res.name = ref_number
        return res

    @api.model
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

    @api.model
    def get_end_date(self):
        if self._context.get('default_intervention_type') != 'sales_pitch_bbbee':
            return datetime.date.today()
        else:
            return False

    @api.multi
    @api.onchange('session_1_attendee_ids', 'session_2_attendee_ids', 'session_3_attendee_ids')
    def _onchange_participants_ids(self):
        for rec in self:
            if rec.intervention_type in ['job_preparedness', 'life_skills', 'digital_skills','sales_pitch', 'bbbee']:
                total_attendees = len(rec.session_3_attendee_ids)
                if not rec.max_count <= 0:
                    if total_attendees > rec.max_count:
                        raise UserError(_('Your Participants count has reached max limit. Please do not add more.'))
            elif rec.intervention_type in ['sales_pitch_bbbee']:
                total_attendees = len(rec.session_1_attendee_ids) + len(rec.session_2_attendee_ids)
                if not rec.max_count <= 0:
                    if total_attendees > rec.max_count:
                        raise UserError(_('Your Participants count has reached max limit. Please do not add more.'))

    @api.depends('session_1_attendee_ids', 'session_2_attendee_ids', 'session_3_attendee_ids')
    def calculate_participants(self):
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
        for rec in self:
            if rec.intervention_type in ['job_preparedness', 'life_skills', 'digital_skills','sales_pitch', 'bbbee']:
                rec.total_youth = len(rec.session_3_attendee_ids)
                for single_rec in rec.session_3_attendee_ids:
                    if single_rec.gender == 'male':
                        males += 1
                    if single_rec.gender == 'female':
                        females += 1
                    if single_rec.geographic_location in ['urban', 'peri-urban']:
                        urban += 1
                    if single_rec.geographic_location in ['rural-area-villages', 'rural-area-farms']:
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
                    if single_rec.is_disabled:
                        disabled += 1
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
            elif rec.intervention_type in ['sales_pitch_bbbee']:
                rec.total_youth = len(rec.session_1_attendee_ids) + len(rec.session_2_attendee_ids)
                for single_rec in rec.session_1_attendee_ids:
                    if single_rec.gender == 'male':
                        males += 1
                    if single_rec.gender == 'female':
                        females += 1
                    if single_rec.geographic_location in ['urban', 'peri-urban']:
                        urban += 1
                    if single_rec.geographic_location in ['rural-area-villages', 'rural-area-farms']:
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
                    if single_rec.is_disabled:
                        disabled += 1
                for single_rec in rec.session_2_attendee_ids:
                    if single_rec.gender == 'male':
                        males += 1
                    if single_rec.gender == 'female':
                        females += 1
                    if single_rec.geographic_location in ['urban', 'peri-urban']:
                        urban += 1
                    if single_rec.geographic_location in ['rural-area-villages', 'rural-area-farms']:
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
                    if single_rec.is_disabled:
                        disabled += 1
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

    @api.depends('session_3_attendee_ids')
    def calculate_participants_jld(self):
        for res in self:
            count_len = len(res.session_3_attendee_ids)
            res.total_participants_jld = count_len

    def apply_for_training(self):
        particpant = ''
        for rec in self:
            if rec.state == 'new':
                if not rec.max_count <= 0:
                    if rec.total_youth >= rec.max_count:
                        raise UserError(_('Batch Full !!'))
                current_user_youth_id = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.env.user.id)])
                training_id = self.search([('intervention_type', '=', rec.intervention_type)])
                if rec.intervention_type == 'sales_pitch_bbbee':
                    for training in training_id:
                        for attendees in training.session_1_attendee_ids:
                            if attendees.participant_id.id == current_user_youth_id.id:
                                particpant = True
                                if training.name:
                                    raise UserError(_("You have already applied for the training named '" + training.name + "', so you cant apply for this training."))
                                else:
                                    raise UserError(_(
                                        "You have already applied for the training named, so you cant apply for this training."))
                        for attendees in training.session_2_attendee_ids:
                            if attendees.participant_id.id == current_user_youth_id.id:
                                particpant = True
                                if training.name:
                                    raise UserError(_("You have already applied for the training named '" + training.name + "', so you cant apply for this training."))
                                else:
                                    raise UserError(_(
                                        "You have already applied for the training named, so you cant apply for this training."))
                elif rec.intervention_type in ['job_preparedness', 'life_skills', 'digital_skills', 'sales_pitch',
                                               'bbbee']:
                    for training in training_id:
                        for attendees in training.session_3_attendee_ids:
                            if attendees.participant_id.id == current_user_youth_id.id:
                                particpant = True
                                if training.name:
                                    raise UserError(_("You have already applied for the training named '" + training.name + "', so you cant apply for this training."))
                                else:
                                    raise UserError(_(
                                        "You have already applied for the training named, so you cant apply for this training."))
                training_attendance_id = self.env['training.attendance'].sudo().search([('participant_id', '=', current_user_youth_id.id)])
                # if not particpant and training_attendance_id:
                if rec.intervention_type in ['job_preparedness', 'life_skills', 'digital_skills','sales_pitch', 'bbbee']:
                    all_ben_users = []
                    ben_users = youth = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.env.user.id)])
                    for ben in ben_users:
                        all_ben_users.append(ben.user_id.id)
                    all_trainers_users = self.env.ref('bmt_training.group_trainer').users.ids
                    if not self.env.user.id in all_ben_users and not self.env.user.id in all_trainers_users:
                        raise UserError(_("Only registered beneficiaries can apply to this course !!"))
                    elif self.env.user.id in all_ben_users:
                        youth = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.env.user.id)])
                        training_participants = self.env['training.attendance'].sudo().create({
                            'participant_id': youth.id,
                            'gender': youth.gender,
                            'geographic_location': youth.geographic_location,
                            'is_disabled': youth.gender,
                            'race': youth.population_group,
                            'physical_address': youth.physical_address,
                            'contact_number': youth.cell_phone_number,
                            'sp_training_id_3': rec.id
                        })
                    elif self.env.user.id in all_trainers_users:
                        action = {
                            'type': 'ir.actions.act_window',
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_model': 'sales.pitch.training',
                            'target': 'current',
                            'res_id': rec.id,
                            'flags': {'initial_mode': 'edit'},
                            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
                        }
                        return action
                elif rec.intervention_type in ['sales_pitch_bbbee']:
                    all_ben_users = self.env.ref('client_management.group_branch_beneficiary').users.ids
                    all_trainers_users = self.env.ref('bmt_training.group_trainer').users.ids
                    if not self.env.user.id in all_ben_users and not self.env.user.id in all_trainers_users:
                        raise UserError(_("Only beneficiaries or trainers can apply to this course !!"))
                    elif self.env.user.id in all_ben_users:
                        youth = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.env.user.id)])
                        training_participants_1 = self.env['training.attendance'].sudo().create({
                            'participant_id': youth.id,
                            'gender': youth.gender,
                            'geographic_location': youth.geographic_location,
                            'is_disabled': youth.gender,
                            'race': youth.population_group,
                            'physical_address': youth.physical_address,
                            'contact_number': youth.cell_phone_number,
                            'sp_training_id': rec.id
                        })
                    elif self.env.user.id in all_trainers_users:
                        action = {
                            'type': 'ir.actions.act_window',
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_model': 'sales.pitch.training',
                            'target': 'current',
                            'res_id': rec.id,
                            'flags': {'initial_mode': 'edit'},
                            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
                        }
                        return action
                # else:
                #     raise UserError(
                #         _("You can only apply to one training at a time !!"))
            else:
                raise UserError(_("You cannot apply for these training as batch is confirmed !!"))

    def view_edit_training(self):
        for record in self:
            action = {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sales.pitch.training',
                'target': 'current',
                'res_id': record.id,
                'flags': {'initial_mode': 'edit'},
                'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
            }
            return action

    @api.model
    def get_attendance_data(self):
        single_attendees = []
        for attendees in self.session_3_attendee_ids:
            single_attendees.append(attendees)
        return single_attendees

    @api.model
    def get_first_attendance_data(self):
        session_one_attendees = []
        for first_attendees in self.session_1_attendee_ids:
            session_one_attendees.append(first_attendees)
        return session_one_attendees

    @api.model
    def get_second_attendance_data(self):
        session_two_attendees = []
        for second_attendees in self.session_2_attendee_ids:
            session_two_attendees.append(second_attendees)
        return session_two_attendees

    @api.multi
    def get_attendance_register(self):
        if self.intervention_type in ['job_preparedness', 'life_skills', 'digital_skills','sales_pitch', 'bbbee']:
            return self.env.ref('bmt_training.action_report_attendance_registerr').report_action(self)
        elif self.intervention_type in ['sales_pitch_bbbee']:
            return self.env.ref('bmt_training.action_report_multiple_attendance_registerr').report_action(self)

    def start_training(self):
        self.state = 'start_training'

    def end_training(self):
        self.state = 'end_training'

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
        mail_template = self.env.ref('bmt_training.sale_pitch_training_email_template')
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
        mail_template = self.env.ref('bmt_training.sale_pitch_training_email_template')
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
        mail_template = self.env.ref('bmt_training.sale_pitch_training_email_template')
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
        mail_template = self.env.ref('bmt_training.sale_pitch_training_email_template')
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
