# -*- coding: utf-8 -*-

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import float_compare, float_is_zero

class AssetDisposal(models.Model):
    
    _name = 'asset.disposal'
    _inherit = ['mail.thread']
    _rec_name = 'asset_number'
    
    serial_number                       = fields.Char('Serial Number')
    asset_disposal_title                = fields.Char(string='Asset Disposal Title')
    asset_register                      = fields.Many2one('account.asset',string='Asset Register')
    asset_model                         = fields.Char(string='Asset Model',related="asset_register.model")
    asset_number                        = fields.Char(string='Asset Number',related="asset_register.asset_id")
    asset_serial_number                 = fields.Char(string='Asset Serial Number',related="asset_register.serial")
    state                               = fields.Selection([('new','New'),
                                                            ('review','Review'),
                                                            ('cfo_review','CFO Review'),
                                                            ('dispose','Dispose'),
                                                            ('obsolete','Obsolete'),
                                                            ('storage','Storage')],
                                                            string='state',group_expand='_expand_states',default='new')
    
    asset_disposal_date                 = fields.Date(string="Disposal Date")
    asset_disposal_employee             = fields.Many2one('hr.employee', string="Employee")
    asset_disposal_employee_department  = fields.Many2one('hr.department',related="asset_disposal_employee.department_id",string="Department")
    
    asset_disposal_branch             = fields.Many2one('res.branch',related='asset_disposal_employee.branch_id', string="Branch")
    
    asset_disposal_department         = fields.Many2one('hr.department', string='Department')

    
    asset_disposal_comments             = fields.Text(string="Asset Disposal Comments")
    asset_disposal_manager_comments     = fields.Text(string="Asset Disposal Manager Comments")
    asset_disposal_cfo_comments         = fields.Text(string="Asset Disposal CFO Comments")
    color                               = fields.Integer(string='Color Index', default=4)
    
    def _expand_states(self, state, domain, order):
         return [key for key, val in type(self).state.selection]
     
    '''@api.onchange('asset_register')
    def onchange_asset_register(self):
        for rec in self:
            if self.asset_register:
                rec.asset_model = rec.asset_register.x_model
                rec.asset_number = rec.asset_register.x_asset_number 
                rec.asset_serial_number  = rec.asset_register.x_serial
    '''
    @api.onchange('state')
    def onchange_state(self):
        
        if self.state == 'new':
            self.color = 10
        if self.state == 'review':
            self.color = 1
        if self.state == 'cfo_review':
            self.color = 4
        if self.state == 'dispose':
            self.color = 6
        if self.state == 'obsolete':
            self.color = 3
        if self.state == 'storage':
            self.color = 3    
            
    @api.multi
    def asset_disposal_proceed_button(self):
        for records in self:
            records.write({
                'state' : 'review',
                })
    @api.multi
    def asset_disposal_store_button(self):
        for records in self:
            records.write({
                'state' : 'storage',
                })
            
    @api.multi
    def asset_disposal_2nd_dispose_button(self):
        for records in self:
            records.write({
                'state' : 'cfo_review',
                })
        
    @api.multi
    def asset_disposal_dispose_button(self):
        for records in self:
            records.write({
                'state' : 'dispose',
                })
    @api.multi
    def asset_disposal_obsolete_button(self):
        for records in self:
            records.write({
                'state' : 'obsolete',
                })
            
    @api.model
    def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['serial_number'] = self.env['ir.sequence'].next_by_code('asset.disposal')
        rec_obj = super(AssetDisposal, self).create(values)
       
        return rec_obj