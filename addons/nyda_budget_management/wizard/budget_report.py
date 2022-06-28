 # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError
import logging
from openerp.osv import orm

_logger = logging.getLogger(__name__)

class FinancePayrollReport(models.TransientModel):
    """Finance Payroll Report"""
    _name           = "finance.budget.report"
    _description    = 'Finance Budget Report'

    start_date  = fields.Date(string="Start Date")
    end_date    = fields.Date(string="End Date")
    year = fields.Selection(
        [('2020', '2020'), ('2021', '2021'),('2022', '2022'), ('2023', '2023'),('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027')],
        string="Year")
    
    division = fields.Many2one('hr.department', string='Division')
    branch  = fields.Many2one('branch', string='Branch')
    budget_type = fields.Selection(
        [('mid-term','Mid-Term'),('standard','Standard')],
        string="Budget Type")    

    period = fields.Selection(
        [('Year 1','Year 1'),('Year 2','Year 2'),('Year 3','Year 3')],
        string="Period")    
    
    def get_budget_mid_org_report_data(self):
        budget_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
            
        if self.division:
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'mid-term')
                 , ('department', '=', self.division.id)])          
        else:            
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'mid-term')])
        
        if len(budgets) >= 1:
            budget_list.append(budgets)
        
        rec_no          = 0
        total_budget    = 0
        
        for sv in budget_list:
            rec_no += 1
            multi   = 0

            for budget in sv:
                
                budget_total = 0
                
                for bline in budget.crossovered_budget_line:
                    budget_total += (bline.planned_amount + bline.x_planned_amount_y2 + bline.x_planned_amount_y2) 
                    
                budget_data = { 'rec_no': rec_no,
                                'name': budget.name,
                                'responsible': budget.creating_user_id.name,
                                'department': budget.x_department.name,
                                'branch': budget.x_branch_id.x_name,
                                'date_from': budget.date_from,
                                'date_to': budget.date_to,
                                'budget_lines': budget.crossovered_budget_line,
                                'budget_total': budget_total
                            }
                
                final_list.append(budget_data)  
                total_budget += budget_total
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date,
                'period': self.period,
                'department': self.division.name, 
                'branch': self.branch.x_name,
                'budget_type': self.budget_type,
                'budgets': final_list, 
                'total_budget': total_budget}
        
    def get_budget_mid_org_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_finance_reports.action_finance_budget_mid_org_report').report_action(self)
            
    def get_budget_mid_division_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_finance_reports.action_finance_budget_mid_division_report').report_action(self)            
            

    def get_budget_mid_period_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_finance_reports.action_finance_budget_mid_period_report').report_action(self)            
                      
    def get_budget_management_report_data(self):
        budget_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
            
        if self.division:
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'standard')
                 , ('department', '=', self.division.id)])        
        elif self.branch:
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'standard')
                 , ('branch_id', '=', self.branch.id)])        
        
        elif self.budget_type:
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'standard')
                 , ('budget_type', '=', self.budget_type)])        
        else:            
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'standard')])
        
        if len(budgets) >= 1:
            budget_list.append(budgets)
        
        rec_no          = 0
        total_budget    = 0
        
        for sv in budget_list:
            rec_no += 1
            multi   = 0

            for budget in sv:
                
                budget_total = 0
                
                for bline in budget.crossovered_budget_line:
                    budget_total += bline.planned_amount
                    
                budget_data = { 'rec_no': rec_no,
                                'name': budget.name,
                                'responsible': budget.creating_user_id.name,
                                'department': budget.x_department.name,
                                'branch': budget.x_branch_id.x_name,
                                'date_from': budget.date_from,
                                'date_to': budget.date_to,
                                'budget_lines': budget.crossovered_budget_line,
                                'budget_total': budget_total
                            }
                
                final_list.append(budget_data)  
                total_budget += budget_total
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date,
                'department': self.division.name, 
                'branch': self.branch.x_name,
                'budget_type': self.budget_type,
                'budgets': final_list, 
                'total_budget': total_budget}
        
    def get_budget_management_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_finance_reports.action_finance_budget_management_report').report_action(self)      


    def get_budget_annual_exp_report_data(self):
        budget_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
            
        if self.division:
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'standard')
                 , ('department', '=', self.division.id)])        
        elif self.branch:
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'standard')
                 , ('branch_id', '=', self.branch.id)])        
        
        elif self.budget_type:
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'standard')
                 , ('budget_type', '=', self.budget_type)])        
        else:            
            budgets = self.env['crossovered.budget'].sudo().search(
                [('date_from', '>=', sdate), ('date_to', '<=', edate), ('budget_type', '=', 'standard')])
        
        if len(budgets) >= 1:
            budget_list.append(budgets)
        
        rec_no          = 0
        total_budget    = 0
        
        for sv in budget_list:
            rec_no += 1
            multi   = 0

            for budget in sv:
                
                budget_total = 0
                
                for bline in budget.crossovered_budget_line:
                    budget_total += bline.planned_amount
                    
                budget_data = { 'rec_no': rec_no,
                                'name': budget.name,
                                'responsible': budget.creating_user_id.name,
                                'department': budget.x_department.name,
                                'branch': budget.x_branch_id.x_name,
                                'date_from': budget.date_from,
                                'date_to': budget.date_to,
                                'budget_lines': budget.crossovered_budget_line,
                                'budget_total': budget_total
                            }
                
                final_list.append(budget_data)  
                total_budget += budget_total
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date,
                'department': self.division.name, 
                'branch': self.branch.x_name,
                'budget_type': self.budget_type,
                'budgets': final_list, 
                'total_budget': total_budget}
        
    def get_budget_annual_exp_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_finance_reports.action_finance_budget_expenditure_report').report_action(self)  
            
                      