# coding=utf-8
from odoo import api, fields, models
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo import http


class VoucherApplication(models.Model):
    """ Model to register all the appications for grant. """
    _name = 'voucher.application'
    _rec_name = 'serial_number'

    @api.multi
    @api.depends('estimate_annual_turnover')
    @api.onchange('estimate_annual_turnover')
    def get_expected_turn_over_hidden_value(self):
        for record in self:
            if record.estimate_annual_turnover:
                if (
                        record.estimate_annual_turnover == 'lttthousand' or record.estimate_annual_turnover == 'ttfthousand' or
                        record.estimate_annual_turnover == 'ftnthousand' or record.estimate_annual_turnover == 'othhthousand' or
                        record.estimate_annual_turnover == 'htththousand' or record.estimate_annual_turnover == 'ttththousand' or
                        record.estimate_annual_turnover == 'ttfhthousand' or record.estimate_annual_turnover == 'ftnhthousand'):
                    record.expected_turn_over_hidden_value = 1

                elif (
                        record.estimate_annual_turnover == 'ottmillion' or record.estimate_annual_turnover == 'tttmillion' or
                        record.estimate_annual_turnover == 'ttfmillion'):
                    record.expected_turn_over_hidden_value = 2

                elif (record.estimate_annual_turnover == 'mtfmillion'):
                    record.expected_turn_over_hidden_value = 3

    @api.multi
    @api.depends('ownership_status_ids')
    @api.onchange('ownership_status_ids')
    def get_total_status_ownership_percent(self):
        for rec in self:
            rec.total_status_ownership_percent = 0
            for line in rec.ownership_status_ids:
                if line.ownership and line.name:
                    rec.total_status_ownership_percent += line.ownership

    @api.multi
    @api.depends('business_ownership_status_ids')
    @api.onchange('business_ownership_status_ids')
    def get_total_business_ownership_percent(self):
        for rec in self:
            rec.total_business_ownership_percent = 0
            for line in rec.business_ownership_status_ids:
                if line.ownership and line.name:
                    rec.total_business_ownership_percent += line.ownership

    @api.multi
    @api.depends('business_development_assistance_ids', 'expected_turn_over_hidden_value')
    @api.onchange('business_development_assistance_ids', 'expected_turn_over_hidden_value')
    def compute_voucher_value(self):
        for rec in self:
            rec.voucher_value_vat = 0
            rec.voucher_isurance_objective = ''
            for values in rec.business_development_assistance_ids:
                if (values.id == 1 and int(rec.expected_turn_over_hidden_value) == 1):
                    rec.voucher_isurance_objective += "To ensure and demonstrate that the business to be started is feasible from a market, financial, technical and managerial perspective. " + "\n"
                    rec.voucher_value_vat += 6600
                if (values.id == 1 and int(rec.expected_turn_over_hidden_value) == 2):
                    rec.voucher_isurance_objective += "To ensure and demonstrate that the business to be started is feasible from a market, financial, technical and managerial perspective. " + "\n"
                    rec.voucher_value_vat += 10000

                if (values.id == 1 and int(rec.expected_turn_over_hidden_value) == 3):
                    rec.voucher_isurance_objective += "To ensure and demonstrate that the business to be started is feasible from a market, financial, technical and managerial perspective. " + "\n"
                    rec.voucher_value_vat += 13000
                if (values.id == 2):
                    rec.voucher_isurance_objective += "To ensure and demonstrate that the business to be purchased is feasible from a market, financial, technical and managerial perspective. " + "\n"
                    rec.voucher_value_vat += 19800
                if (values.id == 3 and int(rec.expected_turn_over_hidden_value) == 1):
                    rec.voucher_isurance_objective += "To enhance the bankability and planning orientation of youth enterprises. " + "\n"
                    rec.voucher_value_vat += 10000
                if (values.id == 3 and int(rec.expected_turn_over_hidden_value) == 2):
                    rec.voucher_isurance_objective += "To enhance the bankability and planning orientation of youth enterprises. " + "\n"
                    rec.voucher_value_vat += 12500
                if (values.id == 3 and int(rec.expected_turn_over_hidden_value) == 3):
                    rec.voucher_isurance_objective += "To enhance the bankability and planning orientation of youth enterprises. " + "\n"
                    rec.voucher_value_vat += 15000
                if (values.id == 4):
                    rec.voucher_isurance_objective += "To ensure that the entity is able to function professionally using relevant marketing materials and tools. " + "\n"
                    rec.voucher_value_vat += 8800
                if (values.id == 5):
                    rec.voucher_isurance_objective += "To ensure that the entity is able to function professionally using relevant marketing materials and tools. " + "\n"
                    rec.voucher_value_vat += 6600
                if (values.id == 6):
                    rec.voucher_isurance_objective += "To assist the entrepreneur in obtaining a web presence and market. " + "\n"
                    rec.voucher_value_vat += 9350
                if (values.id == 7):
                    rec.voucher_isurance_objective += "To ensure that the enterprise is governed by a set of appropriate policies. " + "\n"
                    rec.voucher_value_vat += 7425
                if (values.id == 8):
                    rec.voucher_isurance_objective += "To provide existing businesses with business improvement and turnaround strategies and plans with regard to HR, production, marketing, purchasing, cost structuring, etc. " + "\n"
                    rec.voucher_value_vat += 11000
                if (values.id == 9):
                    rec.voucher_isurance_objective += "To provide  additional support services to businesses requiring more detailed analysis in order to increase sales and market share. " + "\n"
                    rec.voucher_value_vat += 13200
                if (values.id == 10):
                    rec.voucher_isurance_objective += "To ensure that the entrepreneur is able to set up an administration system to effectively start and manage a business." + "\n"
                    rec.voucher_value_vat += 13200
                if (values.id == 11):
                    rec.voucher_isurance_objective += "To ensure that the business has an adequate accounting system, capable of producing the key management information and controls in the required format, timeously and cost effectively. " + "\n"
                    rec.voucher_value_vat += 8800
                if (values.id == 12):
                    rec.voucher_isurance_objective += "To ensure that the entrepreneur has adequate control  of the payroll system in terms of personnel costs and rewards and complies with statutory requirements. " + "\n"
                    rec.voucher_value_vat += 7425

        data_object = self.env['business.development.assistance'].search([])

    expected_turn_over_hidden_value = fields.Char(string="expected_turn_over_hidden_value",
                                                  compute=get_expected_turn_over_hidden_value)

    serial_number = fields.Char('Serial #')
    # branch_id = fields.Many2one('res.branch', string='Branch Name')
    application_date = fields.Date('Date of Application', default=fields.Date.today())
    client_gr_number = fields.Char('GR Number')
    client_bsc_number = fields.Char('BSC Number')
    applicant_id = fields.Many2one('youth.enquiry', string='Applicant')
    status = fields.Selection(
        [('new', 'New'), ('appointment_drafted', 'Appointment Drafted'), ('assessment_report', 'Assessment Reported'),
         ('recommended', 'Recommended'), ('approved', 'Approved'), ('voucher_isurance', 'Voucher Issuance'), ('work_plan', 'Work Plan'),
         ('work_plan_submitted', 'Work Plan Submitted'), ('submitted_product', 'Submitted Product'),
         ('client_review', 'Client Review'), ('nyda_review', 'NYDA Review'),
         ('bda_review', 'BDA Review'), ('bdo_review', 'BDO Review'),('pc_review', 'PC Review'),
         ('branch_manager_review', 'Branch Manager Review'), ('ho_admin_review', 'HO Admin Review'),
         ('qa_officer_review', 'QA Officer Review'),('ed_manager_review', 'ED Manager Review'),
         ('nyda_head_office', 'NYDA Head Office Review'), ('send_payment_reciept', 'Send Payment Reciept'),
         ('post_disbursement_done', 'Post Disbursement Done'),
         ('pending_payment', 'Pending Payment'), ('payment_completed', 'Payment Posted'), ('payment_released', 'Payment Released'),
         ('link_mkl_database', 'Link MKL Database'), ('decline', 'Declined'), ('cancelled', 'Cancelled'), ('Legacy', 'Legacy')],
        default='new', string="status")

    # HIDDEN FIELD FOR GETTING BENIFICIARY ID FROM USER APPLICATION

    beneficiary_id = fields.Many2one('youth.enquiry', string="Beneficiary")
    user_id = fields.Many2one('res.users', string="User Id", related='beneficiary_id.user_id')
    branch_id = fields.Many2one('res.branch', string="Branch", related='beneficiary_id.nearest_branch')

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
    geographical_type = fields.Selection([('urban', 'Urban'), ('peri_urban', 'Peri Urban'),
                                          ('rural_villages', 'Rural Area-Villages'),
                                          ('rural_farms', 'Rural Area-Farms'),
                                          ('informa_settlement', 'Informa Settlement')],
                                         string="Geographical Type")
    formal_qualification = fields.Char('Formal Qualifications')
    trainings_attended = fields.Text('Training Courses Attended')
    next_of_kin = fields.Char('Next of Kin')
    relative_physical_address = fields.Text('Physical Address')
    relative_mobile = fields.Char('Cell Number')
    relationship = fields.Char('Relationship')

    # entrepreneurial status
    existing_business = fields.Boolean('Do you have an existing business that is currently in operation?')
    business_idea = fields.Boolean('Do you Have a business idea?')
    no_business = fields.Boolean('Do you have any business Idea/ or Have not started a business?')

    entrepreneurial_training = fields.Boolean('Have you ever received any Entrepreneurship Development Training?')
    job_creation_info_ids = fields.One2many('job.creation.information', 'voucher_application_id',
                                            string="Job Creation Information")
    business_start_reason_ids = fields.Many2many('business.start.reason', 'business_start_reason_1', 'business_type_1',
                                                 'reson_type_1', string="Why do you want to start a business?")
    business_start_reason_char = fields.Char('Specify Other Reasons.')
    business_goals = fields.Text('Please describe the goals you want to achieve in business')
    business_experience = fields.Text(
        'What type of business experience do you have and what type of business do you want to start?')
    expertise_in_business = fields.Text(
        'What knowledge or expertise do you have that is relevant to the proposed business?')

    # Start-up Details
    startup_business_name = fields.Char('Business Name')
    startup_business_type = fields.Char('Please explain what you do in your business')
    startup_business_sector_ids = fields.Many2many('mentor.sectors', 'existing_business_sector_1', 'mentor_1',
                                                   'sector_1',
                                                   string="Please indicate the Sector in which your business is operating:")
    startup_business_sector_char = fields.Char('Specify Other Sectors.')
    startup_legal_entity_ids = fields.Many2many('legal.entity', 'existing_legal_entity_1', 'legal_1', 'entity1',
                                                string='Please indicate the Legal Entity in which your business is operating:')
    startup_legal_entity_char = fields.Char('Specify Other Entity')
    startup_business_start_reason_ids = fields.Many2many('business.start.reason', 'startup_business_start_reason_2',
                                                         'business_type_2', 'reson_type_2',
                                                         string="Why do you want to start a business?")
    startup_business_start_reason_char = fields.Char('Specify Other Reasons.')

    startup_idea_description_type_of_business = fields.Text('(a) The type of business')
    startup_idea_description_business_need_satisfy = fields.Text('(b) The need the business seeks to satisfy')
    startup_idea_description_potential_customers = fields.Text('(c) Who your potential customers are?')
    startup_idea_description_operate_business = fields.Text('(d)  Where you will operate the business from?')
    startup_idea_description_operate_product_servivces = fields.Text(
        '(e) How you will deliver your product or service?')

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
    ownership_status_ids = fields.One2many('business.ownership.status', 'voucher_application_id_ownership',
                                           string="Please indicate the Ownership status in your business :")
    total_status_ownership_percent = fields.Float(string="Total Ownership Percentage(%)",
                                                  compute=get_total_status_ownership_percent)

    # Grant Existing Business
    existing_business_name = fields.Char("Business Name")
    existing_business_type = fields.Char('Business Type')
    existing_business_sector_ids = fields.Many2many('business.sector', 'existing_business_sector_2', 'mentor_2',
                                                    'sector_2',
                                                    string='1. Please indicate the Sector in which your business is operating:')
    existing_business_sector_char = fields.Char('Specify Other')
    existing_legal_entity_ids = fields.Many2many('legal.entity', 'existing_legal_entity_2', 'legal_2', 'entity2',
                                                 string='2. Please indicate the Legal Entity in which your business is operating:')
    existing_legal_entity_char = fields.Char('Specify Other Entity')
    existing_business_start_reason_ids = fields.Many2many('business.start.reason', 'startup_business_start_reason_3',
                                                          'business_type_3', 'reson_type_3',
                                                          string="3. Why do you want to start a business?")
    existing_business_start_reason_char = fields.Char('Specify Other Reasons.')

    # existing_idea_description = fields.Text(
    #     '4. Please give a brief description of the idea in terms of:(a) the type of business; (b) the need the business addresses (c) who your customers are; (d) where you operate the business from; and (e) how you deliver your products or services. ')

    existing_idea_description_type_of_business = fields.Text('(a) The type of business')
    existing_idea_description_business_need_satisfy = fields.Text('(b) The need the business seeks to satisfy')
    existing_idea_description_potential_customers = fields.Text('(c) Who your potential customers are?')
    existing_idea_description_operate_business = fields.Text('(d)  Where you will operate the business from?')
    existing_idea_description_operate_product_servivces = fields.Text(
        '(e) How you will deliver your product or service?')

    business_running_time = fields.Selection([('lt20', 'Less than 12 months'),
                                              ('ottyears', '1 - 2 Years'),
                                              ('ttfyears', '3 - 4 Years'),
                                              ('ftfyears', '4 - 5 Years'),
                                              ('ftsyears', '5 - 6 Years'),
                                              ('stsyears', '6 - 7 Years'),
                                              ('ettyears', '8 - 10 Years'),
                                              ('mttyears', 'More than 10')],
                                             string="5. How long has the business been in operation and trading?")
    count_employees = fields.Integer(string='6. How many people (including yourself) are employed in the business?')
    change_in_emp_count = fields.Selection([('increased', 'Increased'),
                                            ('decreased', 'Decreased'),
                                            ('no_change', 'No Change')],
                                           string="7. Has there been a change in the number of people employed in the business over the last 12 months?")
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
                                                string="8. Please provide an estimate of your annual turnover (total amount of income)")
    change_in_turnover = fields.Selection([('increased', 'Increased'),
                                           ('decreased', 'Decreased'),
                                           ('no_change', 'No Change')],
                                          string="9. Has there been a change in the turnover of the business over the last 12 months?")
    change_in_turnover_reason = fields.Char('Reason')
    separate_bank_account = fields.Boolean('10. Do you have a separate bank account for the business?')
    business_start_method = fields.Selection([('myself', 'I started it myself'),
                                              ('bought', 'I bought Business'),
                                              ('with_partner_friend',
                                               'I started the business with a partner(s)/ friend(s)'),
                                              ('overtook_from_family', 'I took it over from someone in the family'),
                                              ('business_start_method_other', 'Other')],
                                             string="11. Please indicate how you started the business : ")
    business_start_monetary_id = fields.Many2one('business.start.monetary',
                                                 string="12. Where did you get the money to start your business?")
    business_operate_premises_id = fields.Many2one('business.operate.premises',
                                                   string="13. Describe the premises your business operates from : ")
    business_operate_premises_char = fields.Char("Other")
    business_premise = fields.Selection([('own', 'Own'),
                                         ('rent', 'Rent')],
                                        string="14. Do you own or rent the premises? ")
    business_area_description = fields.Text('15. Please describe the area in which the business operates : ')
    business_geographical_location_id = fields.Many2one('business.geographical.location',
                                                        string="16.1 Geographical Location")
    business_sector_id = fields.Many2one('business.sector', string="16.2 Type of Business Sector")
    business_sector_char = fields.Char('Specify Other')
    growth_business_sector = fields.Selection([('growing', 'Growing'),
                                               ('growing_moderate', 'Growing Moderately'),
                                               ('growing_strongly', 'Growing Strongly'),
                                               ('in_decline', 'In Decline')],
                                              string="17. How would you describe the growth of the industry sector in which you operate?")
    business_comply_industry = fields.Selection([('yes', 'Yes'),
                                                 ('no', 'No'),
                                                 ('not_sure', 'Not Sure'),
                                                 ('none_applicable', 'None Applicable')],
                                                string="18. Does your business comply with industry registration requirements?")
    startup_involvement = fields.Selection([('only_current', 'Only this One'),
                                            ('two', '2'),
                                            ('three', '3'),
                                            ('more_than_three', 'More than 3')],
                                           string="19. How many business start-ups have you been involved in?")
    previous_work_on_industry = fields.Boolean(
        '20. Did you previously work in the industry sector or type of business you currently run ? ')
    previous_work_on_industry_duration = fields.Selection([('lt1year', 'Less than 1 year'),
                                                           ('tttyears', '2-3 years'),
                                                           ('ttfyears', '3-5 years'),
                                                           ('mtfyears', 'More than 5 years')],
                                                          string="For how long?")
    business_management_experiance = fields.Selection([('lt1year', 'Less than 1 year'),
                                                       ('tttyears', '2-3 years'),
                                                       ('ttfyears', '3-5 years'),
                                                       ('mtfyears', 'More than 5 years')],
                                                      string="21. How many years of business management experience do you have?")
    future_business_goals = fields.Text('22. Please describe your business goals for the future : ')
    # for EXISTING BUSINESS section
    business_development_assistance_ids = fields.Many2many('business.development.assistance',
                                                           string="23. Please indicate what type of business development assistance you need : ")
    business_assistance_improvements = fields.Text(
        '24. Describe how this assistance is likely to improve your business: ')
    able_invest_resource = fields.Boolean(
        '25. Are you able to investment time, financial and other resources in improving your business?')
    able_invest_resource_description = fields.Text('Explain further : ')

    # ------------
    # for start-up  section
    business_development_assistance_startup_ids = fields.Many2many('business.development.assistance',
                                                                   string="Please indicate what type of business development assistance you need : ")
    business_assistance_improvements_startup_ids = fields.Text(
        'Describe how this assistance is likely to improve your business: ')
    able_invest_resource_startup_ids = fields.Boolean(
        'Are you able to investment time, financial and other resources in improving your business?')
    able_invest_resource_description_startup_ids = fields.Text('Explain further : ')

    # ------------------
    # for Business Ideasection
    business_development_assistance_business_idea_ids = fields.Many2many('business.development.assistance',
                                                                         string="Please indicate what type of business development assistance you need : ")
    business_assistance_improvements_business_idea = fields.Text(
        'Describe how this assistance is likely to improve your business: ')
    able_invest_resource_business_idea = fields.Boolean(
        'Are you able to investment time, financial and other resources in improving your business?')
    able_invest_resource_description_business_idea = fields.Text('Explain further : ')

    # ----------------------

    business_development_assistance = fields.Many2many('business.operate.premises',
                                                       string="Please indicate what type of business development assistance you need:")

    business_ownership_status_ids = fields.One2many('business.ownership.status',
                                                    'voucher_application_id_business_ownership',
                                                    string="26. Please indicate the Ownership status in your business :")
    total_business_ownership_percent = fields.Float(string="Total Ownership Percentage(%)",
                                                    compute=get_total_business_ownership_percent)

    # Supporting Document
    identity_document_1 = fields.Binary(string='Identity Document 1')
    identity_document_1_name = fields.Char(string='Identity Document 1')
    identity_document_2 = fields.Binary(string='Identity Document 2')
    identity_document_2_name = fields.Char(string='Identity Document 2')
    identity_document_3 = fields.Binary(string='Identity Document 3')
    identity_document_3_name = fields.Char(string='Identity Document 3')
    proof_of_residence = fields.Binary(string='Proof of Residence')
    proof_of_residence_name = fields.Char(string='Proof of Residence')
    company_registration = fields.Binary(string='Copy of Company Registration from CIPC')
    company_registration_name = fields.Char(string='Copy of Company Registration from CIPC')
    company_profile = fields.Binary(string='Company Profile')
    company_profile_name = fields.Char(string=' Company Profile')
    current_employees = fields.Binary(string='Detailed list of the current employees')
    current_employees_name = fields.Char(string='Detailed list of the current employees')
    other_doc = fields.Binary(string='Any other document that might be required')
    other_doc_name = fields.Char(string='Any other document that might be required')

    # Appointment Schedule
    user_name = fields.Char(string="Name")
    bdo_name = fields.Many2one('res.users', string="BDO Assigned", readonly=True)
    appointment_date = fields.Datetime(string="Appointment Date")

    # Voucher Isurance Page Fields
    work_plan_report = fields.Binary(string="Submit Work Plan Report")
    work_plan_report_name = fields.Char('File Name')
    product_inline_bcs_approved = fields.Binary(
        string="Product Inline with Approved BCS Product and Service Guidelines")
    product_inline_bcs_approved_name = fields.Char('File Name')

    service_provider = fields.Many2one('partner.enquiry', string="Service Provider")
    company_reg_number = fields.Char('Company Register Number', related='service_provider.company_reg_number')
    cell_phone_number = fields.Char('Cell Phone Number', related='service_provider.cell_phone_number')
    nearest_branch = fields.Many2one('res.branch', string="Nearest Branch", related='service_provider.nearest_branch')
    job_title = fields.Char('Job Title', related='service_provider.job_title')

    partner_user_id = fields.Many2one('res.users', related='service_provider.user_id')

    service_provider_email = fields.Char('Email', related='service_provider.email')
    service_enable_date = fields.Datetime(string="Service Enabled Date")
    voucher_isurance_objective = fields.Text("Voucher Isurance Objective", compute=compute_voucher_value, store=True)
    voucher_value_vat = fields.Float("Voucher value excl VAT", compute=compute_voucher_value, store=True)

    # Product Submit Wizard Fields
    product_doc = fields.Binary('Product')
    product_doc_name = fields.Char('File Name')
    invoice_doc = fields.Binary('Invoice')
    invoice_doc_name = fields.Char('File Name')
    timesheet_doc = fields.Binary('Timesheet')
    timesheet_doc_name = fields.Char('File Name')

    # Voucher Proof of Payment Submit Wizard Fields
    proof_of_payment = fields.Binary(string='Proof Of Payment')
    proof_of_payment_name = fields.Char(string='File Name')
    proof_of_payment_date = fields.Date(string='Date')
    payment_approval_date = fields.Date(string='Payment Approval Date')
    service_provider_id = fields.Many2one('res.users', string="Payment Service Provider", domain=lambda self: [
        ("groups_id", "=", self.env.ref("client_management.group_partner_service_provider").id)])
    finance_admin_id = fields.Many2one('res.users', string="Finance Administrator", domain=lambda self: [
        ("groups_id", "=", self.env.ref("nyda_grant_and_voucher.group_grant_voucher_fa").id)])

    # Voucher Post Disbursement Submit Wizard Fields
    post_disbursement = fields.Binary(string='Proof Disbursement')
    post_disbursement_name = fields.Char(string='File Name')

    # BDO Rejection Reason
    bdo_reason_text = fields.Text('Reason for BDO Rejection')

    # INTERNAL REPORT PAGE FIELDS
    # work_plan_report = fields.Binary(string="Submit Work Plan Report")
    # work_plan_report_name = fields.Char('File Name')

    assessment_report = fields.Binary(string="Assessment Report")
    assessment_report_name = fields.Char('File Name')

    # product_inline_bcs_approved = fields.Binary(
    #     string="Product Inline with Approved BCS Product and Service Guidelines")
    # product_inline_bcs_approved_name = fields.Char('File Name')

    client_approve_reject_state = fields.Selection(string="Client Approve/Reject",
                                                   selection=[('approve', 'Approve'), ('reject', 'Reject'), ('query', 'Query')])
    client_approve_reject_description = fields.Text(string="Explain in brief, reasons of your decision")

    client_redemption_pack = fields.Binary(string="Submit Work Plan Report")
    client_redemption_pack_name = fields.Char('File Name')

    # NYDA Branch Review
    nyda_bda_bool = fields.Boolean(string='NYDA BDA Review')
    nyda_bdo_bool = fields.Boolean(string='NYDA BDO Review')
    nyda_pc_bc_bool = fields.Boolean(string='NYDA PC/BC Review')

    nyda_bcs_bool = fields.Boolean(string='NYDA BCS Review')
    nyda_qao_bool = fields.Boolean(string='NYDA QAO Review')
    nyda_edm_bool = fields.Boolean(string='NYDA EDM Review')

    # query = fields.Text(string='Please Write Below If You Have Any Query')
    query_record_ids = fields.One2many('any.query.record', 'voucher_id',
                                       string="Query")

    cancel_voucher_reason = fields.Text(string='Reason To Cancel')
    is_valid = fields.Boolean(string="Is Valid", default=True)
    # partner_service_ids = fields.One2many('partner.service', 'voucher_application_id', string='Services Offered')

    recommendationnote = fields.Char(string='Recommendation Note')
    reject_reason_pcbc = fields.Text(string='Rejection Reason By PC/BC')
    query_pcbc = fields.Text(string='Query By PC/BC')

    rejection_reason_all_ids = fields.One2many('rejection.reason.all', 'voucher_id', string='Rejection Reason For All')
    #Undefined fields in view
    x_attendance_register = fields.Binary(string="Attendance Register")
    x_attendance_register_name = fields.Char(string='Attendance Register')
    x_bda_comments = fields.Text(string='BDA Comments')
    x_bda_state = fields.Selection(string="BDA State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_bdo_comments = fields.Text(string='BDO Comments')
    x_bdo_state = fields.Selection(string="BDO State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_bmt_certificate = fields.Binary(string="BTM Certificate")
    x_bmt_certificate_name = fields.Char(string='Attendance Register')
    x_branch_manager_approval_date = fields.Datetime(string="Branch Manager Date")
    x_branch_manager_comments = fields.Text(string='Branch Manager Comments')
    x_branch_manager_state = fields.Selection(string="Branch Manager State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_ed_manager_comments = fields.Text(string='ED Comments')
    x_ed_manager_state = fields.Selection(string="ED Manager State",
                                   selection=[('Approved', 'Approved'), ('Query Invoice', 'Query Invoice'), ('Query Product', 'Query Product')])
    x_existing_business_sector_id = fields.Many2many('business.sector',relation='x_business_sector_voucher_application_rel',
                                                     column1='voucher_application_id',column2='business_sector_id',store=True,copy=True,string="Existing Business Sector")
    x_finance_submission_date = fields.Datetime(string="Payment Submission Date")
    x_ho_admin_comments = fields.Text(string='HO Admin Comments')
    x_ho_admin_state = fields.Selection(string="HO Admin State",
                                  selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_invoice_date = fields.Datetime(string="Invoice Date")
    x_location = fields.Text(string="Location")
    x_mentor_sector_id = fields.Many2one('mentor.sectors',string="VMS Mentor Sector")
    x_pc_approve_date = fields.Datetime(string="PC Approval date")
    x_pc_bc_comments = fields.Text(string="Comments")
    x_pc_bc_state = fields.Selection(string="PC State",
                                   selection=[('Approved', 'Approved'), ('Decline', 'Decline'), ('Query', 'Query')])
    x_pc_comments = fields.Text(string="PC Comments")
    x_pc_state = fields.Selection(string="PC State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_pc_status = fields.Char(string='PC Status')
    x_qa_officer_comments = fields.Text(string="QA Officer Comments")
    x_qa_officer_state = fields.Selection(string="QA Officer State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_recommended_service = fields.Many2many('business.development.assistance',relation='x_business_development_assistance_voucher_application_rel',
                                                     column1='voucher_application_id',column2='business_development_assistance_id',string="Recommended Service")
    x_service_provider = fields.Many2one('res.partner',string="Service Provider", domain=[('x_voucher_vendor', '=', True)])
    x_service_provider_user_id = fields.Many2one('res.users',related='x_service_provider.user_id',readonly=True, string="Service Provider User", help="The internal user that is in charge of communicating with this contact if any.")
    x_sp_city = fields.Char(related='x_service_provider.city', string='City', readonly=True)
    x_sp_company_email = fields.Char(related='x_service_provider.email', string='Company Email', readonly=True)
    x_sp_company_website = fields.Char(related='x_service_provider.website', string='Company Website', readonly=True)
    x_sp_country_id = fields.Many2one('res.country',related='x_service_provider.country_id',readonly=True, string="Country")
    x_sp_street_address = fields.Char(related='x_service_provider.street', string='Street Address', readonly=True)
    x_sp_zip = fields.Char(related='x_service_provider.zip', string='Zip', readonly=True)
    x_startup_business_sector_id = fields.Many2many('business.sector',relation='x_business_sector_voucher_application_rel',
                                                     column1='voucher_application_id',column2='business_sector_id',string="Startup Business Sector")
    x_voucher_issued = fields.Many2one('voucher.isurance', string="Voucher Issued")
    x_voucher_end_date = fields.Date(related="x_voucher_issued.end_date",string="Voucher End Date")
    x_voucher_number = fields.Char(string='Voucher Number')
    x_voucher_reissue_end_date = fields.Date(string="Re-Issue End Date")
    x_voucher_reissue_start_date = fields.Date(string="Re-Issue Start date")
    x_voucher_start_date = fields.Date(related='x_voucher_issued.start_date',string="Start Date")
    x_voucher_value = fields.Integer(related='x_recommended_service.voucher_value', string='Voucher Value')
    #fields for client.approve.reject.wizard


    def check_validity(self):
        all_rec = self.env['voucher.application'].sudo().search([])
        if all_rec:
            for rec in all_rec:
                cdate = datetime.strptime(rec.create_date, '%Y-%m-%d %H:%M:%S')
                diff = datetime.now() - cdate
                if rec.is_valid and diff.days > 90:
                    rec.is_valid = False

    # @api.onchange('service_provider')
    # def service_all_by_provider(self):
    #     print('===========', self.service_provider.partner_service_ids.ids)
    #     print('===========', self)
    #
    #     self.partner_service_ids = [(6, 0, self.service_provider.partner_service_ids.ids)]

    def approve_payment(self):
        self.status = 'pending_payment'
        if self.status == 'pending_payment':
            approval_mail = self.env.ref('nyda_grant_and_voucher.send_fa_approve_mail_template')
            print(approval_mail, self, self.id)
            approval_mail.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login
                                    })

    def process_payment(self):
        self.status = 'payment_completed'
        self.payment_approval_date = datetime.now()

    @api.model
    def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['serial_number'] = self.env['ir.sequence'].next_by_code('voucher.application')
            print('---------\n\n\n', values['serial_number'])
        record_obj = super(VoucherApplication, self).create(values)
        print('----record_obj-----\n\n\n', record_obj)
        if record_obj.email:
            user_confirmation_mail_template = self.env.ref('nyda_grant_and_voucher.user_confirmation_mail_template')
            print('--=-user_confirmation_mail_template=====', user_confirmation_mail_template)
            print('--------\n\n', )
            user_confirmation_mail_template.with_context(user=self.env.user).send_mail(record_obj.id, force_send=True)
        '''
        for record_mail in self.env['res.users'].search([('branch_id','=',self.env.user.branch_id)]).has_group('nyda_grant_and_voucher.group_grant_voucher_bda'):
            bda_confirmation_mail_template = self.env.ref('nyda_grant_and_voucher.bda_confirmation_mail_template')
            bda_confirmation_mail_template.with_context(user=self.env.user, bda=record_mail).send_mail(record_obj.id, force_send=True)
        '''
        return record_obj

    @api.multi
    def btn_voucher_isurance(self):
        action = self.sudo().env.ref(
            'nyda_grant_and_voucher.voucher_isurance_wizard_action').read()[0]
        for rec in self:
            voucher_id = self.env['voucher.isurance'].search([('voucher_applicant_id', '=', rec.id)], limit=1)
            action['views'] = [(False, u'form')]
            action['res_id'] = voucher_id.id or False
            return action

    # ---------Method for changing Appointment drafted to Recommended State and sends mail to pc_bc groups.
    @api.multi
    def set_recommend(self):
        """ Sets state to recomended. Add logic if need anything once application is moved to reject state. """
        for rec in self:
            rec.write({'status': 'recommended'})

        email_list = []
        if self.status == 'recommended':
            body = "<html>\
                        <body><p>Recomended Application " + str(self.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            #Ammended Sep 15, 2021 : User must be in group and in branch similar to voucher application
            #for record_mail in self.env['res.users'].search([]):
            #    if record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_pc_bc') and record_mail.email:
            #        email_list.append(str(record_mail.email))
            '''
            for record_mail in self.env['res.users'].search([]):
                if record_mail.email:
                    if record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_pc_bc') and (record_mail.branch_id == self.branch_id):
                        email_list.append(str(record_mail.email))
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Application for " + str(self.name) + " with Serial Number: " + str(self.serial_number) + " has been recommended.</p>\
                                <p>Now you can proceed to Approve/Decline/Refer application for Voucher Programme provided by NYDA.</p>\
                                <p>Please contact the administration if you have any query.</p><br></br>\
                                <p>Regards, </p>\
                                <p>NYDA</p>"

            body += "</body></html>"
            if email_list and mail_server_ids.smtp_user:
                email_to = ','.join(email_list)
                template = self.env['mail.mail'].create({
                    'subject': 'Recommended Application',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
            '''
        return {
            'type': 'ir.actions.act_window',
            'name': 'Recommendation Note',
            'res_model': 'recommendation.note',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def set_approve(self):
        """ Sets state to approved and sends mail to applicant. Add logic if need anything once application is moved to approved state. """
        for rec in self:
            rec.write({'status': 'approved', 'x_pc_status': 'Approved'})

        mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_approval_mail_template')
        if mail_template_id and self.status == 'approved':
            mail_template_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)

    @api.multi
    def set_decline(self):
        """ Sets state to Declied and sends mail to applicant. Add logic if need anything once application is moved to reject state. """
        for rec in self:
            rec.write({'status': 'decline', 'x_pc_status': 'Declined'})

            mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_declined_mail_template')
            if mail_template_id and self.status == 'decline':
                mail_template_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)

    @api.multi
    def set_nyda_bda_bool(self):
        """ Sets nyda_bda_bool to True which means NYDA BDA approve review"""
        for rec in self:
            rec.write({'nyda_bda_bool': 'True'})

    @api.multi
    def set_nyda_bda_r_bool(self):
        """ Sets nyda_bda_bool to False which means the documents must be submitted again"""
        for rec in self:
            rec.write({'status': 'voucher_isurance'})
            rec.write({'nyda_bda_bool': True})

    # @api.multi
    # def set_nyda_bda_(self):
    #     """ Sets nyda_bda_bool to True which means NYDA BDA approve review"""
    #     for rec in self:
    #         rec.write({'nyda_bda_bool': True})

    @api.multi
    def set_nyda_bdo_bool(self):
        """ Sets nyda_bdo_bool to True which means NYDA BDO approve review"""
        for rec in self:
            rec.write({'nyda_bdo_bool': True})

    @api.multi
    def set_cancelled(self):
        """ Sets nyda_bdo_bool to True which means NYDA BDO approve review"""
        for rec in self:
            rec.write({'status': 'cancelled'})

    @api.multi
    def set_nyda_bdo_r_bool(self):
        """ Sets nyda_bda_bool to False which means NYDA BDA has to review again"""
        for rec in self:
            rec.write({'nyda_bda_bool': False})

    @api.multi
    def set_nyda_pc_bc_bool(self):
        """ Sets nyda_pc_bc_bool to True which means NYDA PC/BC approve review"""
        for rec in self:
            rec.write({'nyda_pc_bc_bool': 'True', 'status': 'nyda_review'})

            mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_approval_mail_template')
            if mail_template_id and self.status == 'nyda_review':
                mail_template_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)

    @api.multi
    def set_nyda_pc_bc_r_bool(self):
        """ Sets nyda_pc_bc_bool to True which means NYDA PC/BC approve review"""
        for rec in self:
            rec.write({'nyda_bdo_bool': False})

            mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_approval_mail_template')
            if mail_template_id and self.nyda_bdo_bool == False:
                mail_template_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Rejection Reason',
            'res_model': 'reject.reason.pcbc',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def rating_proceed(self):
        """ Transitions the voucher application after service rating"""
        for rec in self:
            rec.write({'status': 'submitted_product'})

    @api.multi
    def set_nyda_bcs_bool(self):
        """ Sets nyda_bda_bool to True which means NYDA BDA approve review"""
        for rec in self:
            rec.write({'nyda_bcs_bool': 'True'})


    @api.multi
    def set_nyda_bcs_r_bool(self):
        """ Sets nyda_bda_bool to True which means NYDA BDA approve review"""
        for rec in self:
            rec.write({'nyda_pc_bc_bool': False, 'status': 'client_review'})


    @api.multi
    def set_nyda_qao_bool(self):
        """ Sets nyda_bdo_bool to True which means NYDA BDO approve review"""
        for rec in self:
            rec.write({'nyda_qao_bool': 'True'})


    @api.multi
    def set_nyda_qao_r_bool(self):
        """ Sets nyda_bdo_bool to True which means NYDA BDO approve review"""
        for rec in self:
            rec.write({'nyda_bcs_bool': False})


    @api.multi
    def set_nyda_edm_bool(self):
        """ Sets nyda_pc_bc_bool to True which means NYDA PC/BC approve review"""
        for rec in self:
            rec.write({'nyda_edm_bool': 'True', 'status': 'nyda_head_office'})


    @api.multi
    def set_nyda_edm_r_bool(self):
        """ Sets nyda_pc_bc_bool to True which means NYDA PC/BC approve review"""
        for rec in self:
            rec.write({'nyda_qao_bool': False})


    @api.multi
    def set_mkl_database(self):
        """ Sets state to reject. Add logic if need anything once application is moved to reject state. """

        mkl_beneficiary = self.env['mkl.beneficiary'].create({
            'title': 'Voucher Application - ' + self.serial_number,
            'branch_id': self.branch_id.id,
            'beneficiary_id': self.user_id.id,
            'business_name': self.existing_business_name,
            'contact_person': self.name,
            'contact_details': self.mobile,
        })
        # grant_edm_approval_mail_template_id = self.env.ref('nyda_grant_and_voucher.grant_edm_approval_mail_template')
        # grant_edm_approval_mail_template_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)

        for rec in self:
            rec.write({'status': 'link_mkl_database'})

        if self.status == 'link_mkl_database':

            base_url = http.request.env['ir.config_parameter'].get_param('web.base.url')
            base_url += '/web/login?db={}#id={}&view_type=form&model=mkl.beneficiary'.format(self.env.cr.dbname,
                                                                                             mkl_beneficiary.id)
            # ___________________--------SENDS EMAIL LINK TO USER FOR SEEEING HIS RECORD WHEN EDM APPROVE

            mail_template_id = self.env.ref('nyda_grant_and_voucher.link_mkl_db_mail_template')
            if mail_template_id and self.status == 'link_mkl_database':
                mail_template_id.with_context(user=self.env.user, base_url=base_url).send_mail(self.id, force_send=True)


# ----------Empty for now
    @api.multi
    def set_refer(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Any Query',
            'res_model': 'query.pcbc',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }


# ----------------------------->>>>>>>>>>>>>> Display name+serial number
# @api.multi
# def name_get(self):
#     res = []
#     for rec in self:
#         if rec.serial_number or rec.name:
#             namedisplay = rec.serial_number + "-" + rec.name
#             res.append((rec.id, namedisplay))
#         return res

# ----------Creates wizard for scheduling appointment and sends mail to applicant and corresponding BDO
    @api.multi
    def schedule_appointment_wizard(self):
        print("\n\n\n ", self, self.id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Schedule Appointment Wizard',
            'res_model': 'schedule.appointment.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id, 'default_model': 'voucher.application'}
        }


# Opens A wizard for selecting service provider to applicant
    @api.multi
    def select_service_provider(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Service Provider Wizard',
            'res_model': 'select.service.provider.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }


# ----------------- OPENS WIZARD FOR SUBMITIING WORK PLAN AND STATUS CHANGING TO WORK PLAN SUBMITTED
    @api.multi
    def submit_work_plan(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Work Plan Submit Wizard',
            'res_model': 'work.plan.submit.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }


    @api.multi
    def client_approve_reject(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Client Approve/Reject Wizard',
            'res_model': 'client.approve.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_grant_and_voucher.client_approve_reject_wizard_form').id),
            'target': 'new',
        }


    @api.multi
    def pc_bc_review(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Coordinator Review',
            'res_model': 'client.approve.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_pc_bc_review_form').id),
            'target': 'new',
        }

    @api.multi
    def bda_review(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'BDA Review',
            'res_model': 'client.approve.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_bda_review_form').id),
            'target': 'new',
        }

    @api.multi
    def bdo_review(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'BDO Review',
            'res_model': 'client.approve.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_bdo_review_form').id),
            'target': 'new',
        }

    @api.multi
    def pc_review(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'PC Review',
            'res_model': 'client.approve.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_pc_review_form').id),
            'target': 'new',
        }

    @api.multi
    def branch_manager_review(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Branch Manager Review',
            'res_model': 'client.approve.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_branch_manager_review_form').id),
            'target': 'new',
        }

    @api.multi
    def ho_admin_review(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Head Officer Review',
            'res_model': 'client.approve.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_ho_admin_review_form').id),
            'target': 'new',
        }

    @api.multi
    def qa_officer_review(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'QA Officer Review',
            'res_model': 'client.approve.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_qa_officer_review_form').id),
            'target': 'new',
        }

    @api.multi
    def ed_manager_review(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'ED Manager Review',
            'res_model': 'client.approve.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_ed_manager_review_form').id),
            'target': 'new',
        }

    @api.multi
    def assessment_voucher(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Voucher Assessment',
            'res_model': 'voucher.assessment',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_voucher_application_id': self.id}
        }

    @api.multi
    def btn_sp_assessment(self):
        order = self.env['voucher.assessment'].search([('voucher_application_id', '=', self.id)])
        action = self.sudo().env.ref('nyda_grant_and_voucher.action_voucher_sp_assessment').read()[0]
        if len(order) == 1:
            action['views'] = [(self.env.ref('nyda_grant_and_voucher.view_voucher_service_provider_form').id, 'form')]
            action['res_id'] = order.id
        elif len(order) > 1:
            action['domain'] = [('id', '=', order.ids)]
            print('doain\n\n\n\n', action['domain'])
        else:
            return {'name': 'nyda_grant_and_voucher.view_voucher_service_provider_form',
                    'view_type': 'form',
                    'view_mode': 'tree',
                    'views': [(self.env.ref('nyda_grant_and_voucher.view_voucher_service_provider_form').id, 'form')],
                    'res_model': 'voucher.assessment',
                    'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_service_provider_form').id),
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                    'context': {'default_voucher_application_id': self.id}
                    }
        return action


    @api.multi
    def btn_voucher_assessment(self):
        order = self.env['voucher.assessment'].search([('voucher_application_id', '=', self.id)])
        action = self.sudo().env.ref('nyda_grant_and_voucher.action_voucher_assessment').read()[0]
        if len(order) == 1:
            action['views'] = [(self.env.ref('nyda_grant_and_voucher.view_voucher_assessment_form').id, 'form')]
            action['res_id'] = order.id
        elif len(order) > 1:
            action['domain'] = [('id', '=', order.ids)]
            print('doain\n\n\n\n', action['domain'])
        else:
            return {'name': 'nyda_grant_and_voucher.view_voucher_assessment_form',
                    'view_type': 'form',
                    'view_mode': 'tree',
                    'views': [(self.env.ref('nyda_grant_and_voucher.view_voucher_assessment_form').id, 'form')],
                    'res_model': 'voucher.assessment',
                    'view_id': (self.env.ref('nyda_grant_and_voucher.view_voucher_assessment_form').id),
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                    'context': {'default_voucher_application_id': self.id}
                    }
        return action

    @api.multi
    def btn_service_provider(self):
        for app in self:
            order = self.env['partner.enquiry'].sudo().search(
                [('enquire_type', '=', 'become-service-provider'), ('state', '=', 'accepted'),
                 (['partner_service_ids', 'in', app.business_development_assistance_ids.ids])])

        action = self.sudo().env.ref('client_management.action_partner_enquiry').read()[0]

        if len(order) >= 1:
            action['domain'] = [('id', '=', order.ids)]
            action['views'] = [(self.env.ref('client_management.view_partner_enquiry_tree').id, 'tree')]
            print('doain\n\n\n\n', action['domain'])

        return action