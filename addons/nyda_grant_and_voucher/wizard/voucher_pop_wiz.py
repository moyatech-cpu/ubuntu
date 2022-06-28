from datetime import date
from odoo import api, fields, models


class VoucherPop(models.TransientModel):
    _name = 'voucher.pop.wiz'
    _description = 'Voucher Proof Of Payment Memo'

    proof_of_payment = fields.Binary(string='Proof Of Payment')
    proof_of_payment_date = fields.Date(string='Date', default=date.today())
    proof_of_payment_name = fields.Char(string='File Name')

    @api.multi
    def btn_voucher_pop_req(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        voucher_application.status = 'payment_completed'
        voucher_application.proof_of_payment = self.proof_of_payment
        voucher_application.proof_of_payment_date = self.proof_of_payment_date
        voucher_application.proof_of_payment_name = self.proof_of_payment_name
        attachment = {
                   'name': str(self.proof_of_payment_name),
                   'datas': self.proof_of_payment,
                   'datas_fname': self.proof_of_payment_name,
                   'res_model': voucher_application._name,
                   'type': 'binary'
                   }
        ir_attechment_id = self.env['ir.attachment'].create(attachment)
        approve_mail_wiz_template = self.env.ref('nyda_grant_and_voucher.voucher_send_proof_of_payment_mail_template')
        if approve_mail_wiz_template:
            approve_mail_wiz_template.attachment_ids = [(6, 0, [])]

            approve_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]

            #approve_mail_wiz_template.with_context(user=self.env.user,bda=voucher_application.email).send_mail(voucher_application.id,
            #                                                                       force_send=True)
        return True
