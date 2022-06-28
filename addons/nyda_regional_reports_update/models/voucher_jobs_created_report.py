from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class voucherJobsCreatedReport(models.Model):
    
    _name = 'voucher.jobs.createrd.report'
        
    region_id               = fields.Many2one('res.region', string='Region')
    start_date              = fields.Date(string="Start Date")
    end_date                = fields.Date(string="End Date")
    
    def get_voucher_jobs_created_data(self):
    
        voucher_list        = []
        final_list_before   = []
        final_list_after    = []

        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')

        if self.region_id:
            
            vouchers = self.env['voucher.application'].sudo().search([('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                     ('application_date', '>=', sdate), ('application_date', '<=', edate),('branch_id.region_id', '=', self.region_id.id)])
            
        if vouchers:

            rec_no          = 0
            multi   = 0
            total_voucher   = 0
            for voucher in vouchers:
                
                rec_no += 1
                
                job_creation = self.env['job.creation.information'].search([('voucher_application_id', '=', voucher.id)])
                
                for jc in job_creation:
                
                    before_data = {'rec_no': rec_no,
                                   'voucher_number': voucher.x_voucher_number,
                                   'before_funding_female': jc.before_funding_female,
                                   'before_funding_male': jc.before_funding_male,                             
                                   'before_funding_age_female': jc.before_funding_age_female,
                                   'beneficiary_branch' : voucher.branch_id.name,
                                   'before_funding_age_male': jc.before_funding_age_male,
                                   'before_funding_disabled_female': jc.before_funding_disabled_female,
                                   'before_funding_disabled_male': jc.before_funding_disabled_male,                                     
                                   }
                
                    
                    after_data = {'rec_no': rec_no,
                                  'voucher_number': voucher.x_voucher_number,
                                  'after_funding_female': jc.after_funding_female,
                                  'beneficiary_branch' : voucher.branch_id.name,
                                  'after_funding_male': jc.after_funding_male,                     
                                  'after_funding_age_female': jc.after_funding_age_female,
                                  'after_funding_age_male':   jc.after_funding_age_male,
                                  'after_funding_disabled_female': jc.after_funding_disabled_female,
                                  'after_funding_disabled_male': jc.after_funding_disabled_male,                                     
                                }
                    final_list_before.append(before_data)
                    final_list_after.append(after_data)
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'final_list_before': final_list_before,
                'final_list_after': final_list_after,
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
        
    def get_voucher_jobs_created_report(self):
         
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_regional_reports_update.action_voucher_jobs_created_report').report_action(self)
            