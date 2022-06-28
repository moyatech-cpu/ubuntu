from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class VPQuery(models.TransientModel):
    _name = 'query.vp'
    _description = 'Voucher Reissuance Wizard'

    query = fields.Text('VP19 Query')
    
    @api.multi
    def voucher_vp_documents_seq(self):  #modified lines 23,34-38
        voucher_id = self.env['bcs.vsp'].browse(self._context.get('active_id'))
        
        voucher_id.query_comment = self.query
        
    

