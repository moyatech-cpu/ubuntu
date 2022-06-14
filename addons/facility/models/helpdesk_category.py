# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Normal'),
    ('2', 'Urgent'),
    ('3', 'High'),
]

class HelpdeskSubCategory(models.Model):
    _name = 'helpdesk.subcategory'
    _rec_name = 'name'
    _description= 'Helpdesk Sub Category'

    name = fields.Char(string="Name")

class HelpdeskCategory(models.Model):
    _name = 'helpdesk.category'
    _rec_name = 'name'
    _description= 'Helpdesk Category'

    name = fields.Char(string="Name")
    sub_category_id = fields.Many2one('helpdesk.subcategory', string="Sub category")
    facility_officer_id = fields.Many2one('res.users', string="Facility Officer", domain=lambda self: [
        ("groups_id", "=", self.env.ref("facility.facility_officer").id)])
    facility_manager_id = fields.Many2one('res.users', string="Facility Manager", domain=lambda self: [
        ("groups_id", "in", [self.env.ref("facility.facility_manager").id, self.env.ref("base.group_system").id])],
                                          default=lambda self: self.env.user.id)
    team_leader_id = fields.Many2one('res.users', string="Team Leader", domain=lambda self: [
        ("groups_id", "=", self.env.ref("facility.team_leader").id)])

