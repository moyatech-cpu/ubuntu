# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError

class TrainingReportWizard(models.TransientModel):
    """Training Report Wizard"""
    _name = "regional.grant.status.report.wizard"
    _description = 'Grant Status Regional Report Wizard'

    start_date              = fields.Date(string="Start Date")
    end_date                = fields.Date(string="End Date")
    show                    = fields.Selection([('grant_values', 'Grant Values'), ('grant_count', 'Number Of Grant Applications')],string="Show")
    region_id               = fields.Many2one("res.region", string="Region")
    
    
    def get_regional_grant_data(self):
        
         converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
         converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
         grant_data = []
         grant_list = []
         
         if self.region_id:
             
             grants = self.env['grant.application'].sudo().search([('branch_id.region_id', '=', self.region_id.id),
                                            ('application_date', '>=', converted_start_date), ('application_date', '<=', converted_end_date)])
        
            
         if self.show == 'grant_values':
          
             for grant in grants:
                 show = "grant_values"
                 
                 approved = 0
                 declined = 0
                 paid = 0
                 cancelled = 0
                 
                 if grant.status == 'approved':
                     approved += grant.grant_amount_required
                
                 elif grant.status == 'reject':
                     declined += grant.grant_amount_required
                    
                 elif grant.status == 'completed':
                     paid += grant.grant_amount_required
                    
                 elif grant.status == 'cancelled':
                     cancelled += grant.grant_amount_required  
                                              
                 total_grant = approved + declined + paid + cancelled
                     
                 data = {   'branch': grant.branch_id.name, 
                            'approved': approved,
                            'name': grant.name,
                            'surname': grant.surname, 
                             'declined': declined,'paid': paid,'cancelled': cancelled,
                             'total': total_grant, 'region': self.region_id.name,
            
                             }
                 grant_data.append(data)
                    
         elif self.show == 'grant_count':
             show = "grant_count"
             for grant in grants:

                    approved = 0
                    declined = 0
                    paid = 0
                    cancelled = 0
                    

                    if grant.status == 'approved':
                        approved += 1
                        
                    elif grant.status == 'reject':
                        declined += 1
                    
                    elif grant.status == 'completed':
                        paid += 1
                    
                    elif grant.status == 'cancelled':
                        cancelled += 1  
                                              
                    total_voucher = approved + declined + paid + cancelled
                     
                    data = {'branch': grant.branch_id.name,
                            'name': grant.name,
                            'surname': grant.surname,
                             'approved': approved, 
                             'declined': declined,'paid': paid,'cancelled': cancelled,
                             'total': total_voucher, 'region': self.region_id.name,
                             
            
                             }
                    grant_data.append(data)
             
         if grant_data:
             
             return {'start_date': self.start_date,
                 'end_date': self.end_date,
                 'grant': grant_data, 'region':self.region_id.name,
                 'show': show,
                 }
         
   
    def get_regional_grant_report(self):
        
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('system_update_008.action_regional_report_grant_status').report_action(self)
            
                        