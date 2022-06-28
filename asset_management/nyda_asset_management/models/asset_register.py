# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import odoo.addons.decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import float_compare, float_is_zero

import logging
from sys import exc_info
from traceback import format_exception

import odoo.addons.decimal_precision as dp
from functools import reduce


class AssetCategoryInheritence(models.Model):
    _inherit='account.asset.profile'
    #_name='asset.category'
    
    salvage_percentage      = fields.Float(string="Salvage Percentage %", default=4)
    code                    = fields.Selection(selection=[('CE', 'Computer Equipment'),
                                                          ('F', 'Furniture'),
                                                          ('MV', 'Motor Vehicles'),
                                                          ('OE', 'Office Furniture'),
                                                          ('LH', 'Leaseholds')
                                                          ],
                                                          string="Asset ID Code",default='F')
    #account_impairment_id   = fields.Many2one('account.account',string='Impairment Account')
    
class AssetCategoryInheritence(models.Model):
    _inherit='account.move'
    
    @api.multi
    def reverse_moves(self, date=None, journal_id=None):
        date = date or fields.Date.today()
        reversed_moves = self.env['account.move']
        for ac_move in self:
            reversed_move = ac_move._reverse_move(date=date,
                                                  journal_id=journal_id)
            reversed_moves |= reversed_move
            #unreconcile all lines reversed
            aml = ac_move.line_ids.filtered(lambda x: x.account_id.reconcile or x.account_id.internal_type == 'liquidity')
            aml.remove_move_reconcile()
            #reconcile together the reconciliable (or the liquidity aml) and their newly created counterpart
            for account in list(set([x.account_id for x in aml])):
                to_rec = aml.filtered(lambda y: y.account_id == account)
                to_rec |= reversed_move.line_ids.filtered(lambda y: y.account_id == account)
                #reconciliation will be full, so speed up the computation by using skip_full_reconcile_check in the context
                to_rec.with_context(skip_full_reconcile_check=True).reconcile()
                to_rec.force_full_reconcile()
        if reversed_moves:
            #reversed_moves._post_validate()
            #reversed_moves.post()
            return [x.id for x in reversed_moves]
        return []
    
