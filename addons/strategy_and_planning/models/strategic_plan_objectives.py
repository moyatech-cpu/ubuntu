from odoo import api, fields, models
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper


class strategic_plan_objectives(models.Model):
    _name = "strategic.plan.objectives"
    _rec_name = "strategic_objective"
    
    strategic_objective = fields.Text(string="Strategic Objective")
    objective_statement = fields.Text(string="Objective Statement")
    baseline = fields.Text(string="Baseline")
    justification = fields.Text(string="Justification")
    risk = fields.Text(string="Risk")
    cause = fields.Text(string="Cause")
    impact = fields.Text(string="Impact")
    impact_scale = fields.Selection([("minor","Minor"),
                                     ("mild","Mild"),
                                     ("major","Major"),
                                     ("supreme","Supreme")], string="Impact Scale")
    likelihood = fields.Selection([("unlikely","Unlikely"),
                                     ("likely","Likely"),
                                     ("highly_Probable","Highly Probable")], string="Likelihood")
    inherent_risk = fields.Selection([("4","4"),
                                     ("8","8"),
                                     ("16","16")], string="Inherent Risk")    
    
    controls = fields.Text(string="Controls")
    control_effectiveness = fields.Selection([("weak","Weak"),
                                              ("poor","Poor"),
                                              ("satisfactory","Satisfactory"),
                                              ("good","Good")], string="Control Effectiveness")
    risidual_risk = fields.Selection([("4","4"),
                                     ("8","8"),
                                     ("16","16")], string="Risidual Risk")
    action_plans = fields.Text(string="Action Plans")
    implementation_date = fields.Date(string="Implementation Date")
    risk_elevation_reason = fields.Text(string="Risk Elevation Reason")
    budget = fields.Float(string="Budget")
    programme = fields.Text()
    expected_outcome = fields.Text()
    # strategic_goals = fields.Text()
    strategic_goal_id = fields.Many2one("strategic.goals", string="Strategic Outcome")
    strategic_plan_id = fields.Many2one('strategic.plan', string='Strategic Plan')
    annual_performance_plan_id = fields.Many2one("annual.performance.plan", string="Annual performance Plan")
    annual_performance_plan_target_id = fields.Many2one("annual.performance.plan.target", string="Annual performance Plan Target")

    @api.model
    def create(self, vals):
        res = super(strategic_plan_objectives, self).create(vals)
        model_id = self.env['ir.model'].sudo().search([('model', '=', res._name)])
        # For Sending Message
        # ts = TwilioSMSHelper()
        # message = self.env['twilio.sms'].search([('message_model_id', '=', model_id.id), ('type', '=', 'create')])
        # if message:
        #     for msg in message:
        #         ts.send_enquiry_sms({
        #             # 'message_from': msg.message_from,
        #             'message_to': msg.message_to,
        #             'message_text': msg.message_text
        #         })
        # For Sending Email
        email_template = self.env['mail.template'].search([('model_id', '=', model_id.id), ('type', '=', 'create')])
        if email_template:
            for mail in email_template:
                if mail:
                    mail.send_mail(res.id, force_send=True)
        return res

    @api.multi
    def write(self, vals):
        res = super(strategic_plan_objectives, self).write(vals)
        model_id = self.env['ir.model'].sudo().search([('model', '=', self._name)])
        # For sending message
        # ts = TwilioSMSHelper()
        # message = self.env['twilio.sms'].search([('message_model_id', '=', model_id.id), ('type', '=', 'write')])
        # if message:
        #     for msg in message:
        #         ts.send_enquiry_sms({
        #             # 'message_from': msg.message_from,
        #             'message_to': msg.message_to,
        #             'message_text': msg.message_text
        #         })
        # For Sending Email
        email_template = self.env['mail.template'].search([('model_id', '=', model_id.id), ('type', '=', 'write')])
        if email_template:
            for mail in email_template:
                if mail:
                    mail.send_mail(self.id, force_send=True)
        return res

    @api.multi
    def app_targets_smart_button(self):
        app_target = self.env['annual.performance.plan'].search([('strategic_objectives_id', '=', self.id)])

        app_target_action = self.env.ref('strategy_and_planning.action_annual_performance_plan').read()[0]
        if len(app_target) > 1:
            app_target_action['domain'] = [('id', 'in', app_target.ids)]
            return app_target_action
        else:
            return {'name': 'App Targets',
                    'view_type': 'form',
                    'view_mode': 'tree',
                    'views': [(self.env.ref('strategy_and_planning.view_annual_performance_plan_form').id, 'form')],
                    'res_model': 'annual.performance.plan',
                    'view_id': self.env.ref('strategy_and_planning.view_annual_performance_plan_form').id,
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                    'context': {'default_strategic_objectives_id': self.id,'default_type_bool':'app'}
                    }

    @api.multi
    def view_app_target_smart_button(self):
        outcome = self.env['annual.performance.plan'].search([('strategic_objectives_id', '=', self.id)])
        outcome_action = self.env.ref('strategy_and_planning.action_annual_performance_plan').read()[0]
        if len(outcome) >= 1:
            outcome_action['domain'] = [('id', 'in', outcome.ids)]
            return outcome_action
        else:
            return None