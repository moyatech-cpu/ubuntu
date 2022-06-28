# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class BmtTrainingApplication(models.Model):
    _name = 'bmt.training.application'
    _rec_name = 'participant_name'
    _description = 'BMT Training Application'

    pddd_training_id = fields.Many2one('pddd.training', string="PDDD Training")
    # participant_name = fields.Char(string='Participant Name')
    participant_name = fields.Many2one('youth.enquiry', string='Participant Name', default=lambda self: self.default_participant())
    participant_surname = fields.Char(string='Participant Surname', related="participant_name.surname")
    physical_address = fields.Text(string="Physical Address", related="participant_name.physical_address")
    telephone_number = fields.Char(string="Telephone Number")
    cellphone_number = fields.Char(string="Cellphone Number", related="participant_name.cell_phone_number")
    email_address = fields.Char(string="E-mail Address", related="participant_name.email")
    branch_id = fields.Many2one('res.branch', string="Branch", related="participant_name.nearest_branch")
    south_african_identity_number = fields.Char(string="ID Number(Age should be 18-35)", related="participant_name.id_number")
    age = fields.Integer(string="Age")
    race = fields.Selection(
        [('asian', 'Asian'), ('african', 'African'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Race", related="participant_name.population_group")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", related="participant_name.gender")
    employment_status = fields.Selection([('yes','Yes'), ('no', 'No')],string="Are you currently employed ?")
    disability_status = fields.Selection([('yes','Yes'), ('no', 'No')],string="Disabled ?")
    highest_standard_of_education_completed = fields.Selection([('secondary', 'Secondary'), ('tertiary', 'Tertiary')],
                                                               string="Highest Standard Of Education Completed")
    home_language = fields.Selection([('sepedi','Sepedi'),('sesotho', 'Sesotho'), ('setswana','Setswana'), ('siswati','siSwati'),
                                      ('tshivenda', 'Tshivenda'), ('xitsonga', 'Xitsonga'), ('afrikaans','Afrikaans'),
                                      ('english', 'English'), ('isindebele','isiNdebele'), ('isixhosa', 'isiXhosa'),
                                      ('isizulu','isiZulu')],string="Home Language")
    read_write_english = fields.Selection([('good', 'Good'), ('not_good', 'Not Good')], string="Can you read and write in english ?")
    please_explain_english = fields.Text(string="Please Explain")
    simple_calculations = fields.Selection([('yes','Yes'), ('no','No')], string="Can you do simple Calculations ?")
    please_explain_simple_calculations = fields.Text(string="Please Explain")
    attended_bus_mgmt_skills = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                string="Attended any business or management skills training before ?")
    bus_mgmt_skills_days = fields.Integer(string="What was the duration in days ?")
    attended_tech_voc_skills = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                string="Have you attended any techincal or vocational skills training before ?")
    tech_voc_skills_days = fields.Integer(string="What was the duration in days ?")
    current_occupation_employment = fields.Selection([('public_sector_employed', 'Are you employed in public sector'),
                                                      ('private_sector_employed', 'Are you employed in private sector'),
                                                      ('unemployed', 'Unemployed')],
                                                     string="What is your current occupation/Employment status")
    employment_type = fields.Selection([('full_time', 'Full Time'), ('part_time', 'Part Time')],
                                              string="Employment Type")
    # private_sector_employed = fields.Selection([('full_time', 'Full Time'), ('part_time', 'Part Time')],
    #                                           string="Are you employed in public sector ?")
    # are_you_unemployed = fields.Boolean(string="Are you unemployed ?")
    average_income = fields.Selection(
        [('z_five', 'R 0 to R 5000'), ('five_ten', 'R 5001 to R 10000'), ('ten_twenty', 'R 10001 to R 20000'),
         ('mt_twenty', 'More Than R 20000')], string="Average Monthly Family Income")
    not_in_business = fields.Boolean(string="Not in business")
    operating_informal_business = fields.Boolean(string="Operating An Informal Business")
    operating_formal_business = fields.Boolean(string="Operating A Formal Business")
    tested_bus_idea = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                       string="Do you have a tested and feasible Business Idea ?")
    describe_bus_idea = fields.Text(string="Describe Business Idea")
    reason_to_start_business = fields.Text(string="Why do you want to start business ?")
    when_to_start_business = fields.Selection(
        [('within_3_months', 'Within in 3 months'), ('within_6_months', 'Within in 6 months'),
         ('within_1_year', 'Within in 1 year'), ('after_1_year', 'After 1 year')],
        string="When do you intend to start the business ?")
    relevant_tech_skills = fields.Selection([('yes', 'Yes'), ('no', 'No')],
        string="For the business you intend to start, do you have the relevant technical skills ?")
    funding_required = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string="Do you require funding to start your business ?")
    name_of_business = fields.Char(string="Name Of Business")
    current_business_activities = fields.Text(string="Describe your current business activities ?")
    product_type_services = fields.Text(string="What type of products and services does the business offer")
    current_business_line = fields.Selection(
        [('retail', 'Retail'), ('serv_operation', 'Service Operation'), ('wholesale', 'Wholesale'),
         ('manufacturing', 'Manufacturing'), ('agriculture', 'Agriculture'), ('other', 'Other')],
        string="What sector is your business currently operating ?")
    business_line_specify = fields.Text(string="Specify your business line")
    is_business_registered = fields.Boolean(string="Is Your Business Formally Registered ?")
    is_business_not_registered = fields.Boolean(string="Is Your Business is not Formally Registered ?")
    business_type = fields.Selection(
        [('sole_propritor', 'Sole Proprietor'), ('closed_corporation', 'Closed Corporation'),
         ('private_company', 'Private Company'), ('cooperative', 'Co-operative'), ('ngo_npo', 'NGO/NPO'),
         ('other', 'Other')], string="What are your business registered as ?")
    other_business_type = fields.Text(string="Specify Business Type")
    comm_viable_business = fields.Selection([('yes', 'Yes'), ('not_sure', 'Not Sure'), ('no', 'No')],
                                            string="Is your business commercially viable at the moment?")
    why_not_comm_viable = fields.Text(string="Please explain why not commercially viable")
    business_position = fields.Selection(
        [('owner_manager', 'Owner/Manager'), ('partner_director_member', 'Partner/Director/Member'),
         ('employee', 'Employee')], string="Position in the Business")
    percentage_ownership = fields.Integer(string="Percentage Ownership %")
    daily_customers = fields.Selection([('lt_ten', 'Less Than 10'), ('bet_ten_and_twenty', 'Between ten and twenty'),
                                        ('mt_twenty', 'More than twenty'), ('not_sure', 'I don’t know / Not sure')],
                                       string="How many daily customers does your business have ?")
    future_business_plans = fields.Selection([('remain_in', 'Remain in / Strengthen / Expand the same business'), (
        'start_new', 'Start new business activities in addition to the existing business'),
                                              ('replace_business', 'Start a new business to replace the old business'),
                                              ('dont_know', 'Don’t know / Don’t have any plans'), ('other', 'Other')],
                                             string="What are your plans for the business in the future ?")
    business_started = fields.Selection(
        [('lt_one_year', 'Less than 1 year ago'), ('mt_one_year', 'More than 1 year ago')],
        string="When was the business started ?")
    how_long = fields.Integer(string="How long is your business running ?")
    avg_daily_sales = fields.Selection(
        [('lt_thousand', 'Less Than R 1000'), ('bet_thousand_and_five', 'Between R 1000 and R 5000'),
         ('mt_five', 'More than R 5000'), ('not_sure', 'I don’t know / Not sure')],
        string="What is the value of your average daily sales? Rands?")
    emp_part_time = fields.Integer(string="Employees(Part Time)")
    emp_full_time = fields.Integer(string="Employees(Full Time)")
    sars_registrations = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                          string="Is your business compliant in terms of SARS registrations")
    dol_registrations = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                         string="Is your business compliant in terms of DOL registrations")
    more_than_one_business = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                              string="Do you personally own more than one business ?")
    business_number = fields.Integer(string="Please specify number")
    what_business = fields.Text(string="What type of business")
    interest_in_other_business = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                  string="Do you have interests in any other business ?")
    other_interest_numbers = fields.Integer(string="Please Specify Number")
    what_business_other = fields.Text(string="What type of business")

    business_funded_before = fields.Selection([('yes', 'Yes'), ('no','No')],
                                              string="Has the business been funded before")
    business_funded_by = fields.Selection(
        [('gov', 'Government'), ('banks', 'banks'), ('grants', 'Grants'), ('private_sector', 'Private Sector'),
         ('nat_int_donors', 'National/ International donors'), ('other', 'Other')],
        string="Business funded by")
    business_funded_before_others = fields.Text(string="Others")
    diff_costs = fields.Text(
        string="Please list all the different types of Costs one should consider when calculating the total cost of your product/ Service")
    business_plan = fields.Text(string="Describe the main components of your business plan")
    marketing_plan = fields.Text(string="Describe the main components of your marketing plan")
    emp_benifits = fields.Text(string="List the different types of employee benefits you know")
    safe_healthy_environment = fields.Text(string="What constitutes a safe and healthy work environment")
    learning_expectation = fields.Text(string="What do you expect to learn from the training ?")
    participant_signature = fields.Binary(string="Participant Signature")
    signature_date = fields.Datetime(string="Signature Date")
    course_start_date = fields.Datetime(string="Start Date",
                                        related="bmt_id.start_date")
    course_end_date = fields.Datetime(string="End Date",
                                        related="bmt_id.end_date")
    course_trainer_id = fields.Many2one('res.users', string="Trainer",
                                         domain=lambda self: [
                                            ("groups_id", "=", self.env.ref("bmt_training.group_trainer").id)],
                                        related="bmt_id.facilitator_id")
    training_type = fields.Selection(
        [('gyb', 'GYB - 3 days'), ('syb', 'SYB - 5 days'),
         ('iyb_one', 'IYB 1 - 5 days'),
         ('iyb_two', 'IYB 2 - 5 days'), ('syb_coops', 'SYB/Co-ops - 3 days')],
        string="Training course",related="bmt_id.training_type")
    assessed_by_id = fields.Many2one('res.users', string="Assessed By")
    assessement_date = fields.Datetime(string="Assessement Date")
    part_ref_number = fields.Char(string="Participant Reference Number")
    youth_enquiry_id = fields.Many2one('youth.enquiry', string="Youth Enquiry", related="participant_name")
    bmt_id = fields.Many2one('business.mgmt.training', string="Business Management Training")
    is_trainee_confirm = fields.Boolean(string="Is Trainee Confirm")
    is_trainer = fields.Boolean(string="Is Trainer", compute="check_is_trainer")
    is_accepted = fields.Boolean(string="I Accept", default=True)
    # benificiary_bmt_id = fields.Many2one('business.mgmt.training', string="BMT Training")
    # benificiary_bmt_start_date = fields.Datetime(string="Start Date", related="benificiary_bmt_id.start_date")
    # benificiary_bmt_end_date = fields.Datetime(string="End Date", related="benificiary_bmt_id.end_date")
    # benificiary_trainer_id = fields.Many2one('res.users',string="Trainer", related="benificiary_bmt_id.facilitator_id")
    # benificiary_training_type = fields.Selection(
    #     [('gyb', 'GYB'), ('syb', 'SYB'), ('iyb', 'IYB'), ('gyb_co_gov', 'GYB/Co-operative Governance')],
    #     string="Training type", related="benificiary_bmt_id.training_type")
    is_benificiary = fields.Boolean(string="Is Benificiary", compute="check_is_benificiary")
    user_id = fields.Many2one('res.users', string="Users", default=lambda self: self.env.user.id)
    # application_submitted = fields.Boolean(string="Application Submitted")

    @api.constrains('is_accepted')
    @api.one
    def is_agreement_accepted(self):
        if not self.is_accepted:
            raise ValidationError(_("Please accept terms and condition !!"))

    @api.multi
    def default_participant(self):
        youth_enquiry = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.env.user.id)])
        if youth_enquiry:
            return youth_enquiry.id

    # def submit_application(self):
    #     print ("\n\n\n\n")
    #     print ("Benificiary BMT ID", self.benificiary_bmt_id)
    #     if self.benificiary_bmt_id:
    #         self.application_submitted =True

    @api.depends('user_id')
    def check_is_benificiary(self):
        for rec in self:
            benificiary = self.env.ref('client_management.group_branch_beneficiary')
            b_list = benificiary.users.ids
            youth_id = self.env['youth.enquiry'].search([('user_id', '=', self.user_id.id)])
            if self.user_id.id in b_list and youth_id:
                rec.is_benificiary = True

    def check_is_trainer(self):
        for rec in self:
            admin = self.env.ref('base.group_system')
            trainer = self.env.ref('bmt_training.group_trainer')
            groups = self.env.user.groups_id.ids
            if trainer.id in groups or admin.id in groups:
                rec.is_trainer = True

    @api.onchange('bmt_id')
    def onchange_business_mgmt_training(self):
        if self.bmt_id.training_type == 'syb_iyb':
            self.training_type = 'syb'
        elif self.bmt_id.training_type == 'gyb_only':
            self.training_type = 'gyb'
        elif self.bmt_id.training_type == 'gyb_co_gov':
            self.training_type = 'gyb_co_gov'
        elif not self.bmt_id:
            self.training_type = ''

    def confirm_trainee(self):
        mail_template_id = self.env.ref('bmt_training.bmt_training_application_mail_template')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)
        birth_date = ''
        if self.bmt_id and self.youth_enquiry_id:
            print (len(self.bmt_id.bmt_participants_ids.ids))
            if self.youth_enquiry_id.id_number:
                try:
                    if int(self.youth_enquiry_id.id_number[:2]) < 50:
                        date = "20" + self.youth_enquiry_id.id_number[:2] + "-" + self.youth_enquiry_id.id_number[
                                                                                  2:4] + "-" + self.youth_enquiry_id.id_number[
                                                                                               4:6]
                        self.dob = datetime.strptime(date, '%Y-%m-%d').date()
                    else:
                        date = "19" + self.youth_enquiry_id.id_number[:2] + "-" + self.youth_enquiry_id.id_number[
                                                                                  2:4] + "-" + self.youth_enquiry_id.id_number[
                                                                                               4:6]
                        birth_date = datetime.strptime(date, '%Y-%m-%d').date()
                except Exception:
                    raise UserError(_('You are not on our age group'))
            if not len(self.bmt_id.bmt_participants_ids.ids) >= 40:
                participant_record = self.env['bmt.participants'].create({
                    'participant_id': self.youth_enquiry_id.id,
                    'dob': birth_date,
                    'gender': self.youth_enquiry_id.gender,
                    'area': self.youth_enquiry_id.geographic_location,
                    'race': self.youth_enquiry_id.population_group,
                    'mobile': self.youth_enquiry_id.cell_phone_number,
                    'business_mgmt_training_id': self.bmt_id.id,
                    'bmt_training_app_id': self.id
                })
                if participant_record:
                    self.is_trainee_confirm = True
                    return True
            else:
                training = self.bmt_id.copy()
                participant_record = self.env['bmt.participants'].create({
                    'participant_id': self.youth_enquiry_id.id,
                    'dob': birth_date,
                    'gender': self.youth_enquiry_id.gender,
                    'area': self.youth_enquiry_id.geographic_location,
                    'race': self.youth_enquiry_id.population_group,
                    'mobile': self.youth_enquiry_id.cell_phone_number,
                    'business_mgmt_training_id': training.id,
                    'bmt_training_app_id': self.id
                })
                self.bmt_id = training.id
                if participant_record and training:
                    self.is_trainee_confirm = True
                    return True

    @api.model
    def create(self, vals):
        res = super(BmtTrainingApplication, self).create(vals)
        if res.training_type:
            if res.training_type == 'gyb':
                if not res.part_ref_number:
                    ref_number = self.env['ir.sequence'].next_by_code('bmt_syb') or _('New')
                    res.part_ref_number = ref_number
            if res.training_type == 'syb':
                if not res.part_ref_number:
                    ref_number = self.env['ir.sequence'].next_by_code('bmt_syb') or _('New')
                    res.part_ref_number = ref_number
            if res.training_type == 'iyb':
                if not res.part_ref_number:
                    ref_number = self.env['ir.sequence'].next_by_code('bmt_syb') or _('New')
                    res.part_ref_number = ref_number
        mail_template = self.env.ref('bmt_training.benificiary_bmt_training_application_mail_template')
        print ("Mail Template ", mail_template)
        mail_template.send_mail(res.id, force_send=True,
                                email_values={
                                    'email_from': res.user_id.company_id.email,
                                    'email_to': res.email_address
                                })
        # youth_enquiry = self.env['youth.enquiry'].create({
        #     'gender': res.gender,
        #     'name': res.participant_name,
        #     'surname': res.participant_surname,
        #     'email': res.email_address,
        #     'cell_phone_number': res.cellphone_number,
        #     'id_number': res.south_african_identity_number,
        #     'nearest_branch': res.branch_id.id,
        #     'physical_address': res.physical_address,
        #     'population_group': res.race,
        #     'alternative_number': res.telephone_number
        # })
        if int(res.south_african_identity_number[:2]) < 50:
            date = "20" + res.south_african_identity_number[:2] + "-" + res.south_african_identity_number[
                                                                         2:4] + "-" + res.south_african_identity_number[
                                                                                      4:6]
            birth_date = datetime.strptime(date, '%Y-%m-%d')
        else:
            date = "19" + res.south_african_identity_number[:2] + "-" + res.south_african_identity_number[
                                                                         2:4] + "-" + res.south_african_identity_number[
                                                                                      4:6]
            birth_date = datetime.strptime(date, '%Y-%m-%d')
        # youth_enquiry.team_id = self.env.ref('client_management.team_bmt')
        # youth_enquiry.state = 'accepted'
        # res.youth_enquiry_id = youth_enquiry.id
        # if 'bmt_id' in vals and res.bmt_id:
        #     bmt_participants = self.env['bmt.participants'].create({
        #         'participant_id': res.youth_enquiry_id.id,
        #         'dob': birth_date,
        #         'gender': res.youth_enquiry_id.gender,
        #         'area': res.youth_enquiry_id.geographic_location,
        #         'race': res.youth_enquiry_id.population_group,
        #         'mobile': res.youth_enquiry_id.cell_phone_number,
        #         'business_mgmt_training_id': res.bmt_id.id,
        #         'bmt_training_app_id': res.id
        #     })
        return res

    def thank_you(self):
        if self.env.ref('client_management.group_branch_beneficiary').id in self.env.user.groups_id.ids:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            end_url = '/thank_you'
            full_url = base_url + end_url
            print ("\n\n\nURL", full_url)
            return {
                'name': "Thank you",
                'res_model': 'ir.actions.act_url',
                'type': 'ir.actions.act_url',
                'target': 'self',
                'url': full_url,
            }

    @api.multi
    def write(self, vals):
        if 'bmt_id' in vals:
            bmt_part_old = self.env['bmt.participants'].search([('bmt_training_app_id', '=', self.id)])
            bmt_part_old.unlink()
        res = super(BmtTrainingApplication, self).write(vals)
        print ("\n\n\n\nwrite called")
        if self.training_type:
            if self.training_type == 'gyb':
                if not self.part_ref_number:
                    ref_number = self.env['ir.sequence'].next_by_code('bmt_gyb') or _('New')
                    self.part_ref_number = ref_number
            if self.training_type == 'syb':
                if not self.part_ref_number:
                    ref_number = self.env['ir.sequence'].next_by_code('bmt_syb') or _('New')
                    self.part_ref_number = ref_number
            if self.training_type == 'iyb_one':
                if not self.part_ref_number:
                    ref_number = self.env['ir.sequence'].next_by_code('bmt_iyb') or _('New')
                    self.part_ref_number = ref_number
            if self.training_type == 'iyb_two':
                if not self.part_ref_number:
                    ref_number = self.env['ir.sequence'].next_by_code('bmt_iyb_two') or _('New')
                    self.part_ref_number = ref_number
        if int(self.south_african_identity_number[:2]) < 50:
            date = "20" + self.south_african_identity_number[:2] + "-" + self.south_african_identity_number[
                                                                         2:4] + "-" + self.south_african_identity_number[
                                                                                      4:6]
            birth_date = datetime.strptime(date, '%Y-%m-%d')
        else:
            date = "19" + self.south_african_identity_number[:2] + "-" + self.south_african_identity_number[
                                                                         2:4] + "-" + self.south_african_identity_number[
                                                                                      4:6]
            birth_date = datetime.strptime(date, '%Y-%m-%d')
        # if 'bmt_id' in vals and self.bmt_id:
        #     bmt_participants = self.env['bmt.participants'].create({
        #         'participant_id': self.youth_enquiry_id.id,
        #         'dob': birth_date,
        #         'gender': self.youth_enquiry_id.gender,
        #         'area': self.youth_enquiry_id.geographic_location,
        #         'race': self.youth_enquiry_id.population_group,
        #         'mobile': self.youth_enquiry_id.cell_phone_number,
        #         'business_mgmt_training_id': self.bmt_id.id,
        #         'bmt_training_app_id': self.id
        #     })
        return res

    @api.onchange('not_in_business')
    def onchange_not_in_business(self):
        if self.not_in_business:
            self.operating_informal_business = False
            self.operating_formal_business = False

    @api.onchange('operating_informal_business')
    def onchange_operating_informal_business(self):
        if self.operating_informal_business:
            self.not_in_business = False
            self.operating_formal_business = False

    @api.onchange('operating_formal_business')
    def onchange_operating_formal_business(self):
        if self.operating_formal_business:
            self.not_in_business = False
            self.operating_informal_business = False

    @api.onchange('south_african_identity_number')
    def onchange_id(self):
        if self.south_african_identity_number:
            try:
                if int(self.south_african_identity_number[:2]) < 50:
                    date = "20" + self.south_african_identity_number[:2] + "-" + self.south_african_identity_number[2:4] + "-" + self.south_african_identity_number[4:6]
                    diff = datetime.now() - datetime.strptime(date, '%Y-%m-%d')
                    years = diff.days / 365
                    if int(years) >= 36 or int(years) <= 17:
                        self.south_african_identity_number = None
                        self.age = None
                    elif int(years) <= 36 and int(years) >= 17:
                        self.age = int(years)
                else:
                    date = "19" + self.south_african_identity_number[:2] + "-" + self.south_african_identity_number[2:4] + "-" + self.south_african_identity_number[4:6]
                    diff = datetime.now() - datetime.strptime(date, '%Y-%m-%d')
                    years = diff.days / 365
                    if int(years) >= 36 or int(years) <= 17:
                        self.south_african_identity_number = None
                        self.age = None
                    elif int(years) <= 36 and int(years) >= 17:
                        self.age = int(years)
            except Exception:
                self.south_african_identity_number = None
                self.age = None
