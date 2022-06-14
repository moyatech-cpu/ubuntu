# -*- coding: utf-8 -*-

from odoo import fields, models


class InsuranceExcess(models.Model):
    """ Insurance Excess model """
    _name = "insurance.excess"
    _description = "Insurance Excess"
    _rec_name = "loss_damage_assets_id"

    loss_damage_assets_id = fields.Many2one('loss.damage.assets', string="Loss Damage Assets")
    employee_id = fields.Many2one('hr.employee', string="Name of Staff Member")
    id_number = fields.Char(string="ID Number")
    employee_number = fields.Char(string="Employee Number")
    position_id = fields.Many2one('hr.job', string="Position")
    cluster = fields.Char(string="Cluster")
    deduction_amount = fields.Char(string="Deduction amount")
    deduction_amount_in_words = fields.Char(string="Deduction amount in words")
    installments_period = fields.Selection(
        [('one_month', '1 month'), ('two_month', '2 month'), ('three_month', '3 month')], string="Installments Period")
    month = fields.Selection([('jan', 'January'), ('feb', 'February'), ('march', 'March'),
                              ('april', 'April'), ('may', 'May'), ('june', 'June'),
                              ('july', 'July'), ('aug', 'August'), ('sep', 'September'),
                              ('oct', 'October'), ('nov', 'November'), ('dec', 'December')],
                             string="Starting in Month of")
    insurance_date = fields.Datetime(string="Insurance Date")
    digital_sign = fields.Binary(string="Signature")
