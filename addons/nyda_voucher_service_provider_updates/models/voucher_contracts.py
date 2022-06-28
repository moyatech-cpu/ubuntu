# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    constract_status = fields.Boolean("Contract Active")
    contract_start_date = fields.Date("Contract Start")
    contract_end_date = fields.Date("Contract End")
    
class SelectServiceProviderWizard(models.TransientModel):
    _inherit = 'select.service.provider.wizard'
    _description = 'Opens wizard for applicant to select service provider'
    

    @api.onchange('x_service_provider_1')
    def onchange_service_provider(self):
        active_id = self._context.get('active_id')
        voucher_application_ids = self.env['voucher.application'].browse([active_id])

        print('----------voucher_application_ids->', voucher_application_ids)
        for app in voucher_application_ids:
            partner_model_records = self.env['res.partner'].sudo().search([ (['x_services', 'in', app.x_recommended_service.ids]), (['state_id', '=', app.province_id.id]), (['constract_status', '=', True])])
            print('------->>>>>',partner_model_records)
            partner_model_records_ids = partner_model_records.ids

        return {'domain': {'x_service_provider_1': [('id', 'in', partner_model_records_ids)]}}

class Enquiry(models.Model):
    _inherit = 'youth.enquiry'

    is_duplicate = fields.Boolean("Contract Active")