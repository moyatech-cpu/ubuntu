from datetime import date
from odoo import api, fields, models


class UploadContract(models.TransientModel):
    _name = 'upload.contract.wiz'
    _description = 'Upload Contract'

    upload_contract = fields.Binary(string='Contract')
    upload_contract_name = fields.Char(string='File Name')

    signed_letter = fields.Binary(string='Signed Letter')
    signed_letter_name = fields.Char(string='File Name')

    @api.multi
    def upload_contract_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'disbursement_pack'
        grant_application.upload_contract_name = self.upload_contract_name
        grant_application.upload_contract = self.upload_contract
        grant_application.signed_letter_name = self.signed_letter_name
        grant_application.signed_letter = self.signed_letter
        return True
