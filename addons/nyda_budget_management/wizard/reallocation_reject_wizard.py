# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class BudgetReallocationReject(models.Model):
    _name = 'budget.reallocation.reject'
    _rec_name = 'reallocation_id'

    reallocation_id     = fields.Many2one('budget.reallocation', string='Reallocation Memo')
    reject_reason       = fields.Text(string='Reject Reason')
    
    @api.multi
    def submit_reject_reason(self):

        content_data = self.env['budget.reallocation'].browse(self._context.get('active_id'))
        content_data.write({
            'reject_reason': self.rejection_reason,
            'state': 'rejected'
        })

        return True