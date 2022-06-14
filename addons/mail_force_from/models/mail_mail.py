"""Mail related code"""
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
from openerp import models, api


class MailMail(models.Model):
    """mail.mail model"""
    _inherit = 'mail.mail'

    @api.model
    def create(self, vals):
        """Force FORCE_EMAIL in email_from"""
        IrConfig = self.env['ir.config_parameter'].sudo()
        force_email = IrConfig.get_param('email.force_from')
        vals['email_from'] = force_email
        return super(MailMail, self).create(vals)

    @api.multi
    def write(self, vals):
        """Force FORCE_EMAIL in email_from"""
        IrConfig = self.env['ir.config_parameter'].sudo()
        force_email = IrConfig.get_param('email.force_from')
        vals['email_from'] = force_email
        return super(MailMail, self).write(vals)
