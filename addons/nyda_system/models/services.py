# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Service(models.Model):
    _name = 'service'

    name = fields.Char(string="Service Name")
    service_item_seq = fields.Char(string="Service Item ID")
    voucher_value = fields.Integer(strinh="Voucher Value")
    min_dur = fields.Integer(string="Minimum Duration(Hours)")
    is_enabled = fields.Boolean(string="Enabled")

    def toggle_active(self):
        if self.is_enabled:
            self.is_enabled = False
        elif not self.is_enabled:
            self.is_enabled = True
