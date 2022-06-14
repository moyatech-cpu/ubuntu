
from odoo import api, fields, models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    type = fields.Selection([('create', 'Creation'), ('write', 'Updating'), ('archive', 'Archiving')],
                            string="Send Message On")
