# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)
# import base64

class Compliance(models.Model):
    _name = 'performancemanagement.compliance'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    @api.multi 
    def _default_comp_title(self):
        total_len = self.env['performancemanagement.compliance'].search_count([])
        new_entry = total_len + 1
        comp_title = ("EMP%s - Performance Agreement" %new_entry)

        return comp_title

    name = fields.Char(
        string="Title",
        default=_default_comp_title,
        readonly=True,
        required=True
        )
    agreement_start = fields.Datetime(
        string="Agreement Start"
        )
    agreement_end = fields.Date(
        string="Agreement End"
        )
    monitoring_start = fields.Date(
        string="Monitoring Start"
        )
    monitoring_end = fields.Date(
        string="Monitoring End"
        )
    description = fields.Html()
    priority = fields.Selection(
        [
            ('level 1', 'LEVEL 1'), 
            ('level 2', 'LEVEL 2')
        ])

    @api.model
    def create(self, vals):
        result = super(Compliance, self).create(vals)
        cron_info = {
            'name': 'Agreement Card Scheduler',
            'active': True,
            'user_id': 'base.user_root',
            'interval_number': 0,
            'interval_type': 'hours',
            'numbercall': -1,
            'doall': False,
            'nextcall': result.agreement_start,
            'model_id': 'performance_management.model_performancemanagement_agreement'
        }
        self.env['ir.cron'].create(cron_info)

        return result

