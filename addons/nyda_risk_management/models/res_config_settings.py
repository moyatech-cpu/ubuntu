# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        from_date = params.get_param('from_date')
        to_date = params.get_param('to_date')
        res.update(from_date = from_date or '',
                   to_date = to_date or '')
        return res

    @api.multi
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('from_date', self.from_date and self.from_date or '')
        config.set_param('to_date', self.to_date and self.to_date or '')
