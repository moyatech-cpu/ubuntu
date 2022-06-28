# coding=utf-8
from odoo import api, fields, models, _
from datetime import date, datetime


class ClientPreassessment(models.Model):
    _name = 'client.preassessment'
    _rec_name = 'client_id'


    def get_user_id(self):
        return self.client_id

    branch_id = fields.Many2one('res.branch', string="Nearest Branch", default=lambda self: self.env.user.branch_id)
    area = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Rural area - Villages'),
         ('rural-area-farms', 'Rural area - Farms')], string=" Geographical Type")
    state = fields.Selection([('new', 'New'), ('pitch_polish', 'Pitch and Polish'),('BMT_Referred','BMT Referred'), ('recommended', 'Recommended')],
                             default='new', string="State")
    province_id = fields.Many2one('res.country.state', domain=[('country_id.name', '=', 'South Africa')],
                                  string="Province")
    client_ref_no = fields.Char(string="Client Reference Number")
    client_id = fields.Many2one('res.users', string="Client Name")
    assessor_id = fields.Many2one('res.users', string="Assessor Name")
    position_id = fields.Many2one('hr.job', string="Position")
    date = fields.Date(string="Date")
    outcome_of_the_assessment = fields.Selection(
        [('approved', 'Approved'), ('referral', 'Referral'), ('rejection', 'Rejection'), ('cancelled', 'Cancelled')],
        string="Outcome Of the Assessment")
    comment_on_assessment = fields.Text(string="Comment on Assessment")
    follow_up_on_assessment_outcomes = fields.Text(string="Follow-up on Assessment Outcomes")

    user_id = fields.Many2one('res.users', string="User", compute=get_user_id)

    # PERSONAL PROFILE OF POTENTIAL CLIENT(S)

    name = fields.Char(string='Name')
    surname = fields.Char(string='Surname')
    id_number = fields.Char(string='South African Citizen Identity Number:')
    home_telephone = fields.Char(string='Home Telephone')
    cell = fields.Char(string='Cellphone Number')
    fax_number = fields.Char(string='Fax number')
    email = fields.Char(string='E-mail Address')
    physical_address = fields.Text(string='Physical Address')
    postal_code = fields.Char(string='Postal Code')
    geographic_location = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Rural area - Villages'),
         ('rural-area-farms', 'Rural area - Farms'), ('informa-settlement', 'Informa settlement')],
        string="Geographic Location")
    marital_status = fields.Selection(
        [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')],
        string='Marital status')
    no_of_Children = fields.Char(string='No. of Children')
    children_supporting = fields.Char(string='No. of other family members you are currently supporting')
    board_member = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                    string='Are you related to any NYDA staff or Board member?')
    if_yes = fields.Char(string='If yes, indicate who')

    # Educational Information

    highest_standard_passed = fields.Char(String='Highest standard passed')
    tertiary_education = fields.Char(String='Tertiary education (e.g. certificate/diploma/Degree etc.)')
    specify_study = fields.Char(String='Please specify the field of study')
    training_acquired = fields.Char(String='Any other technical training acquired')

    # Employment History
    currently_employed = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Are you currently employed?')
    how_long = fields.Char(string='If yes, for how long?')
    technical_experience = fields.Text(
        string='If no, indicate if you have any previous work or technical experience? (Please explain)')

    # General Information

    # purpose_visit = fields.Char(string='What is the purpose for your visit to NYDA? (Intervention required)?')
    benefited_from_nyda = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                           string='Have you benefited from any NYDA support services before?')
    yes_specify = fields.Char(string='If Yes Please specify')
    # assessed_to_be_requiring = fields.Selection([('yes', 'Yes'), ('no', 'No')],
    #                                             string='Are you willing to participate in the NYDA Business '
    #                                                    'Development Support if assessed to be requiring them?')
    # no_indicate = fields.Char(string='If no, indicate why')
    branch_name = fields.Char(string='Branch Name')
    date_time = fields.Date(string='date')

    # Entrepreneurial Analysis

    business_idea = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Do you have a business Idea?')
    own_business = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                    string='Are you currently running your own business?')
    business_plan = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Do you have business plan?')
    business_plan_document = fields.Binary("Business Plan")
    business_plan_document_name = fields.Binary("Business Plan Name")
    # start up
    start_a_business = fields.Text(string='Why do you want to start a business?')
    business_sector = fields.Text(string='Indicate the sector in which the business will be operating')
    type_of_business = fields.Text(string='The type of business')
    need_the_business = fields.Text(string='The need the business seeks to satisfy is')
    potential_customers = fields.Text(string='The potential customers are')
    business_operate = fields.Text(string='The business operate from')
    business_develop = fields.Text(string='The product/service which the business develop are')
    service_rendered = fields.Text(string='The service be rendered are')
    funding = fields.Text(string='What amount of funding would you require for your business? R')
    management_skills = fields.Text(string='What management skills/experience do you have to start the business?')
    technical_skills = fields.Text(string='What technical skills do you have to start the business?')
    identified_potential_customers = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                      string='Have you identified potential customers?')
    if_yes_ipc = fields.Char(string='If yes, who are they')
    funds_to_invest = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                       string='Do you have any funds to invest in the business?')
    if_yes_fti = fields.Char(string='If yes, how much?')
    any_equipment = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                     string='Do you have any equipment to start the business?')
    if_yes_ae = fields.Char(string='If yes, list them')

    # Existing Business

    start_the_business = fields.Text(string='Why did you start the business?')
    Indicate_the_business_sector = fields.Text(string='Why did you start the business?')
    business = fields.Text(string='The type of business')
    business_seeks_to_satisfy = fields.Text(string='The type of business')
    seeks_to_satisfy = fields.Text(string='The need the business seeks to satisfy is to')
    potential_customers_eb = fields.Text(string='Who are the customers/ potential customers?')
    business_operating = fields.Text(string='Where is the business operating from?')
    service_business = fields.Text(string='What is the product/ service of the business?')
    service_rendered_eb = fields.Text(string='How is the product/ service delivered/ rendered?')
    operation_business_eb = fields.Text(string='How long has the business been in operation?')
    people_are_employed = fields.Text(string='How many people are employed by the business?')
    annual_turnover = fields.Text(string='What is the estimated annual turnover of the business?')

    # Capacity Building
    business_you_want_to_start = fields.Text(
        string='What skills/ knowledge do you have about the business you want to start?')
    # Entrepreneurship_training = fields.Selection([('yes', 'Yes'), ('no', 'No')],
    #                                              string='Have you ever received Entrepreneurship training?')
    training_you_received = fields.Text(
        string='If yes, indicate the training you received and name of the '
               'institution.(E.g. financial management, project management, etc. '
               'and provide proof of the training received.)')
    development_training = fields.Char(
        string='Are you willing to attend the Entrepreneurship Development Training if required?')
    # Business Plan Element

    executive_summary = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    company_overview = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    market_opportunity = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    market_opportunitys = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    marketing_strategy = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    competitive_advantage = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    products_or_services = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    management = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    management_capability = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    financials = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    financial_understanding = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    operations = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    plan_composition = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')])
    related_total = fields.Integer('Related Total')
    total = fields.Integer('', related='related_total')

    provide_feedback = fields.Text(string='')
    strengths = fields.Text(string='')
    weaknesses = fields.Text(string='')
    suggestions = fields.Text(string='')
    recommendation = fields.Text(string='')
    supporting_document_ids = fields.One2many('preassessment.supporting.documents', 'pre_assessment_id',
                                              string="Supporting Documents")
    registered_business = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    reg_number = fields.Text(string='Enter Company Registration Number')
    entrepreneurship_training = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                 string='Have you ever received Entrepreneurship training? ')

    @api.onchange('plan_composition', 'executive_summary', 'company_overview', 'market_opportunity',
                  'products_or_services', 'marketing_strategy', 'competitive_advantage',
                  'management', 'management_capability', 'financials', 'financial_understanding',
                  'operations')
    def total_for_business_element(self):
        total = int(self.executive_summary) + int(self.company_overview) + int(self.market_opportunity) + int(
            self.market_opportunitys) + int(self.marketing_strategy) + int(self.competitive_advantage) + int(
            self.products_or_services) + int(self.management) + int(self.management_capability) + int(
            self.financials) + int(self.financial_understanding) + int(self.operations) + int(
            self.plan_composition)

        self.related_total = total

    @api.multi
    def create_pitch_and_polish(self):
        action = self.sudo().env.ref(
            'nyda_grant_and_voucher.action_pitch_polish_rating').read()[0]
        for record in self:
            ctx = {'default_branch_id': record.branch_id.id or False,
                   'default_entrepreneur_id': record.client_id.id or False,
                   'default_pitch_date': datetime.today().date() or False,
                   'default_evaluator': self.env.user.name}
            action['views'] = [(False, u'form')]
            action['context'] = ctx
            return action

    @api.multi
    def pitch_polish_rec(self):
        action = self.sudo().env.ref(
            'nyda_grant_and_voucher.action_pitch_polish_rating').read()[0]
        for rec in self:
            pitch_id = self.env['pitch.polish.rating'].search([('client_preassessment_id', '=', rec.id)], limit=1)
            action['views'] = [(False, u'form')]
            action['res_id'] = pitch_id.id or False
            return action

    @api.multi
    def set_cancelled(self):
        for rec in self:
            rec.write({'state': 'cancelled'})

    @api.multi
    def set_recommended(self):
        """ Sets state to recommended. Add logic if need anything once application is moved to recommended state. """
        mail_template_id = self.env.ref('nyda_grant_and_voucher.preassessment_acceptance_mail_template')
        for rec in self:
            if mail_template_id:
                mail_template_id.with_context(user=self.env.user).send_mail(rec.id, force_send=True)
            rec.write({'state': 'recommended'})


class PreassessmentSupportingDocuments(models.Model):
    """ Supporting document model """
    _name = 'preassessment.supporting.documents'
    _description = "Allows User to attach supporting documents along with application."

    pre_assessment_id = fields.Many2one('client.preassessment', string="Pre-Assessment Application")
    supporting_doc = fields.Binary('Supporting Document')
    supporting_doc_name = fields.Char('Supporting Document')