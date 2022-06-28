from odoo import api, fields, models
from datetime import date, datetime

class CustReviewBatch(models.TransientModel):
    _name = 'customer.batch.review'
    _description = 'Review Batch'

    reason = fields.Text(string='Rejection Reason')
    choice = fields.Selection([
            ('approve','Approve'),
            ('reject','Reject'),
            ('query','Query')],string="")
    
    @api.multi
    def review_batch(self):
        batch = self.env['customer.batch.entry'].browse(self._context.get('active_id'))
        
        if self.choice == 'approve':
            batch.invoice_status = 'approve'
            batch.approval_date = date.today()
        elif self.choice == 'reject':
            batch.invoice_status = 'reject'
        
        return True