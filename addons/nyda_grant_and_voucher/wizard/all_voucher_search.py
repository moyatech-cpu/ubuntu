from datetime import date
from odoo import api, fields, models


class AllVoucherSeearch(models.TransientModel):
    _name = 'all.voucher.search'
    _description = 'All Voucher Search'

    voucher_serial_number = fields.Char(string='Serial Number')

    # @api.multi
    # def search_voucher(self):
    #     voucher_application = self.env['voucher.application'].search([('serial_number', '=', self.voucher_serial_number)])
    #     print('voucher_application \n\n\n', voucher_application)
    #     if voucher_application:
    #         return {
    #             'name': 'All Document',
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             'res_model': 'voucher.application',
    #             'views': [(self.env.ref('nyda_grant_and_voucher.view_voucher_application_form_two').id, 'form')],
    #             'view_id': self.env.ref('nyda_grant_and_voucher.view_voucher_application_form_two').id,
    #             # 'res_id': voucher_application.id,
    #             'type': 'ir.actions.act_window',
    #             'domain': [('id', '=', voucher_application.id)],
    #         }
