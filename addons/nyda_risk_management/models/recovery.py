# -*- coding: utf-8 -*-

from odoo import fields, models


class Recovery(models.Model):
    """ Recovery model """
    _name = "recovery"
    _description = "Recovery"
    _rec_name = "loss_damage_assets_id"

    loss_damage_assets_id = fields.Many2one('loss.damage.assets', string="Loss Damage Assets")
    employee_id = fields.Many2one('hr.employee', string="Name of Staff Member")
    description_of_stolen = fields.Text(string="Description of asset damaged /stolen")
    describe_the_cause = fields.Text(string="Describe the cause for loss/damage")
    date_lost_damaged = fields.Datetime(string="Date of lost/damaged")
    previous_loss_damage_date = fields.Datetime(string="Details of previous loss or damage")
    employee_motivation = fields.Text(string="Employee Motivation")
    emp_digital_sign = fields.Binary(string="Employee Signature")
    emp_date = fields.Datetime(string="Employee Signature Date")
    rec_cfo = fields.Text(string="Recommended/Not Recommended by the Chief Financial Officer (CFO)")
    cfo_digital_sign = fields.Binary(string="CFO Signature")
    cfo_date = fields.Datetime(string="CFO Signature Date")
    app_ceo = fields.Text(string="Approved/Not Approved by Chief Executive Officer (CEO)")
    ceo_digital_sign = fields.Binary(string="CEO Signature")
    ceo_date = fields.Datetime(string="CEO Signature Date")
