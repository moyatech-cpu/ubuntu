# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class voucherReissueReport(models.Model):
     
     _name = 'voucher.reissue.report'
     
     region_id               = fields.Many2one('res.region', string='Region')
     start_date              = fields.Date(string="Start Date")
     end_date                = fields.Date(string="End Date")
     
     
     def get_voucher_reissue_data(self):
        voucher_list    = []
        final_list      = []
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.region_id:
            
            vouchers = self.env['voucher.application'].sudo().search([('branch_id.region_id', '=', self.region_id.id),('x_voucher_reissue_start_date', '!=', False),
                                                                      ('x_voucher_reissue_end_date','!=', False)])
        
        
        rec_no          = 0
        total_voucher   = 0
        if vouchers:
        
            for voucher in vouchers:
                
                check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(voucher.create_date, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), '%Y-%m-%d')
                
                if sdate <= check_date <= edate:
                    
                    vdata = {'rec_no': rec_no,
                         'name': voucher.name, 
                         'surname': voucher.surname,
                         'serial_number': voucher.serial_number,
                         'sa_identity_number': voucher.sa_identity_number,
                         'x_voucher_number': voucher.x_voucher_number,
                         'x_service_provider': voucher.x_service_provider.name,
                         'x_voucher_value': voucher.x_voucher_value,
                         
                         'beneficiary_branch' : voucher.branch_id.name,
                         'x_voucher_reissue_start_date': voucher.x_voucher_reissue_start_date,
                         'x_voucher_reissue_end_date': voucher.x_voucher_reissue_end_date,
                         
                         'gender': voucher.gender,
                         'geographical_type': voucher.geographical_type,
                         'disability': voucher.disability,
                         'population_group': voucher.population_group,
                         'application_date': voucher.application_date
                         }
                
                final_list.append(vdata)  
                total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
     
     def get_regional_voucher_reissue_report(self):
         
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_regional_reports_update.action_voucher_reissued_report').report_action(self)
                                                                                                               