class Agreement(models.Model):
    _name = 'performancemanagement.agreement'
    _inherit = ['mail.thread','mail.activity.mixin', 'mail.mail']
    _rec_name = "name"

    compliance_id = fields.Many2one(
        'performancemanagement.compliance', 
        string="Related CC"
        )
    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee"
        )
    image_small = fields.Binary('Image', related='employee_id.image_small')
    date_start = fields.Datetime(
        string="Date Started",
        related="compliance_id.agreement_start",
        readonly=True
        )
    date_end = fields.Date(
        string="Date Ending",
        related="compliance_id.agreement_end"
        )
    name = fields.Char(
        string="Title",
        related="compliance_id.name"
        )
    employee_pos = fields.Many2one(
        string="Employee Position",
        related="employee_id.job_id"
        )
    line_manager = fields.Many2one(
        'hr.employee',
        string="Line Manager",
        related="employee_id.parent_id"
        )
    manager_pos = fields.Many2one(
        "hr.job",
        string="Manager Position",
        related="employee_id.parent_id.job_id"
        )
    pmanagement = fields.One2many(
        "performancemanagement.performance", 
        "performance_id", 
        string="Performance Management"
        )
    personal_dev = fields.One2many(
        "performancemanagement.development", 
        "development_id", 
        string="Personal Development Plan"
        )
    readonly_employee = fields.Boolean(compute="_check_user_role", store=False)
    emp_comments = fields.Html()
    add_duties = fields.Html()
    readonly_manager = fields.Boolean(compute="_check_manager_role", store=False)
    manager_comments = fields.Text()
    readonly_executive = fields.Boolean(compute="_check_executive_role", store=False)
    executive_comments = fields.Text()
    color = fields.Integer()
    state = fields.Selection(
        [
            ('new', 'NEW'),
            ('review', 'REVIEW'),
            ('performance dialogue', 'PERFORMANCE DIALOGUE'),
            ('performance contract', 'PERFORMANCE CONTRACT'),
            ('completed', 'COMPLETED'),
            ('training intervention', 'TRAINING INTERVENTION'),
            ('grievance', 'GRIEVANCE')
        ],
        string='Status',
        readonly=True,
        group_expand='_expand_states',
        default='new'
        )
    priority = fields.Selection(
        [
            ('level 1', 'LEVEL 1'), 
            ('level 2', 'LEVEL 2')
        ])
    kanban_state = fields.Selection(
        [
            ('done', 'Done'), 
            ('blocked', 'Blocked'),
            ('normal', 'Normal')
        ],
        'Kanban State',
        default='normal'
        )

    def _check_user_role(self):
        for rec in self:
            rec.readonly_employee = self.env.user.has_group('monitoring_and_evaluation.group_nyda_employees')

    def _check_manager_role(self):
        for rec in self:
            rec.readonly_manager = self.env.user.has_group('strategy_and_planning.group_line_manager')

    def _check_executive_role(self):
        for rec in self:
            rec.readonly_executive = self.env.user.has_group('strategy_and_planning.group_executive_director')

    @api.constrains('pmanagement')
    def _check_total(self):
        for rec in self:
            total = 0
            for weight in rec['pmanagement']:
                total += weight['weight']
        if total > 100:
            raise ValidationError('Weight total cannot be greater than 100.')
        elif total < 100:
            raise ValidationError('Weight total cannot be lesser than 100.')

    def action_to_lm(self):
        self.state = 'review'

    def action_to_dia(self):
        self.state = 'performance dialogue'

    def action_to_int(self):
        self.state = 'training intervention'

    def action_to_con(self):
        self.state = 'performance contract'

    def action_to_grieve(self):
        self.state = 'grievance'

    def action_completed(self):
        self.state = 'completed'

    @api.multi
    def action_to_monitoring(self):
        monitoring_info = 0

        monitoring_record = self.env['performancemanagement.monitoring'].create({
            'name': self.name,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'compliance_id': self.compliance_id.id,
            'employee_id': self.employee_id.id,
            'image_small': self.image_small,
            'priority': self.priority,
            'kanban_state': self.kanban_state,
            'employee_pos': self.employee_pos.id,
            'line_manager': self.line_manager.id,
            'manager_pos': self.manager_pos.id,
            'emp_comments': self.emp_comments,
            'manager_comments': self.manager_comments,
        })
        
        for rec in self.pmanagement:
            self.env['performancemanagement.scores'].create({
                'perspective': rec.perspective,
                'kpa': rec.kpa,
                'kpi': rec.kpi,
                'weight': rec.weight,
                'monitoring_id': monitoring_record.id,
                'scores_id': monitoring_record.id,
            })

    def schedule_activiy(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Schedule',
            'res_model': 'mail.activity',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'form_view_initial_mode': 'edit'},
        }

        return action

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def _check_date(self):
        agreement_obj = self.env['performancemanagement.agreement']
        mail_mail = self.env['mail.mail']
        mail_ids = []
        today = datetime.now().date()
        #date = agreement_obj.date_start.date()
        day_before = today + timedelta(days=1)
        _logger.info("Checking date for rec in self: %s",day_before)
        comp_id = agreement_obj.search([])
        _logger.info("Checking date for rec in self: %s",comp_id)

        if comp_id:
            try:
                for val in comp_id:
                    if val.date_start[:10] == str(day_before):
                        email = val.employee_id.work_email
                        name = val.employee_id.name
                        subject = "Performance Agreement Starting"
                        body = _("Hello %s,\n",name)
                        body += _("\tYour performance agreement is starting at %s\n" ,date_start)
                        footer = _("Kind regards.\n")
                        footer += _("%s\n\n",val.employee_id.company_id)
                        email_template = self.env['mail.mail'].create({
                            'email_from': self.env.user.email or '',
                            'subject': subject,
                            'body_html': '<pre><span class="inner-pre" style="font-size: 15px">'+body+'<br>'+footer+'</span></pre>', 
                            'notification': True
                        })
                        email_template.write({'email_to': email})
                        _logger.info("Checking date for rec in self: %s ======",email_template)
                        
                        email_template.send(force_send=True)
            except Exception:
                print("Exception")
        return None

class P_Management(models.Model):
    _name = 'performancemanagement.performance'

    perspective = fields.Char("Perspective")
    kpa = fields.Char("KPA")
    kpi = fields.Char("KPI")
    weight = fields.Integer("Weight")

    performance_id = fields.Many2one(
        'performancemanagement.agreement',
        ondelete="cascade"
    )
    monitoring_id = fields.Many2one(
        'performancemanagement.monitoring',
        ondelete="cascade"
    )

class P_Development(models.Model):
    _name = 'performancemanagement.development'

    t_type = fields.Selection(
        [
            ('short term', 'SHORT TERM'),
            ('medium term', 'MEDIUM TERM'),
            ('long term', 'LONG TERM')
        ],
        string="Training Type",
        default='short term'
        )
    competence = fields.Char("Competence")
    method = fields.Char("Method")
    responsibility = fields.Text("Responsibility")
    t_frame = fields.Char("Time Frame")
    e_outcome = fields.Text("Expected Outcome")
    a_cost = fields.Float("Anticipated Cost")

    development_id = fields.Many2one(
        'performancemanagement.agreement',
        ondelete="cascade"
    )
    monitoring_id = fields.Many2one(
        'performancemanagement.monitoring',
        ondelete="cascade"
    )

