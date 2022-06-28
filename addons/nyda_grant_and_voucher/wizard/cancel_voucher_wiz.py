from odoo import api, fields, models

class CancelVoucherWiz(models.TransientModel):
    _name = 'cancel.voucher.wizard'
    _description = 'cancel voucher for Admin, SBDO, RO, RA'

    cancel_voucher_reason = fields.Text(string='Reason To Cancel')

    @api.multi
    def cancel_voucher(self):
        grant_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        cancel_v = grant_application.write({
            'cancel_voucher_reason': self.cancel_voucher_reason,
            'status': 'cancel'
        })

        return True