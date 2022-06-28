from datetime import date
from odoo import api, fields, models,_


class SendRejectionLetter(models.TransientModel):
    _name = 'send.rejection.letter.wiz'
    _description = 'Send Rejection Letter To Client'

    rejection_letter = fields.Binary(string='Approval Letter')
    rejection_letter_name = fields.Char(string='File Name')
    rejection_letter_send_date = fields.Date(string="Date", default=date.today())

    @api.multi
    def reject_letter_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        jeck = grant_application.write({
            'rejection_letter': self.rejection_letter or False,
            'rejection_letter_name': self.rejection_letter_name or False,
            'rejection_letter_send_date': self.rejection_letter_send_date or False,

        })
        grant_application.status = 'reject'

        # grant_application.approval_letter_name = self.approval_letter_name
        # grant_application.approval_letter = self.approval_letter
        # grant_application.approval_letter_send_date = self.approval_letter_send_date

        attachment = {
            'name': str(self.rejection_letter_name),
            'datas': self.rejection_letter,
            'datas_fname': self.rejection_letter_name,
            'res_model': grant_application._name,
            'type': 'binary'
        }
        ir_attechment_id = self.env['ir.attachment'].create(attachment)
        print('-------', ir_attechment_id)
        rejection_mail_wiz_template = self.env.ref('nyda_grant_and_voucher.rejection_latter_wizard_mail_template')
        print('------', rejection_mail_wiz_template)
        if rejection_mail_wiz_template:
            rejection_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]
            print('111111111111')
            rejection_mail_wiz_template.with_context(user=self.env.user, bda=grant_application.email).send_mail(
                grant_application.id, force_send=True)
            print('------222222222')
        return True

