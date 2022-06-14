# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class TeamWiz(models.TransientModel):
    _name = 'report.wiz'
    _description = 'Risk Report'

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one('hr.employee',string="Employee",default=_default_employee)
    risk_id = fields.Many2one('risk.management',string="Name")
    report_doc = fields.Binary('Report')
    p_o_e_doc = fields.Binary('Portfolio of evidence.')
    store_report_name = fields.Char("Report Name")
    store_p_o_e_name = fields.Char("POE Name")
    monitoring_intervals = fields.Selection([('monthly', 'Monthly'), ('quarterly', 'Quarterly'),
                                             ('annually', 'Annually')], string='Monitoring Intervals')
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

    @api.multi
    def submit_report(self):
        report_data = {
            'risk_id' : self.risk_id.id,
            'employee_id' : self.employee_id.id,
            'report_doc' : self.report_doc,
            'p_o_e_doc' : self.p_o_e_doc,
            'store_report_name': self.store_report_name,
            'store_p_o_e_name':self.store_p_o_e_name
        }
        report = self.env['risk.report'].create(report_data)
        report_data.update({
            'monitoring_intervals': self.monitoring_intervals,
            'submit_date': datetime.now(),
            'monitoring_month': self.monitoring_month,
            'monitoring_quarter': self.monitoring_quarter,
            'monitoring_year': self.monitoring_year,
            'user_id': self.env.user.id or False,
            'note': self.note or ''
        })
        self.env['risk.reporting.history'].create(report_data)
        return True

    @api.onchange('risk_id')
    def _onchange_risk_id(self):
        if self.risk_id:
            self.monitoring_intervals = self.risk_id.monitoring_intervals
