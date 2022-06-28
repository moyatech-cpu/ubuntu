from odoo import api, fields, models
from datetime import date, datetime
import logging
_logger = logging.getLogger(__name__)


class AssetTransfer(models.TransientModel):
    _name = 'asset.transfer.report'
    _description = 'Asset Transfer Report'

    sdate = fields.Date(string='Start Date')
    edate = fields.Date(string='End Date')
    branch = fields.Many2one('res.branch',string="Branch")
    status = fields.Selection([('new','New'),
                                ('1st_review','1st Review'),
                                ('2nd_review','2nd Review'),
                                ('completed','Completed'),
                                ('end','End')],'Status')
    
    by_status = fields.Boolean(string="Filter by Status")
    by_period = fields.Boolean(string="Filter by Period")
    by_branch = fields.Boolean(string="Filter by Branch")
    
    @api.multi
    def account_asset_transfer_report(self):
        
        if self.by_period and self.by_status and self.by_branch:
            asset_transfers = self.env['asset.transfer'].sudo().search([('create_date','>=',self.sdate),
                                                                        ('create_date','<=',self.edate),
                                                                        ('state','=',self.status),
                                                                        ('asset_register.location','=',self.branch.id)])
        elif self.by_period and self.by_status:
            asset_transfers = self.env['asset.transfer'].sudo().search([('create_date','>=',self.sdate),
                                                                        ('create_date','<=',self.edate),
                                                                        ('state','=',self.status)])
        elif self.by_period and self.by_branch:
            asset_transfers = self.env['asset.transfer'].sudo().search([('create_date','>=',self.sdate),
                                                                        ('create_date','<=',self.edate),
                                                                        ('asset_register.location','=',self.branch.id)])
        elif self.by_status and self.by_branch:
            asset_transfers = self.env['asset.transfer'].sudo().search([('asset_register.location','=',self.branch.id)])
        elif self.by_period:
            asset_transfers = self.env['asset.transfer'].sudo().search([('create_date','>=',self.sdate),
                                                                        ('create_date','<=',self.edate)])
        elif self.by_status:
            asset_transfers = self.env['asset.transfer'].sudo().search([('state','=',self.status)])
        elif self.by_branch:
            asset_transfers = self.env['asset.transfer'].sudo().search([('asset_register.location','=',self.branch.id)])
        else:
            asset_transfers = self.env['asset.transfer'].sudo().search([])
            
        
        _logger.info(asset_transfers)
        dict_custom = {}
        final_list = []
        if self.by_branch:
            branches = self.env['res.branch'].sudo().search([('id','=',self.branch.id)])
        else:
            branches = self.env['res.branch'].sudo().search([])
        
        for branch in branches:
            tot_transfered = 0
            assets = []
            for transfer in asset_transfers:
                if transfer.asset_register.location == branch:
                    vdata = {
                        'branch':branch.name,
                        'number':tot_transfered+1,
                        'asset': transfer.asset_transfer_title,
                        'model': transfer.asset_model,
                        'asset_number': transfer.asset_number,
                        'asset_serial_number': transfer.asset_serial_number,
                        'asset_dispatcher': transfer.asset_dispatcher.name,
                        'asset_recipient': transfer.asset_recipient.name,
                        'asset_recipient_branch': transfer.asset_recipient_branch.x_name,
                        'status': transfer.state,
                    }
                    assets.append(vdata)
                    tot_transfered += 1
            branch_data = {
                        'branch':branch.name,
                        'assets': assets,
                        'total_assets':tot_transfered,
                    }
            if branch_data['assets']:
                final_list.append(branch_data)
            
        
        dict_custom = {
            'branch_data':final_list,
            'sdate':self.sdate,
            'edate':self.edate,
            'status':self.status,
            'branch':self.branch.name,
            }
        
        return dict_custom
    
    def print_transfer_report(self):
        return self.env.ref('account_batch_state_update.action_report_transfer_asset').report_action(self)
    