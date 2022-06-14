# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper
from datetime import datetime,date
from odoo.exceptions import UserError


class EmployeeMonitoringReport(models.Model):
    _name = "employee.monitoring.report"
    _rec_name = "monitoring_report_id"

    monitoring_report_id = fields.Many2one("monitoring.report", string="Monitoring Report")
    file = fields.Binary(string="File")
    filename = fields.Char(string="File Name")
    comments = fields.Char(string="Comments")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    poe_file = fields.Binary(string="POE File")
    poe_filename = fields.Char(string="POE File Name")
    is_nyda_employee = fields.Boolean(string="Is NYDA Employee", default=lambda self: self.nyda_employee(),
                                     compute="nyda_employee")

    @api.multi
    def nyda_employee(self):
        for rec in self:
            if self.env.user.has_group('monitoring_and_evaluation.group_nyda_employees'):
                if rec.id:
                    rec.is_nyda_employee = True
                else:
                    bool = True
                    return bool
            else:
                if rec.id:
                    rec.is_nyda_employee = False
                else:
                    bool = False
                    return bool

class MonitoringReport(models.Model):
    _name = "monitoring.report"
    _rec_name = "name"
    _description = 'Monitoring Report'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    employee_monitoring_report_ids = fields.One2many('employee.monitoring.report', 'monitoring_report_id',
                                                     string="Employee monitoring Report")
    strategic_plan_id = fields.Many2one("strategic.plan", string="Strategic Plan")
    is_perfomance_deadline_mailed = fields.Boolean(string="Is Perfomance report Mail Sent")
    is_me_personnal = fields.Boolean(string="ME Personnal", default=lambda self: self.compute_me_personnal(),
                                     compute="compute_me_personnal")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    department_id = fields.Many2one('hr.department', 'Department')
    sign = fields.Binary(string="Signature")
    state = fields.Selection([
        ('new', 'New'),
        ('submitted', 'Submitted'),
        ('review', 'Line Manager Review'),
        ('approve', 'Line Manager Approve'),
        ('reject', 'Line Manager Rejected'),
        ('sm_review', 'Senior Manager Review'),
        ('sm_approve', 'Senior Manager Approve'),
        ('sm_reject', 'Senior Manager Rejected'),
        ('ed_review', 'Executive Director Review'),
        ('ed_approve', 'Executive Director Approve'),
        ('ed_reject', 'Executive Director Rejected'),
    ], string='Monitoring Report Status', default='new', track_visibility='onchange')
    employee_id = fields.Many2one('res.users', string="Employee", domain=lambda self: [
        ("groups_id", "=", self.env.ref("monitoring_and_evaluation.group_nyda_employees").id)])
    type = fields.Selection([('programme', 'Programme'), ('division', 'Division'), ('business_unit', 'Business Unit'),
                             ('individual', 'Individual')], string="Type")
    is_submit = fields.Boolean(string="Is Submiited")
    line_manager_id = fields.Many2one('res.users', string="Line Manager")
    senior_manager_id = fields.Many2one('res.users', string="Senior Manager", domain=lambda self: [
        ("groups_id", "=", self.env.ref("monitoring_and_evaluation.group_senior_manager").id)])
    executive_director_id = fields.Many2one('res.users', string="Executive Director", domain=lambda self: [
        ("groups_id", "=", self.env.ref("strategy_and_planning.group_executive_director").id)])

    @api.onchange('department_id')
    def onchange_dept_id(self):
        if self.department_id:
            self.line_manager_id = False
            dept = self.env['hr.department'].search([('id', '=', self.department_id.id)]).line_manager_ids.ids
            if not dept:
                raise UserError(_("Please select another department.There are no line managers in these department !!"))

    @api.multi
    def compute_me_personnal(self):
        if self.env.user.has_group('monitoring_and_evaluation.group_me_personnal') or self.env.user.has_group('base.group_system'):
            if self.id:
                self.is_me_personnal = True
            else:
                bool = True
                return bool
        else:
            if self.id:
                self.is_me_personnal = False
            else:
                bool = False
                return bool

    @api.multi
    def submit_report(self):
        for rec in self:
            rec.write({
                'state': 'submitted',
                'is_submit': True
            })
            if rec.state == "submitted":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.employee_id.login,
                                                                                      'email_to': rec.line_manager_id.login
                                                                                  })
        return True

    @api.multi
    def reviewFuncation(self):
        for rec in self:
            rec.write({
                'state': 'review',
            })
            if rec.state == "review":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.line_manager_id.login,
                                                                                      'email_to': rec.employee_id.login
                                                                                  })
        return True

    @api.multi
    def SmReviewFunction(self):
        for rec in self:
            rec.write({
                'state': 'sm_review',
            })
            if rec.state == "sm_review":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.senior_manager_id.login,
                                                                                      'email_to': rec.line_manager_id.login
                                                                                  })
        return True

    @api.multi
    def EdReviewFunction(self):
        for rec in self:
            rec.write({
                'state': 'ed_review',
            })
            if rec.state == "ed_review":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.line_manager_id.login,
                                                                                      'email_to': rec.employee_id.login
                                                                                  })
        return True

    @api.multi
    def acceptedFuncation(self):
        for rec in self:
            rec.write({
                'state': 'approve',
            })
            if rec.state == "approve":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.line_manager_id.login,
                                                                                      'email_to': rec.senior_manager_id.login
                                                                                  })
        return True

    @api.multi
    def SmAcceptedFunction(self):
        for rec in self:
            rec.write({
                'state': 'sm_approve',
            })
            if rec.state == "sm_approve":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.senior_manager_id.login,
                                                                                      'email_to': rec.line_manager_id.login
                                                                                  })
        return True

    @api.multi
    def EdAcceptedFunction(self):
        for rec in self:
            rec.write({
                'state': 'ed_approve',
            })
            if rec.state == "ed_approve":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.executive_director_id.login,
                                                                                      'email_to': rec.senior_manager_id.login
                                                                                  })
        return True

    def send_deadline_mail(self):
        mail = self.env['monitoring.report'].sudo().search(
            [('is_perfomance_deadline_mailed', '=', False), ('to_date', '!=', False)])
        for rec in mail:
            date_time_obj = datetime.strptime(rec.to_date, '%Y-%m-%d')
            hours =  date_time_obj.date() - date.today()
            if 2 > hours.days > 0:
                email_template = self.env.ref('monitoring_and_evaluation.deadline_mail_template')
                if email_template:
                    mailed = self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True)
                    if mailed:
                        rec.is_perfomance_deadline_mailed = True

    @api.multi
    def rejectedFuncation(self):
        for rec in self:
            rec.write({
                'state': 'reject',
            })
            if rec.state == "reject":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.line_manager_id.login,
                                                                                      'email_to': rec.employee_id.login
                                                                                  })
        return True

    @api.multi
    def SmRejectedFunction(self):
        for rec in self:
            rec.write({
                'state': 'sm_reject',
            })
            if rec.state == "sm_reject":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.senior_manager_id.login,
                                                                                      'email_to': rec.line_manager_id.login
                                                                                  })
        return True

    @api.multi
    def EdRejectedFunction(self):
        for rec in self:
            rec.write({
                'state': 'ed_reject',
            })
            if rec.state == "ed_reject":
                email_template = self.env.ref('monitoring_and_evaluation.monitoring_report_mail_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(rec.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_from': rec.executive_director_id.login,
                                                                                      'email_to': rec.senior_manager_id.login
                                                                                  })
        return True

    @api.model
    def create(self, vals):
        res = super(MonitoringReport, self).create(vals)
        # employee = self.env['hr.employee'].search([('department_id','=',vals.get('department_id'))])
        # employee = self.env['hr.employee'].search([('department_id', '=', vals.get('department_id'))])
        # if res.employee_id:
            # for emp in employee:
            # if emp.user_id.has_group('monitoring_and_evaluation.group_monitoring_user'):
            # email_template = self.env.ref('monitoring_and_evaluation.reporting_time_email_template')
            # inquiry_email_template.with_context(u=emp.user_id).send_mail(res.id, force_send=True)
            # self.env['mail.template'].browse(email_template.id).send_mail(res.id, force_send=True)
        is_me = res.employee_id.has_group('monitoring_and_evaluation.group_me_personnal')
        is_admin = res.employee_id.has_group('base.group_system')
        if not is_me:
            if not is_admin:
                if 'from_date' in vals:
                    if vals.get('from_date') != False:
                        # For Sending Mail
                        email_template = self.env.ref('monitoring_and_evaluation.reporting_time_email_template')
                        if email_template:
                            self.env['mail.template'].browse(email_template.id).send_mail(res.id, force_send=True)
                        # For Sending Message
                        model_id = self.env['ir.model'].sudo().search([('model', '=', self._name)])
                        ts = TwilioSMSHelper()
                        twilio_message = self.env['twilio.sms'].search([('message_model_id', '=', model_id.id), ('type', '=', 'create')])
                        if twilio_message:
                            for msg in twilio_message:
                                message = msg.message_text + "\nYour monitoring plan name is " + res.name + " and meeting time is " + res.from_date + "."
                                ts.send_enquiry_sms({
                                    'message_to': res.employee_id.mobile,
                                    'message_text': message
                                })
        return res

    @api.multi
    def write(self, vals):
        res = super(MonitoringReport, self).write(vals)
        is_me = self.employee_id.has_group('monitoring_and_evaluation.group_me_personnal')
        is_admin = self.employee_id.has_group('base.group_system')
        if not is_me:
            if not is_admin:
                if 'from_date' in vals:
                    if vals.get('from_date') != False:
                        # For Sending Mail
                        email_template = self.env.ref('monitoring_and_evaluation.update_reporting_time_email_template')
                        if email_template:
                            self.env['mail.template'].browse(email_template.id).send_mail(self.id, force_send=True)
                        # For Sending Message
                        model_id = self.env['ir.model'].sudo().search([('model', '=', self._name)])
                        ts = TwilioSMSHelper()
                        twilio_message = self.env['twilio.sms'].search([('message_model_id', '=', model_id.id), ('type', '=', 'write')])
                        if twilio_message:
                            for msg in twilio_message:
                                message = msg.message_text + "\nYour monitoring plan name is " + self.name + " and meeting time is updated which is " + self.from_date + "."
                                ts.send_enquiry_sms({
                                    'message_to': self.employee_id.mobile,
                                    'message_text': message
                                })
        is_me_emp = self.env.user.has_group('monitoring_and_evaluation.group_me_personnal')
        is_admin_emp = self.env.user.has_group('base.group_system')
        is_line_emp = self.env.user.has_group('strategy_and_planning.group_line_manager')
        if vals.get('employee_monitoring_report_ids'):
            if not is_me_emp and not is_admin_emp and not is_line_emp:
                if vals.get('to_date'):
                    date_time_obj = datetime.strptime(vals.get('to_date'), '%Y-%m-%d')
                elif self.to_date:
                    date_time_obj = datetime.strptime(self.to_date, '%Y-%m-%d')
                if date_time_obj:
                    diff = date_time_obj.date() - date.today()
                    if not diff.days >= 0:
                        raise UserError(_("You cannot update reports as the deadline has been passed."))
        return res
