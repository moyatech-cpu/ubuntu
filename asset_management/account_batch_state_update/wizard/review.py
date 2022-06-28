from odoo import api, fields, models
from datetime import date, datetime

class ReviewBatch(models.TransientModel):
    _name = 'asset.dispose.wiz'
    _description = 'Review Batch'

    review_by = fields.Many2one('hr.employee')
    review_state = fields.Selection([
            ('approved','Approved'),
            ('reject', 'Rejected')],
        string="Batch State")
    review_comment = fields.Text('Comments')
    
    @api.multi
    def review_batch(self):
        batch = self.env['batch.asset.disposal'].browse(self._context.get('active_id'))
        batch.review_by = self.env.user
        
        batch.review_comment = self.review_comment
        
        
        batch.review_date = date.today()
        if self.review_state == 'approved':
            batch.invoice_status = 'dispose'
            batch.review_state = 'approved'
            batch.approval_date = date.today()
        elif self.review_state == 'reject':
            batch.invoice_status = 'reject'
            batch.review_state = 'reject'
        return True