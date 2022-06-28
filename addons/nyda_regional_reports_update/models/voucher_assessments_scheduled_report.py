# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class voucherAssessmentsScheduledReport(models.Model):
     
     _name = 'voucher.assessments.scheduled.report'
     
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
     
     
     def get_voucher_assessments_scheduled_data(self):
        voucher_list    = []
        final_list      = []
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.region_id:
            
            vouchers = self.env['voucher.application'].sudo().search([('appointment_date','!=', False),('branch_id.region_id', '=', self.region_id.id)])
                        
        if vouchers:
            rec_no          = 0
            total_voucher   = 0
            
            for voucher in vouchers:
                
                check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(voucher.create_date, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), '%Y-%m-%d')
                
                if sdate <= check_date <= edate:
                    
                    vdata = {
                            'rec_no': rec_no,                    
                            'serial_number': voucher.serial_number,
                            'application_date': voucher.application_date,
                            'status': dict(voucher._fields['status'].selection).get(voucher.status),
                            'service': voucher.business_development_assistance_ids,
                            'beneficiary_branch' : voucher.branch_id.name,
                            'name': voucher.name,
                            'surname': voucher.surname,
                            'mobile': voucher.mobile,
                            'appointment_date': voucher.appointment_date,
                            'bdo_name': voucher.bdo_name.name
                         }
                final_list.append(vdata)  
                total_voucher += voucher.x_voucher_value
                rec_no += 1
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
     
     def get_voucher_assessments_scheduled_report(self):
         
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_regional_reports_update.action_voucher_assessments_scheduled_report').report_action(self)
                                                                                                               