from odoo import api, fields, models

class CancelSalesPitchTrainingWizard(models.TransientModel):
    
    _name="cancel.sales.pitch.training.wizard"
    
    reinstate_sales_pitch_reason = fields.Text(string='Reason To Reinstate')
    cancel_sales_pitch_reason = fields.Text(string='Reason To Cancel')
    
    @api.multi
    def cancel_pitch(self):
     sales_pitch = self.env['sales.pitch.training'].browse(self._context.get('active_id'))
     sales_pitch.write({
            'cancel_sales_pitch_reason': self.cancel_sales_pitch_reason,
            'current_state': sales_pitch.state,
            'state': 'cancelled'
        })
    
    @api.multi
    def reinstate_pitch(self):
     sales_pitch = self.env['sales.pitch.training'].browse(self._context.get('active_id'))
     sales_pitch.write({
            'reinstate_sales_pitch_reason': self.reinstate_sales_pitch_reason,
            'state': sales_pitch.current_state
        })