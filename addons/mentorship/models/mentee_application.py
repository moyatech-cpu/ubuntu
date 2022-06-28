# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class MenteeApplication(models.Model):
    _name = 'mentee.application'
    _rec_name = 'firstName'
    _description = 'Mentee Application Form'

    state = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('reject', 'Rejected'),
    ], string='Application Status', default='new')
    reject_reason = fields.Text('Reason for Rejection')
    surname = fields.Char(string='Surname')
    firstName = fields.Char(string='First Name')
    saiDentityNumber = fields.Char(string='SA Identity Number')
    dateOfBirth = fields.Date(string='Date of birth')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('not_specify', 'Not Specify')], string="Gender")
    # populationGroup = fields.Char(string="Population Group")
    populationGroup = fields.Selection(
        [('african', 'African'), ('asian', 'Asian'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Population Group")
    homeTelephoneNumber = fields.Char(string='Home Telephone Number')
    mobile = fields.Char(string='Mobile')
    fax = fields.Char(string='Fax')
    email = fields.Char(string='E-mail')
    physical_street = fields.Char(related='')
    physical_street2 = fields.Char(related='')
    physical_zip = fields.Char(related='')
    physical_city = fields.Char(related='')
    physical_state_id = fields.Many2one("res.country.state", string='State',
                                        domain="[('country_id.name', '=', 'South Africa')]")
    postal_street = fields.Char(related='')
    postal_street2 = fields.Char(related='')
    postal_zip = fields.Char(related='')
    postal_city = fields.Char(related='')
    postal_state_id = fields.Many2one("res.country.state", string='State',
                                      domain="[('country_id.name', '=', 'South Africa')]")
    typeOfLocation = fields.Selection([('rural', 'Rural'), ('urban', 'Urban'), ('peri_urban', 'Peri-urban'),
                                       ('informal_settlement', 'Informal Settlement')], string="Type of location")
    disabledPerson = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Are you a disabled person?')
    describeDisability = fields.Text(string='If yes, please describe your disability')
    # referenceOne
    refNameOne = fields.Char(string='Name')
    refTelOne = fields.Char(string='Tel')
    refRelationshipOne = fields.Char(string='Relationship')
    # referenceTwo
    refNameTwo = fields.Char(string='Name')
    refTelTwo = fields.Char(string='Tel')
    refRelationshipTwo = fields.Char(string='Relationship')
    mentorshipService = fields.Text(string='How did you hear about this mentorship service?')
    nydaFundedServices = fields.Text(
        string='Have you benefited from any NYDA funded services before? If Yes Please specify')
    businessName = fields.Char(string='Business Name')
    yearEstablished = fields.Char(string='Year Established')
    legalEntity = fields.Many2many('legal.entity', string='Legal Entity')
    legalEntityBool = fields.Boolean(string='Legal Entity Bool')
    legalEntityChar = fields.Char(string='Other then above')
    registrationNumber = fields.Char(string='Registration Number:')
    vatRegistrationNumber = fields.Char(string='VAT Registration Number')
    setaNumber = fields.Char(string='SETA Number')
    BEEShareholding = fields.Char(string='% of BEE Shareholding(in %)')
    SectorIndustry = fields.Char(string='Sector/Industry')
    business_street = fields.Char(related='')
    business_street2 = fields.Char(related='')
    business_zip = fields.Char(related='')
    business_city = fields.Char(related='')
    business_state_id = fields.Many2one("res.country.state", string='State',
                                        domain="[('country_id.name', '=', 'South Africa')]")
    business_country_id = fields.Many2one('res.country', string='Country', related='')
    business_postal_street = fields.Char(related='')
    business_postal_street2 = fields.Char(related='')
    business_postal_zip = fields.Char(related='')
    business_postal_city = fields.Char(related='')
    business_postal_state_id = fields.Many2one("res.country.state", string='State',
                                               domain="[('country_id.name', '=', 'South Africa')]")
    business_postal_country_id = fields.Many2one('res.country', string='Country', related='')
    businessTelephone = fields.Char(string='Business Telephone')
    businessFax = fields.Char(string='Business Fax')
    businessEmail = fields.Char(string='Business Email')
    webAddress = fields.Char(string='Web Address')
    averageAnnualTurnover = fields.Char(string='Average Annual Turnover(R)')
    financialYear = fields.Char(string='Profit in the last financial year(R)')
    numberOfEmployees = fields.Char(string='Number of Employees')
    totalAssetValue = fields.Char(string='Total Asset Value(R)')
    brieflyDescribeYourBusiness = fields.Text(string='Briefly describe your business')
    proposedBusinessName = fields.Char(string='Proposed Business Name')
    proposedStartDate = fields.Char(string='Proposed Start Date')
    slegalEntity = fields.Many2many('legal.entity', 'legal_entity_mentee_apllication_rel', 'slegal_entity_id',
                                    'legal_entity_id', string='Legal Entity')
    slegalEntityBool = fields.Boolean(string='Legal Entity Bool')
    slegalEntityChar = fields.Char(string='Other then above')
    sBEEShareholding = fields.Char(string='% of BEE Shareholding(in %)')
    sector = fields.Many2many("mentor.sectors", string="Sectors")
    proposedBusiness = fields.Text(string='Briefly explain your proposed business')
    startThisBusiness = fields.Text(string='Why do you want to start this business?')
    personalGoals = fields.Text(string='Personal Goals')
    areasSupport = fields.Many2many('areas.support',
                                    string='Please indicate the areas you would like to be supported on')
    areasSupportBool = fields.Boolean(string='Areas Support Bool')
    areasSupportChar = fields.Char(string='Other then above')
    mentoringSupport = fields.Many2many('mentoring.support',
                                        string='Please indicate the form of mentoring support you are interested in')
    mentorshipProgramme = fields.Text(
        string='How do you see this mentorship programme assist you to \
        achieve your business and personal goals? Explain:')
    courseOne = fields.Char(string='courseOne')
    skillsTraining_ids = fields.One2many('skills.training', 'menteeApplication_id', string='skills training')
    experienceInManagingABusiness = fields.Text(string='experience in managing a business')
    highestStandardPassed = fields.Selection([('below8', 'Below 8'),
                                              ('grade9', 'Grade 9'),
                                              ('grade10', 'Grade 10'),
                                              ('grade11', 'Grade 11'),
                                              ('grade12', 'Grade 12 (Matric)')]
                                             , string='Highest Standard Passed')
    Qualifications = fields.Char(string='Qualifications (if any)')
    motivation_ids = fields.One2many('motivation', 'menteeApplication_id', string='motivation ids')
    signature = fields.Binary(string='SIGNATURE')
    dateTime_application = fields.Date(string='Date', default=date.today())
    user_id = fields.Many2one('res.users', string='User ID')
    branch_id = fields.Many2one('res.branch', string="Nearest Branch")
    attachment_id = fields.Binary(string='Upload ID copy')
    attachment_name = fields.Char(string='Upload ID copy')
    is_assigned = fields.Boolean('Matched', default=False)

    @api.model
    def default_get(self, fields):
        result = super(MenteeApplication, self).default_get(fields)
        user = self.env['youth.enquiry'].sudo().search([('email', '=', self.env.user.login)], limit=1, order="id desc")
        result.update({
            'firstName': user.name,
            'surname': user.surname,
            'gender': user.gender,
            'email': user.email,
            'mobile': user.cell_phone_number,
            'physical_street': user.physical_address,
            'saiDentityNumber': user.id_number,
            'physical_state_id': user.province.id,
            'branch_id': user.nearest_branch.id,

        })
        return result

    #validation for south_african_id number
    @api.onchange('saiDentityNumber')
    def onchange_of_saiDentityNumber(self):
        if self.saiDentityNumber:
            try:
                if int(self.saiDentityNumber[:2]) < 50:
                    date = "20" + self.saiDentityNumber[:2] + "-" + self.saiDentityNumber[2:4] + "-" \
                           + self.saiDentityNumber[4:6]
                    b_date = datetime.strptime(date, '%Y-%m-%d')
                    temp_date = datetime.today().strftime('%Y-%m-%d')
                    current_date = datetime.strptime(temp_date, '%Y-%m-%d')
                    difference_in_years = relativedelta(current_date, b_date).years
                    if difference_in_years < 14 or difference_in_years > 35:
                        raise UserError(_('You are not on our age group'))
                else:
                    date = "19" + self.saiDentityNumber[:2] + "-" + self.saiDentityNumber[2:4] + "-" \
                           + self.saiDentityNumber[4:6]
                    b_date = datetime.strptime(date, '%Y-%m-%d')
                    temp_date = datetime.today().strftime('%Y-%m-%d')
                    current_date = datetime.strptime(temp_date, '%Y-%m-%d')
                    difference_in_years = relativedelta(current_date, b_date).years
                    if difference_in_years < 14 or difference_in_years > 34:
                        raise UserError(_('You are not on our age group'))
            except Exception:
                raise UserError(_('You are not on our age group'))

    # validation for mobile field
    @api.onchange('mobile')
    def onchange_of_mobile(self):
        if self.mobile:
            if self.mobile.isdigit():
                if len(self.mobile) != 10:
                    raise UserError(_('Number Must be 10 digits'))
            else:
                raise UserError(_("Phone number should only contain digits."))

    # validation for telephone field
    @ api.onchange('homeTelephoneNumber')
    def onchange_of_homeTelephoneNumber(self):
        if self.homeTelephoneNumber:
            if self.homeTelephoneNumber.isdigit():
                if len(self.homeTelephoneNumber) != 10:
                    raise UserError(_('Number Must be 10 digits'))
            else:
                raise UserError(_("Phone number should only contain digits."))

    @api.onchange('email')
    def onchange_email(self):
        """ Email validation """
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if self.email:
            if not re.search(regex, self.email):
                raise UserError(_("Please Enter valid email address."))

    # report function
    @api.multi
    def _get_legalEntity_value(self):
        res = []
        vals = {}
        for rec in self.legalEntity:
            if rec:
                if rec.name == 'Close':
                    vals.update({'Close': True})
                if rec.name == 'PTY':
                    vals.update({'PTY': True})
                if rec.name == 'Co-ops':
                    vals.update({'Co_ops': True})
                if rec.name == 'Other':
                    vals.update({'Other': True})

        if not vals.get('Close'):
            vals.update({'Close': False})
        if not vals.get('PTY'):
            vals.update({'PTY': False})
        if not vals.get('Co_ops'):
            vals.update({'Co_ops': False})
        if not vals.get('Other'):
            vals.update({'Other': False})
        res.append(vals)
        return res

    # report function
    @api.multi
    def _get_slegalEntity_value(self):
        res = []
        vals = {}
        for rec in self.slegalEntity:
            if rec:
                if rec.name == 'Close':
                    vals.update({'Close': True})
                if rec.name == 'PTY':
                    vals.update({'PTY': True})
                if rec.name == 'Co-ops':
                    vals.update({'Co_ops': True})
                if rec.name == 'Other':
                    vals.update({'Other': True})

        if not vals.get('Close'):
            vals.update({'Close': False})
        if not vals.get('PTY'):
            vals.update({'PTY': False})
        if not vals.get('Co_ops'):
            vals.update({'Co_ops': False})
        if not vals.get('Other'):
            vals.update({'Other': False})
        res.append(vals)
        return res

    # report function
    @api.multi
    def _get_saiDentityNumber_value(self):
        res = []
        for rec in self:
            if rec.saiDentityNumber:
                list_of_number = [int(x) for x in str(rec.saiDentityNumber)]
                for list_number in list_of_number:
                    res.append({'saiDentityNumbe': list_number})
            else:
                return False
        return res

    # report function
    @api.multi
    def _get_areasSupport_value(self):
        res = []
        vals = {}
        for rec in self.areasSupport:
            if rec:
                if rec.name == 'Financial Management':
                    vals.update({'Financial_Management': True})
                if rec.name == 'Technology: Needs Assessment':
                    vals.update({'Technology_Needs_Assessment': True})
                if rec.name == 'Business Strategy':
                    vals.update({'Business_Strategy': True})
                if rec.name == 'Marketing and Sales':
                    vals.update({'Marketing_and_Sales': True})
                if rec.name == 'HR and IR':
                    vals.update({'HR_and_IR': True})
                if rec.name == 'Admin and General Management':
                    vals.update({'Admin_and_General_Management': True})
                if rec.name == 'Tax and Auditing':
                    vals.update({'Tax_and_Auditing': True})
                if rec.name == 'Legal Advice and Commercial Law':
                    vals.update({'Legal_Advice_and_Commercial_Law': True})
                if rec.name == 'Other':
                    vals.update({'Other': True})

        if not vals.get('Financial_Management'):
            vals.update({'Financial_Management': False})
        if not vals.get('Technology_Needs_Assessment'):
            vals.update({'Technology_Needs_Assessment': False})
        if not vals.get('Business_Strategy'):
            vals.update({'Business_Strategy': False})
        if not vals.get('Marketing_and_Sales'):
            vals.update({'Marketing_and_Sales': False})
        if not vals.get('HR_and_IR'):
            vals.update({'HR_and_IR': False})
        if not vals.get('Admin_and_General_Management'):
            vals.update({'Admin_and_General_Management': False})
        if not vals.get('Tax_and_Auditing'):
            vals.update({'Tax_and_Auditing': False})
        if not vals.get('Legal_Advice_and_Commercial_Law'):
            vals.update({'Legal_Advice_and_Commercial_Law': False})
        if not vals.get('Other'):
            vals.update({'Other': False})
        res.append(vals)
        return res

    # report function
    @api.multi
    def _get_mentoringSupport_value(self):
        res = []
        vals = {}
        for rec in self.mentoringSupport:
            if rec:
                if rec.name == 'One-on-One Mentoring':
                    vals.update({'One_on_One_Mentoring': True})
                if rec.name == 'Specialist Mentoring':
                    vals.update({'Specialist_Mentoring': True})
                if rec.name == 'Group Mentoring':
                    vals.update({'Group_Mentoring': True})
                if rec.name == 'Peer Mentoring':
                    vals.update({'Peer_Mentoring': True})

        if not vals.get('One_on_One_Mentoring'):
            vals.update({'One_on_One_Mentoring': False})
        if not vals.get('Specialist_Mentoring'):
            vals.update({'Specialist_Mentoring': False})
        if not vals.get('Group_Mentoring'):
            vals.update({'Group_Mentoring': False})
        if not vals.get('Peer_Mentoring'):
            vals.update({'Peer_Mentoring': False})
        res.append(vals)
        return res

    @api.multi
    def acceptedFuncation(self):
        for rec in self:
            mail_template_id = self.env.ref('mentorship.mentee_application_accept_mail_template')
            if mail_template_id:
                mail_template_id.with_context(mail_from=self.env.user.partner_id.email). \
                    send_mail(rec.id, force_send=True)
            rec.write({
                'state': 'accepted',
            })
        return True

    @api.multi
    def rejectedFuncation(self):
        for rec in self:
            rec.write({
                'state': 'reject',
            })
        return True

    @api.onchange('legalEntity')
    def onchangeLegalEntity(self):
        temp_bool_1 = False
        for res in self.legalEntity:
            if res.name == 'Other':
                temp_bool_1 = True
        if temp_bool_1:
            self.legalEntityBool = True
        else:
            self.legalEntityBool = False

    @api.onchange('slegalEntity')
    def onchangesLegalEntity(self):
        temp_bool_1 = False
        for res in self.slegalEntity:
            if res.name == 'Other':
                temp_bool_1 = True
        if temp_bool_1:
            self.slegalEntityBool = True
        else:
            self.slegalEntityBool = False

    @api.onchange('areasSupport')
    def onchangesAreasSupport(self):
        temp_bool_1 = False
        for res in self.areasSupport:
            if res.name == 'Other':
                temp_bool_1 = True
        if temp_bool_1:
            self.areasSupportBool = True
        else:
            self.areasSupportBool = False


class resUserInherit(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        groups = vals.get('groups_id')
        if "youth_user" in self.env.context.keys():
            groups.append((4, self.env.ref('client_management.group_branch_beneficiary').id))

        if "partner_user" in self.env.context.keys():
            groups.append((4, self.env.ref('client_management.group_partner_service_provider').id))

        return super(resUserInherit, self).create(vals)
