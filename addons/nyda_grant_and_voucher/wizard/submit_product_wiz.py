import datetime
from odoo import api, fields, models

class SubmitProductWiz(models.TransientModel):
    _name = 'submit.product.wiz'
    _description = 'Submit Product'

    product_doc = fields.Binary('Product')
    product_doc_name = fields.Char('File Name')
    invoice_doc = fields.Binary('Invoice')
    invoice_doc_name = fields.Char('File Name')
    timesheet_doc = fields.Binary('Timesheet')
    timesheet_doc_name = fields.Char('File Name')

    @api.multi
    def submit_product_req(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        #voucher_application.status = 'submitted_product'
        voucher_application.status = 'client_review'
        voucher_application.product_doc_name = self.product_doc_name
        voucher_application.product_doc = self.product_doc
        voucher_application.invoice_doc_name = self.invoice_doc_name
        voucher_application.invoice_doc = self.invoice_doc
        voucher_application.x_invoice_date = datetime.datetime.now()
        voucher_application.timesheet_doc_name = self.timesheet_doc_name
        voucher_application.timesheet_doc = self.timesheet_doc
        if voucher_application.email:
            voucher_product_submit_mail_template = self.env.ref('nyda_grant_and_voucher.voucher_product_submit_mail_template')
            voucher_product_submit_mail_template.with_context(user=self.env.user).send_mail(voucher_application.id, force_send=True)
        return True