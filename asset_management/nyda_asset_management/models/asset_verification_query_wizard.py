# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AssetVerificationQueryWizard(models.Model):
    
    _name = 'asset.verification.query.wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    asset_id                            = fields.Many2one('account.asset', string='Asset ID', ondelete='cascade')
    branch_manager_query_comment        = fields.Text(sting="Branch Manager Comment")
    accountant_query_comment            = fields.Text(string="Accountant Comment")
    asset_manager_query_comment         = fields.Text(string="Asset Manager Comment")
    snr_manager_query_comment           = fields.Text(string="Snr Manager Comment")
    cfo_query_comment                   = fields.Text(string="CFO Comment")
    
    @api.multi
    def branch_manager_query_comment_proceed_button(self):
    
        asset_data = self.env['asset.verification'].browse(self._context.get('active_id'))
        asset_data.write({
            'state' : 'verification',
        })
    
    @api.multi
    def accountant_query_comment_proceed_button(self):
    
        asset_data = self.env['asset.verification'].browse(self._context.get('active_id'))
        asset_data.write({
            'state' : 'branch_review',
        })
        
    @api.multi
    def asset_manager_query_comment_proceed_button(self):
    
        asset_data = self.env['asset.verification'].browse(self._context.get('active_id'))
        asset_data.write({
            'state' : '1st_review',
        })
        
    @api.multi
    def snr_manager_query_comment_proceed_button(self):
    
        asset_data = self.env['asset.verification'].browse(self._context.get('active_id'))
        asset_data.write({
            'state' : '2nd_review',
        })
    
    @api.multi
    def cfo_query_comment_proceed_button(self):
    
        asset_data = self.env['asset.verification'].browse(self._context.get('active_id'))
        asset_data.write({
            'state' : '3rd_review',
        })