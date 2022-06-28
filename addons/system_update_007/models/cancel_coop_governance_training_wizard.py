from odoo import api, fields, models

class CancelCoopGovTrainingWizard(models.TransientModel):
    
    _name="cancel.coop.governance.training.wizard"
        
    reinstate_gov_training_reason = fields.Text(string='Reason To Reinstate')
    cancel_gov_training_reason = fields.Text(string='Reason To Cancel')
    
    @api.multi
    def cancel_coop_gov_training(self):
     coop_training = self.env['cooperative.governance.training'].browse(self._context.get('active_id'))
     coop_training.write({
            'cancel_gov_training_reason': self.cancel_gov_training_reason,
            'current_state': coop_training.state,
            'state': 'cancelled'
        })
    
    @api.multi
    def reinstate_coop_gov_training(self):
     coop_training = self.env['cooperative.governance.training'].browse(self._context.get('active_id'))
     coop_training.write({
            'reinstate_gov_training_reason': self.reinstate_gov_training_reason,
            'state': coop_training.current_state
        })