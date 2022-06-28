from odoo import api, fields, models
from datetime import date, datetime

class TransactionEnquiry(models.Model):
    _name = 'transactions.enquiry'
    _description = 'Enquiry Batch'

    #creditor_id = fields.Many2one('creditor.id',string='Creditor ID') #removed
    #comment = fields.Text("Comment")
    
    date_filter = fields.Boolean("Date Filter")
    status_filter = fields.Boolean("Status Filter")
    
    customerID = fields.Many2one('res.partner',string='Customer ID')
    #customerID = fields.Many2one('res.partner',related='customerID.id',string='Name') #removed
    type = fields.Selection([
            ('All','All Types'),
            ('out_invoice','Sales Invoices'),
            ('out_refund', 'Credit Notes'),
        ],default='All', string='Type')
    
    invoice_status = fields.Selection([
            ('draft','Draft'),
            ('pending','Pending'),
            ('open', 'Open'),
            ('posted', 'Posted'),
            ('recon', 'Reconciled'),            
            ('paid', 'Paid'),
            ('review','Review'),
            ('cancel', 'Cancelled'),
        ], string='Status Filter')
    
    from_date = fields.Date("From")
    to_date = fields.Date("To")
    state = fields.Selection(
        [('available', 'Available'), ('not_available', 'Un Available')],
        default='available', string="Batch State")
    transactions = fields.One2many('account.invoice','last_enquiry_id',string="Transactions")
    
    @api.multi
    @api.depends('customerID','invoice_status','type','to_date')
    @api.onchange('customerID','invoice_status','type','to_date')
    def compute_voucher_value(self):
        
        if self.type == "All":
            if self.date_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('user_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date)])
                    rec['transactions'] = result
                    for inv in result:
                        inv.last_enquiry_id = self.id 
            elif self.date_filter and self.status_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('state','=',self.invoice_status),('user_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date)])
                    rec['transactions'] = result
                    for inv in result:
                        inv.last_enquiry_id = self.id
            elif self.status_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('state','=',self.invoice_status),('user_id','=',self.customerID.id)])
                    rec['transactions'] = result
                    for inv in result:
                        inv.last_enquiry_id = self.id 
            else:
                for rec in self:
                    result = self.env['account.invoice'].search([('user_id','=',self.customerID.id)])
                    rec['transactions'] = result
                    for inv in result:
                        inv.last_enquiry_id = self.id
        else:
            if self.date_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('user_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date),('type','=',self.type)])
                    rec['transactions'] = result
                    for inv in result:
                        inv.last_enquiry_id = self.id 
            elif self.date_filter and self.status_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('state','=',self.invoice_status),('user_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date),('type','=',self.type)])
                    rec['transactions'] = result
                    for inv in result:
                        inv.last_enquiry_id = self.id
            elif self.status_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('state','=',self.invoice_status),('user_id','=',self.customerID.id),('type','=',self.type)])
                    rec['transactions'] = result
                    for inv in result:
                        inv.last_enquiry_id = self.id 
            else:
                for rec in self:
                    result = self.env['account.invoice'].search([('user_id','=',self.customerID.id),('type','=',self.type)])
                    rec['transactions'] = result
                    for inv in result:
                        inv.last_enquiry_id = self.id
    
    @api.multi
    @api.depends('customerID','invoice_status','to_date','type')
    @api.onchange('customerID','invoice_status','to_date','type')
    def compute_voucher_value(self):
        if self.type == "All":
            if self.date_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('partner_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date)])
                    rec['transactions'] = result
                    #for inv in result:
                    #    inv.last_enquiry_id = self.id 
            elif self.status_filter and self.date_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('state','=',self.invoice_status),('partner_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date)])
                    rec['transactions'] = result
                    #for inv in result:
                    #    inv.last_enquiry_id = self.id 
            elif self.status_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('state','=',self.invoice_status),('partner_id','=',self.customerID.id)])
                    rec['transactions'] = result
                    #for inv in result:
                    #    inv.last_enquiry_id = self.id 
            else:
                for rec in self:
                    result = self.env['account.invoice'].search([('partner_id','=',self.customerID.id)])
                    rec['transactions'] = result
                    #for inv in result:
                    #    inv.last_enquiry_id = self.id 
        else:
            if self.date_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('partner_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date),('type','=',self.type)])
                    rec['transactions'] = result
                    #for inv in result:
                    #    inv.last_enquiry_id = self.id 
            elif self.status_filter and self.date_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('state','=',self.invoice_status),('partner_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date),('type','=',self.type)])
                    rec['transactions'] = result
                    #for inv in result:
                    #    inv.last_enquiry_id = self.id 
            elif self.status_filter:
                for rec in self:
                    result = self.env['account.invoice'].search([('state','=',self.invoice_status),('partner_id','=',self.customerID.id),('type','=',self.type)])
                    rec['transactions'] = result
                    #for inv in result:
                    #    inv.last_enquiry_id = self.id 
            else:
                for rec in self:
                    result = self.env['account.invoice'].search([('partner_id','=',self.customerID.id),('type','=',self.type)])
                    rec['transactions'] = result
                    #for inv in result:
                    #    inv.last_enquiry_id = self.id 

    
    def print_enquiry(self):
        return self.env.ref('account_receivables.action_report_trans_enq').report_action(self)
    
    '''@api.multi
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
        
        return dict_custom'''
    @api.multi
    def get_transaction_enquiry(self):
        system_time = datetime.now()
        doc_date = datetime.now()
        create_user = self.env.user.name
        customer_id = self.customerID.customer_id
        #system_time = datetime.now()
        create_date = self.create_date
        #create_user = self.env.user.name
        #batch_id = self.batch_id
        #posting_date = self.posting_date
        #comment = self.comment
        #transactions_actual = self.transactions_actual
        #transactions_control = self.transactions_control
        #batch_actual = self.batch_actual
        #batch_control = self.batch_control
        state = self.invoice_status
        #approvalUser = self.approvalUser.name
        #approval_date = self.approval_date
        
        #debit_totals = 0
        #credit_totals = 0
        applied_distribution_ids = []
        
        total_invoices_amount = 0
        total_write_off = 0
        total_discounts = 0
        total_unapplied_amount = 0
        total_applied_ = 0
        
        dictionairy = []
        dict_custom = {}
        vouchers = {}
        final_list = []
        ledger_data = []
        for sv in self.transactions:
            for invoice in sv:
                temp_ledger = []
                move_id = invoice.move_id
                debit_totals = 0
                credit_totals = 0
                if move_id:
                    for line in move_id.line_ids:
                        debit_totals =debit_totals+ line.debit
                        credit_totals = credit_totals + line.credit
                        ledger = {
                         'code': line.account_id.code, 
                         'account_id': line.account_id.code+" "+line.account_id.name + " " +line.name,
                         'type': line.account_id.user_type_id.name,
                         'debit': line.debit,
                         'credit': line.credit,
                         
                        }
                        ledger_data.append(ledger)
                        temp_ledger.append(ledger)
                    
                vdata = {
                         'number': invoice.number, 
                         'date_invoice': invoice.date_invoice,
                         'due_date': invoice.date_due,
                         #'customer_id': invoice.partner_id.name,
                         #'name': invoice.partner_id.name,
                         'sales_person': "",
                         'amount_total_signed': invoice.amount_total_signed,
                         #'write_off': "0.00",
                         'customer_id': customer_id,
                         'name': self.customerID.name,
                         'comment': "N/A",
                         #'amount_total_signed': invoice.amount_total_signed,
                         'write_off': "0.00",
                         'discount': invoice.discount * invoice.sales_amount,
                         'discount': invoice.discount * invoice.sales_amount,
                         'ledger_data':temp_ledger,
                         'debit_totals':debit_totals,
                         'credit_totals':credit_totals,
                         #'unapplied': invoice.amount_total_signed - (invoice.amount_total_signed * invoice.percentage),
                         }
                       
                final_list.append(vdata)
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
                'create_user':create_user,
                'create_date':create_date,
                'customer_id':customer_id,
                #'batch_id':batch_id,
                #'posting_date':posting_date,
                #'comment':comment,
                #'transactions_actual':transactions_actual,
                #'transactions_control':transactions_control,
                #'batch_actual':batch_actual,
                #'batch_control':batch_control,
                #'state':state,
                #'approval_date':approval_date,
                #'approvalUser':approvalUser,
                'invoice_status':self.invoice_status,
                'invoice_ids':final_list,
                'ledger_ids':ledger_data,
                'applied_distribution_ids':applied_distribution_ids,
                'total_invoices_amount':total_invoices_amount,
                'total_discounts':total_discounts,
                'total_unapplied_amount':total_unapplied_amount,
                'total_write_off':total_write_off,
                'name':self.customerID.name,
                'discount_total':total_discounts,
                'write_off_total':total_write_off,
                'total_applied':total_applied_,
                'debit_totals':debit_totals,
                'credit_totals':credit_totals,
                'from_date':self.from_date,
                'to_date':self.to_date,
                'invoice_status':self.invoice_status,
            }
        
        return dict_custom
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    