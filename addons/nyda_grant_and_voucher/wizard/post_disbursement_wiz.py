from datetime import date
from odoo import api, fields, models


class ProofDisbursement(models.TransientModel):
    _name = 'post.disbursement.wiz'
    _description = 'Proof Of Payment Memo'

    post_disbursement = fields.Binary(string='Proof Disbursement')
    post_disbursement_name = fields.Char(string='File Name')

    @api.multi
    def btn_proof_of_payment_req(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        voucher_application.status = 'post_disbursement_done'
        voucher_application.post_disbursement = self.post_disbursement
        voucher_application.post_disbursement_name = self.post_disbursement_name
        return True
