# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class RFQRecommendationReject(models.Model):
    _name = 'rfq.recommendation.reject'
    _rec_name = 'content_id'

    content_id          = fields.Many2one('scm.rfq.main', string='RFQ')
    rejection_reason    = fields.Text(string='Reject Reason')
    
    @api.multi
    def submit_reject_reason(self):

        content_data = self.env['scm.rfq.main'].browse(self._context.get('active_id'))
        content_data.write({
            'reject_reason': self.rejection_reason,
            'state': 'recommendation'
        })

        return True

class RFQCancelReason(models.Model):
    _name = 'cancel.rfq.reason'
    _rec_name = 'content_id'

    content_id          = fields.Many2one('scm.rfq.main', string='RFQ')
    cancellation_reason = fields.Text(string='Cancellation Reason')
    
    @api.multi
    def submit_cancel_reason(self):

        content_data = self.env['scm.rfq.main'].browse(self._context.get('active_id'))
        content_data.write({
            'cancel_reason': self.cancellation_reason,
            'state': 'cancelled'
        })

        return True