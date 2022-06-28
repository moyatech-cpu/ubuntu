from odoo import models, fields, api, _


class VoucherAssessmnent(models.Model):
    _name = 'voucher.assessment'
    _rec_name = 'voucher_application_id'

    @api.onchange('features_product', 'benefits_product', 'equipment_product', 'reasons_product', 'describe_customer',
                  'currently_buying', 'customers_currently', 'product_services', 'calculated_startup_cost',
                  'calculated_expenses_potential_income', 'contribution_startup', 'deliver_product',
                  'business_management', 'start_your_business', 'regulatory_requirements', 'most_appropriate')
    def total_for_business_element(self):
        total = int(self.features_product) + int(self.benefits_product) + int(self.equipment_product) + int(
            self.reasons_product) + int(self.describe_customer) + int(self.currently_buying) + int(
            self.customers_currently) + int(self.product_services) + int(self.calculated_startup_cost) + int(
            self.calculated_expenses_potential_income) + int(self.contribution_startup) + int(self.deliver_product) \
                + int(self.business_management) + int(self.start_your_business) + int(
            self.regulatory_requirements) + int(
            self.most_appropriate)
        self.related_total = total

    voucher_application_id = fields.Many2one('voucher.application', string='Voucher Application')
    # Fields For Business Feasibility Assessment
    related_total = fields.Integer('Related Total')
    total = fields.Integer('Total', related='related_total')

    features_product = fields.Selection([('1', 'Im unable to describe the product/service features.'),
                                         ('2',
                                          'I can provide a limited description of the product/service features'),
                                         ('3', 'I can describe the basic product/service features clearly.'),
                                         ('4',
                                          'I can describe the product/service features and how it will satisfy the needs of my potential customers.')])
    benefits_product = fields.Selection([('1', 'Im unable to describe the product/service features.'),
                                         ('2',
                                          'I can provide a limited description of the product/service features'),
                                         ('3', 'I can describe the basic product/service features clearly.'),
                                         ('4',
                                          'I can describe the benefits of the product/service features really well.')])
    equipment_product = fields.Selection(
        [('1', 'I dont know what materials or equipment are needed to make the product or deliver the service.'),
         ('2', 'I have identified some of the material or equipment needed to make the product/service'),
         ('3', 'I have identified all the materials or equipment needed to make the product/service'),
         ('4',
          'I have identified all the materials or equipment needed to make the product/service and have identified suppliers where I can')])
    reasons_product = fields.Selection([('1', 'I cant explain the reasons why customers will buy the product/service'),
                                        ('2',
                                         'I can provide a limited explanation of the reasons why customers will buy the product/service'),
                                        ('3',
                                         'I can explain the reasons why customers will buy the product/service clearly'),
                                        ('4',
                                         'I can explain the reasons why customers will buy the product/service in great detail')])
    describe_customer = fields.Selection([('1', 'I dont know who my potential customers will be'),
                                          ('2', 'I am not sure who my potential customers will be'),
                                          ('3', 'I have identified my potential customers and can describe them'),
                                          ('4',
                                           'I have identified my customers and know how my product/service will satisfy their needs')])
    currently_buying = fields.Selection(
        [('1', 'I dont know what advantages my product/service have over other products/ services in the market'),
         ('2', 'I cant describe the advantages my product/service have over similar products in the market'),
         ('3', 'I can explain to customer what advantages my product/service have over other products in the market'),
         ('4',
          'I can explain and motivate the advantages my product/service have over similar products/ services in the market')])
    customers_currently = fields.Selection([('1', 'I dont know who my competitors are'),
                                            ('2', 'I have identify some of my competitors'),
                                            ('3',
                                             'I have identified all the competitors in my area who sell the same/ or similar product/service'),
                                            ('4',
                                             'I have identified all the competitors in my area and have studied their strengths and weaknesses')])
    product_services = fields.Selection([('1', 'I will have to compete against large numbers of businesses'),
                                         ('2', 'I will have to compete against many other businesses'),
                                         ('3', 'I will have to compete against a small number of businesses'),
                                         ('4', 'I will compete with only a few businesses/ or none at all')])
    calculated_startup_cost = fields.Selection([('1', 'I have not yet identified and calculated my start-up costs.'),
                                                ('2',
                                                 'I have identified my start-up costs, but dont know where I will find the money.'),
                                                ('3',
                                                 'I have calculated my start-up costs and identified possible sources of funding.'),
                                                ('4',
                                                 'I have calculated my start-up costs and am able to source the funding for it.')])

    calculated_expenses_potential_income = fields.Selection(
        [('1', 'Im unable to calculate my expenses and income.'),
         ('2',
          'I can calculate my expenses and income, but have not done it yet.'),
         ('3',
          'I have calculated my expenses and my projected income will be enough to cover my expenses.'),
         ('4',
          'I have calculated my expenses and my projected income will be enough to cover my expenses and to reinvest in the business.')])

    contribution_startup = fields.Selection(
        [('1', 'Im unable to contribute anything to the start-up costs or operating expenses.'),
         ('2',
          'I dont have enough money for the business, or security to take out a loan.'),
         ('3',
          'I dont have the money, but I can provide security for taking out a loan.'),
         ('4',
          'I have my own money and Im willing to invest in the business.')])

    deliver_product = fields.Selection(
        [('1', 'I dont have the skills to deliver product/service to the customer.'),
         ('2',
          'I dont have the skill to deliver the product/service to the customer, but I can develop it or get it.'),
         ('3',
          'I have the skills to deliver the product/service to the customer.'),
         ('4',
          'I have the all the skills necessary to develop the product/service.')])

    business_management = fields.Selection(
        [('1', 'No I dont have the business management skills to manage the business.'),
         ('2',
          'I have basic business management skills, but will need help in managing my business.'),
         ('3',
          'I have adequate business management skills to manage my business.'),
         ('4',
          'I have very good business management skills for managing my business.')])

    start_your_business = fields.Selection(
        [('1', 'I have no experience in the field in which I want to start my business.'),
         ('2',
          'I have some years of experience in the field in which I want to start my business.'),
         ('3',
          'I have adequate experience in the field in which I want to start my business.'),
         ('4',
          'I have many years of experience in the field in which I want to start my business.')])

    regulatory_requirements = fields.Selection(
        [('1',
          'I dont know how to determine if there are any business and regulatory requirements I have to comply with.'),
         ('2',
          'I know what legal and regulatory requirements I have to comply with, but Im not sure what I have to do to comply.'),
         ('3',
          'I have identified the legal and regulatory requirements and identified what I need to do to comply with it.'),
         ('4',
          'I have already checked that I will be able to comply with the necessary legal and regulatory requirements for starting and running my business.')])

    most_appropriate = fields.Selection(
        [('1', 'I do not know the different types of entities.'),
         ('2',
          'I know the different types of entities, but not sure how they are relevant to my business idea.'),
         ('3',
          'I know the types of business entities and have identified an appropriate one.'),
         ('4',
          'I know the different entities and have evaluated each to determine the most appropriate one for my business idea.')])

    @api.onchange('growth_objectives', 'grow_the_business', 'investment_requirements', 'adapt_changing',
                  'market_growing', 'changing_market', 'growing_demand', 'sales_growth', 'analyse_information',
                  'customer_preferences', 'marketing_activities', 'marketing_capacity', 'competition_market',
                  'undertake_competitor', 'competitiveness', 'funding_required', 'financial_planning_management',
                  'performance_targets', 'your_revenue', 'your_growth_objectives', 'general_business_advice',
                  'implemented_methods')
    def total_for_assessment_index(self):
        total = int(self.growth_objectives) + int(self.grow_the_business) + int(
            self.investment_requirements) + int(self.adapt_changing) + int(self.market_growing) + int(
            self.changing_market) + int(self.growing_demand) + int(self.sales_growth) + int(
            self.analyse_information) + int(self.customer_preferences) + int(self.marketing_activities) + int(
            self.marketing_capacity) + int(self.competition_market) + int(
            self.undertake_competitor) + int(self.competitiveness) + int(self.funding_required) + int(
            self.financial_planning_management) + int(
            self.performance_targets) + int(
            self.your_revenue) + int(
            self.your_growth_objectives) + int(
            self.general_business_advice) + int(
            self.implemented_methods)
        self.related_assessment_index_total = total

    # Fields For Business Growth and Sustainability Assessment Index

    related_assessment_index_total = fields.Integer('Related Total')
    assessment_index_total = fields.Integer(string="Total", related="related_assessment_index_total")

    growth_objectives = fields.Selection(
        [('1', 'We have not yet defined our growth objectives.'),
         ('2',
          'Our growth objectives are unclear.'),
         ('3',
          'We have defined our growth objectives.'),
         ('4',
          'We have defined our growth objectives clearly over the short, medium and long term.')])

    grow_the_business = fields.Selection(
        [('1', 'We have not made any choices about how we should achieve business growth objectives.'),
         ('2',
          'We are considering several growth strategies, but are unsure about the most appropriate strategy to adopt.'),
         ('3',
          'We have identified the appropriate growth strategy(ies) for the business and have developed an implementation plan to implement the strategy.'),
         ('4',
          'We have identified the appropriate growth strategy(ies) for the business and have started implementing the plan.')])

    investment_requirements = fields.Selection(
        [('1', 'We have not yet assessed the investment requirements for growth.'),
         ('2',
          'We have some idea for the investment requirements for growth.'),
         ('3',
          'We have identified and assessed our investment requirements for growth.'),
         ('4',
          'We have assessed our investment requirements and have developed a document outlining the requirement in detail.')])

    adapt_changing = fields.Selection(
        [('1', 'We do not monitor changes in the business environment that may affect the business.'),
         ('2',
          'We have an ad-hoc approach to monitoring and assessing the business environment for identifying changes that may affect us.'),
         ('3',
          'We have a systematic approach to monitoring and assessing the business environment.'),
         ('4',
          'We assess the business environment on a regular basis to identify possible opportunities and develop and implement measures to adapt and respond to these changes.')])

    market_growing = fields.Selection(
        [('1', 'The market is in a state of decline.'),
         ('2',
          'The growth in the market is stagnant.'),
         ('3',
          'The market is experiencing stable growth.'),
         ('4',
          'The market is experiencing strong growth.')])

    changing_market = fields.Selection(
        [('1', 'We are unable to identify changing market trends and respond to it.'),
         ('2',
          'We are able to identify changing market trends, but we are unable to respond to it.'),
         ('3',
          'We are able to identify changing market trends and respond to it.'),
         ('4',
          'We take advantage of opportunities resulting from changing market trends and adapt to risks identified.')])

    growing_demand = fields.Selection(
        [('1', 'There is no evidence to indicate that there is a growing demand for our product or service.'),
         ('2',
          'There is some evidence that there is a growing demand for our product.'),
         ('3',
          'There is adequate evidence that there is a growing demand for our product or service.'),
         ('4',
          'There is substantial evidence that there is strong growth in the demand for our product or service.')])

    sales_growth = fields.Selection(
        [('1', 'The business has not experienced any sales growth over the last 12 months.'),
         ('2',
          'Our sales growth over the last 12 months has been inconsistent.'),
         ('3',
          'Our sales growth has been moderate and consistent over the last 12 months.'),
         ('4',
          'Our sales have shown strongly, showing consistent growth over the last 12 months.')])

    analyse_information = fields.Selection(
        [('1', 'We dont analyse customer information.'),
         ('2',
          'The analysis on our customers are inadequate.'),
         ('3',
          'We effectively analyse information on customers.'),
         ('4',
          'We have a systematic approach to gathering and analysing customer information to identify changing customer needs and wants.')])

    customer_preferences = fields.Selection(
        [('1', 'We are unable to identify and respond to changing customer preferences.'),
         ('2',
          'We are not effective at identifying and responding to changing customer preferences.'),
         ('3',
          'We have a systematic process in place for monitoring changing customer preferences.'),
         ('4',
          'We are able to identify changing customer preferences and use this as input into the development of our products and services.')])

    marketing_activities = fields.Selection(
        [('1', 'Our marketing activities are ineffective.'),
         ('2',
          'The effectiveness of our marketing activities are limited.'),
         ('3',
          'Our marketing activities are effective in creating a presence in the market for us.'),
         ('4',
          'Our marketing activities are very effective and have a direct impact on sales growth.')])

    marketing_capacity = fields.Selection(
        [('1', 'Our marketing capacity is already stretched and will need substantial investment to increase it.'),
         ('2',
          'We will need additional resources to increase our marketing capacity.'),
         ('3',
          'We have the necessary resources to increase our marketing capacity.'),
         ('4',
          'We can deploy the required resources immediately to increase our marketing capacity.')])

    competition_market = fields.Selection(
        [('1', 'The level of competition in our market is fierce.'),
         ('2',
          'There is a high level of competition in our market.'),
         ('3',
          'The level of competition in our market is moderate.'),
         ('4',
          'The level of competition in our market is low.')])

    undertake_competitor = fields.Selection(
        [('1', 'We do not have the ability to analyse our competitors.'),
         ('2',
          'Our ability to analyse our competitors is limited.'),
         ('3',
          'We analyse our competitors on a regular basis to identify their strengths and weaknesses.'),
         ('4',
          'We analyse our competitors on a regular basis and use the strengths and weaknesses we identify to enhance our own competitive advantage.')])

    competitiveness = fields.Selection(
        [('1', 'We are unable to compete against our competitors.'),
         ('2',
          'We struggle to compete against our competitors.'),
         ('3',
          'We are able to compete effectively against our competitors.'),
         ('4',
          'We are more competitive that our competitors.')])

    funding_required = fields.Selection(
        [('1', 'We have not identified the funding levels required to finance the projected growth.'),
         ('2',
          'We have identified some of the funding requirements for financing the growth of the business.'),
         ('3',
          'We have undertaken a comprehensive analysis of the funding needed to finance our growth.'),
         ('4',
          'We have identified the funding requirements and possible sources of funding to finance our growth.')])

    financial_planning_management = fields.Selection(
        [('1', 'We do not have a working financial planning and management system in place.'),
         ('2',
          'Our financial planning and management system does not adequately meet the needs of the business.'),
         ('3',
          'We have an effective financial planning and management system in place.'),
         ('4',
          'We have an effective financial planning and management system that is able to provide us with reliable and up to date financial information for decision-making.')])

    performance_targets = fields.Selection(
        [('1', 'We have not established financial performance targets against which to monitor our progress.'),
         ('2',
          'We have set financial performance targets, but do not have the ability to monitor these indicators effectively.'),
         ('3',
          'We have set financial performance targets that we monitor on a regular basis.'),
         ('4',
          'We use the financial performance targets that we track and monitor to help us plan ad make decisions in the business. We have identified and track several financial performance targets, including revenue, expenditure, sales, profit margin and other ta')])

    your_revenue = fields.Selection(
        [('1', 'We expect a decline in our revenue over the next 12 months.'),
         ('2',
          'We expect our revenue to remain the same over the next 12 months.'),
         ('3',
          'We expect a moderate increase in our revenue over the next 12 months.'),
         ('4',
          'We expect strong growth in our revenue over the next 12 months.')])

    your_growth_objectives = fields.Selection(
        [('1', 'We have not identified the business management requirements of support our growth objectives.'),
         ('2',
          'We have assessed the business management requirements for growth, but do not have the capacity to meet these requirements.'),
         ('3',
          'We have determined the business management requirements for supporting our growth, and have the necessary capacity in place.'),
         ('4',
          'We have determined the business management requirements for supporting our growth, and have the necessary capacity in place to effectively manage the expected growth.')])

    general_business_advice = fields.Selection(
        [('1', 'We do not have access to, and use external expertise and advice on growing the business.'),
         ('2',
          'We have access to, but do not use external expertise and advice on growing the business.'),
         ('3',
          'We have access to, and use external expertise and advice on growing the business.'),
         ('4',
          'We have established relationships with external service providers for advice and expertise on the growth of the business.')])

    implemented_methods = fields.Selection(
        [('1', 'We have not implemented any new methods or concepts over the last 12 months.'),
         ('2',
          'We have not been successful at implementing any new methods or concepts in the business over the last 12 months.'),
         ('3',
          'We have been successful at implementing at least one new method or concept in the business over the last 12 months.'),
         ('4',
          'We have been successful at implementing several new methods or concepts in the business over the last 12 months.')])

    @api.onchange('analyse_the_environment', 'set_business_goals', 'develop_implement_plans',
                  'your_customers', 'changes_happening', 'undertake_marketing', 'set_sales_targets', 'marketing_capacitys',
                  'undertake_financial_planning', 'adequate_cash_flow', 'maintain_financial', 'financial_controls',
                  'established_financial_ratios', 'established_structure', 'coordinate_different', 'communicate_effectively',
                  'required_management_capacity', 'business_documented', 'necessary_controls', 'monitor_business')
    def total_for_viability_assessment(self):
        total = int(self.analyse_the_environment) + int(
            self.set_business_goals) + int(self.develop_implement_plans) + int(
            self.your_customers) + int(self.changes_happening) + int(self.undertake_marketing) + int(
            self.set_sales_targets) + int(self.marketing_capacitys) + int(self.undertake_financial_planning) + int(
            self.adequate_cash_flow) + int(self.maintain_financial) + int(self.established_financial_ratios)+ int(
            self.financial_controls) + int(self.communicate_effectively) + int(self.required_management_capacity) + int(
            self.coordinate_different) + int(
            self.business_documented) + int(
            self.necessary_controls) + int(
            self.monitor_business)
        self.related_viability_assessment_total = total

    # Business Viability Assessment
    related_viability_assessment_total = fields.Integer('Related Total')
    viability_assessment_total = fields.Integer(string="Total", related="related_viability_assessment_total")

    analyse_the_environment = fields.Selection(
        [('1', 'We never analyse the environment we operate in.'),
         ('2', 'We sometimes analyse our business environment.'),
         ('3', 'We regularly analyse the business environment.'),
         ('4',
             'We regularly analyse the business environment to determine if there are any opportunities or threats.')])

    set_business_goals = fields.Selection(
        [('1', 'We do not set business goals.'),
         ('2', 'We set business goals, but never achieve them.'),
         ('3', 'We set business goals and regularly achieve them.'),
         ('4', 'We set business goals, regularly achieve them and continuously review them.')])

    develop_implement_plans = fields.Selection(
        [('1', 'We dont develop plans to achieve our business goals.'),
         ('2', 'We develop plans, but find it difficult to implement them.'),
         ('3', 'We develop and implement plans that help us to achieve our business goals regularly.'),
         ('4', 'We implement plans and review the plans to determine where we can improve in future.')])

    your_customers = fields.Selection(
        [('1', 'I dont know who our customers are.'),
         ('2', 'I have a general idea of who our customers are.'),
         ('3', 'I know who our customers are.'),
         ('4', 'I know our customers and have identified different customer segments.')])

    changes_happening = fields.Selection(
        [('1', 'I dont know what changes are taking place in our market.'),
         ('2', 'Our knowledge of the changes in the market is inadequate.'),
         ('3', 'I know what changes are taking place in our market.'),
         ('4', 'I monitor the changes in our market to determine if it is growing or declining.')])

    undertake_marketing = fields.Selection(
        [('1', 'We never undertake marketing and promotional activities.'),
         ('2', 'We sometimes undertake marketing and promotional activities.'),
         ('3', 'We regularly undertake marketing and promotional activities in line with our marketing plan.'),
         ('4', 'We regularly undertake marketing and promotional activities and evaluate the success of these.')])

    set_sales_targets = fields.Selection(
        [('1', 'We do not set sales targets.'),
         ('2', 'We set sales targets, but never achieve them.'),
         ('3', 'We set sales targets and regularly achieve them.'),
         ('4', 'We set sales targets, regularly achieve them and continuously review them.')])

    marketing_capacitys = fields.Selection(
        [('1', 'We have no marketing and sales capacity.'),
         ('2', 'We have limited marketing and sales capacity.'),
         ('3', 'Our marketing and sales capacity effectively meets the needs of the business.'),
         ('4',
          'We have good marketing and sales capacity and focus on continuously building this capacity in the business.')])

    undertake_financial_planning = fields.Selection(
        [('1', 'We dont do financial planning.'),
         ('2', 'Our financial planning is ad-hoc.'),
         ('3', 'We undertake regular and effective financial planning.'),
         ('4', 'Our financial planning activities effectively enable us to determine our financial needs.')])

    adequate_cash_flow = fields.Selection(
        [('1', 'We are always struggling with our cash flow.'),
         ('2', 'We sometimes experience problems with our cash flow.'),
         ('3', 'We have adequate cash flow.'),
         ('4',
          'We have adequate cash flow and access to reserve funding to cover our cash flow should the need arise.')])

    maintain_financial = fields.Selection(
        [('1', 'We do not maintain financial records.'),
         ('2', 'We do have financial records, but they are in a chaotic state.'),
         ('3', 'We maintain financial records and they are up to date.'),
         ('4',
          'We maintain good financial records that are always current.')])

    financial_controls = fields.Selection(
        [('1', 'We have no financial policies and controls in the business.'),
         ('2', 'We have limited financial policies and controls in the business.'),
         ('3', 'We have sound and effective financial policies and controls in the business.'),
         ('4',
          'We have sound financial policies and controls in the business that are reviewed regularly to ensure its effectiveness')])

    established_financial_ratios = fields.Selection(
        [('1', 'We have not identified financial ratios.'),
         ('2', 'We have identified some financial ratios.'),
         ('3', 'We have identified all the required financial ratios.'),
         ('4',
          'We have identified all the required financial ratios and use it to assess our financial performance.')])


    established_structure = fields.Selection(
        [('1', 'We have not yet established a structure for the distribution of tasks and allocation of resources.'),
         ('2', 'We have designed a structure, but have not yet implemented it.'),
         ('3', 'We have designed and implemented a structure that enables us to run the business effectively.'),
         ('4',
          'We have designed and implemented a structure that works effectively to distribute tasks and allocate resources, with a description of roles and responsibilities.')])


    coordinate_different = fields.Selection(
        [('1', 'We are unable to coordinate the various business functions.'),
         ('2', 'The coordination of business activities are random.'),
         ('3', 'We coordinate the different business functions effectively. '),
         ('4',
          'We coordinate the different business functions effectively and continuously find ways to improve our coordination.')])

    communicate_effectively = fields.Selection(
        [('1', 'We do not communicate effectively with our staff, suppliers and customers.'),
         ('2', 'Our communication activity with our staff is haphazard.'),
         ('3',
             'Our communication mechanisms enable us to communicate effectively with staff, suppliers and customers.'),
         ('4',
          'We plan our communication activities and use the communication mechanisms at our disposal effectively.')])

    required_management_capacity = fields.Selection(
        [('1', 'We do not have the skills and knowledge in our team to effectively manage the business.'),
         ('2', 'The skills and knowledge needed to manage the business are limited in our team.'),
         ('3', 'The skills and knowledge in our team are adequate to manage the business.'),
         ('4',
          'Our team has excellent skills and knowledge to manage the business.')])

    business_documented = fields.Selection(
        [('1', 'We have not documented the processes in the business.'),
         ('2', 'Some processes in the business have been documented.'),
         ('3', 'We have documented all the key processes in the business.'),
         ('4',
          'We have documented all the key processes in the business and focus on improving them continuously.')])

    necessary_controls = fields.Selection(
        [('1', 'We do not have any controls to ensure safety and security.'),
         ('2',
          'We have developed controls (policies and procedures) to ensure safety and security, but have not implemented it yet.'),
         ('3', 'We have developed and implemented safety and security controls.'),
         ('4',
          'We have developed and implemented safety and security controls and regularly monitor these.')])

    monitor_business = fields.Selection(
        [('1', 'We do not identify and monitor risks that threaten the existence of the business.'),
         ('2',
          'We sometimes identify and monitor risks that threaten the existence of the business.'),
         ('3', 'We regularly identify and monitor risks that threaten the existence of the business.'),
         ('4',
          'We sometimes identify and monitor risks that threaten the existence of the business and develop plans to mitigate those risks.')])

    @api.onchange('business_opportunities', 'market_trends', 'potential_target_market', 'market_entry_strategy',
                  'Test_business_ideas', 'Make_plans', 'Organise_resources', 'coordinate_activities', 'organise_people',
                  'Manage_time', 'Analyse_problems', 'Think_critically', 'Innovate', 'Goal_oriented',
                  'achievement_oriented', 'Follow_through', 'Self_disciplined', 'Competitiveness', 'required_physical',
                  'into_partnerships', 'Acquire_resources', 'Allocate_resources', 'use_of_resources')
    def total_for_preparedness_assessment(self):
        total = int(self.business_opportunities) + int(self.market_trends) + int(self.potential_target_market) + int(
            self.market_entry_strategy) + int(self.Test_business_ideas) + int(self.Make_plans) + int(
            self.Organise_resources) + int(self.coordinate_activities) + int(self.organise_people) + int(
            self.Manage_time) + int(self.Analyse_problems) + int(self.Think_critically) + int(
            self.Diagnose_problems) + int(self.Innovate) + int(self.Goal_oriented) + int(
            self.achievement_oriented) + int(self.Follow_through) + int(self.Self_disciplined) + int(
            self.Competitiveness) + int(self.required_physical) + int(self.into_partnerships) + int(
            self.Acquire_resources) + int(self.Allocate_resources) + int(self.use_of_resources)
        self.related_preparedness_assessment_total= total

    # Entrepreneurial Preparedness Assessment
    related_preparedness_assessment_total = fields.Integer('Related Total')
    preparedness_assessment_total = fields.Integer(string="Total", related="related_preparedness_assessment_total")

    business_opportunities = fields.Selection(
        [('1', 'I dont know where to find or whom to ask about information on business opportunities.'),
         ('2', 'I need assistance with finding information about business opportunities.'),
         ('3', 'I can find information about business opportunities on my own, without assistance from anyone.'),
         ('4',
          'I can find information about business opportunities on my own, without assistance and am able to use this information in planning and starting my business.'),
         ('5',
          'I can find information about business opportunities on my own, use it in starting my business and can even show others how and where to find it.')])

    market_trends = fields.Selection(
        [('1', 'I do not know what market trends are, and how it can assist in identifying business opportunities.'),
         ('2',
          'I need assistance with identifying trends in the market and understanding the implications of such trends.'),
         ('3',
          'I can identify changes in the market and am able to identify potential opportunities arising from such changes.'),
         ('4',
          'I keep track of changes in the market and assess how trends can lead to new opportunities for business.'),
         ('5', 'I keep track of market trends and actively identify potential business opportunities.')])

    potential_target_market = fields.Selection(
        [('1',
          'I am not able to clearly describe the benefits of my intended product and services and I have not yet identified a potential market for it.'),
         ('2',
          'I have some idea about the benefits of my envisaged product or service, but have not yet identified a specific target market.'),
         ('3',
          'I know how my intended product/ service will benefit my clearly identified target market.'),
         ('4',
          'I know what my target market wants, who my target market is and how to reach them.'),
         ('5',
          'I have clearly defined the benefits of my product or service, have matched it to the needs of a specific target market and have already checked whether they are prepared to buy my product and service in the way I intend to deliver it to them.')])

    market_entry_strategy = fields.Selection(
        [('1', 'I do now know what market entry strategies are, or how to select them.'),
         ('2',
          'I know the different types of market entry strategies, but do not know how to select the appropriate strategy for taking potential product or service to the market.'),
         ('3',
          'I can select an appropriate market entry strategy.'),
         ('4',
          'I know several different market entry strategies and am able to match the appropriate market entry strategy to my idea.'),
         ('5',
          'I have evaluated several market entry strategies and have selected the most appropriate market strategy for taking my idea to the market.')])

    Test_business_ideas = fields.Selection(
        [('1',
          'I do not know how to go about evaluating whether any of my ideas are realistic business opportunities.'),
         ('2',
          'I can test my business idea, but need assistance to do so.'),
         ('3',
          'I am able to test which of my ideas are real business opportunities.'),
         ('4',
          'I can systematically and logically evaluate which of my ideas are real business opportunities.'),
         ('5',
          'I can systematically and logically evaluate which of my ideas are real business opportunities against a specific set of criteria.')])

    Make_plans = fields.Selection(
        [('1', 'I cant formulate a set of activities to achieve a specific goal.'),
         ('2',
          'I need assistance to create a set of actions to achieve a goal.'),
         ('3',
          'I can set out number of actions in a coherent and logical way to achieve a goal.'),
         ('4',
          'I can set out a number of actions in a coherent, logical and sequential way to achieve a goal.'),
         ('5',
          'I am very good at outlining a set of actions in a coherent, logical and sequential way to achieve a goal and can show others how to do it.')])

    Organise_resources = fields.Selection(
        [('1', 'I am unable to assess what resources are needed for the activities I plan.'),
         ('2',
          'I need assistance with identifying the resource I need to carry out an activity.'),
         ('3',
          'I am able to assess the resources needed to undertake an activity.'),
         ('4',
          'I am able to assess the resources needed to undertake an activity, while at the same time organising it in a way to make the activity a success.'),
         ('5',
          'I continuously assess the resources I need to undertake activities, and find creative ways to organise and use the resources efficiently in making the activity a success.')])

    coordinate_activities = fields.Selection(
        [('1',
          'I struggle with making different people work together and integrating different activities to achieve a goal. '),
         ('2',
          'Although I can integrate different activities, I find it hard to make different people work together.'),
         ('3',
          'I am able to make different people work together and integrate their activities to achieve a goal.'),
         ('4',
          'I am able to make different people work together on multiple activities and integrate these activities systematically to achieve a goal.'),
         ('5',
          'I have experience in coordinating multiple activities systematically among different people to achieve a goal.')])

    organise_people = fields.Selection(
        [('1', 'People tend not to listen to me when I try to get them to work together to achieve a goal.'),
         ('2',
          'Although people are prepared to follow me when I try to undertake an activity, I find it hard to organise them properly to achieve a goal.'),
         ('3',
          'I am able to motivate people and get them to work together to achieve a specific goal.'),
         ('4',
          'I am able to motivate people, delegate tasks and get them to work together to achieve a specific goal.'),
         ('5',
          'I am always organising, motivating and leading people in undertaking activities in order to achieve specific goals')])

    Manage_time = fields.Selection(
        [('1',
          'I am unable to keep to a schedule and therefore, Im forever running late with completing activities.'),
         ('2',
          'Although I am able to schedule the timing of an activity, I rarely manage to keep to it.'),
         ('3',
          'I am able to schedule and complete the activities within the planned time.'),
         ('4',
          'I am able to analyse the time required to undertake an activity, schedule and complete the tasks necessary to complete the activity within the planned time.'),
         ('5',
          'I am continuously looking for ways to improve how I manage my time and the time of those who are involved in tasks that have to be accomplished to achieve a goal.')])

    Analyse_problems = fields.Selection(
        [('1',
          'I do not know how to go about analysing problems.'),
         ('2',
          'I am able to analyse problems with the assistance of someone else.'),
         ('3',
          'I can analyse problems systematically.'),
         ('4',
          'When I analyse a problem I systematically work my way through the best approach to analysing this particular kind of problem.'),
         ('5',
          'My approach to problem solving consistently gives me reliable results.')])

    Think_critically = fields.Selection(
        [('1',
          'I do not know how to critically evaluate information. I generally accept the information Im given, especially if it comes from someone more educated and experienced that I am'),
         ('2',
          'I can only reflect critically on information I am given in consultation with someone else.'),
         ('3',
          'I purposefully reflect on the information that Im given and evaluate its usefulness.'),
         ('4',
          'I reflect and question the information that Im given so that I can evaluate the assumptions on which it is based.'),
         ('5',
          'I continuously reflect on, and evaluate the advice I get from different perspectives before accepting it.')])

    Diagnose_problems = fields.Selection(
        [('1',
          'I dont know where to start or how to go about diagnosing a problem.'),
         ('2',
          'I can only diagnose a problem with the assistance from someone else.'),
         ('3',
          'I am able to identify the cause of a problem and separate it from the symptoms.'),
         ('4',
          'I apply a systematic and logical method of detecting the root causes of a problem.'),
         ('5',
          'I am very successful at diagnosing problems correctly by using a systematic and logical approach.')])

    Innovate = fields.Selection(
        [('1',
          'I dont know how to come up with new or different ways to address the problems I am confronted with.'),
         ('2',
          'If am more comfortable trying new or different ways to address a problem with assistance from someone else.'),
         ('3',
          'I try to find new or different approaches and techniques to address the problems I face I continuously experiment with newer or different ways to address the problems I face.'),
         ('4',
          'I am successful in regularly finding new and different ways of addressing problems I experience.')])

    Provide_solutions = fields.Selection(
        [('1',
          'I dont know how to formulate solutions to the problems I face.'),
         ('2',
          'I always need assistance in formulating solutions to the problems I experience.'),
         ('3',
          'I formulate workable solutions to the problems I experience.'),
         ('4',
          'I always formulate the best solutions to solve problems.'),
         ('5',
          'People often come to me for assistance with developing solutions to their problems.')])

    Goal_oriented = fields.Selection(
        [('1',
          'I manage to get by without setting goals for myself.'),
         ('2',
          'I always need assistance in formulating solutions to the problems I experience.'),
         ('3',
          'Even if I set goals for myself, I keep on changing them Goals give me motivation and direction.'),
         ('4',
          'I have to set goals for myself, otherwise it is hard for me to stay focused Setting and achieving goals give me meaning in life.')])

    achievement_oriented = fields.Selection(
        [('1',
          'I set goals that I can easily accomplish.'),
         ('2',
          'I set challenging goals for myself, but Im not too concerned if I do not achieve them.'),
         ('3',
          'I set challenging goals for myself and strive to achieve them.'),
         ('4',
          'I set challenging goals for myself and strive to achieve them at all times.'),
         ('5',
          'I continue to set more challenging goals for myself each time I accomplish one.')])

    Follow_through = fields.Selection(
        [('1',
          'When I start a project or an activity and the work becomes too much I give up easily.'),
         ('2',
          'I enjoy starting projects, but dont always see it through to its completion.'),
         ('3',
          'When I start a project or an activity, I keep on going at it even if the work gets too much and too hard.'),
         ('4',
          'When I start a project or an activity, I always try to complete it.'),
         ('5',
          'I always try complete projects or activities I start successfully, regardless of the obstacles and difficulties.')])

    Self_disciplined = fields.Selection(
        [('1',
          'I need other people to motivate and encourage me.'),
         ('2',
          'I can discipline myself to do something but I need other people to motivate me.'),
         ('3',
          'I am able to motivate and discipline myself when I need to complete a project or an activity.'),
         ('4',
          'I enjoy motivating myself and testing my discipline when I need to complete a project or activity.'),
         ('5',
          'I thrive in an environment that challenges me to motivate and discipline myself to achieve a goal.')])

    Competitiveness = fields.Selection(
        [('1',
          'Not being the best does not bother me.'),
         ('2',
          'Im comfortable not being the best at something, if the effort involved becomes too much.'),
         ('3',
          'I enjoy being the best at everything I do.'),
         ('4',
          'I always strive to be the best at everything I do, even if it means I have to make sacrifices.'),
         ('5',
          'I will do what it takes to make sure that I am the best at everything I do.')])

    required_physical = fields.Selection(
        [('1',
          'I dont know what physical, financial and human resources I will need to start my business and have difficulty in identifying these.'),
         ('2',
          'I need someone to work with me so that I can identify what physical, financial and human resources I will need to start my business.'),
         ('3',
          'I have identified the physical, financial and human resources I will need to start my business.'),
         ('4',
          'I have identified the physical, financial and human resources I will need to start my business and know where to find it.'),
         ('5',
          'I have identified my physical, financial and human resources I will need to start my business and have already started to acquire these.')])

    into_partnerships = fields.Selection(
        [('1',
          'I dont know how to form partnerships and tap into the resources of my partners.'),
         ('2',
          'I need assistance with forming partnerships for the purposes of mobilising resources.'),
         ('3',
          'I am able to form partnerships and mobilise resources through such partnerships.'),
         ('4',
          'I have already developed a few partnerships that are able to assist me in mobilising resources.'),
         ('5',
          'I excel in forming partnerships for the purpose of mobilising resources.')])

    Acquire_resources = fields.Selection(
        [('1',
          'I dont know where to start or how to go about acquiring the resources I need to start my business.'),
         ('2',
          'I need assistance with acquiring the resources I need to start my business.'),
         ('3',
          'I can acquire the resources I need to start my business on my own.'),
         ('4',
          'I have already started acquiring the resources I need to start my business.'),
         ('5',
          'I have acquired all the resources I need for starting my business.')])

    Allocate_resources = fields.Selection(
        [('1',
          'I dont know how to assign resources to successfully start and complete projects or activities.'),
         ('2',
          'I need assistance with assigning resources effectively.'),
         ('3',
          'I am able to assign resources effectively on my own.'),
         ('4',
          'I apply a systematic approach to assigning resources.'),
         ('5',
          'I am effective in assigning resources so that my projects or activities succeed.')])

    use_of_resources = fields.Selection(
        [('1',
          'I dont know how to monitor the use of resources during the implementation of a project or activities.'),
         ('2',
          'I need assistance with monitoring the use of resources during the implementation of a project or activities.'),
         ('3',
          'I am able to monitor the use of resources in the implementation of projects or activities on my own.'),
         ('4',
          'I have a systematic approach to monitoring the use of resources in the implementation of projects or activities.'),
         ('5',
          'I am effective at monitoring the use of resources in the implementation of projects or activities.')])
    
    #newly added fields...
    @api.onchange('x_overall_experience', 'x_sp_facilities', 'x_sp_friendliness', 'x_sp_professionalism',
                  'x_waiting_period')
    def total_for_service_provider_rating(self):
        total_score = int(self.x_overall_experience) + int(self.x_sp_facilities) + int(self.x_sp_friendliness) + int(
            self.x_sp_professionalism) + int(self.x_waiting_period)
        self.service_rating_assessment_total = total_score
    
    service_rating_assessment_total = fields.Integer('Service Total', compute='total_for_service_provider_rating')
    x_business_idea = fields.Boolean(string="Business Idea",related='voucher_application_id.business_idea',readonly=True)
    x_existing_business = fields.Boolean(string="Existing Business",related='voucher_application_id.existing_business',readonly=True)
    x_no_business = fields.Boolean(string="No Business",related='voucher_application_id.no_business',readonly=True)
    x_overall_experience = fields.Selection([('5','Excellent'),('4','Good'),('3','Average'),('2','Fair'),('1','Poor')],String="Overall Experience")
    x_sp_facilities = fields.Selection([('5','Excellent'),('4','Good'),('3','Average'),('2','Fair'),('1','Poor')],String="Facilities")
    x_sp_friendliness = fields.Selection([('5','As friendly as I expected'),('4','Friendly'),('3','Average'),('2','Less friendly than I expected'),('1','Unfriendly')],String="Service provider Friendliness")
    x_sp_professionalism = fields.Selection([('5','As professional as I expected'),('4','Professional'),('3','Neither professional nor unprofessional'),('2','Less professional than I expected'),('1','Unprofessional')],String="Professionalism")
    x_waiting_period = fields.Selection([('5','I saw them Immediatedly'),('4','I waited less than 5 minutes'),('3','I waited 5 - 10 minutes'),('2','I waited 10 - 15 minutes'),('1','I waited more than 15 minutes')],String="Waiting period")
    
    def get_va_data(self):
        return {'rec': self}
    
    @api.model
    def create(self, vals):
        rec = super(VoucherAssessmnent, self).create(vals)
        voucher_application         = self.env['voucher.application'].browse(self._context.get('active_id'))
        #voucher_application.status  = 'submitted_product'  
           
        return rec
            
