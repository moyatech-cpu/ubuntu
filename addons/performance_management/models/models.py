# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Compliance(models.Model):
    _name = 'performancemanagement.compliance'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(
        string="Title"
        )
    agreement_start = fields.Datetime(
        string="Agreement Start" 
        # default=fields.Datetime.today
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

    @api.model
    def create(self, vals):
        result = super(Compliance, self).create(vals)
        agreement_info ={
            'name': result.name,
            'date_start': result.agreement_start,
            'compliance_id': result.id
        }
        self.env['performancemanagement.agreement'].create(agreement_info)

        return result

class Agreement(models.Model):
    _name = 'performancemanagement.agreement'
    _inherit = ['mail.thread','mail.activity.mixin']

    compliance_id = fields.Many2one(
        'performancemanagement.compliance', 
        string="Related CC"
        )
    employee_id = fields.Many2one(
        'hr.employee',
        string="Related Employee"
        )

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
    employee = fields.Char(
        string="Employee",
        related="employee_id.name"
        )
    employee_pos = fields.Many2one(
        string="Employee Position",
        related="employee_id.job_id"
        )
    line_manager = fields.Many2one(
        string="Line Manager",
        related="employee_id.parent_id"
        )
    manager_pos = fields.Char(
        string="Manager Position"
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
    emp_comments = fields.Html()
    color = fields.Integer()
    state = fields.Selection(
        [
            ('new', 'NEW'),
            ('review', 'REVIEW'),
            ('performance dialogue', 'PERFORMANCE DIALOGUE'),
            ('performance contract', 'PERFORMANCE CONTRACT'),
            ('completed', 'COMPLETED')
        ],
        string='Status',
        readonly=True,
        group_expand='_expand_states',
        default='new'
        )

    def action_to_lm(self):
        self.state = 'review'

    def action_to_dia(self):
        self.state = 'performance dialogue'

    def action_to_con(self):
        self.state = 'performance contract'

    def action_completed(self):
        self.state = 'completed'

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    # @api.model
    # def create(self, values):
    #     record = self.env['performancemanagement.compliance'].create(values)
    #     return record

class P_Management(models.Model):
    _name = 'performancemanagement.performance'

    perspective = fields.Char("Perspective")
    kpa = fields.Char("KPA")
    kpi = fields.Char("KPI")
    weight = fields.Integer("Weight", default=25, readonly=True)

    performance_id = fields.Many2one(
        'performancemanagement.agreement',
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
        group_expand='_expand_states',
        default='short term'
        )
    competence = fields.Char("Competence")
    method = fields.Char("Method")
    responsibility = fields.Char("Responsibility")
    t_frame = fields.Char("Time Frame")
    e_outcome = fields.Char("Expected Outcome")
    a_cost = fields.Float("Anticipated Cost")

    development_id = fields.Many2one(
        'performancemanagement.agreement',
        ondelete="cascade"
    )