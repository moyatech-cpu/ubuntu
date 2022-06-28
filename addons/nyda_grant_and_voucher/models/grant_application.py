# coding=utf-8

from odoo import api, fields, models, _
from odoo import http
from datetime import date, datetime


class GrantApplication(models.Model):
    """ Model to register all the appications for grant. """
    _name = 'grant.application'
    _rec_name = 'serial_number'

    def create_monthly_smart_button(self):
        res = {
            'type': 'ir.actions.act_window',
            'name': _('Investment_'),
            'res_model': 'investment.',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('serial_number', '=', self.id)],
        }
        return res

    def _get_default_company(self):
        return self._context.get('force_company', self.env.user.company_id.id)

    # @api.multi
    # def compute_record_access_link(self):
    #     for rec in self:
    #         if rec.email:
    #             base_url = http.request.env['ir.config_parameter'].get_param('web.base.url')
    #             base_url += '/web#id=%d&view_type=form&model=%s' % (rec.id, rec._name)
    #             rec.record_access_link = base_url

    @api.multi
    @api.onchange('grant_amount_utilization')
    def get_total_grant_amount_utilization(self):
        self.total_grant_amount_utilization = 0
        for line in self.grant_amount_utilization:
            if line.name and line.amount:
                self.total_grant_amount_utilization += line.amount
        # return total

    @api.multi
    @api.onchange('grant_business_income_ids', 'grant_business_income_other_rupees')
    def get_total_grant_business_income(self):
        self.total_grant_business_income = 0
        for line in self.grant_business_income_ids:
            if line.name and line.rupees:
                self.total_grant_business_income += line.rupees

        for rec in self:
            if rec.grant_business_income_other_rupees:
                rec.total_grant_business_income = rec.total_grant_business_income + rec.grant_business_income_other_rupees

    @api.multi
    @api.onchange('grant_personal_income_ids', 'grant_personal_income_other_rupees')
    def get_total_grant_personal_income(self):
        self.total_grant_personal_income = 0
        for line in self.grant_personal_income_ids:
            if line.name and line.rupees:
                self.total_grant_personal_income += line.rupees
        for rec in self:
            if rec.grant_personal_income_other_rupees:
                rec.total_grant_personal_income = rec.total_grant_personal_income + rec.grant_personal_income_other_rupees

    @api.multi
    @api.onchange('grant_business_expenses_ids', 'grant_business_expenses_other_rupees')
    def get_total_grant_business_expenses(self):
        self.total_grant_business_expenses = 0
        for line in self.grant_business_expenses_ids:
            if line.name and line.rupees:
                self.total_grant_business_expenses += line.rupees

        for rec in self:
            if rec.grant_business_expenses_other_rupees:
                rec.total_grant_business_expenses = rec.grant_business_expenses_other_rupees + rec.total_grant_business_expenses

    @api.multi
    @api.onchange('grant_personal_expenses_ids', 'grant_personal_expenses_other_rupees')
    def get_total_grant_personal_expenses(self):
        self.total_grant_personal_expenses = 0
        for line in self.grant_personal_expenses_ids:
            if line.name and line.rupees:
                self.total_grant_personal_expenses += line.rupees

        for rec in self:
            if rec.grant_personal_expenses_other_rupees:
                rec.total_grant_personal_expenses = rec.total_grant_personal_expenses + rec.grant_personal_expenses_other_rupees

    @api.multi
    @api.onchange('other_expenses_ids')
    def get_total_grant_other_expenses(self):
        self.total_grant_other_expenses = 0
        for line in self.other_expenses_ids:
            if line.name and line.rupees:
                self.total_grant_other_expenses += line.rupees

    serial_number = fields.Char('Serial #')
    branch_id = fields.Many2one('res.branch', string='Branch Name')
    application_date = fields.Date('Date of Application', default=fields.Date.today())
    client_gr_number = fields.Char('GR Number')
    client_bsc_number = fields.Char('BSC Number')
    applicant_id = fields.Many2one('youth.enquiry', string='Applicant')
    legacy_creation_date = fields.Char('Legacy Creation Date')
    status = fields.Selection(
        [('new', 'New'), ('ict_checked', 'ITC Checked'), ('inspected', 'Inspected'),
         ('deligence_done', 'Deligence Done')
            , ('investment_memo_upload', 'Investment  Upload'), ('bgarg_review', 'BGARC Review'),
         ('send_letter', 'Send Rejection Letter'), ('hogac_review', 'HOGAC Review'),
         ('approved', 'Approved'), ('sent_approval_letter', 'Send Approval Letter'),
         ('uploaded_approval_letter', 'Contracting'),
         ('bdo_review', 'BDO Review'), ('branch_manager_review', 'Branch Manager Review'),
         ('disbursement', 'Disbursement Pack'),
         ('bcs_approved', 'BCS Approved'), ('qao_approved', 'QAO Approved'), ('edm_approved', 'EDM Approved'),
         ('approval_revoked', 'Approval Revoked'), ('aftercare', 'Aftercare'), ('completed', 'Completed'),
         ('reject', 'Reject'),
         ('cancelled', 'Cancelled'),
         ('Legacy', 'Legacy')],
        default='new',
        string="status")

    # Personal Information
    name = fields.Char('Name')
    surname = fields.Char('Surname')
    sa_identity_number = fields.Char('Identity Number')
    gender = fields.Selection([('female', 'Female'), ('male', 'Male')], string='Gender')
    age = fields.Integer('Age')
    population_group = fields.Selection([('african', 'African'),
                                         ('white', 'White'),
                                         ('asian', 'Asian'),
                                         ('indian', 'Indian'),
                                         ('coloured', 'Coloured')],
                                        default='african', string='Population Group')
    home_language = fields.Char('Home Language')
    disability = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no', string="Disability Status")
    disability_description = fields.Char('Describe Disability')
    telephone = fields.Char('Telephone Number')
    mobile = fields.Char('Cell Phone Number')
    email = fields.Char('Email')
    fax = fields.Char('Fax')
    physical_address = fields.Text('Physical Address')
    physical_postal_code = fields.Char('Postal Code')
    postal_address = fields.Text('Postal Address')
    postal_code = fields.Char('Postal Code')
    province_id = fields.Many2one('res.country.state', domain=[('country_id.name', '=', 'South Africa')],
                                  string="Province")
    geographical_type = fields.Selection([('urban', 'Urban'),
                                          ('peri-urban', 'Peri Urban'),
                                          ('rural-area-villages', 'Rural area - Villages'),
                                          ('rural-area-farms', 'Rural area - Farms'),
                                          ('informa-settlement', 'Informa settlement')],
                                         string="Geographical Type")
    formal_qualification = fields.Char('Formal Qualifications')
    trainings_attended = fields.Text('Training Courses Attended')
    next_of_kin = fields.Char('Next of Kin')
    relative_physical_address = fields.Text('Physical Address')
    relative_mobile = fields.Char('Cell Number')
    relationship = fields.Char('Relationship')

    beneficiary_id = fields.Many2one('youth.enquiry', string="Beneficiary")
    user_id = fields.Many2one('res.users', string="User Id", related='beneficiary_id.user_id')
    branch_id = fields.Many2one('res.branch', string="Branch", related='beneficiary_id.nearest_branch')

    # entrepreneurial status
    existing_business = fields.Boolean('Do you have an existing business that is currently in operation?')
    entrepreneurial_training = fields.Boolean('Have you ever received any Entrepreneurship Development Training?')
    job_creation_info_ids = fields.One2many('job.creation.information', 'grant_application_id',
                                            string="Job Creation Information")
    business_start_reason_ids = fields.Many2many('business.start.reason', string="Why do you want to start a business?")
    business_start_reason_char = fields.Char('Specify Other Reasons.')
    business_goals = fields.Text('Please describe the goals you want to achieve in business')
    business_experience = fields.Text(
        'What type of business experience do you have and what type of business do you want to start?')
    expertise_in_business = fields.Text(
        'What knowledge or expertise do you have that is relevant to the proposed business?')

    # Start-up Details
    startup_business_name = fields.Char('Business Name')
    startup_business_type = fields.Char('Type of Business')
    startup_business_sector_ids = fields.Many2many('mentor.sectors',
                                                   string="Please indicate the Sector in which your business is operating:")
    startup_business_sector_char = fields.Char('Specify Other Sectors.')
    startup_legal_entity_ids = fields.Many2many('legal.entity',
                                                string='Please indicate the Legal Entity in which your business is operating:')
    startup_legal_entity_char = fields.Char('Specify Other Entity')
    startup_business_start_reason_ids = fields.Many2many('business.start.reason',
                                                         string="Why do you want to start a business?")
    startup_idea_description = fields.Text('Please give a brief description of the idea in terms of:')
    management_skills_start_business = fields.Selection([('yes', 'Yes'),
                                                         ('no', 'No'),
                                                         ('not_sure', 'Not Sure')],
                                                        string="Do you have the management skills/ experience to start the business?")
    technical_skills_start_business = fields.Selection([('yes', 'Yes'),
                                                        ('no', 'No'),
                                                        ('not_sure', 'Not Sure')],
                                                       string="Do you have the technical skills to start the business?")
    identified_potential_customers = fields.Selection([('yes', 'Yes'),
                                                       ('no', 'No'),
                                                       ('not_sure', 'Not Sure')],
                                                      string="Have you identified your potential customers?")
    know_competitors = fields.Selection([('yes', 'Yes'),
                                         ('no', 'No'),
                                         ('not_sure', 'Not Sure')],
                                        string="Do you know who your competitors are?")
    money_to_cover_startup = fields.Selection([('yes', 'Yes'),
                                               ('no', 'No'),
                                               ('not_sure', 'Not Sure')],
                                              string="Do you have the money to cover your start-up costs?")
    money_to_cover_operating = fields.Selection([('yes', 'Yes'),
                                                 ('no', 'No'),
                                                 ('not_sure', 'Not Sure')],
                                                string="Do you have enough money to cover the operating costs?")
    required_equipments_and_machine = fields.Selection([('yes', 'Yes'),
                                                        ('no', 'No'),
                                                        ('not_sure', 'Not Sure')],
                                                       string="Do you have the equipment and machinery required to run the business?")
    ownership_status_ids = fields.One2many('business.ownership.status', 'grant_application_id',
                                           string="Please indicate the Ownership status in your business :")

    # Existing Business Details
    existing_business_name = fields.Char('Business Name')
    existing_business_type = fields.Char('Type of Business')
    existing_business_sector_ids = fields.Many2many('mentor.sectors',
                                                    string="Please indicate the Sector in which your business is operating:")
    existing_business_sector_char = fields.Char('Specify Other Sectors.')
    existing_legal_entity_ids = fields.Many2many('legal.entity',
                                                 string='Please indicate the Legal Entity in which your business is operating:')
    existing_legal_entity_char = fields.Char('Specify Other Entity')
    existing_business_start_reason_ids = fields.Many2many('business.start.reason',
                                                          string="Why do you want to start a business?")
    existing_idea_description = fields.Text('Please give a brief description of the idea in terms of:')
    business_running_time = fields.Selection([('lt20', 'Less than 12 months'),
                                              ('ottyears', '1 - 2 Years'),
                                              ('ttfyears', '3 - 4 Years'),
                                              ('ftfyears', '4 - 5 Years'),
                                              ('ftsyears', '5 - 6 Years'),
                                              ('stsyears', '6 - 7 Years'),
                                              ('ettyears', '8 - 10 Years'),
                                              ('mttyears', 'More than 10')],
                                             string="How long has the business been in operation and trading?")
    count_employees = fields.Integer(string='How many people (including yourself) are employed in the business?')
    change_in_emp_count = fields.Selection([('increased', 'Increased'),
                                            ('decreased', 'Decreased'),
                                            ('no_change', 'No Change')],
                                           string="Has there been a change in the number of people employed in the business over the last 12 months?")
    change_in_emp_reason = fields.Char('Reason')
    estimate_annual_turnover = fields.Selection([('lttthousand', 'Less than R20000'),
                                                 ('ttfthousand', 'R20000 - R49999'),
                                                 ('ftnthousand', 'R50000 - R99999'),
                                                 ('othhthousand', 'R100000 - R149999'),
                                                 ('htththousand', 'R150000 - R199999'),
                                                 ('ttththousand', 'R200000 - R299999'),
                                                 ('ttfhthousand', 'R300000 - R499000'),
                                                 ('ftnhthousand', 'R500000 - R999999'),
                                                 ('ottmillion', 'R1  - R2 Million'),
                                                 ('tttmillion', 'R2 - R3 Million'),
                                                 ('ttfmillion', 'R3 – R4 Million'),
                                                 ('mtfmillion', 'More than R5 million')],
                                                string="Please provide an estimate of your annual turnover (total amount of income)")
    change_in_turnover = fields.Selection([('increased', 'Increased'),
                                           ('decreased', 'Decreased'),
                                           ('no_change', 'No Change')],
                                          string="Has there been a change in the turnover of the business over the last 12 months?")
    change_in_turnover_reason = fields.Char('Reason')
    separate_bank_account = fields.Boolean('Do you have a separate bank account for the business?')
    business_start_method = fields.Selection([('myself', 'I started it myself'),
                                              ('bought', 'I bought Business'),
                                              ('with_partner_friend',
                                               'I started the business with a partner(s)/ friend(s)'),
                                              ('overtook_from_family', 'I took it over from someone in the family')],
                                             string="Please indicate how you started the business : ")
    business_start_monetary_id = fields.Many2one('business.start.monetary',
                                                 string="Where did you get the money to start your business?")
    business_operate_premises_id = fields.Many2one('business.operate.premises',
                                                   string="Describe the premises your business operates from : ")
    business_premise = fields.Selection([('own', 'Own'),
                                         ('rent', 'Rent')],
                                        string="Do you own or rent the premises? ")
    business_area_description = fields.Text('Please describe the area in which the business operates : ')
    business_geographical_location_id = fields.Many2one('business.geographical.location',
                                                        string="Geographical Location")
    business_sector_id = fields.Many2one('business.sector', string="Type of Business Sector")
    business_sector_char = fields.Char('Specify Other')
    growth_business_sector = fields.Selection([('growing', 'Growing'),
                                               ('growing_moderate', 'Growing Moderately'),
                                               ('growing_strongly', 'Growing Strongly'),
                                               ('in_decline', 'In Decline')],
                                              string="How would you describe the growth of the industry sector in which you operate?")
    business_comply_industry = fields.Selection([('yes', 'Yes'),
                                                 ('no', 'No'),
                                                 ('not_sure', 'Not Sure'),
                                                 ('none_applicable', 'None Applicable')],
                                                string="Does your business comply with industry registration requirements?")
    startup_involvement = fields.Selection([('only_current', 'Only this One'),
                                            ('two', '2'),
                                            ('three', '3'),
                                            ('more_than_three', 'More than 3')],
                                           string="How many business start-ups have you been involved in?")
    previous_work_on_industry = fields.Boolean(
        'Did you previously work in the industry sector or type of business you currently run ? ')
    previous_work_on_industry_duration = fields.Selection([('lt1year', 'Less than 1 year'),
                                                           ('tttyears', '2-3 years'),
                                                           ('ttfyears', '3-5 years'),
                                                           ('mtfyears', 'More than 5 years')],
                                                          string="For how long?")
    business_management_experiance = fields.Selection([('lt1year', 'Less than 1 year'),
                                                       ('tttyears', '2-3 years'),
                                                       ('ttfyears', '3-5 years'),
                                                       ('mtfyears', 'More than 5 years')],
                                                      string="How many years of business management experience do you have?")
    future_business_goals = fields.Text('Please describe your business goals for the future : ')
    business_development_assistance_ids = fields.Many2many('business.development.assistance',
                                                           string="Please indicate what type of business development assistance you need (you can tick more than one service) : ")
    business_assistance_improvements = fields.Text('Describe how this assistance is likely to improve your business: ')
    able_invest_resource = fields.Boolean(
        'Are you able to investment time, financial and other resources in improving your business?')
    able_invest_resource_description = fields.Text('Explain further : ')
    business_ownership_status_ids = fields.One2many('business.ownership.status', 'grant_application_id',
                                                    string="Please indicate the Ownership status in your business :")

    # Grant Existing Business
    grant_business_name = fields.Char("Business Name")
    grant_business_type = fields.Char('Business Type')
    grant_business_sector_ids = fields.Many2many('mentor.sectors',
                                                 string='Please indicate the Sector in which your business is operating:')
    grant_business_sector_char = fields.Char('Specify Other')
    grant_legal_entity_ids = fields.Many2many('legal.entity',
                                              string='Please indicate the Legal Entity in which your business is operating:')
    grant_legal_entity_char = fields.Char('Specify Other Entity')
    company_id = fields.Many2one('res.company', string='Company', default=_get_default_company)
    grant_business_registration = fields.Char("Business Registration")
    grant_business_registration_number = fields.Char("Business Registration Number")
    grant_threshold = fields.Selection([
        ('threshold_1', 'Threshold 1 - Idea generation and survivalist – R1000 – R10 000'),
        ('threshold_2', 'Threshold 2 - Start-ups, registered businesses (pty,cc,co-ops) – R10 001 – R50 000'),
        ('threshold_3',
         'Threshold 3 - Early Development(existing for 2 years) and growth stage(pty,cc,co-ops) – R50 001 – R100 000'),
        ('threshold_4',
         'Threshold 4 - Threshold 4 - Growth And Expansion Stage(pty,cc,co-ops) – R100 001 – R200 000, Co-ops up to R250 000')],
        # ('threshold_5', 'Threshold 5 - for agriculture and technology related  projects - maximum threshold is R250,000.00')
        string="Grant Threshold")

    grant_amount_required = fields.Float(string="Grant Amount required")
    grant_amount_utilization = fields.One2many('grant.amount.utilization', 'grant_application_id',
                                               string="To be utilized as follows")
    total_grant_amount_utilization = fields.Float(string="Total Grant Amount Utilized",
                                                  compute=get_total_grant_amount_utilization)
    copy_total_grant_amount_utilization = fields.Float(string="Total Grant Amount Utilized",
                                                       related='total_grant_amount_utilization')

    grant_business_income_ids = fields.One2many('grant.business.income', 'grant_application_id',
                                                string="Business Income")
    grant_business_income_other = fields.Char('Other Business Income')
    grant_business_income_other_rupees = fields.Float('Rands')
    total_grant_business_income = fields.Float(string="Total Grant Business Income",
                                               compute=get_total_grant_business_income)

    grant_personal_income_ids = fields.One2many('grant.personal.income', 'grant_application_id',
                                                string="Personal Income")
    grant_personal_income_other = fields.Char('Other Personal Income')
    grant_personal_income_other_rupees = fields.Float('Rands')
    total_grant_personal_income = fields.Float(string="Total Grant Personal Income",
                                               compute=get_total_grant_personal_income)

    grant_business_expenses_ids = fields.One2many('grant.business.expenses', 'grant_application_id',
                                                  string="Business Expenses")
    grant_business_expenses_other = fields.Char('Other Business Expenses')
    grant_business_expenses_other_rupees = fields.Float('Rands')
    total_grant_business_expenses = fields.Float(string="Total Grant Business Expenses",
                                                 compute=get_total_grant_business_expenses)

    grant_personal_expenses_ids = fields.One2many('grant.personal.expenses', 'grant_application_id',
                                                  string="Personal Expenses")
    grant_personal_expenses_other = fields.Char('Other Personal Expenses')
    grant_personal_expenses_other_rupees = fields.Float('Rands')
    total_grant_personal_expenses = fields.Float(string="Total Grant Personal Expenses",
                                                 compute=get_total_grant_personal_expenses)

    other_expenses_ids = fields.One2many('grant.other.expenses', 'grant_application_id',
                                         string="Other Additional Expenses")
    total_grant_other_expenses = fields.Float(string="Total Grant Other Expenses",
                                              compute=get_total_grant_other_expenses)

    # Supporting Document
    # identity_document_1 = fields.Binary(string='Identity Document 1')
    # identity_document_1_name = fields.Char(string='Identity Document 1')
    # identity_document_2 = fields.Binary(string='Identity Document 2')
    # identity_document_2_name = fields.Char(string='Identity Document 2')
    # identity_document_3 = fields.Binary(string='Identity Document 3')
    # identity_document_3_name = fields.Char(string='Identity Document 3')
    # proof_of_residence = fields.Binary(string='Proof of Residence')
    # proof_of_residence_name = fields.Char(string='Proof of Residence')
    # company_registration = fields.Binary(string='Copy of Company Registration from CIPC')
    # company_registration_name = fields.Char(string='Copy of Company Registration from CIPC')
    # company_profile = fields.Binary(string='Company Profile')
    # company_profile_name = fields.Char(string=' Company Profile')
    # current_employees = fields.Binary(string='Detailed list of the current employees')
    # current_employees_name = fields.Char(string='Detailed list of the current employees')
    # bank_statement = fields.Binary(string='Personal Bank Statement or Business Bank Statement')
    # bank_statement_name = fields.Char(string='Personal Bank Statement or Business Bank Statement')
    # business_plan_grant = fields.Binary(string='Business Plan if looking for grant >R50 000')
    # business_plan_grant_name = fields.Char(string='Business Plan if looking for grant >R50 000')
    # quotations_grant = fields.Binary(string='Quotations if looking for a grant')
    # quotations_grant_name = fields.Char(string='Quotations if looking for a grant')

    certified_identity_document_applicant = fields.Binary(string='Identity Document')
    certified_identity_document_applicant_name = fields.Char(string='Identity Document')
    nyda_business_plan_template_document = fields.Binary(string='NYDA Business plan template')
    nyda_business_plan_template_document_name = fields.Char(string='NYDA Business plan template')
    usage_of_working_capital = fields.Binary(string='Usage of working capital')
    usage_of_working_capital_name = fields.Char(string='Usage of working capital')
    business_bank_account = fields.Binary(string='Business Bank Account')
    business_bank_account_name = fields.Char(string='Business Bank Account')
    proof_of_business_registration = fields.Binary(string='Proof of Business Registration')
    proof_of_business_registration_name = fields.Char(string='Proof of Business Registration')
    requires_skills_operate_business = fields.Binary(string='Skills to Operate Business')
    requires_skills_operate_business_name = fields.Char(string='Skills to Operate Business')
    additional_permanent_job_creation = fields.Binary(string='Additional permanent job creation')
    additional_permanent_job_creation_name = fields.Char(string='Additional permanent job creation')
    formal_business_plan = fields.Binary(string='Formal Business Plan')
    formal_business_plan_name = fields.Char(string='Formal Business Plan')
    provide_management_accounts = fields.Binary(string='Provide Management Accounts')
    provide_management_accounts_name = fields.Char(string='Provide Management Accounts')
    market_letters_off_take_contracts = fields.Binary(string='Market Letters/Cpntracts')
    market_letters_off_take_contracts_name = fields.Char(string='Market Letters/Cpntracts')
    business_operational_years_document = fields.Binary(string='Business operational years')
    business_operational_years_document_name = fields.Char(string='Business operational years')
    valid_tax_clearance_certificate = fields.Binary(string='Valid tax clearance certificate')
    valid_tax_clearance_certificate_name = fields.Char(string='Valid tax clearance certificate')
    breakdown_of_funds = fields.Binary(string='Breakdown of Funds')
    breakdown_of_funds_name = fields.Char(string='Breakdown of Funds')
    financial_statement_signed_accountant = fields.Binary(string='Signed Financial Statement')
    financial_statement_signed_accountant_name = fields.Char(string='Signed Financial Statement')
    one_year_management_account = fields.Binary(string='One Year Management Account')
    one_year_management_account_name = fields.Char(string='One Year Management Account')
    other_doc = fields.Binary(string='Other Documents')
    other_doc_name = fields.Char(string='Other Documents')

    # for page internal report
    ict_report = fields.Binary(string='ITC Report')
    ict_report_name = fields.Char('File Name')
    main_inspect_report = fields.Binary('Inspect Report')
    main_inspect_report_name = fields.Char('File Name')
    inspection_report = fields.Binary('Site Inspection Report')
    inspection_report_name = fields.Char('File Name')
    financial_assessment = fields.Binary('Financial Assessment')
    financial_assessment_name = fields.Char('File Name')
    business_plan = fields.Binary('Business Plan')
    business_plan_name = fields.Char('File Name')
    # itc_report = fields.Binary('ITC Report')
    # itc_report_name = fields.Char('File Name')
    # due_deligence_checklist = fields.Binary('Due deligence checklist')
    # due_deligence_checklist_name = fields.Char('File Name')
    approval_letter = fields.Binary(string='Approval Letter')
    approval_letter_name = fields.Char(string='File Name')
    upload_investiment_ = fields.Binary(string='Investment ')
    upload_investiment__name = fields.Char(string='File Name')
    approval_letter_send_date = fields.Date("Approval Date")
    # declaration_of_interest = fields.Binary(string='Declaration Of Interest')
    # declaration_of_interest_name = fields.Char(string='File Name')
    # minutes = fields.Binary(string='Minutes')
    # minutes_name = fields.Char(string='File Name')
    signed_approval_letter = fields.Binary('Approval Letter signed by Beneficiary')
    signed_approval_letter_filename = fields.Char('Approval letter filename')

    uploaded_approval_letter1 = fields.Binary(String='Signed Letter')
    uploaded_approval_letter1_name = fields.Char(String='File Name')

    contract = fields.Binary(String='Contract')
    contract_name = fields.Char(String='File Name')
    upload_investiment_memo = fields.Binary(string='Investment memo')
    upload_investiment_memo_name = fields.Char(string='File Name')

    cover_letter = fields.Binary(string='Cover Page')
    cover_letter_name = fields.Char(string='File Name')
    supplier_checklist = fields.Binary(string='Supplier Checklist')
    supplier_checklist_name = fields.Char(string='File Name')
    quatation_attech_ids = fields.Many2many('ir.attachment',
                                            string="(Quotation/Bank Confirmation/Director's ID/Company Registration Doc)")
    bank_confirmation_ids = fields.Many2many('ir.attachment', string='Bank Confirmation')
    directors_attech_ids = fields.Many2many('ir.attachment', string="Director's ID")
    company_registration_attech_ids = fields.Many2many('ir.attachment', string="Company Registration Doc")
    # quatation_attech = fields.Binary(string='Quatation')
    # quatation_attech_name = fields.Char(string='File Name')
    # bank_confirmation = fields.Binary(string='Bank Confirmation')
    # bank_confirmation_name = fields.Char(string='File Name')
    # director_ide = fields.Binary(string='Director IDe')
    # director_ide_name = fields.Char(string='File Name')
    # company_registration_doc = fields.Binary(string='Company Registration Doc')
    # company_registration_doc_name = fields.Char(string='File Name')
    # tax_clearance_doc = fields.Binary(string='Tax Clearance Certificate')
    # tax_clearance_doc_name = fields.Char(string='File Name')

    proof_of_payment = fields.Binary(string='Proof Of Payment')
    proof_of_payment_name = fields.Char(string='File Name')

    is_bgarg = fields.Boolean("BGARC Access")
    is_hogarg = fields.Boolean("HOGARG Access")

    # FIELD FOR GENERATIONG URL FOR APPLICANT
    # record_access_link = fields.Char(string="Record Access Link", compute='compute_record_access_link', store=True)
    # access_name = fields.Char(string="Access Name", default="Click Here")

    # Appointment Schedule
    user_name = fields.Char(string="Name")
    bdo_name = fields.Many2one('res.users', string="BDO Assigned", readonly=True)
    appointment_date = fields.Datetime(string="Appointment Date")
    appointment_location = fields.Text(string="Appointment Venue")

    # BGARG APPROVE UPLOADS
    brarg_declaration_of_interest_name = fields.Char(string="File Name")
    bgarg_declaration_of_interest = fields.Binary(string="Declaration of Interest")
    bgarg_minutes_name = fields.Char(string="File Name")
    bgarg_minutes = fields.Binary(string="Minutes")
    bgarg_approval_letter_send_date = fields.Date(string="BGARC Approval Date")
    bgarg_rejection_report = fields.Text(string="BGARC Rejection Reason")
    bgrag_rejection_report_date = fields.Date(string="BGARC Rejection Date", default=date.today())
    bgarc_declaration_of_interest_reject = fields.Binary(string='Declaration Of Interest')
    bgarc_declaration_of_interest_name_reject = fields.Char(string='File Name')
    bgarc_minutes_reject = fields.Binary(string='Minutes')
    bgarc_minutes_name_reject = fields.Char(string='File Name')

    # HOGAC Approve Uploads
    # hogac_approval_letter = fields.Binary(string='Approval Letter')
    # hogac_approval_letter_name = fields.Char(string='File Name')
    hogac_declaration_of_interest = fields.Binary(string='Declaration Of Interest')
    hogac_declaration_of_interest_name = fields.Char(string='File Name')
    hogac_minutes = fields.Binary(string='Minutes')
    hogac_minutes_name = fields.Char(string='File Name')
    hogac_approval_letter_send_date = fields.Date("HOGAC Approval Date")

    hogac_rejection_report = fields.Text(string="HOGAC Rejection Reason")
    hogac_rejection_report_date = fields.Text(string="HOGAC Rejection Date")

    aftercare_report = fields.Binary('Aftercare Report')
    aftercare_report_name = fields.Char('File Name')

    # Rejection Reason
    reason_text = fields.Text('Reason for Rejection')
    # bdo_rejection_reason = fields.Text(string="Reason for Rejection")

    # refer to hogac
    minute_from_bgarg = fields.Binary('Minute From BGARG')
    minute_from_bgarg_name = fields.Char('File Name')
    declaration_of_interest_refer = fields.Binary('Declaration of Interest')
    declaration_of_interest_refer_name = fields.Char('File Name')

    payment_date = fields.Date('Payment Date')

    # Boolean fields check for review

    nyda_bdo_bool = fields.Boolean(string='NYDA BDO Review')
    nyda_branch_manager_bool = fields.Boolean(string='NYDA BM Review')

    nyda_bcs_bool = fields.Boolean(string='NYDA BCS Review')
    nyda_qao_bool = fields.Boolean(string='NYDA QAO Review')
    nyda_edm_bool = fields.Boolean(string='NYDA EDM Review')

    # Boolean fields for rejection and rejection reasons

    nyda_bdo_r_bool = fields.Boolean(string='NYDA BDO Rejection')
    bdo_rejection_report = fields.Text(string="BDO Rejection reasons")
    bdo_rejection_report_date = fields.Date(string='BDO rejection Date')

    nyda_branch_manager_r_bool = fields.Boolean(string='NYDA BM Rejection')
    bm_rejection_report = fields.Text(string="BM Rejection reasons")
    bm_rejection_report_date = fields.Date(string='BM rejection Date')

    nyda_bcs_r_bool = fields.Boolean(string='NYDA BCS Rejection')
    bcs_rejection_report = fields.Text(string="BCS Rejection reasons")
    bcs_rejection_report_date = fields.Date(string='BCS rejection Date')

    nyda_qao_r_bool = fields.Boolean(string='NYDA QAO Rejection')
    qao_rejection_report = fields.Text(string="QAO Rejection reasons")
    qao_rejection_report_date = fields.Date(string='QAO rejection Date')

    nyda_edm_r_bool = fields.Boolean(string='NYDA EDM Rejection')
    edm_rejection_report = fields.Text(string="EDM Rejection reasons")
    edm_rejection_report_date = fields.Date(string='EDM rejection Date')

    refer_rejection = fields.Text(string='correction Note(HOGAC)')
    nyda_refer_r_bool = fields.Boolean(string='nyda_refer_r_bool')
    nyda_refer_bool = fields.Boolean(string='nyda_refer_bool')
    # nyda_refer_bool = fields.Boolean(string='nyda_refer_bool')

    rejection_letter = fields.Binary(string='Approval Letter')
    rejection_letter_name = fields.Char(string='File Name')
    rejection_letter_send_date = fields.Date(string="Date")

    refer_correction = fields.Text(string="Reason for Rejection")
    correction_date = fields.Date(string="Date")

    @api.multi
    def send_mail_bcs(self):
        email_list = []
        body = "<html>\
        <body><p> The Students Participated</p>\
        <table width='100%' height='100%' style='border:1px solid black;'>\
        <tr style='border:1px solid black;'>\
        <td style='border:1px solid black;'> Event NAME</td><td style='border:1px solid black;'>participant Date</td></tr>"
        for record_mail in self.env['res.users'].search([]):
            if record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_bcs') and record_mail.email:
                email_list.append(str(record_mail.email))
        mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
        body += "<p>Your Pre-Assessment application has been recommended.</p>\
                <p>Now you can proceed to apply for Grant/Voucher Programme provided by NYDA from Website.</p>\
                <p>Please contact the administration if you have any query.</p>\
                <p>Regards, </p>\
                <p>NYDA</p>"
        body += "</table></body></html>"
        body += "<p><strong> Your Child Is Participanted This Event, </strong></p><br/>\
                <p>Thank You</p>"
        if email_list and mail_server_ids.smtp_user:
            email_to = ','.join(email_list)
            template = self.env['mail.mail'].create({
                'subject': 'Grant Application Mail',
                'body_html': body,
                'email_from': self.env.user.email or '',
            })
            #template.write({'email_to': email_to})
            #template.send()

    @api.model
    def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['serial_number'] = self.env['ir.sequence'].next_by_code('grant.application')
        record_obj = super(GrantApplication, self).create(values)

        '''
        for rec in record_obj:
            email_list = []
            body = "<html>\
            <body><p> The Students Participated</p>\
            <table width='100%' height='100%' style='border:1px solid black;'>\
            <tr style='border:1px solid black;'>\
            <td style='border:1px solid black;'> Event NAME</td><td style='border:1px solid black;'>participant Date</td></tr>"
            for record_mail in self.env['res.users'].search([]):
                if record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_bda') and record_mail.email:
                    email_list.append(str(record_mail.email))
        mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
        body += "</table></body></html>"
        body += "<p><strong> Your Child Is Participanted This Event, </strong></p><br/>\
                <p>Thank You</p>"
        if email_list and mail_server_ids.smtp_user:
            email_to = ','.join(email_list)
            template = self.env['mail.mail'].create({
                'subject': 'Grant Application Mail',
                'body_html': body,
                'email_from': self.env.user.email or '',
            })
            #template.write({'email_to': email_to})
            #template.send()
        '''
        return record_obj

    @api.multi
    def write(self, values):
        record_obj = super(GrantApplication, self).write(values)
        return record_obj

    @api.multi
    def set_recommended(self):
        """ Sets state to approved. Add logic if need anything once application is moved to approved state. """
        for rec in self:
            rec.write({'status': 'recommended'})

    @api.multi
    def set_cancelled(self):
        for rec in self:
            rec.write({'status':'cancelled'})

    @api.multi
    def set_accept(self):
        """ Sets state to approved. Add logic if need anything once application is moved to approved state. """

        return {
            'type': 'ir.actions.act_window',
            'name': 'BGARG Approve',
            'res_model': 'bgarg.approve.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }

    @api.multi
    def bgarg_check(self):
        """ Sets state to reject. Add logic if need anything once application is moved to reject state. """
        for rec in self:
            rec.write({'status': 'bgarg_review', 'is_bgarg': True})

    def check_approval_letter_status(self):
        """ Check if  """
        grant_approved_applications = self.search([('status', '=', 'sent_approval_letter')])
        mail_template_reminder_id = self.env.ref('nyda_grant_and_voucher.grant_application_reminder_mail_template')
        mail_template_final_call_id = self.env.ref('nyda_grant_and_voucher.grant_application_final_call_mail_template')
        if grant_approved_applications:
            for grant_approved_application in grant_approved_applications:
                if grant_approved_application.approval_letter_send_date:
                    approval_letter_send_date = datetime.strptime(grant_approved_application.approval_letter_send_date,
                                                                  '%Y-%m-%d').date()
                    diff_days = (date.today() - approval_letter_send_date).days
                    if diff_days == 13 and mail_template_reminder_id:
                        mail_template_reminder_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)
                    elif diff_days == 14 and mail_template_final_call_id:
                        mail_template_final_call_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)
                    elif diff_days > 14:
                        grant_approved_application.status = 'approval_revoked'
        pass

    # ------------>>>>>>>>>>>>> Name + Serial number appears on Many2one list

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            if rec.serial_number and rec.name:
                namedisplay = rec.serial_number + "-" + rec.name
                res.append((rec.id, namedisplay))
            return res

    # --------->>>>>>>>>>> Method for BDO TO review application from Branch Admin

    @api.multi
    def bdo_accept_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'BDO Accept Confirmation Wizard',
            'res_model': 'bdo.accept.confirm.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }


    # --------->>>>>>>>>>> Method for BDO TO open a wizard and provide rejection  application from Branch Admin

    @api.multi
    def bdo_reject_report(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'BDO Rejection Reason Wizard',
            'res_model': 'bdo.rejection.reason.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }

    # Branch manager Approve Application Method
    @api.multi
    def branch_manager_accept_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'BM Accept Confirmation Wizard',
            'res_model': 'bm.accept.confirm.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }

    # Branch manager Reject Application Method
    @api.multi
    def branch_manager_reject_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Branch Manager Rejection Report Wizard',
            'res_model': 'bm.rejection.report.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }

    # BCS Application Approval method
    @api.multi
    def bsc_approved_check(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'BCS Accept Confirmation Wizard',
            'res_model': 'bsc.accept.confirm.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }

    # BCS Application Reject method
    @api.multi
    def bcs_reject_check(self):
        # if self.nyda_branch_manager_bool==True and self.nyda_branch_manager_r_bool==False:
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bcs Rejection Report Wizard',
            'res_model': 'bcs.rejection.reason.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }

    # QAO Application Approve method
    @api.multi
    def qao_approved_check(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'QAO Accept Confirmation Wizard',
            'res_model': 'qao.accept.confirm.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }

    # QAO Application Reject method
    @api.multi
    def qao_reject_check(self):
        if self.nyda_bcs_bool == True and self.nyda_bcs_r_bool == False:
            return {
                'type': 'ir.actions.act_window',
                'name': 'QAO Rejection Report Wizard',
                'res_model': 'qao.rejection.report.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': {'current_id': self.id}
            }

    # EDM Application Approve method
    @api.multi
    def edm_approved_check(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'EDM Accept Confirmation Wizard',
            'res_model': 'edm.accept.confirm.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }


    # EDM Application Reject method
    @api.multi
    def edm_reject_check(self):

        if self.nyda_qao_bool == True and self.nyda_qao_r_bool == False:
            return {
                'type': 'ir.actions.act_window',
                'name': 'EDM Rejection Report Wizard',
                'res_model': 'edm.rejection.reason.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': {'current_id': self.id}
            }

    @api.multi
    def refer_hogac(self):
        for rec in self:
            self.is_hogarg = True
            rec.write({'status': 'hogac_review'})


class JobCreationInformation(models.Model):
    """ Container for Job Creation Information for Grant and Voucher Applications. """
    _name = 'job.creation.information'
    _rec_name = 'population_group'

    grant_application_id = fields.Many2one('grant.application', string='Application')
    voucher_application_id = fields.Many2one('voucher.application', string='Application')
    population_group = fields.Selection([('african', 'African'),
                                         ('white', 'White'),
                                         ('indian', 'Indian'),
                                         ('coloured', 'Coloured')],
                                        string='Population Group')
    before_funding_male = fields.Integer('Male (Before Funding)')
    before_funding_female = fields.Integer('Female (Before Funding)')
    before_funding_disabled_male = fields.Integer('Male (Before Funding, Disabled)')
    before_funding_disabled_female = fields.Integer('Female (Before Funding, Disabled)')
    before_funding_age_male = fields.Integer('Male (Before Funding, Avg. Age)')
    before_funding_age_female = fields.Integer('Male (Before Funding, Avg. Age)')
    after_funding_male = fields.Integer('Male (Before Funding)')
    after_funding_female = fields.Integer('Female (Before Funding)')
    after_funding_disabled_male = fields.Integer('Male (Before Funding, Disabled)')
    after_funding_disabled_female = fields.Integer('Female (Before Funding, Disabled)')
    after_funding_age_male = fields.Integer('Male (Before Funding, Avg. Age)')
    after_funding_age_female = fields.Integer('Female (Before Funding, Avg. Age)')


class BusinessStartReason(models.Model):
    """ Model to specify Reasons to start business. """
    _name = 'business.start.reason'

    name = fields.Char('Name')
    code = fields.Char('Internal Code')


class GrantAmountUtilization(models.Model):
    """ Model to specify grant amount utilization """
    _name = "grant.amount.utilization"
    grant_application_id = fields.Many2one('grant.application', string="Grant Application")
    voucher_application_id = fields.Many2one('voucher.application', string='Application')
    name = fields.Char("To be utilized at")
    amount = fields.Float('Amount')


class GrantBusinessIncome(models.Model):
    """ Model to specify grant business income """
    _name = "grant.business.income"
    grant_application_id = fields.Many2one('grant.application', string="Grant Application")
    voucher_application_id = fields.Many2one('voucher.application', string='Application')
    name = fields.Selection([('sales', 'Sales'),
                             ('debtors', 'Debtors')], 'Name')
    rupees = fields.Float('Rands')


class GrantPersonalIncome(models.Model):
    """ Model to specify grant personal income """
    _name = "grant.personal.income"
    grant_application_id = fields.Many2one('grant.application', string="Grant Application")
    voucher_application_id = fields.Many2one('voucher.application', string='Application')
    name = fields.Selection([('applicant_salary', 'Applicant Salary'), ('spouse_salary', 'Spouse Salary')], 'Name')
    rupees = fields.Float('Rands')


class GrantBusinessExpenses(models.Model):
    """ Model to specify grant business expenses """
    _name = "grant.business.expenses"
    grant_application_id = fields.Many2one('grant.application', string="Grant Application")
    voucher_application_id = fields.Many2one('voucher.application', string='Application')
    name = fields.Selection([('rent', 'Rent'), ('equipment', 'Equipment'),
                             ('stock_material', 'Purchases: Stock/Material'),
                             ('water_electricity', 'Water/Electricity'),
                             ('insurance', 'Insurance'), ('security', 'Security'),
                             ('accounting_fees', 'Accounting fees'),
                             ('petrol_transport', 'Petrol/Transport'), ('maintenance', 'Maintenance'),
                             ('salaries_wages', 'Salaries/Wages'), ('owner_drawings', 'Owner’s Drawings'),
                             ('rsc_levies', 'RSC Levies'),
                             ('uif_contributions', 'UIF Contributions'),
                             ('tel_fax_postage', 'Tel/Fax/Postage'), ('stationery', 'Stationery'),
                             ('loan_1_repayment', 'Loan 1 Repayment'), ('loan_2_repayment', 'Loan 2 Repayment'),
                             ('consumables', 'Consumables'), ('sundry_expenses', 'Sundry Expenses')], 'Name')
    rupees = fields.Float('Rands')


class GrantPersonalExpenses(models.Model):
    """ Model to specify grant personal expenses """
    _name = "grant.personal.expenses"
    grant_application_id = fields.Many2one('grant.application', string="Grant Application")
    voucher_application_id = fields.Many2one('voucher.application', string='Application')
    name = fields.Selection([('rent_bond', 'Rent/Bond'), ('car_instalment', 'Car Instalment'),
                             ('water_electricity', 'Water Electricity'), ('groceries', 'Groceries'),
                             ('clothing', 'Clothing'), ('travel_transport', 'Travel/Transport'),
                             ('entertainment', 'Entertainment'),
                             ('medical_expenses', 'Medical Expenses'), ('donations_church', 'Donations/Church'),
                             ('school_fees', 'School Fees'), ('family_commitments', 'Family Commitments'),
                             ('insurance_fees', 'Insurance Fees'),
                             ('life', 'Life'), ('endowment', 'Endowment'), ('investments', 'Investments'),
                             ('funeral', 'Funeral'), ('study', 'Study'), ('savings_stokvel', 'Savings/stokvel'),
                             ('store_cards', 'Store Cards'), ('telephone', 'Telephone'),
                             ('hp_instalments', 'HP Instalments'),
                             ('nlr_exposure', 'NLR Exposure'), ('cca_exposure', 'CCA Exposure')], 'Name')
    rupees = fields.Float('Rands')


class GrantOtherExpenses(models.Model):
    """ Model to specify grant personal income """
    _name = "grant.other.expenses"
    grant_application_id = fields.Many2one('grant.application', string="Grant Application")
    voucher_application_id = fields.Many2one('voucher.application', string='Application')
    name = fields.Selection([('land_buildings', 'Land/Buildings'), ('furniture_fittings', 'Furniture/Fittings'),
                             ('equipment', 'Equipment'), ('vehicles', 'Vehicles'), ], 'Name')
    rupees = fields.Float('Rands')


class BusinessSector(models.Model):
    """ Model to specify business.sector """
    _name = 'business.sector'

    name = fields.Char('Name')
    code = fields.Char('Internal Code')


class BusinessStartMonetary(models.Model):
    """ Model to specify business.sector """
    _name = 'business.start.monetary'

    name = fields.Char('Name')
    code = fields.Char('Internal Code')


class BusinessOperatePremises(models.Model):
    """ Model to specify business.sector """
    _name = 'business.operate.premises'

    name = fields.Char('Name')


class BusinessGeographicalLocation(models.Model):
    """ Model to specify business.sector """
    _name = 'business.geographical.location'

    name = fields.Char('Name')


class BusinessDevelopmentAssistance(models.Model):
    """ Model to specify business.development.assistance """
    _name = 'business.development.assistance'

    name = fields.Char('Name')
    code = fields.Char('Internal Code')
    service_item_seq = fields.Char(string="Service Item ID")
    voucher_value = fields.Integer(strinh="Voucher Value")
    min_dur = fields.Integer(string="Minimum Duration(Hours)")
    is_enabled = fields.Boolean(string="Enabled")
    partner_enquiry_ids = fields.Many2many('partner.enquiry', string='Service Provider')

    # for server if list for partner/service provider

    partner_enquiry_id = fields.Many2one('partner.enquiry', string='Partner Enquiry')

    def toggle_active(self):
        if self.is_enabled:
            self.is_enabled = False
        elif not self.is_enabled:
            self.is_enabled = True


class BusinessOwnershipStatus(models.Model):
    """ Model to provide information regarding ownership of business """
    _name = 'business.ownership.status'

    grant_application_id = fields.Many2one('grant.application', string="Application")
    voucher_application_id_ownership = fields.Many2one('voucher.application', string='Application')
    voucher_application_id_business_ownership = fields.Many2one('voucher.application', string='Application')
    name = fields.Char('Name & Surname of Partner')
    position = fields.Char('Position in Business')
    mobile = fields.Char('Contact Number')
    x_id_number = fields.Char('ID Number')
    disability = fields.Selection([('yes', 'Yes'),
                                   ('no', 'No')],
                                  string="Disability")
    gender = fields.Selection([('female', 'Female'),
                               ('male', 'Male')],
                              string="Gender")
    geographical_type = fields.Selection([('urban', 'Urban'), ('peri_urban', 'Peri Urban'),
                                          ('rural_villages', 'Rural Area-Villages'),
                                          ('rural_farms', 'Rural Area-Farms'),
                                          ('informa_settlement', 'Informa Settlement')],
                                         string="Geographical Type")
    population_group = fields.Selection([('african', 'African'),
                                         ('white', 'White'),
                                         ('indian', 'Indian'),
                                         ('coloured', 'Coloured')],
                                        default='african', string='Race')
    ownership = fields.Float(string="Ownership(%)")

# class BusinessStartMethod(models.Model):
#     """ Model to provide information on how user has started existing business """
#     _name = 'business.start.method'
#
#     name = fields.Char('Name')