class AssetRegisterInheritence(models.Model):    
    _inherit='account.asset'
    #_name='asset.register'
    _rec_name = 'asset_number'
    
    asset_disposal_id           = fields.Many2one('asset.disposal', string='Asset Disposal ID')
    asset_disposal_reason       = fields.Text(string="Disposal Reason")
    #profile_id                  = fields.Many2one('account.asset.profile', string="Category")
    
    #Custom Fields
    asset_label                 = fields.Char('Asset Label')
    asset_quantity              = fields.Char('Asset Quantity')
    asset_type                  = fields.Char('Type')
    asset_class                 = fields.Char('Class')
    asset_manufacture           = fields.Char('Manufacture Description')
    asset_custodian             = fields.Char('Custodian Info')
    
    asset_number                = fields.Char(compute='_compute_asset_number',store=True,string="Asset Number")
    asset_id                    = fields.Char("Asset ID")
    model                       = fields.Char(string="Model")
    serial                      = fields.Char(string="Serial")
    depreciation_date           = fields.Date(string="Depreciation Date")
    location                    = fields.Many2one('res.branch', string="Asset Location")
    office_details              = fields.Char(string="Office Details")
    custodian                   = fields.Many2one('hr.employee', string="Custodian")
    tagged                      = fields.Boolean(string="Tagged")
    asset_condition             = fields.Char(string="Verification")
    manufacturer_id             = fields.Char(string="Manufacturer")
    service_start_date          = fields.Date(string="Service Start Date")
    warranty_start_date         = fields.Date(string="Warranty Start Date")
    purchase_date               = fields.Date(string="Purchase Date")
    warranty_end_date           = fields.Date(string="Warranty End Date")
    '''salvage_value               = fields.Float(digits=dp.get_precision('Account'), 
                                               string='Residual Value', store=True, 
                                               help="This amount represent the estimated value remaining"
                                                    "at the end of the asset's useful life.")
    '''
    impairment_amount           = fields.Float(string='Impairment Amount', default=0.00, store=True,
                                               help="This amount represent the impaired cost on the asset.")
    
    impairment_reason           = fields.Char(string="Impairment Reason",
                                              help="The reason for the asset impairment.")
        
    @api.onchange('impairment_amount')
    def _onchange_impariment(self):
        for record in self:
            record['value_residual'] -= self.impairment_amount
    
    
    @api.onchange('purchase_value')
    def _onchange_purchase_value_salvage(self):
        for record in self:
            record['salvage_value'] = (self.purchase_value * self.profile_id.salvage_percentage/100)
        
    @api.depends('profile_id')
    def _compute_asset_number(self):
        for record in self:
            record['asset_number'] = self.env['ir.sequence'].next_by_code('asset.number.seq')
    
    
    @api.multi
    def add_impairment_value(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Impairment Entry',
            'res_model': 'asset.impairment.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_asset_management.asset_impairment_form').id),
            'target': 'new',
        }
    
    @api.multi
    def compute_depreciation_board(self):
                
        def group_lines(x, y):
            y.update({'amount': x['amount'] + y['amount']})
            return y

        line_obj = self.env['account.asset.line']
        digits = self.env['decimal.precision'].precision_get('Account')

        for asset in self:
            if asset.value_residual <= 0.0:
                continue
            domain = [
                ('asset_id', '=', asset.id),
                ('type', '=', 'depreciate'),
                '|', ('move_check', '=', True), ('init_entry', '=', True)]
            posted_lines = line_obj.search(
                domain, order='line_date desc')
            if posted_lines:
                last_line = posted_lines[0]
            else:
                last_line = line_obj
            domain = [
                ('asset_id', '=', asset.id),
                ('type', '=', 'depreciate'),
                ('move_id', '=', False),
                ('init_entry', '=', False)]
            old_lines = line_obj.search(domain)
            if old_lines:
                old_lines.unlink()

            table = asset._compute_depreciation_table()
            if not table:
                continue

            # group lines prior to depreciation start period
            depreciation_start_date = fields.Datetime.from_string(
                asset.date_start)
            lines = table[0]['lines']
            lines1 = []
            lines2 = []
            flag = lines[0]['date'] < depreciation_start_date
            for line in lines:
                if flag:
                    lines1.append(line)
                    if line['date'] >= depreciation_start_date:
                        flag = False
                else:
                    lines2.append(line)
            if lines1:
                lines1 = [reduce(group_lines, lines1)]
                lines1[0]['depreciated_value'] = 0.0
            table[0]['lines'] = lines1 + lines2

            # check table with posted entries and
            # recompute in case of deviation
            depreciated_value_posted = depreciated_value = 0.0
            if posted_lines:
                last_depreciation_date = fields.Datetime.from_string(
                    last_line.line_date)
                last_date_in_table = table[-1]['lines'][-1]['date']
                if last_date_in_table <= last_depreciation_date:
                    raise UserError(
                        _("The duration of the asset conflicts with the "
                          "posted depreciation table entry dates."))

                for table_i, entry in enumerate(table):
                    residual_amount_table = \
                        entry['lines'][-1]['remaining_value']
                    if entry['date_start'] <= last_depreciation_date \
                            <= entry['date_stop']:
                        break
                if entry['date_stop'] == last_depreciation_date:
                    table_i += 1
                    line_i = 0
                else:
                    entry = table[table_i]
                    date_min = entry['date_start']
                    for line_i, line in enumerate(entry['lines']):
                        residual_amount_table = line['remaining_value']
                        if date_min <= last_depreciation_date <= line['date']:
                            break
                        date_min = line['date']
                    if line['date'] == last_depreciation_date:
                        line_i += 1
                table_i_start = table_i
                line_i_start = line_i

                # check if residual value corresponds with table
                # and adjust table when needed
                depreciated_value_posted = depreciated_value = \
                    sum([l.amount for l in posted_lines])
                residual_amount = asset.depreciation_base - depreciated_value
                amount_diff = round(
                    residual_amount_table - residual_amount, digits)
                if amount_diff:
                    # compensate in first depreciation entry
                    # after last posting
                    line = table[table_i_start]['lines'][line_i_start]
                    line['amount'] -= amount_diff

            else:  # no posted lines
                table_i_start = 0
                line_i_start = 0

            seq = len(posted_lines)
            depr_line = last_line
            last_date = table[-1]['lines'][-1]['date']
            depreciated_value = depreciated_value_posted
            for entry in table[table_i_start:]:
                for line in entry['lines'][line_i_start:]:
                    seq += 1
                    name = asset._get_depreciation_entry_name(seq)
                    if line['date'] == last_date:
                        # ensure that the last entry of the table always
                        # depreciates the remaining value
                        if asset.method in ['linear-limit', 'degr-limit']:
                            depr_max = asset.depreciation_base \
                                - asset.salvage_value
                        else:
                            depr_max = asset.depreciation_base
                        amount = depr_max - depreciated_value
                    else:
                        amount = line['amount']
                    if amount:
                        vals = {
                            'previous_id': depr_line.id,
                            'amount': amount,
                            'asset_id': asset.id,
                            'name': name,
                            'line_date': line['date'].strftime('%Y-%m-%d'),
                            'init_entry': entry['init'],
                        }
                        depreciated_value += amount
                        depr_line = line_obj.create(vals)
                    else:
                        seq -= 1
                line_i_start = 0
        
        for record in self:
            for line in record['depreciation_line_ids']:
                if line.remaining_value == record['value_residual']:
                    line.remaining_value = line.remaining_value - record['impairment_amount']
                    record['value_residual'] = line.remaining_value
        
        return True
    
