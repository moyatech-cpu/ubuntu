# coding=utf-8
from odoo import api, fields, models, _


class HelpdeskLiteStage(models.Model):
    """Inherited Helpdesk Lite Stage."""
    _inherit = "helpdesk_lite.stage"

    dashboard_icon = fields.Binary(string="Dashboard Icon")
    icon_file_name = fields.Char(string="Icon File Name")
