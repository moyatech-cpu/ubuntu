# coding=utf-8
from odoo import api, fields, models, _
from datetime import date

class ClientPreassessment(models.Model):
    _name = 'potential.clients'
    _rec_name = 'client_id'

    client_name_and_surname = fields.Char(string="Client name and surname")
    said = fields.Char(string="South African Citizen Identity Number")
    telephone = fields.Char(string="Telephone")
    cell_phone = fields.Char(string="Cell Phone")
    fax_number = fields.Char(string="Fax Number")
    email_address =  fields.Char(string="E-mail Address")
    physical_address = fields.Text(string="Physical Address")
    postal_code = fields.Char(string="Postal Code")
    geographic_location = fields.Selection(string="Geographic Location")
    marital_status = fields.Selection([('single', 'Single'), ('marrried', 'Married')], string="Marital Status")
    no_of_children = fields.Integer(string="No. Of Children")
    no_of_fam_mem = fields.Integer(string="No. of other family members you are currently supporting")
    related_nyda_staff = fields.Selection([('yes','Yes'), ('no','No')], string="Related NYDA Stafff or Board member ?")
    description_for_staff = fields.Text(string="If yes, indicate who")

    highest_std_passed = fields.Char(string="Highet Standard passes")
    tertiary_education =  fields.Char(string="Tertiary education")
    field_of_study = fields.Text(string="Please specify the field of study")
    any_other_technical_training_acquired = fields.Text(string="Any other technical training acquired")

    are_you_currently_employed = fields.Selection([('yes','Yes'),('no','No')], string="Are You Currently Employed")
    how_long = fields.Char(string="If yes, for how long ?")
    give_reason = fields.Text(
        string="If no, indicate if you have any previous work or technical experience? (Please explain)")
    visit_purpose = fields.Text(string="What is the purpose for your visit to NYDA? (Intervention required)?")
    benifitted_from_nyda = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                            string="Have you benefited from any NYDA support services before?")
    benifits_of_nyda = fields.Text(string="If Yes Please Specify")
    participate_in_nyda = fields.Selection([('yes','Yes'), ('no','No')],
        string="Are you willing to participate in the NYDA Business Development Support if assessed to be requiring them ?")
    why_not_participated = fields.Text(string="If no, indicate why")

    have_a_business_idea = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Do you have a business Idea?")
    currently_running_business = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                  string="Are you currently running your own business ?")
    have_a_business_plan = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Do you have a business Plan?")

    # startup
    why_start_business = fields.Text(string="Why do you want to start a business ?")
    which_sector = fields.Char(string="Indicate the sector in which the business will be operating")
    #starup section 1
    business_type = fields.Char(string="Business Type")
    need_of_business = fields.Text(string="The need the business seeks to satisfy is")
    potential_customer = fields.Char(string="The potential customers are")
    business_operate_from = fields.Char(string="he business operate from")
    service_of_business = fields.Char(string="The product/service which the business develop are")
    rendered_service = fields.Char(string="The service be rendered are")
    funding_required = fields.Char(string="What amount of funding would you require for your business ?")
    # starup section 2
    experience = fields.Text(string="What management skills/experience do you have to start the business ?")
    technical_skills = fields.Text(string="What technical skills do you have to start the business ?")
    identified_potential_customers = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                      string="Have you identified potential customers ?")
    desc_potential_customers = fields.Text(string="If yes, who are they ?")
    fund_to_invest = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                       string="Do you have any funds to invest in the business ?")
    description_for_investment =fields.Text(string="If yes, how much ?")
    equipment_to_start_business = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                   string="Do you have any equipment to start the business ?")
    equipment_list = fields.Text(string="Equipment List")

    # existing business
    why_did_you_start_business = fields.Text(string="Why did you start the business ?")
    existing_in_which_sector = fields.Char(string="Indicate the sector in which the business is operating ?")
    existing_business_type = fields.Char(string="The type of business")
    existing_business_needs = fields.Char(string="The need the business seeks to satisfy is to")
    existing_potential_customers = fields.Char(string="Who are the customers/ potential customers ?")
    existing_bus_operating_from = fields.Char(string="Where is the business operating from ?")
    existing_service = fields.Char(string="What is the product/ service of the business ?")
    existing_service_rendered = fields.Char(string="How is the product/ service delivered/ rendered ?")
    existing_business_operation = fields.Char(string="How long has the business been in operation ?")
    existing_employeed_peoples = fields.Char(string="How many people are employed by the business ?")
    existing_annual_turnover = fields.Char(string="What is the estimated annual turnover of the business ?")
    existing_business_plan = fields.Text(string="Existing Client Business Plan")

    # capacity building
    start_skills_knwoledge = fields.Text(
        string="What skills/ knowledge do you have about the business you want to start?")
    received_ent_traininig = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                              string="2. Have you ever received Entrepreneurship training ?")
    proof_file = fields.Binary(string="Proof")
    proof_file_name = fields.Char(string="Proof File Name")
    willing_to_attend_training = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                  string="Are you willing to attend the Entrepreneurship Development Training if required?")

    # Business Plan Element
    exe_summary = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Executive Summary")
    company_overview = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Company Overview")
    market_opportunity = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Market Opportunity")
    marketting_strategy = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Marketting Strategy")
    competitive_advantage = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Competitive Advantage")
    product_or_service = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Product Or Service")
    management = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Management")
    management_capability = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Management Capability")
    financials = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Financials")
    financial_understanding = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Financial Understanding")
    operations = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Operations")
    plan_composition = fields.Selection([('1', 'Poor'), ('2', 'Adequate'), ('3', 'Good'), ('4', 'Excellent')],
                                   string="Plan Composition")

    # feedback
    feedback_assessment =  fields.Text(string="Feedback")
    strength = fields.Text(string="Strengths")
    weakness = fields.text(string="Weakness")
    other_comm_suggestion = fields.Text(string="Other Comments/Suggestions")
    recommendation = fields.Text(string="Recommendation")
    client_signature = fields.Binary(string="Client Signature")
    signature_date = fields.Date(string="Signature Date")
    accessor_id = fields.Many2one('res.users', string="Accessor")
    accessor_signature = fields.Binary(string="Accessor Signature")
    position = fields.Many2one('hr.job', string="Position")
