from odoo import api, fields, models

class CancelBMTTrainingWizard(models.TransientModel):
    
    _name="cancel.bmt.training.wizard"
    
    reinstate_bmt_reason = fields.Text(string='Reason To Reinstate')
    cancel_bmt_reason = fields.Text(string='Reason To Cancel')

    
    @api.multi
    def cancel_bmt_application(self):
     bmt = self.env['bmt.training.application'].browse(self._context.get('active_id'))
     cancel_bmt = bmt.write({
            'cancel_bmt_reason': self.cancel_bmt_reason,
            'current_state': bmt.status,
            'status': 'cancelled'
        })
    
    @api.multi
    def reinstate_bmt_application(self):
     bmt = self.env['bmt.training.application'].browse(self._context.get('active_id'))
     reinstate_bmt = bmt.write({
            'reinstate_bmt_reason': self.reinstate_bmt_reason,
            'status': bmt.current_state
        })
    
    
    
    