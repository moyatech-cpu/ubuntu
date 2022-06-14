# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)


class WebsiteConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    maintenance_mode = fields.Boolean(
        string="Maintenance Mode", help="Set it true during the maintenance mode")
    allowed_ips = fields.Char(string="Allowed IPs (comma separated)",
                              help="Specify the IPs for whcih you want to allow the acess during the maintenance mode")
    maintenance_mode_id = fields.Many2one(
        'maintenance.mode', string="Set messages")
   

    @api.multi
    def set_values(self):
        super(WebsiteConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("odoo_maintenance_mode.maintenance_mode", self.maintenance_mode)
        ICPSudo.set_param("odoo_maintenance_mode.allowed_ips", self.allowed_ips)
        ICPSudo.set_param("odoo_maintenance_mode.maintenance_mode_id", self.maintenance_mode_id.id)

    @api.model
    def get_values(self):
        res = super(WebsiteConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            maintenance_mode=ICPSudo.get_param('odoo_maintenance_mode.maintenance_mode'),
            allowed_ips=ICPSudo.get_param('odoo_maintenance_mode.allowed_ips'),
            maintenance_mode_id=ICPSudo.get_param('odoo_maintenance_mode.maintenance_mode_id'),
        )
        return res

    @api.multi
    def configure_messages_for_maintenance_mode(self):
        self.ensure_one()
        view_id = self.env.ref(
            'odoo_maintenance_mode.view_maintenance_mode_form').id
        if self.env['ir.config_parameter'].get_param('maintenance_mode_id'):
            try:
                res_id = int(self.env['ir.config_parameter'].get_param(
                    'maintenance_mode_id'))
            except Exception as e:
                raise Warning(e)
        else:
            # For first time
            res_id = self.env.ref(
                'odoo_maintenance_mode.maintenance_mode_data_id').id
            self.env['ir.config_parameter'].sudo().set_param(
                'maintenance_mode_id', (res_id))
        return {
            'name': 'Maintenance Mode Configuration',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'maintenance.mode',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': "inline",
            'res_id': res_id,
        }
        
    @api.model
    def set_demo_data_for_maintenance_mode(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        temp_id = self.env.ref('odoo_maintenance_mode.maintenance_mode_data_id').id
        ICPSudo.set_param("odoo_maintenance_mode.maintenance_mode", True)
        ICPSudo.set_param("odoo_maintenance_mode.allowed_ips", '172.17.0.1')
        ICPSudo.set_param("maintenance_mode_id", temp_id)
        return True
