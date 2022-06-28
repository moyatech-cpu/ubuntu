from odoo import api, fields, models

class RejectReasonPcbc(models.TransientModel):
    _name = 'reject.reason.pcbc'
    _description = 'reject PCBC'

    reject_reason_pcbc = fields.Text(string='Rejection Reason')

    @api.multi
    def rejectpcbc(self):
        grant_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        reject_v = grant_application.write({
            'reject_reason_pcbc': self.reject_reason_pcbc,
        })

        return True