from odoo import api, fields, models
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper


class strategic_plan(models.Model):
    _name = "strategic.plan"
    _rec_name = 'name'

    state = fields.Selection([('new', 'New'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='new'
                             , string="State")
    name = fields.Char(string="Title")
    from_year = fields.Date(string="From Year")
    to_year = fields.Date(string="To Year")
    strategic_goal_ids = fields.One2many('strategic.goals', 'strategic_plan_id', string="Strategic Goal")
    strategic_objective_ids = fields.One2many('strategic.plan.objectives', 'strategic_plan_id',
                                              string="Strategic Objective")

    # type_bool = fields.Selection([('app', 'APP'), ('other', 'Other')], string='Type')

    @api.model
    def create(self, vals):
        res = super(strategic_plan, self).create(vals)
        model_id = self.env['ir.model'].sudo().search([('model', '=', res._name)])
        # if res.name:
        #     res.name.write({
        #         'strategic_plan_id': res.id,
        #     })
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
    def action_approve(self):
        return self.write({
            'state': 'approved'
        })

    @api.multi
    def action_reject(self):
        return self.write({
            'state': 'rejected'
        })

    @api.multi
    def write(self, vals):
        res = super(strategic_plan, self).write(vals)
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
    def view_outcome_smart_button(self):
        outcome = self.env['strategic.goals'].search([('strategic_plan_id', '=', self.id)])
        outcome_action = self.env.ref('strategy_and_planning.action_strategic_goals2').read()[0]
        if len(outcome) >= 1:
            outcome_action['domain'] = [('id', 'in', outcome.ids)]
            return outcome_action
        else:
            return None

    @api.multi
    def create_outcome_smart_button(self):
        outcome = self.env['strategic.goals'].search([('strategic_plan_id', '=', self.id)])
        outcome_action = self.env.ref('strategy_and_planning.action_strategic_goals2').read()[0]
        return {'name': 'Goal Form',
                'view_type': 'form',
                'view_mode': 'tree',
                'views': [(self.env.ref('strategy_and_planning.view_strategic_goals_form').id, 'form')],
                'res_model': 'strategic.goals',
                'view_id': self.env.ref('strategy_and_planning.view_strategic_goals_form').id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_strategic_plan_id': self.id}
                }

