# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class voucherBeneficiariesSupportedReport(models.Model):
     
     _name = 'voucher.beneficiaries.report'
     
     region_id               = fields.Many2one('res.region', string='Region')
     start_date              = fields.Date(string="Start Date")
     end_date                = fields.Date(string="End Date")
     
     
     
     def get_voucher_beneficiaries_data(self):
        voucher_list    = []
        final_list      = []
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.region_id:
            
            vouchers = self.env['voucher.application'].sudo().search([('status', 'in', ('voucher_isurance', 'work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                ('branch_id.region_id', '=', self.region_id.id)])
        
        if vouchers:
            
            rec_no          = 0
            total_voucher   = 0

            for voucher in vouchers:
                
                beneficiaries_list = []
                
                #Get count of voucher applications per client
                beneficiaries = self.env['business.ownership.status'].search([('voucher_application_id_business_ownership', '=', voucher.id)])
                
                for va in beneficiaries:
                
                    beneficiary_data = { 'rec_no': rec_no,
                                         'voucher_number': voucher.x_voucher_number,
                                         'name': va.name, 
                                         'contact_number': va.mobile,
                                         'population_group': va.population_group,
                                         'geographical_type': va.geographical_type,
                                         'beneficiary_branch' : voucher.branch_id.name,
                                         'disability': va.disability,
                                         'gender': va.gender,
                                         'ownership': va.ownership,
                                         'id_number': va.x_id_number,
                                         'position': va.position
                                         }
                    
                    beneficiaries_list.append(beneficiary_data)
                    
                    check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(voucher.create_date, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), '%Y-%m-%d')
                
                    if sdate <= check_date <= edate:
                    
                                 voucher_data = {'rec_no': rec_no,
                                 'name': voucher.name,
                                 'surname': voucher.surname,
                                 'voucher_number': voucher.x_voucher_number,
                                 'sa_identity_number': voucher.sa_identity_number,
                                 'beneficiary_branch' : voucher.branch_id.name,
                                 'gender': voucher.gender,
                                 'geographical_type': voucher.geographical_type,
                                 'disability': voucher.disability,
                                 'population_group': voucher.population_group,
                                 'contact_number': voucher.mobile,
                                 'beneficiaries':beneficiaries_list
                                 }
                    
                    final_list.append(voucher_data)                    
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
               
     
     def get_regional_voucher_beneficiaries_report(self):
         
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_regional_reports_update.action_voucher_beneficiaries_report').report_action(self)
                                                                                                               