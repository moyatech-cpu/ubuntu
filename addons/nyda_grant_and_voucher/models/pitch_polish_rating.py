# coding=utf-8
from odoo import api, fields, models, _
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper
from datetime import date

from odoo import http


class PitchPolishRating(models.Model):
    _name = 'pitch.polish.rating'
    _rec_name = 'branch_id'

    branch_id = fields.Many2one('res.branch', string="Nearest Branch", default=lambda self: self.env.user.branch_id)
    business_name = fields.Char(string="Business Name")
    client_preassessment_id = fields.Many2one('client.preassessment', string="Nearest Branch")
    entrepreneur_id = fields.Many2one('res.users', string="Entrepreneur Name & Surname")
    funding_criteria = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string="Is the concept in line with the NYDA funding criteria? (NOT FOR SCORING PURPOSES)")
    state = fields.Selection([('new', 'New'), ('recommended', 'Recommended')], default='new', string="State")

    evaluation_criteria_business = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    evaluation_criteria_balanced = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    evaluation_criteria_products = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    evaluation_criteria_needs = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    evaluation_criteria_market = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])

    vision_and_mission_idea = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    vision_and_mission_business = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    vision_and_mission_role = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])

    market_and_competition_research = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    market_and_competition_services = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    market_and_competition_market = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])

    solution_business_idea = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    solution_viability = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    solution_market = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])

    differentiation_products_and_services = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    differentiation_innovations = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])

    business_model_understanding = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    business_model_implement = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])

    team_management_capacity = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    team_management_employees = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])

    request_require = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    request_amount = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])

    growth_and_expansion_grow = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])
    growth_and_expansion_years = fields.Selection(
        [('1', 'Poor'), ('2', 'Below Average'), ('3', 'Satisfactory'), ('4', 'Above Average'), ('5', 'Excellent')])

    recommendation = fields.Text(string='')
    evaluator = fields.Char(string='')
    signature = fields.Char(string='')
    pitch_date = fields.Date(string='')
    total = fields.Integer('', related='related_total')
    related_total = fields.Integer(string='Related Total')

    urlemail = fields.Char(string='urlemail')

    @api.model
    def create(self, vals):
        record = super(PitchPolishRating, self).create(vals)
        active_id = self._context.get('active_id')
        preassessment_id = self.env['client.preassessment'].browse([active_id])
        if preassessment_id:
            preassessment_id.write({'state': 'pitch_polish'})
        record.write({'client_preassessment_id': active_id or False})
        return record

    @api.multi
    def btn_recommend(self):
        """ Sets state to recommended. Add logic if need anything once application is moved to recommended state. """
        mail_template_id = self.env.ref('nyda_grant_and_voucher.picth_and_polish_mail_template')
        active_id = self._context.get('active_id')
        preassessment_id = self.env['client.preassessment'].browse([active_id])
        for rec in self:
            if mail_template_id:

                base_url = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                base_url += '/web/login?db={}#id={}&view_type=form&model=client.preassessment'.format(self.env.cr.dbname,
                                                                                                 preassessment_id.id)

                mail_template_id.with_context(user=self.env.user, grant_url=base_url).send_mail(rec.id, force_send=True)
            rec.write({'state': 'recommended'})
            if preassessment_id:
                ts = TwilioSMSHelper()
                ts.send_sms({
                'message_to': preassessment_id.cell,
                'message_text': """Hello, \n Your application has been recommended has been accepted.\n You can login to system to check details."""
                })
                preassessment_id.write({'state': 'recommended'})


    @api.multi
    def btn_refer(self):
        """ Sets state to Refer. Add logic if need anything once application is moved to BTM Training Application Form. """
        active_id = self._context.get('active_id')
        preassessment_id = self.env['client.preassessment'].browse([active_id])
        youth_enquiry_id = self.env['youth.enquiry'].search([('user_id', '=', preassessment_id.client_id.id)], limit=1)
        action = self.sudo().env.ref(
            'bmt_training.action_bmt_training_application').read()[0]
        for record in self:
            ctx = {'default_participant_name': youth_enquiry_id.id or False}
            action['views'] = [(False, u'form')]
            action['context'] = ctx
            preassessment_id.write({'state': 'BMT_Referred'})
            return action

    @api.onchange('evaluation_criteria_business', 'evaluation_criteria_balanced', 'evaluation_criteria_products',
                  'evaluation_criteria_needs', 'evaluation_criteria_market', 'vision_and_mission_idea',
                  'vision_and_mission_business', 'vision_and_mission_role', 'market_and_competition_research',
                  'market_and_competition_services', 'market_and_competition_market', 'solution_business_idea',
                  'solution_viability', 'solution_market', 'differentiation_products_and_services',
                  'differentiation_innovations', 'business_model_understanding', 'business_model_implement',
                  'team_management_capacity', 'team_management_employees', 'request_require', 'request_amount',
                  'growth_and_expansion_grow', 'growth_and_expansion_years')
    def pitch_polish_total(self):
        total = int(self.evaluation_criteria_business) + int(self.evaluation_criteria_balanced) + \
                int(self.evaluation_criteria_products) + int(self.evaluation_criteria_needs) + int(
            self.evaluation_criteria_market) + int(self.vision_and_mission_idea) \
                + int(self.vision_and_mission_business) + int(self.vision_and_mission_role) + int(
            self.market_and_competition_research) \
                + int(self.market_and_competition_services) + int(self.market_and_competition_market) + int(
            self.solution_business_idea) \
                + int(self.solution_viability) + int(self.solution_market) + int(
            self.differentiation_products_and_services) \
                + int(self.differentiation_innovations) + int(self.business_model_understanding) + int(
            self.business_model_implement) \
                + int(self.team_management_capacity) + int(self.team_management_employees) + int(
            self.request_require) + int(self.request_amount) \
                + int(self.growth_and_expansion_grow) + int(self.growth_and_expansion_years)

        self.related_total = total
