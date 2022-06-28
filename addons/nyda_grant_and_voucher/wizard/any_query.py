from datetime import date
from odoo import api, fields, models


class AnyQuery(models.TransientModel):
    _name = 'any.query'
    _description = 'Any Query'
    _rec_name = 'query'

    query = fields.Text(string='Please Write Below If You Have Any Query')

    @api.multi
    def query_for_voucher(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        voucher_application.query = self.query

        query_ids = self.env['any.query.record'].create({
            'query': self.query or False,
            'status': voucher_application.status,
            'voucher_id': voucher_application.id
        })

        # grant_application.status = 'disbursement_pack'
        # grant_application.upload_contract_name = self.upload_contract_name
        # grant_application.upload_contract = self.upload_contract
        # grant_application.signed_letter_name = self.signed_letter_name
        # grant_application.signed_letter = self.signed_letter
        return True
