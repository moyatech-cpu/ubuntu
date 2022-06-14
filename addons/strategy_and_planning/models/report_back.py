from odoo import api, fields, models


class ReportBack(models.Model):
    _name = 'report.back'

    progress = fields.Selection([('Achieved', 'Achieved'), ('not_achieved', 'Not Achieved')])
    actual_performance = fields.Text(string='Actual Performance')
    reg_not_achieved = fields.Text(string='Reasons For Non-Achievement')
    update_previous_month = fields.Text(string='Update Previous Month')
    cost = fields.Integer(string='Cost')
    report_acc = fields.Binary(string='Attache Evidence/Report')
    monthly_id = fields.Many2one('monthly.target.main', string='monthly ID')
    quarter_id = fields.Many2one('annual.performance.plan.target', string='Quarter ID')
    annual_id = fields.Many2one('annual.performance.plan', string='Annual ID')
    risk_id = fields.Many2one('risk.reporting.history', string='Risk ID')

