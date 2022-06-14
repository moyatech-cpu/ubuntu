from odoo import api, fields, models
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper


class strategic_goals(models.Model):
    _name = "strategic.goals"
    _rec_name = "strategic_goal"

    automated_numbering = fields.Char(string="Automated Numbering",default='New')
    strategic_goal = fields.Text(string="Strategic Outcome")
    goal_statement = fields.Text(string="Goal Statement")
    justification = fields.Text(string="Justification")
    # strategic_goal_link = fields.Char(string="Strategic Goal Link")
    # number_of_additional_links = fields.Selection([('1', '1'), ('2', '2'),
    #                                                ('3', '3'), ('4', '4'),
    #                                                ('5', '5'), ('6', '6'),
    #                                                ('7', '7'), ('8', '8'),
    #                                                ('9', '9'), ('10', '10'),
    # ], string="Number of Additional Links")
    budget = fields.Float(string="Budget")
    strategic_plan_id = fields.Many2one("strategic.plan", string="Strategic Plan")
    annual_performance_plan_id = fields.Many2one("annual.performance.plan", string="Strategic Plan")
    strategic_plan_objectives_ids = fields.One2many('strategic.plan.objectives', 'strategic_goal_id',
                                                    string="Strategic Plan Objectives")
    expenses = fields.Integer(string="Expenses")
    programme_id = fields.Many2one('programme', string="Programme")
    government_outcomes = fields.Html(string="Contribution to Government Outcomes")

    @api.model
    def create(self, vals):

        seq = self.env['ir.sequence'].next_by_code('strategic.goals') or '/'
        vals['automated_numbering'] = seq
        res = super(strategic_goals, self).create(vals)
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
        res = super(strategic_goals, self).write(vals)
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
    def create_objective_smart_button(self):
        objectives = self.env['strategic.plan.objectives'].search([('strategic_goal_id', '=', self.id)])
        objectives_action = self.env.ref('strategy_and_planning.action_strategic_plan_objectives').read()[0]
        if len(objectives) > 1:
            objectives_action['domain'] = [('id', 'in', objectives.ids)]
            return objectives_action
        else:
            return {'name': 'Objective Form',
                    'view_type': 'form',
                    'view_mode': 'tree',
                    'views': [(self.env.ref('strategy_and_planning.view_strategic_plan_objectives_form').id, 'form')],
                    'res_model': 'strategic.plan.objectives',
                    'view_id': self.env.ref('strategy_and_planning.view_strategic_plan_objectives_form').id,
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                    'context': {'default_strategic_goal_id': self.id}
                    }

    @api.multi
    def view_objective_smart_button(self):
        outcome = self.env['strategic.plan.objectives'].search([('strategic_goal_id', '=', self.id)])
        outcome_action = self.env.ref('strategy_and_planning.action_strategic_plan_objectives').read()[0]
        if len(outcome) >= 1:
            outcome_action['domain'] = [('id', 'in', outcome.ids)]
            return outcome_action
        else:
            return None