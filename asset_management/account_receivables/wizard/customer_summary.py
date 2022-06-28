from odoo import api, fields, models
from datetime import date, datetime

class CustomerSummary(models.Model):
    _name = 'customer.summary'
    _description = 'Customer Summary'

    date_filter = fields.Boolean("Date Filter")
    
    customerID = fields.Many2one('res.partner',string='Customer ID')
    #customerID = fields.Many2one('res.partner',related='customerID.id',string='Name') #removed
    
    from_date = fields.Date("From")
    to_date = fields.Date("To")
    
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    
    total_invoices = fields.Integer("Invoices")
    total_sales = fields.Integer("Sales")
    total_sales_amount = fields.Monetary("Total Sales Amount")
    total_credit_notes = fields.Integer("Credit Notes")
    total_credit_amount = fields.Monetary("Total Credit Note")
    total_payment_received = fields.Monetary("Total Payments Received")
    
    @api.multi
    @api.depends('customerID','customerID','to_date','from_date')
    @api.onchange('customerID','customerID','to_date','from_date')
    def compute_voucher_value(self):
        #invoices total
        sales = 0.0
        s = 0
        purchases = 0.0
        p = 0
        total_payments = 0.0
        
        if self.date_filter:
            invoices = self.env['account.invoice'].search([('partner_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date),('state','in',('posted','paid','open'))])
        else:
            invoices = self.env['account.invoice'].search([('partner_id','=',self.customerID.id),('state','in',('posted','paid','open'))])
        #[('type','=','out_invoice'),('type','=','out_refund')]
        
        for inv in invoices:
            if inv.type == 'out_invoice':
                sales = sales+inv.amount_total
                s = s + 1
            elif inv.type == 'out_refund':
                purchases = purchases + inv.amount_total
                p = p + 1
        self.total_invoices = len(invoices)
        self.total_sales = s
        self.total_credit_notes = p
        
        self.total_sales_amount = sales
        self.total_credit_amount = purchases
        
        if self.date_filter:
            paid_inv = self.env['account.invoice'].search([('partner_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date),('state','in',('posted','paid')),('type','=','out_invoice')])
        else:
            paid_inv = self.env['account.invoice'].search([('partner_id','=',self.customerID.id),('state','in',('posted','paid')),('type','=','out_invoice')])
        
        for inv in paid_inv:
            total_payments = total_payments+inv.amount_total
        
        self.total_payment_received = total_payments
        
    def print_enquiry(self):
        return self.env.ref('account_receivables.action_report_trans_enq').report_action(self)
'''    
    @api.multi
    def get_transaction_enquiry(self):
        system_time = datetime.now()
        doc_date = datetime.now()
        create_user = self.env.user.name
        customer_id = self.customerID.customer_id
        
        debit_totals = 0
        credit_totals = 0
        applied_distribution_ids = []
        
        total_invoices_amount = 0
        total_write_off = 0
        total_discounts = 0
        total_unapplied_amount = 0
        total_applied_ = 0
        
        dict_custom = {}
        vouchers = {}
        final_list = []
        ledger_data = []
        for sv in self.transactions:
            for invoice in sv:
                vdata = {
                         'number': invoice.number, 
                         'date_invoice': invoice.date_invoice,
                         'due_date': invoice.date_due,
                         'customer_id': customer_id,
                         'name': self.customerID.name,
                         'comment': "N/A",
                         'amount_total_signed': invoice.amount_total_signed,
                         'write_off': "0.00",
                         'discount': invoice.discount * invoice.sales_amount,
                         'unapplied': invoice.amount_total_signed - (invoice.amount_total_signed * invoice.percentage),
                         }
                final_list.append(vdata)
                move_id = invoice.move_id
                if move_id:
                    for line in move_id.line_ids:
                        debit_totals =debit_totals+ line.debit
                        credit_totals = credit_totals+ line.credit
                        ledger = {
                         'code': line.account_id.code, 
                         'account_id': line.account_id.code+" "+line.account_id.name + " " +line.name,
                         'type': line.account_id.user_type_id.name,
                         'debit': line.debit,
                         'credit': line.credit,
                        }
                        ledger_data.append(ledger)
                
                app_data = {
                         'type': invoice.number, 
                         'inv_name': invoice.number,
                         'date_inv': invoice.date_invoice,
                         'discount_amount': invoice.discount_amount,
                         'write_off_amount': "0.00",
                         'amount_applied': invoice.amount_total_signed,
                        }
                applied_distribution_ids.append(app_data)
                total_invoices_amount = total_invoices_amount + invoice.amount_total_signed
                total_discounts = total_discounts+invoice.discount * invoice.sales_amount
                total_unapplied_amount = total_unapplied_amount+invoice.amount_total_signed - (invoice.amount_total_signed * invoice.percentage)
                total_applied_ = total_applied_+invoice.amount_total_signed
        dict_custom = {
                'system_time':system_time, 
                'doc_date':doc_date,
                'create_user':create_user,
                'customer_id':customer_id,
                'from_date':self.from_date,
                'to_date':self.to_date,
                'invoice_status':self.invoice_status,
                'name':self.customerID.name,
                'invoice_ids':final_list,
                'ledger_ids':ledger_data,
                'applied_distribution_ids':applied_distribution_ids,
                'total_invoices_amount':total_invoices_amount,
                'total_discounts':total_discounts,
                'total_unapplied_amount':total_unapplied_amount,
                'total_write_off':total_write_off,
                
                'discount_total':total_discounts,
                'write_off_total':total_write_off,
                'total_applied':total_applied_,
                'debit_totals':debit_totals,
                'credit_totals':credit_totals,
            }
        
        return dict_custom
    
'''    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    