class HelpdeskliteTicket(models.Model):
    _inherit = 'helpdesk_lite.ticket'

    helpdesk_category_id = fields.Many2one('helpdesk.category', string="Category")
    facility_officer_id = fields.Many2one('res.users', string="Facility Officer", domain=lambda self: [
        ("groups_id", "=", self.env.ref("facility.facility_officer").id)],
                                          related="helpdesk_category_id.facility_officer_id")
    facility_manager_id = fields.Many2one('res.users', string="Facility Manager", domain=lambda self: [
        ("groups_id", "=", self.env.ref("facility.facility_manager").id)],
                                          related="helpdesk_category_id.facility_manager_id")
    sla_time = fields.Datetime(string="SLA Time")
    is_mailed_sla = fields.Boolean(string="Is SLA Mailed")
    status = fields.Selection([('working', 'Working'), ('not_working', 'Not Working')], string='Status', default='working')
    priority = fields.Selection(AVAILABLE_PRIORITIES, 'Priority', index=True, default='1', track_visibility='onchange')
    cancellation_reason = fields.Text(String="Cancellation Reason")
    service = fields.Selection(
        [('worst', 'Worst'), ('bad', 'Bad'), ('good', 'Good'), ('best', 'Best'), ('excellent', 'Excellent'),
         ('outstanding', 'Outstanding')], string="Service Level")
    is_new_stage = fields.Boolean(string="Is New Stage", compute="compute_new_stage")
    is_progress_stage = fields.Boolean(string="Is Progress Stage", compute="compute_progress_stage")
    is_solved_stage = fields.Boolean(string="Is Solved Stage", compute="compute_solved_stage")
    is_solved_officer_stage = fields.Boolean(string="Is Solved By Officer Stage", compute="compute_solved_officer_stage")
    contact_number = fields.Char(string="Contact Number")
    subcategory_id = fields.Many2one('helpdesk.subcategory', string="Subcategory")
    service_description = fields.Text(string="Service Description")
    end_user_id = fields.Many2one('res.users', string="Name", domain=lambda self: [
        ("groups_id", "=", self.env.ref("facility.end_user").id)], default=lambda self:self.get_end_user())

    def get_end_user(self):
        end_user_ids = self.env.ref('facility.end_user').users.ids
        #end_user_ids = self.env.ref('facility.end_user').id
        if self.env.user.id in end_user_ids:
            return self.env.user.id

    def solved_by_officer(self):
        stage = self.env.ref('facility.stage_solved_officer').id
        if stage:
            mail_template = self.env.ref('facility.solved_by_officer_email_template')
            if mail_template:
                mail_template.send_mail(self.id, force_send=True)
            self.stage_id = stage

    @api.onchange('end_user_id')
    def onchange_end_user_id(self):
        if self.end_user_id:
            print ("\n\n\nCalled\n\n\n")
            self.partner_id = self.end_user_id.partner_id.id
            self.email_from = self.end_user_id.login
            self.contact_number = self.end_user_id.phone

    def mark_in_progress(self):
        stage = self.env.ref('helpdesk_lite.stage_inprogress').id
        if stage:
            self.stage_id = stage

    @api.onchange('helpdesk_category_id')
    def onchange_category(self):
        if self.helpdesk_category_id:
            self.subcategory_id = self.helpdesk_category_id.sub_category_id.id

    @api.depends('stage_id')
    def compute_solved_officer_stage(self):
        if self.stage_id.id == self.env.ref('facility.stage_solved_officer').id:
            self.is_solved_officer_stage = True

    @api.depends('stage_id')
    def compute_solved_stage(self):
        if self.stage_id.id == self.env.ref('helpdesk_lite.stage_solved').id:
            self.is_solved_stage = True

    @api.depends('stage_id')
    def compute_new_stage(self):
        if self.stage_id.id == self.env.ref('helpdesk_lite.stage_new').id:
            self.is_new_stage = True

    @api.depends('stage_id')
    def compute_progress_stage(self):
        if self.stage_id.id == self.env.ref('helpdesk_lite.stage_inprogress').id:
            self.is_progress_stage = True

    def mark_solved(self):
        action = {
            'name': "Submit Feedback",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rate.service',
            'context': {'default_type': 'solved'},
            'target': 'new'
        }
        return action

    def cancel_tickets(self):
        action = {
            'name': "Submit Feedback",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rate.service',
            'context': {'default_type': 'cancel'},
            'target': 'new'
        }
        return action

    @api.constrains('sla_time')
    @api.one
    def _check_number(self):
        if self.sla_time:
            time = datetime.strptime(self.sla_time, '%Y-%m-%d %H:%M:%S')
            if time <= datetime.now():
                raise ValidationError(_("Date has already passed please select another date."))
            else:
                if self.priority == '1':
                    after_4_days = datetime.now() + timedelta(days=4)
                    if time > after_4_days:
                        raise ValidationError(_('SLA Time should not be greater 120 hours from current time.'))
                elif self.priority == '2':
                    after_3_days = datetime.now() + timedelta(days=3)
                    if time > after_3_days:
                        raise ValidationError(_('SLA Time should not be greater 72 hours from current time.'))
                elif self.priority == '3':
                    after_2_days = datetime.now() + timedelta(days=2)
                    if time > after_2_days:
                        raise ValidationError(_('SLA Time should not be greater 48 hours from current time.'))

    def not_working_state(self):
        for rec in self:
            rec.status = 'not_working'

    def working_state(self):
        for rec in self:
            rec.status = 'working'

    def send_esacalation_mail(self):
        new = self.env.ref('helpdesk_lite.stage_new')
        inprogress = self.env.ref('helpdesk_lite.stage_inprogress')
        tickets = self.env['helpdesk_lite.ticket'].search(
            ['|', ('stage_id', '=', new.id), ('stage_id', '=', inprogress.id), ('is_mailed_sla', '=', False),
             ('sla_time', '!=', False)])
        for ticket in tickets:
            if ticket.sla_time:
                date_sla_time = datetime.strptime(ticket.sla_time, '%Y-%m-%d %H:%M:%S')
                if datetime.now() > date_sla_time:
                    from_user = self.env.ref('base.user_root')
                    mail_template = self.env.ref('facility.escelation_email_template')
                    mail_template.send_mail(ticket.id, force_send=True,
                                            email_values={
                                                'email_from': from_user.company_id.email,
                                                'email_to': ticket.facility_manager_id.login
                                            })
                    ticket.is_mailed_sla = True

    @api.onchange('priority')
    def check_mail(self):
        if self.priority:
            self.sla_time = False
            self.is_mailed_sla = False

    @api.onchange('sla_time')
    def check_time(self):
        if self.sla_time:
            self.is_mailed_sla = False

    @api.model
    def create(self, vals):
        res = super(HelpdeskliteTicket, self).create(vals)
        mail = ''
        mail_template = self.env.ref('facility.logged_ticket_email_template')
        if mail_template:
            mail = res.facility_manager_id.login + ", " + res.facility_officer_id.login + ", " + res.email_from
            mail_template.send_mail(res.id, force_send=True,
                                    email_values={
                                        'email_from': res.env.user.login,
                                        'email_to': mail
                                    })
        return res

    @api.multi
    def takeit(self):
        res = super(HelpdeskliteTicket, self).takeit()
        stage = self.env.ref('helpdesk_lite.stage_inprogress').id
        if stage:
            self.stage_id = stage
        return res
