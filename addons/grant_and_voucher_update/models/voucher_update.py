from odoo import api, fields, models

class CancelVoucherWiz(models.Model):
    _inherit="voucher.application"

    cancel_voucher_reason = fields.Text(string='Reason To Cancel')
    reinstate_voucher_reason = fields.Text(string='Reason To Reinstate')
    current_state = fields.Char('Current State', default='new')
 
    
    @api.multi
    def btn_cancel_voucher(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Voucher Application',
            'res_model': 'voucher.cancel.reason.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('grant_and_voucher_update.cancel_reason_voucher_form').id),
            'target': 'new',
        }
    
    @api.multi
    def btn_reinstate_voucher(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reinstate Voucher Application',
            'res_model': 'voucher.cancel.reason.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('grant_and_voucher_update.reinstate_voucher_form').id),
            'target': 'new',
        }