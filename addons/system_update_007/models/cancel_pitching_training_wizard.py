from odoo import api, fields, models

class CancelPitchingTrainingWizard(models.TransientModel):
    
    _name="cancel.pitching.training.wizard"
    
    reinstate_pitching_reason = fields.Text(string='Reason To Reinstate')
    cancel_pitching_reason = fields.Text(string='Reason To Cancel')
    
    @api.multi
    def cancel_pitching_training(self):
     pitching_training = self.env['business.mgmt.training.pitching'].browse(self._context.get('active_id'))
     cancel_pitch = pitching_training.write({
            'cancel_pitching_reason': self.cancel_pitching_reason,
            'current_state': pitching_training.status,
            'status': 'cancelled'
        })
    
    @api.multi
    def reinstate_pitching_training(self):
     pitching_training = self.env['business.mgmt.training.pitching'].browse(self._context.get('active_id'))
     reinstate_pitch = pitching_training.write({
            'reinstate_pitching_reason': self.reinstate_pitching_reason,
            'status': pitching_training.current_state
        })