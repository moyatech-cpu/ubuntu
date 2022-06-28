# -*- coding: utf-8 -*-

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import float_compare, float_is_zero

class AssetItem(models.Model):
    _inherit = 'account.asset'
    
    batch_id = fields.Many2one('batch.asset.disposal','Batch ID')

class BatchAssetDisposal(models.Model):
    
    _name = 'batch.asset.disposal'
    
    asset_disposal_line_ids         = fields.One2many('account.asset','batch_id', string="Asset Disposal ID")
    
    category_id                     = fields.Many2one('account.asset.category', string='Category', required=True, change_default=True, readonly=True, states={'draft': [('readonly', False)]})
    date                            = fields.Date(string='Date', required=True, readonly=True, states={'draft': [('readonly', False)]}, default=fields.Date.context_today, oldname="purchase_date")
    x_model                         = fields.Char('Model')
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        if values:
            values['batch_id'] = self.env['ir.sequence'].next_by_code('batch.asset.disposal')
        record_obj = super(BatchAssetDisposal, self).create(values)
        return record_obj
    
    @api.multi
    @api.depends('category_id','date','x_model')
    @api.onchange('category_id','date','x_model')
    def compute_voucher_value(self):
        if self.date:
            for rec in self:
                result = self.env['account.asset'].search([('date','=',self.date)])
                rec['asset_disposal_line_ids'] = result
        if self.category_id:
            for rec in self:
                result = self.env['account.asset'].search([('category_id','=',self.category_id.id)])
                rec['asset_disposal_line_ids'] = result
        if self.x_model:
            for rec in self:
                result = self.env['account.asset'].search([('x_model','=like',self.x_model)])
                rec['asset_disposal_line_ids'] = result
    
    
    
    
    