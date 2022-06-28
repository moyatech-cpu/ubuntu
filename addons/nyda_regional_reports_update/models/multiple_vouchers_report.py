# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class MultipleVoucherReport(models.Model):
     
     _name = 'multiple.voucher.report'
     
     region_id               = fields.Many2one('res.region', string='Region')
     start_date              = fields.Date(string="Start Date")
     end_date                = fields.Date(string="End Date")
     
     
     
     def get_muliple_voucher_data(self):
        final_list      = []
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.region_id:
            
            vouchers = self.env['voucher.application'].sudo().search([('branch_id.region_id', '=', self.region_id.id)])
        
        
        rec_no          = 0
        total_voucher   = 0
        if vouchers:
            for voucher in vouchers:
                
                application_count = self.env['voucher.application'].search_count([('sa_identity_number','=',voucher.sa_identity_number)])
                
                if application_count > 1:
                    
                    applications=self.env['voucher.application'].search([('sa_identity_number','=',voucher.sa_identity_number)])
                    beneficiary_total = 0
                    
                    
                    for va in applications:
                        beneficiary_total += va.x_voucher_value
                        
                    check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(va.create_date, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), '%Y-%m-%d')
                
                    if sdate <= check_date <= edate:
                        
                        rec_no += 1
                        vdata = {'rec_no': rec_no,
                             'name': voucher.name, 
                             'surname': voucher.surname,
                             'sa_identity_number': voucher.sa_identity_number,
                             'mobile': voucher.mobile,
                             'beneficiary_branch' : voucher.branch_id.name,
                             'email': voucher.email,
                             'gender': voucher.gender,
                             'population_group': voucher.population_group,
                             'geographical_type': voucher.geographical_type,
                             'disability': voucher.disability,
                             'beneficiary_total': beneficiary_total,
                             }
                                    
                    final_list.append(vdata)  
                    total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}  
                        
     
     def get_regional_multiple_voucher_report(self):
         
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_regional_reports_update.action_multiple_vouchers_report').report_action(self)
                                                                                                               