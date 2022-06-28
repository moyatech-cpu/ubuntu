from odoo import api, fields, models

class CancelBusinessMgmtTrainingWizard(models.TransientModel):
    
    _name="cancel.business.mgmt.training.wizard"
    
    reinstate_b_mgmt_reason = fields.Text(string='Reason To Reinstate')
    cancel_b_mgmt_reason = fields.Text(string='Reason To Cancel')
    
    @api.multi
    def cancel_business_mgmt_training(self):
     business_mgmt_training = self.env['business.mgmt.training'].browse(self._context.get('active_id'))
     cancel_training = business_mgmt_training.write({
            'cancel_b_mgmt_reason': self.cancel_b_mgmt_reason,
            'current_state': business_mgmt_training.status,
            'status': 'cancelled'
        })
    
    @api.multi
    def reinstate_business_mgmt_training(self):
     business_mgmt_training = self.env['business.mgmt.training'].browse(self._context.get('active_id'))
     reinstate_training = business_mgmt_training.write({
            'reinstate_b_mgmt_reason': self.reinstate_b_mgmt_reason,
            'status': business_mgmt_training.current_state
        })