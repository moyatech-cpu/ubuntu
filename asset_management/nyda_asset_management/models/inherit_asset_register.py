# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import float_compare, float_is_zero

class AssetRegisterInheritence(models.Model):
    
    _inherit='account.asset'
    _rec_name = "asset_number"
    
    asset_disposal_id           = fields.Many2one('asset.disposal', string='Asset Disposal ID')
    asset_disposal_reason       = fields.Text(string="Disposal Reason")
    
    #Custome Fields
    asset_number                = fields.Char(string="Asset Number", store=True)
    model                       = fields.Char(string="Model", store=True)
    serial                      = fields.Char(string="Serial", store=True)
    depreciation_date           = fields.Date(string="Depreciation Date", store=True)
    location                    = fields.Char(string="Location", store=True)
    office_details              = fields.Char(string="Office Details", store=True)
    custodian                   = fields.Char(string="Custodian", store=True)
    tagged                      = fields.Char(string="Tagged", store=True)
    asset_verification_id       = fields.Char(string="Verification", store=True)
    manufacturer_id             = fields.Char(string="Manufacturer", store=True)
    service_start_date          = fields.Date(string="Service Start Date", store=True)
    warranty_start_date         = fields.Date(string="Warranty Start Date", store=True)
    purchase_date               = fields.Date(string="Purchase Date", store=True)
    warranty_end_date           = fields.Date(string="Warranty End Date", store=True)
    
    #asset_useful_life           = fields.Integer(string='Asset useful life in months')
    asset_id                    = fields.Char(compute='_compute_asset_id',string="Asset ID", store=True)
    sequence                    = fields.Integer(string='Sequence integer')

    sequence                    = 100000

    @api.depends('category_id')
    def _compute_asset_id(self):
        
        self.sequence += 1
        
        if self.category_id.name == 'Land':
            self.asset_id = "LND"
            self.asset_id += str(self.sequence) 
            
            
        elif self.category_id.name== 'Land Improvements':
            self.asset_id = "LND_IMP"
            self.asset_id += str(self.sequence)
        
        elif self.category_id.name == 'Buildings':
            self.asset_id = 'BLDNGS'
        
        elif self.category_id.name == 'Building Improvements':
            self.asset_id = 'BLDNG_IMP' 
            
        elif self.category_id.name == 'Lease Improvements':
            self.asset_id = 'LSE_IMP'
        
        elif self.category_id.name == 'Intangibles':
            self.asset_id = 'INTBLS'
            
        elif self.category_id.name == 'Equipment':
            self.asset_id = 'EQPMNT'
        
        elif self.category_id.name == 'Furniture and Fixtures':
            self.asset_id = 'FURN'
        
        elif self.category_id.name == 'Computers':
            self.asset_id = 'COMPTRS'
        
        elif self.category_id.name == 'Communication Equipment':
            self.asset_id = 'COMMEQPMNT'
        
        elif self.category_id.name == 'Hardware':
            self.asset_id = 'HRDWARE'
        
        elif self.category_id.name == 'Software':
            self.asset_id = 'SOFTWARE'
            
        elif self.category_id.name == 'Camera':
            self.asset_id = 'CMRA'
            
        elif self.category_id.name == 'Tablet':
            self.asset_id = 'TBLT'
            
        elif self.category_id.name == 'Smart Phone':
            self.asset_id = 'SMRTPHNE'
        return self.sequence
            
class AssetCategoryInheritence(models.Model):
    _inherit='account.asset.profile'
    
    asset_salvage_percentage    = fields.Float(string="Salvage Value %", default=4)