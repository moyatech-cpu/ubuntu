# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class RiskManagement(models.Model):
    """ Main model for risk management. """
    _name = "risk.management"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "This model consist of basic structure and data regarding Risk Management"

    name = fields.Char('Risk')
    state = fields.Selection([('new', 'New'), ('submit', 'Submitted'), ('accepted', 'Accepted'),
                              ('decline', 'Decline'), ('processed', 'Processed')],
                             default='new', string="State")
    risk_level = fields.Selection([('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')],
                                  string="Risk Level")
    reporting_deadline_start = fields.Date('Start Date')
    reporting_deadline_end = fields.Date('End Date')
    responsible_id = fields.Many2one('res.users', string="Responsible")
    plan_id = fields.Many2one('strategic.plan', string="Plan")
    plan_start_date = fields.Date('From Year', related="plan_id.from_year")
    plan_end_date = fields.Date('To Year', related="plan_id.to_year")
    poe_attachment = fields.Binary("Proof of Evidence")
    support_doc_ids = fields.One2many('risk.support.document', 'risk_id', string="Supporting Documents")
    legislation_log_ids = fields.One2many('legislation.log', 'risk_id', string="Legislation Log")
    lost_assets_ids = fields.One2many('lost.assets', 'risk_id', string="Lost Assets")
    deliverable_ids = fields.One2many('deliverable.log', 'risk_id', string="Deliverable")

    strategic_objective_id = fields.Many2one('strategic.plan.objectives', string="Strategic Objective")
    risk_description = fields.Text('Risk Description')
    contributing_factors = fields.Char('Contributing Factors')
    ideal_control = fields.Char('Ideal Control')
    effect = fields.Char('Effect')
    effect_impact = fields.Selection(
        [('critical', 'Critical'), ('serious', 'Serious'), ('catastrophic', 'Catastrophic')], string='Effect Impact')
    likelihood = fields.Selection([('almost', 'Almost Certain'), ('possible', 'Possible'), ('likely', 'Likely')],
                                  string='Likelihood')
    inherent_risk = fields.Selection([('red', 'Red'),('amber', 'Amber'),('green', 'Green')], string='Inherent risk')
    existing_controls = fields.Char('Existing controls')
    perceived_control = fields.Char(string="PC Effectiveness", help='Perceived Control Effectiveness')
    residual_risk = fields.Selection([('red', 'Red'), ('amber', 'Amber'), ('green', 'Green')], string='Residual risk')
    risk_owner = fields.Many2one('res.users', string="Risk owner")
    improve_risk = fields.Char(string="Improve Risk", help='Actions to improve management of the risk')
    action_owner = fields.Many2one('res.users', string="Action owner")
    time_scale = fields.Date('Time scale')
    monitoring_intervals = fields.Selection([('monthly', 'Monthly'), ('quarterly', 'Quarterly'),
                                             ('annually', 'Annually')], string='Monitoring Intervals')
    risk_reports_count = fields.Integer(compute='_compute_count_risk_report', string='Risk Reports Count')

    @api.multi
    def submited_report_smart_button(self):
        report_ids = self.env['risk.reporting.history'].search([('risk_id', '=', self.id)])
        action = self.env.ref('nyda_risk_management.action_risk_reporting_history').read()[0]
        action['domain'] = [('id', 'in', report_ids.ids)]
        return action

    def _compute_count_risk_report(self):
        for risk in self:
            risk.risk_reports_count = self.env['risk.reporting.history'].search_count([('risk_id', '=', risk.id)])

    @api.multi
    def action_reminder_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('nyda_risk_management', 'email_template_edi_risk')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'risk.management',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'mark_so_as_sent': True,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def check_reporting_timeline(self):
        """ Cron function to check for pending enquiries. """
        from_date_str = self.env['ir.config_parameter'].sudo().get_param('from_date')
        to_date_str = self.env['ir.config_parameter'].sudo().get_param('to_date')
        if from_date_str and to_date_str:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
            today = datetime.today()

            if today >= from_date and today <= to_date:
                risks = self.env['risk.management'].search([('state', '!=', 'processed')])
                for risk in risks:
                    nyda_risk_management_email_template = self.env.ref('nyda_risk_management.risk_management_reporting_email_template')
                    nyda_risk_management_email_template.send_mail(risk.id, force_send=True)

    @api.multi
    def action_approval_send(self):
        """ Function for processing Risk record for approval. """
        return self.write({
            'state': 'submit'
        })

    @api.multi
    def action_reset(self):
        """ Resets record to new state. """
        return self.write({
            'state': 'new'
        })

    @api.multi
    def action_accept(self):
        """ Resets record to new state. """
        return self.write({
            'state': 'accepted'
        })

    @api.multi
    def action_decline(self):
        """ Resets record to new state. """
        return self.write({
            'state': 'decline'
        })        
        

class RiskCompliance(models.Model):
    """ User can add Compliance against Risk. """
    _name = "risk.compliance"
    _description = ""


class RiskSupportDocument(models.Model):
    """ User can add supporting document to the risk. """
    _name = "risk.support.document"
    _description = "Attachments for risk related documents."

    risk_id = fields.Many2one('risk.management', string="Risk")
    support_doc = fields.Binary('Document')


class LegislationLog(models.Model):
    """ Allows user to capture legislation logs to risk """
    _name = "legislation.log"
    _description = "Model to allow user register legislation log for risk."

    name = fields.Char('Legislation')
    risk_id = fields.Many2one('risk.management', string="Risk")


class LostAssetsLog(models.Model):
    """ Allows user to capture lost assets against risk """
    _name = "lost.assets"
    _description = "Model to allow user register lost assets against risk"

    name = fields.Char('Lost Asset')
    risk_id = fields.Many2one('risk.management')


