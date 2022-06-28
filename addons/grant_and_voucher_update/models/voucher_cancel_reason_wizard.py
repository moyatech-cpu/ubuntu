from odoo import api, fields, models

class VoucherCancelReasonWizard(models.TransientModel):
    
    _name="voucher.cancel.reason.wizard"
    
    cancel_voucher_reason = fields.Text(string='Reason To Cancel')
    reinstate_voucher_reason = fields.Text(string='Reason To Reinstate')

    @api.multi
    def submit_cancel_voucher(self):
        voucher = self.env['voucher.application'].browse(self._context.get('active_id'))
        cancel_v = voucher.write({
            'cancel_voucher_reason': self.cancel_voucher_reason,
            'current_state': voucher.status,
            'status': 'cancel'
        })
            
    
    @api.multi
    def submit_reinstate_voucher(self):
        voucher = self.env['voucher.application'].browse(self._context.get('active_id'))
        reinstate_v = voucher.write({
            'reinstate_voucher_reason': self.reinstate_voucher_reason,
            'status': voucher.current_state        })