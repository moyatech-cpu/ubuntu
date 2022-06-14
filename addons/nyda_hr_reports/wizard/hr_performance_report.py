 # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError
import logging
from openerp.osv import orm

_logger = logging.getLogger(__name__)

class HRPerformanceReport(models.TransientModel):
    """HR Performance Report"""
    _name           = "hr.performance.report"
    _description    = 'HR Performance Report'

    start_date  = fields.Date(string="Start Date")
    end_date    = fields.Date(string="End Date")
    year = fields.Selection(
        [('2021', '2021/22'),('2022', '2022/23'), ('2023', '2023/24'),('2024', '2024/25')],
        string="Year")
    
    position            = fields.Many2one('hr.job', string='Position')
    gender              = fields.Selection([('male', 'Male'),('female', 'Female'),('other', 'Other')], string="Gender")
    division            = fields.Many2one('hr.department', string='Division', domain=lambda self: [("parent_id", "=", False)])
    business_unit_id    = fields.Many2one('hr.department', string="Business Unit", domain=lambda self: [("parent_id", "!=", False)])
    branch              = fields.Many2one('res.branch', string='Branch')
    race                = fields.Selection([('African', 'African'),('Indian', 'Indian'),('Coloured', 'Coloured'),('White', 'White'),('Asian', 'Asian')], string="Race")
    
    #People that are managers
    manager     = fields.Many2one('hr.employee', string='Manager')

    def get_hr_performance_agreement_report_data(self):
        performance_agreement_list = []
        converted_start_date    = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date      = datetime.strptime(self.end_date, '%Y-%m-%d')
        print ("\n\n\n")
        
        if self.division:
            performance_data = self.env['project.task'].search([('project_id', '=', 55),('x_employee_division', '=', self.division.id)])
            
        elif self.business_unit_id:
            performance_data = self.env['project.task'].search([('project_id', '=', 55), ('x_employee_department', '=', self.business_unit_id.id)])
            
        elif self.branch:
            performance_data = self.env['project.task'].search([('project_id', '=', 55), ('x_employee_branch', '=', self.branch.id)])  
            
        else:            
            performance_data = self.env['project.task'].search([('project_id', '=', 55)])
                    
        #Filter data by date criteria
        if performance_data:
            
            for performance_data_date in performance_data:
                check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(performance_data_date.create_date, '%Y-%m-%d %H:%M:%S'),
                                      '%Y-%m-%d'), '%Y-%m-%d')
                if converted_start_date <= check_date <= converted_end_date:
                    performance_agreement_list.append(performance_data_date)
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date,
                'performance_data': performance_agreement_list}
        
    def get_hr_performance_agreement_report(self):
        return self.env.ref('nyda_hr_reports.action_performance_agreement_report').report_action(self)
    
    def get_hr_employee_report_data(self):
        employees_list = []

        if self.division:
            employee_data = self.env['hr.employee'].search([('department_id', '=', self.division.id)])

        if self.manager:
            employee_data = self.env['hr.employee'].search([('parent_id', '=', self.manager.id)])
                    
        elif self.gender:
            employee_data = self.env['hr.employee'].search([('gender', '=', self.gender)])

        elif self.race:
            employee_data = self.env['hr.employee'].search([('race', '=', self.race)])
                        
        elif self.branch:
            employee_data = self.env['hr.employee'].search([('branch_id', '=', self.branch.id)])
                                                    
        else:            
            employee_data = self.env['hr.employee'].search([])
                    
        #Filter data by date criteria
        if employee_data:
            
            for employee_data_item in employee_data:
                    employees_list.append(employee_data_item)
                    
        return {'division': self.division.name, 
                'employee_data': employees_list}
        
    def get_hr_employees_report(self):
        return self.env.ref('nyda_hr_reports.action_hr_employees_report').report_action(self)    
    
    def get_hr_performance_agreement_report_details_data(self):
        performance_agreement_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
            
        if self.division:
            agreements = self.env['project.task'].search([('project_id', '=', 55), ('x_employee_division', '=', self.division.id)])
            
        elif self.business_unit_id:
            agreements = self.env['project.task'].search([('project_id', '=', 55), ('x_employee_department', '=', self.business_unit_id.id)])
            
        elif self.branch:
            agreements = self.env['project.task'].search([('project_id', '=', 55), ('x_employee_branch', '=', self.branch.id)])            

        elif self.manager:
            agreements = self.env['project.task'].search([('project_id', '=', 55), ('x_employee', '=', self.manager.id)])
                        
        else:
            agreements = self.env['project.task'].search([('project_id', '=', 55)])
        
        if len(agreements) >= 1:
            performance_agreement_list.append(agreements)
        
        rec_no          = 0
        total_budget    = 0
        
        for sv in performance_agreement_list:
            rec_no += 1
            multi   = 0

            for agreement in sv:
                     
                agreement_data = { 'rec_no': rec_no,
                                    'name': agreement.name,
                                    'employee': agreement.x_employee.name,
                                    'position': agreement.x_employee_position.name,
                                    'division': agreement.x_employee_division.name,
                                    'business_unit': agreement.x_employee_department.name,
                                    'branch': agreement.x_employee_branch.name,
                                    'create_date': agreement.create_date,
                                    'agreement_lines': agreement.x_performance_management_id,
                                    'personal_development_lines': agreement.x_personal_development_id,
                                    'stage_id': agreement.stage_id.id,
                                    'x_line_manager': agreement.x_line_manager.name,
                                    'x_employee_director': agreement.x_employee_director.name,
                                    'write_date': agreement.write_date,
                                    'x_total_weights': agreement.x_total_weights,
                            }
                
                final_list.append(agreement_data)  
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date,
                'division': self.division.name, 
                'agreements': final_list}
        
    def get_hr_performance_agreement_details_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_hr_reports.action_performance_agreement_details_report').report_action(self)    