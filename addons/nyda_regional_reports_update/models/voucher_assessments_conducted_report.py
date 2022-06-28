from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class voucherAssessmentsConductedReport(models.Model):
    
    _name = 'voucher.assessments.conducted.report'
        
    region_id               = fields.Many2one('res.region', string='Region')
    start_date              = fields.Date(string="Start Date")
    end_date                = fields.Date(string="End Date")
    
    def get_assessments_conducted_data(self):
    
        voucher_list    = []
        final_list      = []
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')

        if self.region_id:
            
            vouchers = self.env['voucher.assessment'].sudo().search([('voucher_application_id.branch_id.region_id', '=', self.region_id.id)])
            
        if vouchers:

            total_voucher   = 0
            rec_no          = 0
            
            for voucher in vouchers:
                
                rec_no += 1
                
                check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(voucher.create_date, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), '%Y-%m-%d')
                
                if sdate <= check_date <= edate:
                    
                    vdata = { 
                            'rec_no': rec_no,
                            'beneficiary_branch':voucher.voucher_application_id.branch_id.name,
                            'application_id': voucher.voucher_application_id.serial_number,
                            'create_date': voucher.create_date,
                            'total': voucher.assessment_index_total
                         }
                    final_list.append(vdata)
                    
                    
        return {'start_date': self.start_date,
                'end_date': self.end_date,
                'vouchers': final_list,
                'total_voucher': total_voucher,
                'region' : self.region_id.name,
                }
        
        
        
    def get_assessments_conducted_report(self):
         
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_regional_reports_update.action_voucher_assessments_conducted_report').report_action(self)
            