from datetime import date
from odoo import api, fields, models
from datetime import date, datetime



class ProofOfPayment(models.TransientModel):
    _name = 'proof.of.payment.wiz'
    _description = 'Proof Of Payment Memo'

    proof_of_payment = fields.Binary(string='Proof Of Payment')
    proof_of_payment_name = fields.Char(string='File Name')
    payment_date = fields.Date('Payment Date', default=datetime.today())
    
    @api.multi
    def btn_post_disbursement_done_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'aftercare'
        grant_application.proof_of_payment = self.proof_of_payment
        grant_application.proof_of_payment_name = self.proof_of_payment_name
        grant_application.payment_date = self.payment_date
        '''
        attachment = {
                   'name': str(self.proof_of_payment_name),
                   'datas': self.proof_of_payment,
                   'datas_fname': self.proof_of_payment_name,
                   'res_model': grant_application._name,
                   'type': 'binary'
                   }
        ir_attechment_id = self.env['ir.attachment'].create(attachment)
        approve_mail_wiz_template = self.env.ref('nyda_grant_and_voucher.send_proof_of_payment_mail_template')
        if approve_mail_wiz_template:
            approve_mail_wiz_template.attachment_ids = [(6, 0, [])]

            approve_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]

            approve_mail_wiz_template.with_context(user=self.env.user,bda=grant_application.email).send_mail(grant_application.id,
                                                                                   force_send=True)
        '''
        return True
    
    @api.multi
    def btn_submit_proof_of_payment(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        voucher_application.status = 'payment_completed'
        voucher_application.proof_of_payment = self.proof_of_payment
        voucher_application.proof_of_payment_name = self.proof_of_payment_name
        voucher_application.proof_of_payment_date = self.payment_date
        return True