class DeliverableLog(models.Model):
    """ Allows user to capture deliverable for risk. """
    _name = "deliverable.log"
    _description = "Model to allow user register deliverable against risk"

    name = fields.Char("Deliverable")
    risk_id = fields.Many2one('risk.management', string="Risk")


class RiskReportingHistory(models.Model):
    _name = 'risk.reporting.history'
    _description = "Risk Reporting History"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    risk_id = fields.Many2one('risk.management', string="Name")
    report_doc = fields.Binary('Report')
    p_o_e_doc = fields.Binary('Portfolio of evidence.')
    store_report_name = fields.Char("Report Name")
    store_p_o_e_name = fields.Char("POE Name")
    submit_date = fields.Datetime(string="Submit Date")
    state = fields.Selection([('draft', 'Draft'), ('manger', 'Manager'),
                              ('ed', 'Executive Director'), ('approved', 'Approved'),
                              ('reject', 'Reject')], string="state", default="draft")
    user_id = fields.Many2one('res.users', string="Submit By")
    manager_user_id = fields.Many2one('res.users', string="Manager")
    ed_user_id = fields.Many2one('res.users', string="Executive Director")
    ceo_user_id = fields.Many2one('res.users', string="CEO")
    reject_user_id = fields.Many2one('res.users', string="Rejected By")
    monitoring_intervals = fields.Selection(
        [('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Annually')], string='Monitoring Intervals')
    monitoring_month = fields.Selection([('jan', 'January'), ('feb', 'February'),
                                         ('mar', 'March'), ('apr', 'April'),
                                         ('may', 'May'), ('jun', 'June'),
                                         ('jul', 'July'), ('aug', 'August'),
                                         ('sep', 'September '), ('oct', 'October'),
                                         ('nov', 'November'), ('dec', 'December')], string="Month")
    monitoring_quarter = fields.Selection([('q1', 'April to June'),
                                           ('q2', 'July to September'),
                                           ('q3', 'October to December'),
                                           ('q4', 'January to March')], string="Quarter")
    monitoring_year = fields.Selection([(y, str(y)) for y in range(1995, (datetime.now().year + 100) + 1)],
                                       stirng='Financial Year')
    note = fields.Text(string="Note")
    reject_comment = fields.Text(string="Rejection Reason")

    @api.multi
    def name_get(self):
        result = []
        for report in self:
            if report.risk_id and report.user_id:
                name = report.risk_id.name + "-" + report.user_id.name
                result.append((report.id, name))
        return result

    @api.multi
    def action_manager_approve(self):
        self.ensure_one()
        self.write({
            'manager_user_id': self.env.user.id or False,
            'state': 'manger',
        })

    @api.multi
    def action_ed_approve(self):
        self.ensure_one()
        self.write({
            'ed_user_id': self.env.user.id or False,
            'state': 'ed',
        })

    @api.multi
    def action_ceo_approve(self):
        self.ensure_one()
        self.write({
            'ceo_user_id': self.env.user.id or False,
            'state': 'approved',
        })

    @api.multi
    def action_set_to_draft(self):
        self.ensure_one()
        self.write({
            'manager_user_id': False,
            'ed_user_id': False,
            'ceo_user_id': False,
            'reject_user_id': False,
            'state': 'new',
        })

    @api.multi
    def get_rb_data(self):
        print('----se;lfffff---', self)
        reportback_data = self.env['report.back'].search([('risk_id', '=', int(self.id))])
        if reportback_data:
            return reportback_data.ids
        else:
            return False
        
        
class EnterpriseRisk(models.Model):
    """ Enterprise Risk Model """
    
    _name = "enterprise_risk"
    _description = "Enterprise Risk"

    @api.multi
    def default_all_risks(self):
        #url = '<iframe src="http://cs.transcendmx.com/dashboard.php?user={self.env.user.id}" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        url = '<iframe src="http://moyatech.co.za/nydarisk/management/review_risks.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url

    @api.multi
    def default_strategic_risks(self):
        url = '<iframe src="http://moyatech.co.za/nydarisk/management/strategic_risks.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url

    @api.multi
    def default_operational_risks(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/management/operational_risks.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
        
    @api.multi
    def default_risk_appetite(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/risk_appetite.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url

    @api.multi
    def default_risk_overview(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/risk_appetite.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
        
    @api.multi
    def default_risk_trend(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/trend.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_heat_map(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/likelihood_impact.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url

    @api.multi
    def default_risk_advice(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/riskadvice.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url  
    
    @api.multi
    def default_risk_mitigations(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/mitigations_by_date.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_risk_reviews(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/mgmt_reviews_by_date.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_performance_report(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/likelihood_impact.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_performance_dashboard(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/likelihood_impact.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_risk_settings(self):
        url = '<iframe src="https://www.moyatech.co.za/nydarisk/admin/index.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url           
                                      
    all_risks               = fields.Html(string="Primnet URL", default=lambda self: self.default_all_risks())
    strategic_risks         = fields.Html(string="Primnet URL", default=lambda self: self.default_strategic_risks())
    operational_risks       = fields.Html(string="Primnet URL", default=lambda self: self.default_operational_risks())
    risk_appetite           = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_appetite())
    risk_overview           = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_overview())
    risk_trend              = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_trend())
    heat_map                = fields.Html(string="Primnet URL", default=lambda self: self.default_heat_map())
    risk_advice             = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_advice())
    risk_mitigations        = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_mitigations())
    risk_reviews            = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_reviews())
    performance_report      = fields.Html(string="Primnet URL", default=lambda self: self.default_performance_report())
    performance_dashboard   = fields.Html(string="Primnet URL", default=lambda self: self.default_performance_dashboard())
    risk_settings           = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_settings())