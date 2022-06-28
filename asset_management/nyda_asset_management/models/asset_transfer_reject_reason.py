# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AssetTransferRejectWizard(models.Model):
    
    _name = 'asset.transfer.reject.wizard'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    asset_transfer_reject_reason_line_manager = fields.Text(string="Line Manager Comments")
    asset_transfer_delegated_authority_reject_comment = fields.Text(string="Delegated Authority")
    
    @api.multi
    def line_manager_reject_comment_proceed_button(self):
    
        asset_data = self.env['asset.transfer'].browse(self._context.get('active_id'))
        asset_data.write({
            'state': 'new',
        })
        
    @api.multi
    def delegated_authority_reject_comment_proceed_button(self):
    
        asset_data = self.env['asset.transfer'].browse(self._context.get('active_id'))
        asset_data.write({
            'state': '1st_review',
        })