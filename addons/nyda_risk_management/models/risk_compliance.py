# -*- coding: utf-8 -*-

from odoo import api, fields, models


class RiskCompliance(models.Model):
    """ Main model for risk management. """
    _name = "risk.compliance"
    _description = "This model consist of basic structure to Insurance for the Risk"

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1)

    name = fields.Char('Risk Insurance')
    details = fields.Text('Details/Questions')
    state = fields.Selection([('new', 'New'), ('submit', 'Submit'), ('sign_ed', 'Sign by ED'),
                              ('sign_line_manager', 'Sign by Risk Manager'),
                              ('sign_ceo', 'Sign by CEO'), ('reject', 'Reject')],
                             default='new', string="State")
    assign_department_id = fields.Many2one('hr.department', string="Assign Department")
    assign_person_id = fields.Many2one('hr.employee', string="Assign Person")
    responsible_person = fields.Many2one('hr.employee', string="Resposible Person",
                                         default=_default_employee)
    risk_id = fields.Many2one('risk.management', string="Risk")
    plan_id = fields.Many2one('strategic.plan', string="Plan", related="risk_id.plan_id")
    attachment_id = fields.Binary(string='POE Attachment')
    assign_emp_ids = fields.Many2many('hr.employee', 'risk_compliance_employee_rel',
                                      'compliance_id', 'employee_id', string="Assign Users")
    review_ids = fields.One2many('risk.compliance.review', 'compliance_id', string="Answers")

    @api.multi
    def action_submit(self):
        self.ensure_one()
        group_id = self.env.ref('strategy_and_planning.group_executive_director')
        template_id = self.env.ref('nyda_risk_management.email_template_risk_compliance_submit')
        for user in group_id.users:
            emp = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
            template_id.with_context(u=emp).send_mail(self.id, force_send=True)
        for emp in self.assign_emp_ids:
            self.env['risk.compliance.review'].create({'compliance_id': self.id or False,
                                                       'employee_id': emp.id or False})
        return self.write({'state': 'submit'})


    @api.multi
    def action_sign_ed(self):
        group_id = self.env.ref('nyda_risk_management.risk_manager')
        template_id = self.env.ref('nyda_risk_management.email_template_risk_compliance_sign_ed')
        for user in group_id.users:
            emp = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
            template_id.with_context(u=emp).send_mail(self.id, force_send=True)
        return self.write({
            'state': 'sign_ed'
        })

    @api.multi
    def action_sign_risk_manager(self):
        group_id = self.env.ref('strategy_and_planning.group_ceo')
        template_id = self.env.ref('nyda_risk_management.email_template_risk_compliance_sign_risk_manager')
        for user in group_id.users:
            emp = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
            template_id.with_context(u=emp).send_mail(self.id, force_send=True)
        return self.write({
            'state': 'sign_line_manager'
        })

    @api.multi
    def action_sign_ceo(self):
        email_template_risk_compliance_sign_ceo = self.env.ref(
            'nyda_risk_management.email_template_risk_compliance_sign_ceo')
        email_template_risk_compliance_sign_ceo.send_mail(self.id, force_send=True)
        return self.write({
            'state': 'sign_ceo'
        })

    @api.multi
    def action_reject_ed(self):
        email_template_risk_compliance_reject = self.env.ref(
            'nyda_risk_management.email_template_risk_compliance_reject')
        email_template_risk_compliance_reject.send_mail(self.id, force_send=True)
        return self.write({
            'state': 'reject'
        })

    @api.multi
    def action_reject_manager(self):
        template_id = self.env.ref('nyda_risk_management.email_template_risk_compliance_reject')
        template_id.send_mail(self.id, force_send=True)
        return self.write({
            'state': 'reject'
        })

    @api.multi
    def action_reject_ceo(self):
        template_id = self.env.ref('nyda_risk_management.email_template_risk_compliance_reject')
        template_id.send_mail(self.id, force_send=True)
        return self.write({
            'state': 'reject'
        })


class RiskComplianceReview(models.Model):
    _name = 'risk.compliance.review'
    _description = "Risk Compliance Review"

    compliance_id = fields.Many2one('risk.compliance', string='Compliance')
    employee_id = fields.Many2one('hr.employee', string="Person")
    answer = fields.Text(string="Answer")
