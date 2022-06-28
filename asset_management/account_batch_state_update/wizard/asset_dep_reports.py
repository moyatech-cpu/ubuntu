from odoo import api, fields, models
from datetime import date, datetime
import logging
_logger = logging.getLogger(__name__)


class AssetDepreciationReports(models.TransientModel):
    _name = 'asset.dep.report'
    _description = 'Asset Depreciation Report'

    sdate = fields.Date(string='Start Date')
    edate = fields.Date(string='End Date')
    category_id = fields.Many2one('account.asset.profile',"Category") #asset.category
    a_cat_choice = fields.Boolean('Filter by Category')
    
    @api.multi
    def account_asset_report(self):
        
        if self.a_cat_choice:
            assets = self.env['account.asset'].sudo().search([('profile_id','=',self.category_id.id),
                                                               ('date_start','>=',self.sdate),
                                                               ('date_start','<=',self.edate)])
        else:
            assets = self.env['account.asset'].sudo().search([('date_start','>=',self.sdate),
                                                               ('date_start','<=',self.edate)])
        #asset.register
        _logger.info(assets)
        category_lines = self.env['account.asset.profile'].sudo().search([])
        
        assets_bulk = []
        dict_custom = {}
        for category in category_lines:
            number = 1
            assets_in_category = []
            for asset in assets:
                if asset.profile_id == category:     #if asset.category_id == category.id: 
                    depreciations = []
                    for dep_line in asset.depreciation_line_ids:
                        move = 'Yes' if dep_line.move_check else 'No'
                        dep = {
                            'type':dep_line.type,
                            'date':dep_line.line_date,
                            'depreciated_value':dep_line.depreciated_value,
                            'amount':dep_line.amount,
                            'remaining_value':dep_line.remaining_value,
                            'move':move,
                        }
                        depreciations.append(dep)
                    _logger.info(depreciations)
                    a_data = {
                        'number':number,
                        'name':asset.name,
                        'category':asset.profile_id.name, 
                        'asset_number':asset.asset_number, 
                        'asset_location':asset.location.name,
                        'serial':asset.asset_id, 
                        'custodian':asset.partner_id.name,
                        'purchase_value':asset.purchase_value,
                        'residual_value':asset.salvage_value,
                        'date_start':asset.date_start,
                        
                        'depreciation_base':asset.depreciation_base,
                        'carrying_amount': asset.value_residual,
                        'depreciated_value': asset.value_depreciated,
                        'depreciations': depreciations,
                        }
                    number += 1
                    assets_in_category.append(a_data)
                    _logger.info(assets_in_category)
            v_data = {
                        'name':category.name,
                        'code':dict(category._fields['code'].selection).get(category.code),
                        'salvage_percentage': category.salvage_percentage,#category.salvage_percentage,
                        'account_asset_id': category.name,
                        'depreciation_id':category.account_depreciation_id.name,
                        #Depreciation Dates
                        'method_time':category.method_time,
                        'method_number':category.method_number,
                        'method_period':category.method_period,
                        #Depreciation Method
                        'method':category.method,
                        'assets_in_category':assets_in_category,
                        }
            
            if v_data['assets_in_category']:
                assets_bulk.append(v_data)
                
            _logger.info(assets_bulk)
        dict_custom = {
            'system_time':datetime.now(),
            'assets_bulk':assets_bulk,
            'sdate':self.sdate,
            'edate':self.edate,
            
            }
        
        return dict_custom
    
    def print_dep_report(self):
        return self.env.ref('account_batch_state_update.action_report_dep_asset').report_action(self)
    