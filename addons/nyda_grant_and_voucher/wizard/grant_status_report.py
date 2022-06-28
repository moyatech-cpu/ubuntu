# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class GrantStatusReport(models.TransientModel):
    """Grant Status Report"""
    _name = "grant.status.report"
    _description = 'Grant Status Report'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    report_type = fields.Selection(
        [('num_voucher', 'Number of Grants'), ('voucher_values', 'Grant Values')],
        string="Show")
    type = fields.Selection(
        [('status_branch', 'Status Per Branch'), ('status_branch_cons', 'Status Per Branch(Consolidated)')],
        string="Type")

    def get_branch_data(self):
        voucher_list = []
        final_list = []
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        branch = 'All Branch'
        branch_list = self.env['res.branch'].sudo().search([])

        for bid in branch_list:
            vouchers = self.env['grant.application'].sudo().search(
                [('branch_id', '=', bid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        print('Reading Branch Status Report---\n\n\n')
        vouchers = self.env['grant.application'].sudo().search([])
        
        if len(vouchers) >= 1:
            voucher_list.append(vouchers)
                        
        if self.report_type == 'num_voucher':
            val_type = 'number'
            for sv in voucher_list:
                if len(sv) == 1:
                    app = 0
                    dec = 0            
                    if sv.status == 'reject':
                        dec += 1
                    #else sv.status == 'approved' or sv.status == 'Legacy':
                    else:
                        app += 1                                                
                    total_voucher = app + dec
                    vdata = {'name': sv.branch_id.name, 'app': app, 'dec': dec, 'total': total_voucher}
                    final_list.append(vdata)
                elif len(sv) >= 2:
                    app = 0
                    dec = 0
                    name = ''
                    for voucher in sv:
                        name = voucher.branch_id.name
                        if voucher.status == 'reject':
                            dec += 1
                        else:
                            app += 1                            
                    total_voucher = app + dec
                    vdata = {'name': name, 'app': app, 'dec': dec, 'total': total_voucher}
                    final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            for sv in voucher_list:
                if len(sv) == 1:
                    app = 0
                    dec = 0
                    if sv.status == 'reject':
                        dec += sv.grant_amount_required
                    else:
                        app += sv.grant_amount_required                        
                    total_voucher = app + dec
                    vdata = {'name': sv.branch_id.name, 'app': app, 'dec': dec, 'total': total_voucher}
                    final_list.append(vdata)
                elif len(sv) >= 2:
                    app = 0
                    dec = 0
                    name = ''
                    for voucher in sv:
                        name = voucher.branch_id.name
                        if voucher.status == 'reject':
                            dec += voucher.grant_amount_required
                        else:
                            app += voucher.grant_amount_required                            
                    total_voucher = app + dec
                    vdata = {'name': name, 'app': app, 'dec': dec, 'total': total_voucher}
                    final_list.append(vdata)
                    
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch,'value_type': val_type,
                'type': dict(self._fields['report_type'].selection).get(self.report_type), 'vouchers': final_list}

        
    def get_branch_cons_data(self):
        voucher_list = []
        final_list = []
        branch = 'All Branch'
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')

        '''
        vouchers = self.env['grant.application'].sudo().search(
            [('branch_id', '!=', False), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
        '''
        print('Reading Branch Consolidated Status Report---\n\n\n')
        vouchers = self.env['grant.application'].sudo().search([])
                
        if len(vouchers) >= 1:
            voucher_list.append(vouchers)
        if self.report_type == 'num_voucher':
            val_type = 'number'
            for sv in voucher_list:
                if len(sv) >= 1:
                    app = 0
                    dec = 0
                    for voucher in sv:
                        if voucher.status == 'reject':
                            dec += 1
                        else:
                            app += 1                            
                    total_voucher = app + dec
                    vdata = {'name': 'All Branch', 'app': app, 'dec': dec, 'total': total_voucher}
                    final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            for sv in voucher_list:
                if len(sv) >= 1:
                    app = 0
                    dec = 0
                    for voucher in sv:
                        if voucher.status == 'reject':
                            dec += voucher.grant_amount_required
                        else:
                            app += voucher.grant_amount_required                            
                    total_voucher = app + dec
                    vdata = {'name': 'All Branch', 'app': app, 'dec': dec,
                             'total': total_voucher}
                    final_list.append(vdata)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch,'value_type': val_type,
                'type': dict(self._fields['report_type'].selection).get(self.report_type), 'vouchers': final_list}

    def get_status_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            elif self.type == 'status_branch':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_branch_grant').report_action(self)
            elif self.type == 'status_branch_cons':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_branch_cons_grant').report_action(self)
