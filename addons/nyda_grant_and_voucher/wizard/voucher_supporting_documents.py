from odoo import api, fields, models
from odoo.exceptions import UserError #added

class VoucherSupportingDocuments(models.TransientModel):
    _name = 'voucher.supporting.documents'
    _description = 'Voucher Supporting Documents'

    # linkage_report = fields.Binary('Linkage Report')
    # file_name = fields.Char('File Name')
    x_voucher_supporting_documents = fields.Binary('Voucher Issuance Supporting Document')
    x_voucher_supporting_documents_file_name = fields.Char('Voucher Issuance Supporting Document File Name')
    # linkage_report_ids = fields.One2many('linkage.report',Sting="Linkage Report")

    @api.multi
    def voucher_supporting_documents_seq(self):  #modified lines 23,34-38
        voucher_id = self.env['voucher.application'].browse(self._context.get('active_id'))
        
        # user.linkage_file_name =  self.file_name
        # user.linkage_report = self.linkage_report
        voucher_id.x_bmt_certificate = self.x_voucher_supporting_documents
        voucher_id.x_bmt_certificate_name = self.x_voucher_supporting_documents_file_name
        voucher_id.status = 'work_plan'
        voucher_id.x_voucher_number = self.env['ir.sequence'].next_by_code('voucher.isurance')
        print('---------\n\n\n', voucher_id.x_voucher_number)
        mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_issued_sp')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)
        return True

