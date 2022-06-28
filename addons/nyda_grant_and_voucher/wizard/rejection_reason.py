from odoo import api, fields, models

class RejectionReason(models.TransientModel):
    _name = 'reject.reason'
    _description = 'Rejection Reason'

    reason_text = fields.Text('Reason')

    @api.multi
    def set_reject(self):
        """ Sets state to reject. Add logic if need anything once application is moved to reject state. """
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'send_letter'
        grant_application.reason_text = self.reason_text