class ImpairmentWizard(models.TransientModel):
    _name = 'asset.impairment.wizard'

    impairment_amount           = fields.Float(string='Impairment Amount', default=0.00, store=True,
                                               help="This amount represent the impaired cost on the asset.")
    
    impairment_reason           = fields.Char(string="Impairment Reason",
                                              help="The reason for the asset impairment.")
      
    @api.multi
    def action_add_impairment_value(self):
        assets = self.env['account.asset'].browse(
            self.env.context.get('active_ids', False)
        )
        for record in self:
            if record['impairment_amount'] > assets.value_residual:
                self.impairment_amount = 0.0
                raise ValidationError("Impairment value cannot be greater than Carrying Amount of Asset")
                return
        assets.impairment_amount = self.impairment_amount
        assets.impairment_reason = self.impairment_reason
        #assets.value_residual = assets.value_residual - self.impairment_amount
        
    
    @api.constrains('impairment_amount')
    def onchange_impariment(self):
        assets = self.env['account.asset'].browse(
            self.env.context.get('active_ids', False)
        )
        for record in self:
            if record['impairment_amount'] > assets.value_residual:
                raise ValidationError(_("Impairment value cannot be greater than Carrying Amount of Asset: %s") % assets.value_residual)
            
                   
    '''@api.depends('profile_id')
    def _compute_asset_id(self):

        if self.category_id.code == 'CE':
            self.asset_id = self.env['ir.sequence'].next_by_code('asset.id.ce')
        elif self.category_id.code == 'F':
            self.asset_id = self.env['ir.sequence'].next_by_code('asset.id.f')
        elif self.category_id.code == 'MV':
            self.asset_id = self.env['ir.sequence'].next_by_code('asset.id.mv')
        elif self.category_id.code == 'OE':
            self.asset_id = self.env['ir.sequence'].next_by_code('asset.id.oe')
        elif self.category_id.code == 'LH':
            self.asset_id = self.env['ir.sequence'].next_by_code('asset.id.lh')
        else:
            self.asset_id = self.env['ir.sequence'].next_by_code('asset.id.f')
'''