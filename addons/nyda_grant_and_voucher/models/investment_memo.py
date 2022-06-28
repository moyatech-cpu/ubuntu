from odoo import fields, models, api, _
from datetime import datetime


class EnterpriseFinance(models.Model):
    _name = 'investment.memo'
    _rec_name = 'business_name'

    @api.multi
    @api.onchange('stock', 'working_capital', 'equipment', 'others_one', 'others_two')
    @api.depends('stock', 'working_capital', 'equipment', 'others_one', 'others_two')
    def get_total_grant(self):
        for rec in self:
            if (rec.stock or rec.working_capital or rec.equipment or rec.others_one or rec.others_two):
                rec.total_grant = rec.stock + rec.working_capital + rec.equipment + rec.others_one + rec.others_two

    @api.multi
    @api.onchange('residential_property', 'motor_vehicle', 'personal_effects', 'cash', 'business_interest',
                  'others_asset')
    @api.depends('residential_property', 'motor_vehicle', 'personal_effects', 'cash', 'business_interest',
                 'others_asset')
    def get_total_asset(self):
        for rec in self:
            if (
                    rec.residential_property or rec.motor_vehicle or rec.personal_effects or rec.cash or rec.business_interest or rec.others_asset):
                rec.total_asset = rec.residential_property + rec.motor_vehicle + rec.personal_effects + rec.cash + rec.business_interest + rec.others_asset

    @api.multi
    @api.onchange('bond', 'hp_balance', 'personal_loan', 'credit_card')
    @api.depends('bond', 'hp_balance', 'personal_loan', 'credit_card')
    def get_total_liabilities(self):
        for rec in self:
            if (rec.bond or rec.hp_balance or rec.personal_loan or rec.credit_card):
                rec.total_liabilities = rec.bond + rec.hp_balance + rec.personal_loan + rec.credit_card

    @api.multi
    @api.depends('total_asset', 'total_liabilities')
    @api.onchange('total_asset', 'total_liabilities')
    def get_net_total(self):
        for rec in self:
            if rec.total_asset or rec.total_liabilities:
                rec.net_total = rec.total_asset - rec.total_liabilities

    @api.multi
    @api.depends('owner_net_sal', 'spouse_net_sal')
    @api.onchange('owner_net_sal', 'spouse_net_sal')
    def get_total_sal(self):
        for rec in self:
            if rec.owner_net_sal or rec.spouse_net_sal:
                rec.total_sal = rec.owner_net_sal + rec.spouse_net_sal

    @api.multi
    @api.depends('rent', 'water_light', 'groceries', 'clothing', 'medical_expences', 'membership', 'school_fees',
                 'dstv', 'insurance_policy', 'furniture_accounts', 'travel', 'telephone', 'entertainment')
    @api.onchange('rent', 'water_light', 'groceries', 'clothing', 'medical_expences', 'membership', 'school_fees',
                  'dstv', 'insurance_policy', 'furniture_accounts', 'travel', 'telephone', 'entertainment')
    def get_total_expen(self):
        for rec in self:
            if (
                    rec.rent or rec.water_light or rec.groceries or rec.clothing or rec.medical_expences or rec.membership or
                    rec.school_fees or rec.dstv or rec.insurance_policy or rec.furniture_accounts or rec.travel or
                    rec.telephone or rec.entertainment):
                rec.total_expen = rec.rent + rec.water_light + rec.groceries + rec.clothing + rec.medical_expences \
                                  + rec.membership + rec.school_fees + rec.dstv + rec.insurance_policy + rec.furniture_accounts \
                                  + rec.travel + rec.telephone + rec.entertainment

    @api.multi
    @api.depends('total_sal', 'total_expen')
    @api.onchange('total_sal', 'total_expen')
    def get_disposable_income(self):
        for rec in self:
            if rec.total_sal or rec.total_expen:
                rec.disposable_income = rec.total_sal - rec.total_expen

    @api.multi
    @api.depends('member_contr', 'nyda_funding')
    @api.onchange('member_contr', 'nyda_funding')
    def get_total_fund(self):
        for rec in self:
            if rec.member_contr or rec.nyda_funding:
                rec.total_fund = rec.member_contr + rec.nyda_funding

    @api.multi
    @api.depends('equipment_fund', 'motor_veh')
    @api.onchange('equipment_fund', 'motor_veh')
    def get_tot_fix_asset(self): #LM. Mahasha 2021/10/06 16:23 def get_total_fix_asset(self)
        for rec in self:
            if rec.equipment_fund or rec.motor_veh:
                rec.tot_fix_asset = rec.equipment_fund + rec.motor_veh

    @api.multi
    @api.depends('rental', 'salaries', 'stock_cap')
    @api.onchange('rental', 'salaries', 'stock_cap')
    def get_tot_work_cap(self):
        for rec in self:
            if (rec.rental or rec.salaries or rec.stock_cap):
                rec.tot_work_cap = rec.rental + rec.salaries + rec.stock_cap

    @api.multi
    @api.depends('tot_fix_asset', 'tot_work_cap')
    @api.onchange('tot_fix_asset', 'tot_work_cap')
    def get_tot_app_funds(self):
        for rec in self:
            if rec.tot_fix_asset or rec.tot_work_cap:
                rec.tot_app_funds = rec.tot_fix_asset + rec.tot_work_cap

    @api.multi
    @api.depends('total_fund', 'tot_app_funds')
    @api.onchange('total_fund', 'tot_app_funds')
    def get_source_app_tot(self):
        for rec in self:
            if rec.total_fund or rec.tot_app_funds:
                rec.source_app_tot = rec.total_fund - rec.tot_app_funds

    @api.multi
    @api.depends('company_individual', 'grant_officer', 'total_grant')
    @api.onchange('company_individual', 'grant_officer', 'total_grant')
    def compute_transaction(self):
        for rec in self:
            if (rec.company_individual or rec.grant_officer or rec.total_grant):
                rec.transaction = str(rec.grant_officer.name) + " approve a grant of " + str(
                    rec.total_grant) + " to " + str(
                    rec.company_individual) + " on the terms and conditions stated under 'Proposed Terms'"

    serial_number = fields.Many2one('grant.application', String="Serial Number", readonly=True)

    business_name = fields.Char(string="Business Name", required='True')
    document_number = fields.Char(string='Document Number', copy='False', readonly='True', index='True',
                                  default=lambda self: _('New'))
    document_present_date = fields.Date(string="Date", default=datetime.today())

    city_area = fields.Char(string="Area")
    province = fields.Many2one('res.country.state', string="Province",
                               domain="[('country_id.name', '=', 'South Africa')]")
    # project_name = fields.Char(string="Project Name")

    company_individual = fields.Selection([('company', 'Company'), ('individual', 'Individual'), ],
                                          string="Company/Individual")
    sector = fields.Many2many('business.sector', string="Sector")
    activity = fields.Char(string="Product/Services offered")
    product = fields.Char(string="Product", default="Grant Programme")
    grant_officer = fields.Many2one('res.users', string="Officer")
    # source = fields.Char(string="Source")
    amount = fields.Float(string="Amount Recommended")
    branch_manager = fields.Many2one('res.users', string="Branch Manager")
    # date = fields.Date(string="Date")
    chairperson = fields.Many2one('res.users', string="Chairperson")

    # PAGE ONE FIELDS

    transaction_overview = fields.Text(string="Transaction Overview")
    project_description = fields.Text(string="Project Description")
    # summary_proposal = fields.Text(string="Summary Proposal")
    stock = fields.Float(string="Stock")
    working_capital = fields.Float(string="Working Capital")
    equipment = fields.Float(string="Equipment")
    others_one = fields.Float(string="Others 1")
    others_two = fields.Float(string="Others 2")
    description_other_one = fields.Text(string='Description of Other 1')
    description_other_two = fields.Text(string='Description of Other 2')
    total_grant = fields.Float(string="Total Grant Required", compute='get_total_grant', store=True)

    # PAGE REPORT FIELDS   ----------------II. POLICY & PROGRAMME FIT

    stg_of_busin = fields.Char(string="Stage of business")
    youth_share_hol = fields.Char(string="Youth shareholding")
    oper_invo = fields.Char(string="Operational involvement")
    grant_size = fields.Float(string="Grant size")
    profitable = fields.Char(string="Profitable")
    nyda_role = fields.Text(string="NYDA Role")
    employement = fields.Char(string="Youth Employement")

    # PAGE TWO FIELDS

    sponser = fields.Char(string="Sponser")
    management_team = fields.Many2one('res.users', string="Mangement Team")
    employees = fields.Many2many('res.users', string="Employees")

    # --------------(SPONSOR’S NAME) PERSONAL BALANCE SHEET:

    residential_property = fields.Float(string="Residential Property")
    motor_vehicle = fields.Float(string="Motor Vehicle")
    personal_effects = fields.Float(string="Personal Effects")
    cash = fields.Float(string="Cash")
    business_interest = fields.Float(string="Business Interest")
    others_asset = fields.Float(string="Others")
    total_asset = fields.Float(string="Total", compute='get_total_asset', store=True)

    bond = fields.Float(string="Bond")
    hp_balance = fields.Float(string="HP balance")
    personal_loan = fields.Float(string="Personal Loan")
    credit_card = fields.Float(string="Credit Card")
    total_liabilities = fields.Float(string="Total", compute='get_total_liabilities', store=True)

    net_total = fields.Float(string="Net Total", compute='get_net_total', store=True)

    # ----------------SPONSOR’S INCOME & EXPENDITURE STATEMENT:

    owner_net_sal = fields.Float(string="Owner's net salary")
    spouse_net_sal = fields.Float(string="Spouse's net salary")
    total_sal = fields.Float(string="Total salary", compute='get_total_sal', store=True)

    rent = fields.Float(string="Rent")
    water_light = fields.Float(string="Water and Lights")
    groceries = fields.Float(string="Groceries")
    clothing = fields.Float(string="Clothing")
    medical_expences = fields.Float(string="Medical expenses")
    membership = fields.Float(string="Membership")
    school_fees = fields.Float(string="School Fees")
    dstv = fields.Float(string="DSTV")
    insurance_policy = fields.Float(string="Insurance Policies")
    furniture_accounts = fields.Float(string="Furniture Accounts")
    travel = fields.Float(string="Travel/Petrol")
    telephone = fields.Float(string="Telephone")
    entertainment = fields.Float(string="Entertainment")

    total_expen = fields.Float(string="Total Expenditure", compute='get_total_expen', store=True)

    disposable_income = fields.Float(string="Disposable Income", compute='get_disposable_income', store=True)

    # --------------------------SOURCE & APPLICATION OF FUNDS

    # ------------------------------->>>>>>>>>>>>> Source of Funds

    member_contr = fields.Float(string="Member's contr")
    nyda_funding = fields.Float(string="NYDA funding")
    total_fund = fields.Float(string="Total Funding", compute='get_total_fund', store=True)

    # ------------------------->>>>>>>>>>>>>>>>>Application of funds

    # -------------------------00000000000000000000000000000>>>>>>>>>>>>>>>>>Fixed assets

    equipment_fund = fields.Float(string="Equipment")
    motor_veh = fields.Float(string="Motor vehicles")
    tot_fix_asset = fields.Float(sring="Total Fixed Assets", compute='get_tot_fix_asset', store=True)

    # -------------------------00000000000000000000000000000>>>>>>>>>>>>>>>>>Working Capital

    rental = fields.Float(string="Rental")
    salaries = fields.Float(string="Salaries")
    stock_cap = fields.Float(string="Stock")
    tot_work_cap = fields.Float(string="Total Working Capital", compute='get_tot_work_cap', store=True)

    tot_app_funds = fields.Float(string="Total Application Funds", compute='get_tot_app_funds', store=True)

    source_app_tot = fields.Float(string="Net Total", compute='get_source_app_tot', store=True)

    # PAGE THREE FEILDS

    grant_amount = fields.Float(string="Grant Amount")
    tenure = fields.Char(string="Tenure", default="2 Years")
    start_date = fields.Date(string="Start date")
    est_due_date = fields.Date(string="Estimated due date")
    add_condit = fields.Text(string="AdditionalConditions")
    disbursement = fields.Text(string="Disbursement",
                               default=" Funds to purchase equipment to be paid directly to the suppliers of equipment."
                                       " The funds for stock to be paid directly to the farmers who will supply the business with livestock."
                                       " The funds to purchase vehicle (truck)to be made directly to the motor vehicle dealer")

    # MARKET REVIEW
    market_review = fields.Text(string="Market Review")

    # PAGE FOUR FIELDS(SWAT ANALYSIS)

    strengths = fields.Text(string="STRENGTHS")
    weakness = fields.Text(string="WEAKNESSES")
    opportunities = fields.Text(string="OPPORTUNITIES")
    threats = fields.Text(string="THREATS")

    # PAGE FIVE FIELDS

    credit_check = fields.Char(string="Credit Check")
    company_check = fields.Text(string="Company Check",
                                default="A company credit check was done and no judgements or defaults reported on the business. A valid tax clearance certificate for the business has been provided.")
    business_premises = fields.Char(string="Business Premises")
    human_resource = fields.Char(string="Human Resource")
    compliance = fields.Char(string="Compliance")
    int_oth_pro_ser = fields.Char(string="Integration with other NYDA products and services")

    # PAGE SIX FIELDS

    financial_control = fields.Char(string="Financial controls")
    pilferage = fields.Char(string="Pilferage")
    stock_obsolescence = fields.Char(string="Stock Obsolescence")

    # PAGE SEVEN FIELDS

    revenues = fields.Char(string="Revenues")
    sales_cost_gp = fields.Text(string="Cost of Sales and GP (%)")
    rent_analy = fields.Char(string="Rent")
    salary_wages = fields.Char(string="Salary and wages")
    recommendation = fields.Char(string="Recommendation")
    transaction = fields.Text(string="Transaction", compute='compute_transaction', store=True)

    # ----------------------------------------------->>>STAT SHEET

    # ++++++++++++++++++++>>>>>>>>>>Company Details
    #     CompanyName
    #     Trading as (t / a)
    #     Member’sNames
    #     Interest %
    #    Key(default) Person
    #     Company Domcilium
    #     Year end
    #
    #             Company Reg. No.
    #             Member’s ID No.
    #             Member’s Gender
    #             Member’s Race
    #
    company_name = fields.Char(string="Company Name")
    trading_as = fields.Char(string="Trading as(t / a)")
    member_names = fields.Char(string="Member Names")
    interest = fields.Float(string="Interest %")
    key_person = fields.Char(string="Key Person(default)")
    company_domcilium = fields.Char(string="Company Domcilium")
    year_end = fields.Char(string="Year end")

    comp_reg_no = fields.Char(string="Company Reg. No.")
    member_id_no = fields.Char(string="Member’s ID No.")
    gender = fields.Selection(string="Member’s Gender", selection=[('male', 'Male'), ('female', 'Female')])
    member_race = fields.Char(string="Member’s Race")

    #
    #
    #                                     Company Contact Information
    #
    # Contact person
    #
    # Tel. work
    #
    # Fax. Work
    #
    # Postal Address
    # Physical Address
    # Cell Number
    # Tel. Home
    # E-mail
    # Web site

    contact_person = fields.Char(string="Contact person")
    tel_work = fields.Char(string="Tel. work")
    fax_work = fields.Char(string="Fax. Work")
    post_address = fields.Text(string="Postal Address")
    phy_address = fields.Text(string="Physical Addressn")
    cell_number = fields.Char(string="Cell Number")
    tel_home = fields.Char(string="Tel. Home")
    email = fields.Char(string="E-mail")
    web_site = fields.Char(string="Web site")

    #
    #                                         Business Details
    #
    #
    # Industry
    #
    # Activity
    # Province
    # Town
    #
    # Employees:
    # Existing
    # New
    #
    # HDP
    # Youth
    # Gender
    # Cost per job

    industry = fields.Char(string="Industry")
    stat_activity = fields.Char(string="Activity")
    stat_province = fields.Char(string="Province")
    stat_town = fields.Char(string="Town")
    emp_exist = fields.Many2many('res.users', string="Existing")
    emp_new = fields.Many2many('res.users', string="New")
    hdp = fields.Char(string="HDP")
    youth = fields.Char(string="Youth")
    gender_bus_det = fields.Selection(string="Gender", selection=[
        ('male', 'Male'), ('female', 'Female')])
    cost_per_job = fields.Float(string="Cost per job")

    w_working_capital = fields.Text(string="Working capital")
    w_account_name = fields.Char(string="Account Name")
    w_bank_name = fields.Char(string="Bank Name")
    w_branch_name = fields.Char(string="Branch Name")
    w_account_number = fields.Char(string="Account Number")
    w_branch_number = fields.Char(string="Branch Number")
    w_account_type = fields.Char(string="Account Type")

    suppliers = fields.Text(string="Suppliers")
    s_account_name = fields.Char(string="Account Name")
    s_bank_name = fields.Char(string="Bank Name")
    s_branch_name = fields.Char(string="Branch Name")
    s_account_number = fields.Char(string="Account Number")
    s_branch_number = fields.Char(string="Branch Number")
    s_account_type = fields.Char(string="Account Type")

    period = fields.Float(string="period")
    loan_amount = fields.Float(string="Loan Amount")

    pts_project_number = fields.Float(string="PTS Project Number")
    t_stage_of_business = fields.Char(string="Stage of business")
    approval_date = fields.Date(string="Approval Date")
    grants_cdf_Officer = fields.Char(string="Grants/CDF Officer")
    t_due_diligence_date = fields.Date(string="Due diligence Date")
    t_app_rec_date = fields.Date(string="Application received Date")
    timeline_source = fields.Char(string="Source")

    @api.model
    def create(self, vals):
        if vals:
            vals['document_number'] = self.env['ir.sequence'].next_by_code('investment.memo.sequence')

        result = super(EnterpriseFinance, self).create(vals)

        return result