class P_Scores(models.Model):
    _name = 'performancemanagement.scores'
    _inherit = 'performancemanagement.performance'

    i_score = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4')
        ],
        string="Inidividual Score"
        )
    lm_score = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4')
        ],
        string="Line Manager Score"
        )
    m_score = fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4')
        ],
        string="Moderated Score"
        )

    readonly_individual = fields.Boolean(compute="_check_individual", store=False)
    readonly_lmanager = fields.Boolean(compute="_check_lmanager", store=False)
    readonly_exec = fields.Boolean(compute="_check_executive", store=False)

    scores_id = fields.Many2one(
        'performancemanagement.monitoring',
        ondelete="cascade"
    )

    def _check_individual(self):
        for rec in self:
            rec.readonly_individual = self.env.user.has_group('monitoring_and_evaluation.group_nyda_employees')

    def _check_lmanager(self):
        for rec in self:
            rec.readonly_lmanager = self.env.user.has_group('strategy_and_planning.group_line_manager')

    def _check_executive(self):
        for rec in self:
            rec.readonly_exec = self.env.user.has_group('strategy_and_planning.group_executive_director')

class Monitoring(models.Model):
    _name = 'performancemanagement.monitoring'
    _inherit = ['mail.thread','mail.activity.mixin']

    active = fields.Boolean('Active', default=True)

    compliance_id = fields.Many2one(
        'performancemanagement.compliance', 
        string="Related CC"
        )
    
    agreement_id = fields.Many2one(
        'performancemanagement.agreement', 
        string="Related Agreement"
        )

    name = fields.Char(
        string="Title"
        )

    date_start = fields.Datetime(
        string="Date Started"
        )
    date_end = fields.Date(
        string="Date Ending"
        )

    state = fields.Selection(
        [
            ('new', 'NEW'),
            ('review', 'REVIEW'),
            ('moderate performance', 'MODERATE PERFORMANCE'),
            ('hr', 'HR'),
            ('completed', 'COMPLETED'),
            ('performance dialogue', 'PERFORMANCE DIALOGUE'),
            ('grievance', 'GRIEVANCE')
        ],
        string='Status',
        readonly=True,
        group_expand='_expand_states',
        default='new'
        )

    color = fields.Integer(related="agreement_id.color")

    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee"
        )
    image_small = fields.Binary('Image', related='employee_id.image_small')

    employee_pos = fields.Many2one(
        string="Employee Position",
        related="employee_id.job_id"
        )
    line_manager = fields.Many2one(
        'hr.employee',
        string="Line Manager",
        related="employee_id.parent_id"
        )
    manager_pos = fields.Many2one('hr.job',
        string="Manager Position",
        related="employee_id.parent_id.job_id"
        )
    pmanagement = fields.One2many(
        "performancemanagement.performance", 
        "performance_id", 
        string="Performance Management"
        )
    scores = fields.One2many(
        "performancemanagement.scores", 
        "scores_id", 
        string="Scores"
        )
    readonly_employee = fields.Boolean(compute="_check_user_role", store=False)
    emp_comments = fields.Html()
    readonly_manager = fields.Boolean(compute="_check_manager_role", store=False)
    manager_comments = fields.Text()

    priority = fields.Selection(
        [
            ('level 1', 'LEVEL 1'), 
            ('level 2', 'LEVEL 2')
        ])
    kanban_state = fields.Selection(
        [
            ('done', 'Done'), 
            ('blocked', 'Blocked'),
            ('normal', 'Normal')
        ],
        'Kanban State'
        )

    def _check_user_role(self):
        for rec in self:
            rec.readonly_employee = self.env.user.has_group('monitoring_and_evaluation.group_nyda_employees')

    def _check_manager_role(self):
        for rec in self:
            rec.readonly_manager = self.env.user.has_group('strategy_and_planning.group_line_manager')

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def action_to_review(self):
        self.state = 'review'

    def action_agree(self):
        self.state = 'moderate performance'

    def action_disagree(self):
        self.state = 'performance dialogue'

    def action_to_hr(self):
        self.state = 'hr'

    def action_to_complete(self):
        self.state = 'completed'

    def action_to_grieve(self):
        self.state = 'grievance'

    def schedule_activiy(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Schedule',
            'res_model': 'mail.activity',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'form_view_initial_mode': 'edit'},
        }

        return action