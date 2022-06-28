# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class TenderRejectReason(models.TransientModel):
    _name = 'scm.tender.reject'
    _rec_name = 'tender_id'

    tender_id       = fields.Many2one('nyda.scm.tender', string='Tender')
    reject_reason   = fields.Text(string='Reject Reason')
    
    @api.multi
    def submit_reject_reason(self):

        tender_data = self.env['nyda.scm.tender'].browse(self._context.get('active_id'))
        tender_data.write({
            'reject_reason': self.rejection_reason,
            'state': 'rejected'
        })

        return True

class TenderCancelReason(models.TransientModel):
    _name = 'scm.tender.cancel'
    _rec_name = 'tender_id'

    tender_id     = fields.Many2one('nyda.scm.tender', string='Tender')
    cancel_reason = fields.Text(string='Cancellation Reason')
    
    @api.multi
    def submit_cancel_reason(self):

        tender_data = self.env['nyda.scm.tender'].browse(self._context.get('active_id'))
        tender_data.write({
            'cancel_reason': self.cancel_reason,
            'state': 'cancelled'
        })

        return True