# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class voucherApplicationsReport(models.Model):
     
     _name = 'voucher.applications.report'
     
     region_id               = fields.Many2one('res.region', string='Region')
     regional_report         = fields.Boolean(string="Print Regional Report", default=False)
     start_date              = fields.Date(string="Start Date")
     end_date                = fields.Date(string="End Date")
     type = fields.Selection([('all', 'All'),
                             ('received_applications', 'Received'),
                             ('declined_applications', 'Declined'),
                             ('approved_applications', 'Approved'),
                             ('status_client', 'Voucher Issuance Report'),
                             ],
                            string="Type")
     
     
     def get_voucher_application_data(self):
        voucher_list    = []
        final_list      = []
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.region_id:
            
            vouchers = self.env['voucher.application'].sudo().search([('branch_id.region_id', '=', self.region_id.id)])
        
            for voucher in vouchers:
                
                if self.type == 'received_applications':
                    
                    vouchers = self.env['voucher.application'].sudo().search(
                            [('branch_id.region_id', '=', self.region_id.id),('status', '=', 'new')])
                   
                elif self.type == 'declined_applications':
                    
                    vouchers = self.env['voucher.application'].sudo().search([('branch_id.region_id', '=', self.region_id.id),('status', '=', 'decline')])
                      
                elif self.type == 'approved_applications':
                    
                    vouchers = self.env['voucher.application'].sudo().search(
                                    [('branch_id.region_id', '=', self.region_id.id),('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed'))])
                      
                elif self.type == 'status_client':
                    
                    vouchers = self.env['voucher.application'].sudo().search(
                                [('branch_id.region_id', '=', self.region_id.id),('status', 'in', ('voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed'))])
                else:
                    
                    vouchers = self.env['voucher.application'].sudo().search([('branch_id.region_id', '=', self.region_id.id)])
                   
                        
        
        rec_no          = 0
        total_voucher   = 0
        if vouchers:
            
            for voucher in vouchers:

                check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(voucher.create_date, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), '%Y-%m-%d')
                
                if sdate <= check_date <= edate:
                    
                    vdata = {
                        
                         'rec_no': rec_no, 
                         'name': voucher.name, 
                         'surname': voucher.surname,
                         'serial_number': voucher.serial_number,
                         'service': voucher.business_development_assistance_ids,
                         'x_voucher_number': voucher.x_voucher_number,
                         'x_service_provider': voucher.x_service_provider.name,
                         #'x_voucher_value': voucher.x_legacy_value,
                         'beneficiary_branch' : voucher.branch_id.name,
                         'x_voucher_value': voucher.x_voucher_value,
                         'gender': dict(voucher._fields['gender'].selection).get(voucher.gender),
                         'geographical_type': dict(voucher._fields['geographical_type'].selection).get(voucher.geographical_type),
                         'disability': dict(voucher._fields['disability'].selection).get(voucher.disability),
                         'population_group': dict(voucher._fields['population_group'].selection).get(voucher.population_group),
                         'status': dict(voucher._fields['status'].selection).get(voucher.status),
                         'application_date': voucher.application_date
                         }
                    final_list.append(vdata)
                    rec_no += 1   
                    total_voucher += voucher.x_voucher_value
                    
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,
                }
     
     def get_regional_voucher_report(self):
         
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_regional_reports_update.action_voucher_applications_report').report_action(self)
                                                                                                               