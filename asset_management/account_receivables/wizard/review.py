from odoo import api, fields, models
from datetime import date, datetime

class ReviewBatch(models.TransientModel):
    _name = 'batch.review'
    _description = 'Review Batch'

    reason = fields.Text(string='Rejection Reason')
    choice = fields.Selection([
            ('approve','Approve'),
            ('reject','Reject'),
            ('query','Query')],default='approve',string="")
    
    @api.multi
    def review_batch(self):
        batch = self.env['batch.entry'].browse(self._context.get('active_id'))
        batch.invoice_status = 'approve'
        batch.approval_date = date.today()
        batch.approvalUser = self.env.user
        '''if self.choice == 'approve':
            batch.invoice_status = 'approve'
            batch.approval_date = date.today()
        elif self.choice == 'reject':
            batch.invoice_status = reject'''
        
        return True