from odoo import models, fields, api
from odoo import  _
from datetime import date, datetime
from odoo.exceptions import UserError

class ThusanoFundReportWizard(models.TransientModel):
    _name = 'thusano.fund.report.wizard'

    state = fields.Selection([('new', 'New'), ('accepted', 'Accepted'),
                                ('decline', ' Decline'), ('shortlisted', ' Shortlisted')],string='Application Status', default='new')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    @api.multi
    def get_application_report(self):
    
        return self.env.ref('thusano_fund.action_thuso_fund_report').report_action(self)
    
    @api.model
    def get_report_values(self):
        
        applicant_data = []
        
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        
        if self.state:
            applications = self.env['thusano.fund'].sudo().search([('state','=', self.state)])
            
            
        else:
            applications = self.env['thusano.fund'].sudo().search([])
             
        if applications :
            
            for application_date in applications:
                
                check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(application_date.create_date, '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), '%Y-%m-%d')
                if sdate <= check_date <= edate:
                    
                    temp_data = {
                            'applicant_name' :application_date.name,
                            'applicant_date' :application_date.application_date,
                            'applicant_surname' :application_date.surname,
                            'applicant_ID' :application_date.id_number,
                            'applicant_email' :application_date.email,
                            'applicant_gender' :application_date.gender,
                            'applicant_state' :application_date.state,
                            'approved_amount' :application_date.approved_amount,
                            'total_amount' :application_date.total_amount,
                    }
                    applicant_data.append(temp_data)
             
        return{
            
            'applicant': applicant_data,
            'state' : self.state,
            'start_date': self.start_date,
            'end_date': self.end_date,
            }
