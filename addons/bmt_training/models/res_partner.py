# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_facilitator = fields.Boolean(string="Is Facilitator")

