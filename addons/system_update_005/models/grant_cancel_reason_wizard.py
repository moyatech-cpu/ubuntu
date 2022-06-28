from odoo import api, fields, models

class GrantCancelReasonWizard(models.TransientModel):
    _name = 'grant.cancel.reason.wizard'

    cancel_reason = fields.Text(string='Reason To Cancel')
    reinstate_reason = fields.Text(string='Reason To Reinstate')

    @api.multi
    def cancel_grant(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        cancel_grant = grant_application.write({
            'cancel_grant_reason': self.cancel_reason,
            'current_state': grant_application.status,
            'status': 'cancelled'
        })

        return True
    
    @api.multi
    def reinstate_grant(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        reinstate_grant = grant_application.write({
            'reinstate_grant_reason': self.reinstate_reason,
            'status': grant_application.current_state
        })

        return True