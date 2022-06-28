# coding=utf-8

from odoo import api, fields, models, _
from odoo import http
from datetime import date, datetime
import calendar
from dateutil.relativedelta import relativedelta
import logging
from sys import exc_info
from traceback import format_exception
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.osv import expression
from functools import reduce

class AssetBatchDisposal(models.Model):
    _inherit = 'batch.asset.disposal'
    
    invoice_status = fields.Selection([
            ('new','New'),
            ('review', 'Review'),
            ('reject','Rejected'),
            ('dispose','Dispose'),
            ('journal','Journals Created'),
            ('post','Posted'),
            ('obsolete','Obsolete'),
            ('storage','Storage')],
        default='new', string="Batch State")
    
    department = fields.Many2one('hr.department',string='Department')
    review_by = fields.Many2one('res.users',string="Reviewed by")
    review_date = fields.Date("Date")
    review_state = fields.Selection([
            ('approved','Approved'),
            ('reject', 'Rejected')],
        string="Batch State")
    review_comment = fields.Text('Comments')
    
    def proceed(self):
        self.invoice_status = 'review'
    
    @api.multi
    def set_approve_reject(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Batch Asset Disposal Review',
            'res_model': 'asset.dispose.wiz',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    
    def store_stage(self):
        self.invoice_status = 'storage'
    
    def set_post(self):
        self.invoice_status = 'post'
        for record in self:
            for journal in record['journal_ids']:
                journal.action_proceed()
                journal.post()
    
    def dispose(self):
        self.invoice_status = 'dispose'
        return
    
    def obsolete(self):
        self.invoice_status = 'obsolete'
    
    @api.multi
    def print_report(self, docids, data=None):
        return self.env.ref('account_batch_state_update.action_report_bcs_vsp').report_action(self)
    
    
    @api.multi
    def grant_bcs_vsp_data(self):
        dict_custom = {}
        final_list = []
        
        for asset in self.transactions:
            vdata = {
                'asset_name':asset.name,
                'asset_id':asset.asset_id,
                'value_residual':asset.value_residual,
                'date_start':asset.date_start,
                'profile_id':asset.profile_id.name,
                'r_date_remove':asset.r_date_remove,
                'sale_value':asset.sale_value,
                'note':asset.note,
                }
            final_list.append(vdata)
            
        dict_custom = {
                'batch_number':self.asset_batch_id,
                'date':self.batch_date,
                'disposed_date':self.disposed_date,
                'description': self.description,
                'asset_data' :final_list,
            }
        
        return dict_custom
      
    
    