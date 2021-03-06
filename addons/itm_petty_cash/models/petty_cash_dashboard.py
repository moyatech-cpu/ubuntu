# -*- coding: utf-8 -*-
# Odoo, Open Source Itm Petty Cash.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#

from odoo import models, fields, api, _
import datetime
from odoo.http import request
from dateutil.relativedelta import relativedelta
from odoo.exceptions import  UserError

class PettyCashDashboard(models.Model):
    _name = "petty.cash.dashboard"
 
    name = fields.Char(string="Name")


    @api.model
    def get_petty_cash_info(self):
        uid = request.session.uid
        cr = self.env.cr
        petty_line_obj = self.env['petty.cash.line']
        petty_cash_obj = self.env['petty.cash']
        employee_id = self.env['hr.employee'].sudo().search_read([('user_id', '=', uid)], limit=1)
        
        cash_search_view_id = self.env.ref('itm_petty_cash.view_petty_cash_search_id')
        petty_cash_line_view_id = self.env.ref('itm_petty_cash.view_petty_cash_line_search_id')
        user_employee_id = self.env['hr.employee'].search([('user_id', '=', uid)], limit=1)
        amount_received = 0.0
        request_money = 0.0
        request_reconcile =0.0
        dict_list = {}
        amount_request = 0.0
        amount_balance =0.0
        amount_expense = 0.0
        account_expense_count = 0
        expenses_table = []
        expenses_line_ids = []
        has_user_analytic = '' 
        # petty cash expenses for Bar chart
        query = """
            select to_char(to_timestamp (date_part('month', pl.date_maturity)::text, 'MM'), 'Month') as Month, sum(pl.amount)
            as Total, p.requested_employee_id as requested_employee_id from petty_cash p
            INNER JOIN petty_cash_line pl
                on (p.id = pl.cash_id and pl.state = 'paid' and p.state != 'draft')
            group by month, requested_employee_id , pl.date_maturity order by pl.date_maturity
        """
        cr.execute(query)
        petty_cash_data = cr.dictfetchall()
        petty_cash_label = []
        petty_cash_dataset = []
        for data in petty_cash_data:
            if data['requested_employee_id'] == user_employee_id.id :
                petty_cash_label.append(data['month'])
                petty_cash_dataset.append(data['total'])
        
        # custodian Chart Pie
        query = """
            select sum(p.amount_received) as amount_received, p.requested_employee_id as requested_employee_id , e.name as employee
            from petty_cash p
            inner join hr_employee e on(p.employee_id = e.id)
            group by e.name ,requested_employee_id 
        """
        cr.execute(query)
        custodian_data = cr.dictfetchall()
        custodian_labels = []
        custodian_dataset = []
        for data in custodian_data:
            if data['requested_employee_id'] == user_employee_id.id :
                custodian_labels.append(data['employee'])
                custodian_dataset.append(data['amount_received'])
        
        if user_employee_id : 
            if user_employee_id.user_has_groups('analytic.group_analytic_accounting'):
                has_user_analytic = 'True'
            else:
                has_user_analytic = 'False'
            for user in user_employee_id :
                cash_dispatch_cash_id = petty_cash_obj.search(
                    [('state', '=', 'cash_dispatch'), ('requested_employee_id', '=', user.id)])
                if cash_dispatch_cash_id:
                    for cash in  cash_dispatch_cash_id :
                        amount_received += cash.amount_received
                if cash_dispatch_cash_id:
                    for cash in  cash_dispatch_cash_id :
                        amount_balance += cash.petty_cash_balance
                request_cash_id = petty_cash_obj.search(
                    [('state', 'in', ['draft', 'request']), ('requested_employee_id', '=', user.id)])
                request_money_id =  petty_cash_obj.search(
                    [('state', 'in', ['request']), ('employee_id', '=', user.id)])
                request_reconcile_id =  petty_cash_obj.search(
                    [('state', 'in', ['to_reconcile']), ('employee_id', '=', user.id)])
                if request_reconcile_id:
                    for cash in  request_reconcile_id :
                        request_reconcile += cash.amount_received - cash.paid_amount_total
                if request_cash_id:
                    for cash in  request_cash_id :
                        amount_request += cash.amount_received
                if request_money_id:
                    for cash in  request_money_id :
                        request_money += cash.amount_received
                expense_cash_id = petty_cash_obj.search(
                    [('requested_employee_id', '=', user.id)])
                if expense_cash_id:
                    for cash in  expense_cash_id :
                        expense_line_id = petty_line_obj.search(
                            [('cash_id', '=', cash.id), ('state', '=', 'paid')])
                        if  expense_line_id:
                            for line in expense_line_id :
                                amount_expense += round(line.amount, 2)
                            
                account_expense_cash_id = petty_cash_obj.search(
                    [('requested_employee_id', '=', user.id)])
                account_details = []
                account_list = {}
                current_amount = 0
                last_amount = 0
                current_quarter_amount = 0
                last_quarter_amount = 0
                if account_expense_cash_id:
                    for cash in  account_expense_cash_id :
                        current_year = petty_line_obj.search([('cash_id', '=', cash.id), ('state', '=', 'paid'), ('date_maturity',
                        '>=' , (datetime.date.today()).strftime('%Y-01-01')), ('date_maturity', '<' ,
                        (datetime.date.today() + relativedelta(years=1)).strftime('%Y-01-01'))])
                        if current_year :
                            for i in current_year:
                                current_amount += i.amount
                        
                        last_year = petty_line_obj.search([('cash_id', '=', cash.id), ('state', '=', 'paid'), ('date_maturity',
                        '>=' , (datetime.date.today() - relativedelta(years=1)).strftime('%Y-01-01')), ('date_maturity', '<' ,
                        (datetime.date.today()).strftime('%Y-01-01'))])
                        if last_year :
                            for i in last_year:
                                last_amount += i.amount
                                
                        current_quarter_year = petty_line_obj.search([('cash_id', '=', cash.id), ('state', '=', 'paid'),
                           ('date_maturity', '<', (datetime.date.today() + relativedelta(months=3)).strftime('%Y-%m-01')),
                        ('date_maturity', '>=', (datetime.date.today()).strftime('%Y-%m-01'))])
                        if current_quarter_year :
                            for i in current_quarter_year:
                                current_quarter_amount += i.amount
                             
                        last_quarter_year = petty_line_obj.search([('cash_id', '=', cash.id), ('state', '=', 'paid'),
                           ('date_maturity', '>=', (datetime.date.today() - relativedelta(months=3)).strftime('%Y-%m-01')), ('date_maturity', '<', (datetime.date.today()).strftime('%Y-%m-01'))])
                        if last_quarter_year :
                            for i in last_quarter_year:
                                last_quarter_amount += i.amount
                        
                            
                        expense_line_id = petty_line_obj.search(
                            [('cash_id', '=', cash.id), ('state', '=', 'paid')])
                        if  expense_line_id:
                            for line in expense_line_id :
                                expenses_table.append({'memo':line.memo or '',
                                                       'account_expense_id':line.account_expense_id.name or '',
                                                       'date_maturity':line.date_maturity or '',
                                                       'amount': round(line.amount, 2) or 0.0,
                                                        'analytic_tag_ids':[c.name for c in line.analytic_tag_ids if line.analytic_tag_ids ],
                                                        'analytic_account_id': line.analytic_account_id.name or '',
                                                       })
                                
                                expenses_line_ids.append(line.id)
                                account_list[line.account_expense_id.name] = line.account_expense_id.id
                                if not line.account_expense_id.name in dict_list :
                                    dict_list[line.account_expense_id.name] = round(line.amount, 2) 
                                else:
                                    dict_list[line.account_expense_id.name] = dict_list[line.account_expense_id.name] + round(line.amount, 2) 
        
        account_details = sorted(dict_list.items(), key=lambda x: (-x[1], x[0]))
        account_filter_top1 = 0,
        account_filter_top2 = 0
        account_filter_top3 = 0
        account_filter_top4 = 0
        account_filter_top5 = 0
        for acc in account_details :
            if account_expense_count < 6 :
                account_expense_count += 1
                if account_expense_count == 1:
                    if acc[0] in account_list:
                        account_filter_top1 = account_list[acc[0]]
                if account_expense_count == 2:
                    if acc[0] in account_list:
                        account_filter_top2 = account_list[acc[0]]
                if account_expense_count == 3:
                    if acc[0] in account_list:
                        account_filter_top3 = account_list[acc[0]]
                if account_expense_count == 4:
                    if acc[0] in account_list:
                        account_filter_top4 = account_list[acc[0]]
                if account_expense_count == 5:
                    if acc[0] in account_list:
                        account_filter_top5 = account_list[acc[0]]
        if employee_id:
            categories = self.env['hr.employee.category'].sudo().search([('id', 'in', employee_id[0]['category_ids'])])
            data = {
                'categories': [c.name for c in categories],
                'cash_search_view_id': cash_search_view_id.id,
                'petty_cash_line_view_id': petty_cash_line_view_id.id,
                'cash_dispatch_count' : round(amount_received, 2),
                'request_count' :round(amount_request, 2) ,
                'request_money' :round(request_money, 2) ,
                'request_reconcile' :round(request_reconcile, 2) ,
                'expense_count' :round(amount_expense, 2),
                'balance_count' :round(amount_balance, 2) ,
                'account_expense_details' :account_details,
                'current_amount' :round(current_amount, 2),
                'last_amount' :round(last_amount, 2),
                'current_quarter_amount' : round(current_quarter_amount, 2),
                'last_quarter_amount' : round(last_quarter_amount, 2) ,
                'account_expense_count' :account_expense_count,
                'account_filter_top1' :account_filter_top1,
                'account_filter_top2' :account_filter_top2,
                'account_filter_top3' :account_filter_top3,
                'account_filter_top4' :account_filter_top4,
                'account_filter_top5' :account_filter_top5,
                'petty_cash_label': petty_cash_label,
                'petty_cash_dataset': petty_cash_dataset,
                'custodian_labels': custodian_labels,
                'custodian_dataset': custodian_dataset,
                'expenses_table': expenses_table,
                'expenses_line_ids' :expenses_line_ids,
                'has_user_analytic' :has_user_analytic,
            }
            employee_id[0].update(data)
            return employee_id
        else :
            raise UserError(_('Login User Is Not Set As Employee!'))
    
    @api.model
    def get_budget_info(self):
        uid = request.session.uid
        cr = self.env.cr
        budget_expenses_table = []
        acc_ids =  []
        budget_line_ids = []
        budget_account_list = {}
        budget_dict_list = {}
        budget_account_expense_count = 0
        petty_line_obj  = self.env['petty.cash.line']
        payment_line_obj = self.env['account.payment']
        
        #  Custom budget management code PR MOHAPI 23/04/2019
        budget_lines = self.env['crossovered.budget'].sudo().search_read([('creating_user_id', '=', uid)], limit=1)
        
        budget_expense_line_id = payment_line_obj.search([('x_budget_line_id', 'in', budget_lines[0]['crossovered_budget_line'])])
        
        if  budget_expense_line_id:
            for line in budget_expense_line_id :
                budget_expenses_table.append({'name':line.name or '',
                                               'account_to_id':line.account_to_id.name or '',
                                               'payment_date':line.payment_date or '',
                                               'amount': round(line.amount, 2) or 0.0,
                                                'analytic_account_id': line.analytic_account_id.name or '',
                                               })

                budget_line_ids.append(line.id)
                budget_account_list[line.account_to_id.name] = line.account_to_id.id
                if not line.account_to_id.name in budget_dict_list :
                    budget_dict_list[line.account_to_id.name] = round(line.amount, 2)
                else:
                    budget_dict_list[line.account_to_id.name] = budget_dict_list[line.account_to_id.name] + round(line.amount, 2) 

        print('Budget Dictionary Keys')
        print(list(budget_dict_list.keys()))
        print('-----------------')
        print('Budget Dictionary Values')
        print(list(budget_dict_list.values()))
        print('-----------------')        
        budget_account_details = sorted(budget_dict_list.items(), key=lambda x: (-x[1], x[0]))

        budget_account_filter_top1 = 0,
        budget_account_filter_top2 = 0
        budget_account_filter_top3 = 0
        budget_account_filter_top4 = 0
        budget_account_filter_top5 = 0
        
        for acc in budget_account_details :
            if budget_account_expense_count < 6 :
                budget_account_expense_count += 1
                if budget_account_expense_count == 1:
                    if acc[0] in budget_account_list:
                        budget_account_filter_top1 = budget_account_list[acc[0]]
                if budget_account_expense_count == 2:
                    if acc[0] in budget_account_list:
                        budget_account_filter_top2 = budget_account_list[acc[0]]
                if budget_account_expense_count == 3:
                    if acc[0] in budget_account_list:
                        budget_account_filter_top3 = budget_account_list[acc[0]]
                if budget_account_expense_count == 4:
                    if acc[0] in budget_account_list:
                        budget_account_filter_top4 = budget_account_list[acc[0]]
                if budget_account_expense_count == 5:
                    if acc[0] in budget_account_list:
                        budget_account_filter_top5 = budget_account_list[acc[0]]



                                            
        petty_cash_obj = self.env['petty.cash']
        employee_id = self.env['hr.employee'].sudo().search_read([('user_id', '=', uid)], limit=1)
        
        #  Custom budget management code PR MOHAPI 23/04/2019
        budget_id = self.env['crossovered.budget'].sudo().search_read([('creating_user_id', '=', uid)], limit=1)

        cash_search_view_id = self.env.ref('itm_petty_cash.view_petty_cash_search_id')
        petty_cash_line_view_id = self.env.ref('itm_petty_cash.view_petty_cash_line_search_id')
        user_employee_id = self.env['hr.employee'].search([('user_id', '=', uid)], limit=1)
        amount_received = 0.0
        request_money = 0.0
        request_reconcile =0.0
        dict_list = {}
        amount_request = 0.0
        amount_balance =0.0
        amount_expense = 0.0
        account_expense_count = 0
        expenses_table = []
        expenses_line_ids = []
        has_user_analytic = '' 
        # petty cash expenses for Bar chart
        query = """
            select to_char(to_timestamp (date_part('month', pl.date_maturity)::text, 'MM'), 'Month') as Month, sum(pl.amount)
            as Total, p.requested_employee_id as requested_employee_id from petty_cash p
            INNER JOIN petty_cash_line pl
                on (p.id = pl.cash_id and pl.state = 'paid' and p.state != 'draft')
            group by month, requested_employee_id , pl.date_maturity order by pl.date_maturity
        """
        cr.execute(query)
        petty_cash_data = cr.dictfetchall()
        petty_cash_label = []
        petty_cash_dataset = []
        for data in petty_cash_data:
            if data['requested_employee_id'] == user_employee_id.id :
                petty_cash_label.append(data['month'])
                petty_cash_dataset.append(data['total'])
        
        # custodian Chart Pie
        query = """
            select sum(p.amount_received) as amount_received, p.requested_employee_id as requested_employee_id , e.name as employee
            from petty_cash p
            inner join hr_employee e on(p.employee_id = e.id)
            group by e.name ,requested_employee_id 
        """
        cr.execute(query)
        custodian_data = cr.dictfetchall()
        
        #Budget Expendieture Pie Chart PR MOHAPI 23/04/2019
        custodian_labels = ['Budget Received', 'Amount Spent']
        custodian_dataset = [budget_id[0]['x_budget_limit'], budget_id[0]['x_total_spent']]
        
        #for data in custodian_data:
        #    if data['requested_employee_id'] == user_employee_id.id :
        #        custodian_labels.append(data['employee'])
        #        custodian_dataset.append(data['amount_received'])
        
        if user_employee_id : 
            if user_employee_id.user_has_groups('analytic.group_analytic_accounting'):
                has_user_analytic = 'True'
            else:
                has_user_analytic = 'False'
                
            for user in user_employee_id :
                cash_dispatch_cash_id = petty_cash_obj.search(
                    [('state', '=', 'cash_dispatch'), ('requested_employee_id', '=', user.id)])
                if cash_dispatch_cash_id:
                    for cash in  cash_dispatch_cash_id :
                        amount_received += cash.amount_received
                if cash_dispatch_cash_id:
                    for cash in  cash_dispatch_cash_id :
                        amount_balance += cash.petty_cash_balance
                request_cash_id = petty_cash_obj.search(
                    [('state', 'in', ['draft', 'request']), ('requested_employee_id', '=', user.id)])
                request_money_id =  petty_cash_obj.search(
                    [('state', 'in', ['request']), ('employee_id', '=', user.id)])
                request_reconcile_id =  petty_cash_obj.search(
                    [('state', 'in', ['to_reconcile']), ('employee_id', '=', user.id)])
                if request_reconcile_id:
                    for cash in  request_reconcile_id :
                        request_reconcile += cash.amount_received - cash.paid_amount_total
                if request_cash_id:
                    for cash in  request_cash_id :
                        amount_request += cash.amount_received
                if request_money_id:
                    for cash in  request_money_id :
                        request_money += cash.amount_received
                        
                        
                        
                expense_cash_id = petty_cash_obj.search(
                    [('requested_employee_id', '=', user.id)])
                if expense_cash_id:
                    for cash in  expense_cash_id :
                        expense_line_id = petty_line_obj.search(
                            [('cash_id', '=', cash.id), ('state', '=', 'paid')])
                        if  expense_line_id:
                            for line in expense_line_id :
                                amount_expense += round(line.amount, 2)
                            
                account_expense_cash_id = petty_cash_obj.search(
                    [('requested_employee_id', '=', user.id)])
                account_details = []
                account_list = {}
                current_amount = 0
                last_amount = 0
                current_quarter_amount = 0
                last_quarter_amount = 0
                
                if account_expense_cash_id:
                    for cash in  account_expense_cash_id :
                        current_year = petty_line_obj.search([('cash_id', '=', cash.id), ('state', '=', 'paid'), ('date_maturity',
                        '>=' , (datetime.date.today()).strftime('%Y-01-01')), ('date_maturity', '<' ,
                        (datetime.date.today() + relativedelta(years=1)).strftime('%Y-01-01'))])
                        if current_year :
                            for i in current_year:
                                current_amount += i.amount
                        
                        last_year = petty_line_obj.search([('cash_id', '=', cash.id), ('state', '=', 'paid'), ('date_maturity',
                        '>=' , (datetime.date.today() - relativedelta(years=1)).strftime('%Y-01-01')), ('date_maturity', '<' ,
                        (datetime.date.today()).strftime('%Y-01-01'))])
                        if last_year :
                            for i in last_year:
                                last_amount += i.amount
                                
                        current_quarter_year = petty_line_obj.search([('cash_id', '=', cash.id), ('state', '=', 'paid'),
                           ('date_maturity', '<', (datetime.date.today() + relativedelta(months=3)).strftime('%Y-%m-01')),
                        ('date_maturity', '>=', (datetime.date.today()).strftime('%Y-%m-01'))])
                        if current_quarter_year :
                            for i in current_quarter_year:
                                current_quarter_amount += i.amount
                             
                        last_quarter_year = petty_line_obj.search([('cash_id', '=', cash.id), ('state', '=', 'paid'),
                           ('date_maturity', '>=', (datetime.date.today() - relativedelta(months=3)).strftime('%Y-%m-01')), ('date_maturity', '<', (datetime.date.today()).strftime('%Y-%m-01'))])
                        if last_quarter_year :
                            for i in last_quarter_year:
                                last_quarter_amount += i.amount
                            
                        expense_line_id = petty_line_obj.search(
                            [('cash_id', '=', cash.id), ('state', '=', 'paid')])
                        if  expense_line_id:
                            for line in expense_line_id :
                                expenses_table.append({'memo':line.memo or '',
                                                       'account_expense_id':line.account_expense_id.name or '',
                                                       'date_maturity':line.date_maturity or '',
                                                       'amount': round(line.amount, 2) or 0.0,
                                                        'analytic_tag_ids':[c.name for c in line.analytic_tag_ids if line.analytic_tag_ids ],
                                                        'analytic_account_id': line.analytic_account_id.name or '',
                                                       })
                                
                                expenses_line_ids.append(line.id)
                                account_list[line.account_expense_id.name] = line.account_expense_id.id
                                if not line.account_expense_id.name in dict_list :
                                    dict_list[line.account_expense_id.name] = round(line.amount, 2) 
                                else:
                                    dict_list[line.account_expense_id.name] = dict_list[line.account_expense_id.name] + round(line.amount, 2) 

        account_details = sorted(dict_list.items(), key=lambda x: (-x[1], x[0]))
        account_filter_top1 = 0,
        account_filter_top2 = 0
        account_filter_top3 = 0
        account_filter_top4 = 0
        account_filter_top5 = 0
        for acc in account_details :
            if account_expense_count < 6 :
                account_expense_count += 1
                if account_expense_count == 1:
                    if acc[0] in account_list:
                        account_filter_top1 = account_list[acc[0]]
                if account_expense_count == 2:
                    if acc[0] in account_list:
                        account_filter_top2 = account_list[acc[0]]
                if account_expense_count == 3:
                    if acc[0] in account_list:
                        account_filter_top3 = account_list[acc[0]]
                if account_expense_count == 4:
                    if acc[0] in account_list:
                        account_filter_top4 = account_list[acc[0]]
                if account_expense_count == 5:
                    if acc[0] in account_list:
                        account_filter_top5 = account_list[acc[0]]
        if employee_id:
            categories = self.env['hr.employee.category'].sudo().search([('id', 'in', employee_id[0]['category_ids'])])
            data = {
                'categories': [c.name for c in categories],
                'cash_search_view_id': cash_search_view_id.id,
                'petty_cash_line_view_id': petty_cash_line_view_id.id,
                'cash_dispatch_count' : round(amount_received, 2),
                'request_count' :round(amount_request, 2) ,
                'request_money' :round(request_money, 2) ,
                'request_reconcile' :round(request_reconcile, 2) ,
                'expense_count' :round(amount_expense, 2),
                'balance_count' :round(amount_balance, 2) ,
                
                'account_expense_details' :account_details,
                
                'budget_account_expense_details' :budget_account_details,
                
                'current_amount' :round(current_amount, 2),
                'last_amount' :round(last_amount, 2),
                'current_quarter_amount' : round(current_quarter_amount, 2),
                'last_quarter_amount' : round(last_quarter_amount, 2) ,
                'account_expense_count' :account_expense_count,
                'budget_account_expense_count' :budget_account_expense_count,
                
                'account_filter_top1' :account_filter_top1,
                'account_filter_top2' :account_filter_top2,
                'account_filter_top3' :account_filter_top3,
                'account_filter_top4' :account_filter_top4,
                'account_filter_top5' :account_filter_top5,

                'budget_account_filter_top1' :budget_account_filter_top1,
                'budget_account_filter_top2' :budget_account_filter_top2,
                'budget_account_filter_top3' :budget_account_filter_top3,
                'budget_account_filter_top4' :budget_account_filter_top4,
                'budget_account_filter_top5' :budget_account_filter_top5,                
                
                'petty_cash_label': petty_cash_label,
                'petty_cash_dataset': petty_cash_dataset,
                'custodian_labels': custodian_labels,
                'custodian_dataset': custodian_dataset,
                'expenses_table': expenses_table,
                'expenses_line_ids' :expenses_line_ids,
                'budget_line_ids' :budget_line_ids,
                
                'has_user_analytic' :has_user_analytic,
                
                #  Custom budget management code PR MOHAPI 23/04/2019
                'budget_id' :budget_id[0]['id'],
                'budget_received' :budget_id[0]['x_budget_limit'],
                'budget_spent' : budget_id[0]['x_total_spent'],
                'budget_balance' : budget_id[0]['x_budget_balance'],
                'budget_requested' : budget_id[0]['x_budget_request'],
                
                'budget_expenses_table': budget_expenses_table,
                'budget_expenses_labels': (list(budget_dict_list.keys())),
                'budget_expenses_data': (list(budget_dict_list.values())),
                
                
            }
            employee_id[0].update(data)
            return employee_id
        else :
            raise UserError(_('Login User Is Not Set As Employee!'))            
