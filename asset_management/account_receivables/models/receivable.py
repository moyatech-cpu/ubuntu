# coding=utf-8
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.safe_eval import safe_eval
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

import logging

_logger = logging.getLogger(__name__)
# mapping invoice type to refund type
TYPE2REFUND = {
    'out_invoice': 'out_refund',        # Customer Invoice
    'in_invoice': 'in_refund',          # Vendor Bill
    'out_refund': 'out_invoice',        # Customer Credit Note
    'in_refund': 'in_invoice',          # Vendor Credit Note
}

class CreditorID(models.Model):
    """ Model to inherit/extend the voucher application """
    _name = 'creditor.id'
    _rec_name = 'creditor_id'
    
    creditor_id = fields.Char("Debtor ID") #sequence
    user_id = fields.Many2one('res.users','Related User')
    description = fields.Text("Description")
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        if values:
            values['creditor_id'] = self.env['ir.sequence'].next_by_code('creditor.id')
        record_obj = super(CreditorID, self).create(values)
        return record_obj

class POInvoice(models.Model):
    """ Model to inherit/extend the PO"""
    _inherit = 'account.invoice'
    
    unique_credit_no = fields.Char('Credit No') #sequence
    enquiry_id = fields.Many2one('inv.batch')
    last_enquiry_id = fields.Many2one('transactions.enquiry')
    batch_id = fields.Many2one('batch.entry')
    cust_batch_id = fields.Many2one('customer.batch.entry')
    creditor_id = fields.Many2one('creditor.id',string='Creditor ID')
    test = fields.Many2one('res.users')
    partial = fields.Float('Percentage')
    percentage = fields.Float('%',default=1.0)
    discount = fields.Float('Discount')
    sales_amount = fields.Monetary(string='Sales Amount')
    discount_amount = fields.Monetary(string='Discount Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    percentage_amount = fields.Monetary(string='% Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    posting_date = fields.Date("Date Posted")
    entries = fields.One2many('account.move.line','batch_id',related='move_id.line_ids',string="Journal Entries")
    line_description = fields.Text("Description")
    inv_identifier = fields.Char("ID")
    
    @api.multi
    def action_cr_note_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        
        #if to_open_invoices.filtered(lambda inv: inv.state != 'pending'):
        #    raise UserError(_("Invoice must be in draft state in order to validate it."))
        
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        to_open_invoices.invoice_validate()
        
        if self.type == 'out_refund':
            if self.move_id:
                number = str(self.move_id.name)
                self.move_id.name = number.replace("INV", "CRN")
        
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Credit note has been successfully moved to open status."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }
    
    @api.multi
    def action_cr_note_post(self):
        # lots of duplicate calls to action_invoice_paid, so we remove those already paid
        if self.filtered(lambda inv: inv.state != 'open'):
            raise UserError(_('Credit Note must be paid in open status to post it.'))
        
        self.write({'state': 'posted'})
        
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "Credit note has been successfully posted."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,        
            }
    
    
    def print_sale_journal(self):
        return self.env.ref('account_receivables.action_inv_sales_entry').report_action(self)

    @api.multi
    def action_rec_invoice_post(self):
        # lots of duplicate calls to action_invoice_paid, so we remove those already paid
        if self.filtered(lambda inv: inv.state != 'open'):
            raise UserError(_('Invoice must be paid in open status to post it.'))
        
        self.write({'state': 'posted'})
        self.posting_date = date.today()
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoice has been successfully posted."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,        
            }
    
    @api.multi
    def get_invoice_journal(self):
        system_time = datetime.now()
        create_date = self.create_date
        create_user = self.env.user.name
        batch_id = self.batch_id.batch_id
        posting_date = self.posting_date
        #comment = self.comment
        #transactions_actual = self.transactions_actual
        #transactions_control = self.transactions_control
        #batch_actual = self.batch_actual
        #batch_control = self.batch_control
        #state = self.invoice_status
        #approvalUser = self.approvalUser.name
        #approval_date = self.approval_date
        
        debit_totals = 0
        credit_totals = 0
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
        
        temp_ledger = []
        move_id = self.move_id
        if move_id:
            for line in move_id.line_ids:
                debit_totals = debit_totals+ line.debit
                credit_totals = credit_totals+ line.credit
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
                         'number': self.number, 
                         'date_invoice': self.date_invoice,
                         'due_date': self.date_due,
                         'parnter_id': self.partner_id.name,
                         'name': self.partner_id.name,
                         'sales_person': "",
                         'amount_total_signed': self.amount_total_signed,
                         #'write_off': "0.00",
                         'discount': self.discount * self.sales_amount,
                         'ledger_data':temp_ledger,
                         #'unapplied': invoice.amount_total_signed - (invoice.amount_total_signed * invoice.percentage),
        }
                       
        final_list.append(vdata)
        app_data = {
                         'type': self.number, 
                         'inv_name': self.number,
                         'date_inv': self.date_invoice,
                         'discount_amount': self.discount_amount,
                         'write_off_amount': "0.00",
                         'amount_applied': self.amount_total_signed,
        }
        applied_distribution_ids.append(app_data)
        total_invoices_amount = total_invoices_amount + self.amount_total_signed
        total_discounts = total_discounts+self.discount * self.sales_amount
        total_unapplied_amount = total_unapplied_amount+self.amount_total_signed - (self.amount_total_signed * self.percentage)
        total_applied_ = total_applied_+self.amount_total_signed
        dict_custom = {
                'system_time':system_time, 
                'create_user':create_user,
                'create_date':create_date,
                'batch_id':batch_id,
                'posting_date':posting_date,
                #'comment':comment,
                #'transactions_actual':transactions_actual,
                #'transactions_control':transactions_control,
                #'batch_actual':batch_actual,
                #'batch_control':batch_control,
                #'state':state,
                #'approval_date':approval_date,
                #'approvalUser':approvalUser,
                'invoice_status':self.state,
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
    
    '''@api.multi
    @api.depends('test')
    @api.onchange('test')
    def _populate_batch(self):
        records = self.env['inv.batch'].sudo().search([('customerID','=',self.partner_id.id)])
        for record in records:
            self.batch_id = record'''
    
    #Remove Pop ups
    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        
        #if to_open_invoices.filtered(lambda inv: inv.state != 'pending'):
        #    raise UserError(_("Invoice must be in draft state in order to validate it."))
        
        if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        to_open_invoices.invoice_validate()
        
        if self.type == 'out_refund':
            if self.move_id:
                number = str(self.move_id.name)
                self.move_id.name = number.replace("INV", "CRN")
        '''view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoice has been successfully moved to open status."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }'''
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        if values:
            values['unique_credit_no'] = self.env['ir.sequence'].next_by_code('account.invoice.receivable')
            #replace lines with defaul line
            
        record_obj = super(POInvoice, self).create(values)
        
        try:
            if record_obj.type == 'out_invoice':
                record_obj.inv_identifier = self.env['ir.sequence'].next_by_code('batch.invoice')
            elif record_obj.type == 'out_refund':
                record_obj.inv_identifier = self.env['ir.sequence'].next_by_code('credit.invoice')
        except:
            pass
            
        
        if record_obj.batch_id:
            products = self.env['product.product'].sudo().search([('name','=','Generic')])
            accounts = self.env['account.account'].sudo().search([('name','=','SALES')])
            _logger.info(products)
        
            default_lines = self.env['account.invoice.line'].create({ 'product_id': products.id,
                                                                 'name':'Deferred Income',
                                                                 'account_id': accounts.id,
                                                                 'price_unit':self.amount_total,
                                                                 'quantity':1})
        
            record_obj.invoice_line_ids = [(4,default_lines.id)]
                
        if not record_obj.date_invoice:
            record_obj.date_invoice = date.today()
    
        return record_obj
    
    @api.onchange('sales_amount')
    def _change_sale_total(self):
        self.percentage = 1.00
        products = self.env['product.product'].sudo().search([('name','=','Generic')])
        accounts = self.env['account.account'].sudo().search([('name','=','Account Receivable')])
        _logger.info(products)
        default_lines = self.env['account.invoice.line'].create({ 'product_id': products.id,
                                                                 'name':'Deferred Income',
                                                                 'account_id': accounts.id,
                                                                 'price_unit':self.amount_total,
                                                                 'quantity':1})
        
        self.invoice_line_ids = [(4,default_lines.id)]
    
    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type','discount','sales_amount','percentage','partial')
    def _compute_amount(self):
        round_curr = self.currency_id.round
        
        #self.invoice_line_ids = self.env['account.invoice.line'].search(['product_id','=',0])
        if self.sales_amount:
            if self.partial != 0:
                self.amount_untaxed = self.sales_amount #sum(line.price_subtotal for line in self.invoice_line_ids)
                self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
                self.amount_total = (self.amount_untaxed + self.amount_tax) * self.partial
                amount_total_company_signed = self.amount_total
                amount_untaxed_signed = self.amount_untaxed
                if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
                    currency_id = self.currency_id.with_context(date=self.date_invoice)
                    amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
                    amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
                sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
                self.amount_total_company_signed = amount_total_company_signed * sign
                self.amount_total_signed = self.amount_total * sign
                self.amount_untaxed_signed = amount_untaxed_signed * sign
            else :
                self.amount_untaxed = self.sales_amount # sum(line.price_subtotal for line in self.invoice_line_ids)
                self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
                self.amount_total = self.amount_untaxed + self.amount_tax
                self.amount_total = self.amount_total * self.percentage
            
                self.percentage_amount = self.sales_amount * self.percentage
                self.discount_amount = (self.sales_amount * self.percentage)*self.discount
            
                self.amount_total = self.amount_total - self.amount_total*self.discount
                amount_total_company_signed = self.amount_total
                amount_untaxed_signed = self.amount_untaxed
                if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
                    currency_id = self.currency_id.with_context(date=self.date_invoice)
                    amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
                    amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
                sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
                self.amount_total_company_signed = amount_total_company_signed * sign
                self.amount_total_signed = self.amount_total * sign
                self.amount_untaxed_signed = amount_untaxed_signed * sign
        else:
            if self.partial != 0:
                self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids) * self.partial
                self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
                self.amount_total = (self.amount_untaxed + self.amount_tax)
                amount_total_company_signed = self.amount_total
                amount_untaxed_signed = self.amount_untaxed
                if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
                    currency_id = self.currency_id.with_context(date=self.date_invoice)
                    amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
                    amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
                sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
                self.amount_total_company_signed = amount_total_company_signed * sign
                self.amount_total_signed = self.amount_total * sign
                self.amount_untaxed_signed = amount_untaxed_signed * sign
            else :
                self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
                self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
                self.amount_total = self.amount_untaxed + self.amount_tax
                self.amount_total = self.amount_total * self.percentage
            
                self.percentage_amount = self.sales_amount * self.percentage
                self.discount_amount = (self.sales_amount * self.percentage)*self.discount
            
                self.amount_total = self.amount_total - self.amount_total*self.discount
                amount_total_company_signed = self.amount_total
                amount_untaxed_signed = self.amount_untaxed
                if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
                    currency_id = self.currency_id.with_context(date=self.date_invoice)
                    amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
                    amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
                sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
                self.amount_total_company_signed = amount_total_company_signed * sign
                self.amount_total_signed = self.amount_total * sign
                self.amount_untaxed_signed = amount_untaxed_signed * sign
                
        
            
    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None,percentage=None):
        """ Prepare the dict of values to create the new credit note from the invoice.
            This method may be overridden to implement custom
            credit note generation (making sure to call super() to establish
            a clean extension chain).

            :param record invoice: invoice as credit note
            :param string date_invoice: credit note creation date from the wizard
            :param integer date: force date from the wizard
            :param string description: description of the credit note from the wizard
            :param integer journal_id: account.journal from the wizard
            :return: dict of value to create() the credit note
        """
        values = {}
        for field in self._get_refund_copy_fields():
            if invoice._fields[field].type == 'many2one':
                values[field] = invoice[field].id
            else:
                values[field] = invoice[field] or False

        values['invoice_line_ids'] = self._refund_cleanup_lines(invoice.invoice_line_ids)

        tax_lines = invoice.tax_line_ids
        values['tax_line_ids'] = self._refund_cleanup_lines(tax_lines)

        if journal_id:
            journal = self.env['account.journal'].browse(journal_id)
        elif invoice['type'] == 'in_invoice':
            journal = self.env['account.journal'].search([('type', '=', 'purchase')], limit=1)
        else:
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        values['journal_id'] = journal.id

        values['type'] = TYPE2REFUND[invoice['type']]
        values['date_invoice'] = date_invoice or fields.Date.context_today(invoice)
        values['state'] = 'draft'
        values['number'] = False
        values['origin'] = invoice.number
        values['payment_term_id'] = False
        values['refund_invoice_id'] = invoice.id
        values['partial'] = percentage

        if date:
            values['date'] = date
        if description:
            values['name'] = description
        return values

    
    @api.multi
    @api.returns('self')
    def refund(self, date_invoice=None, date=None, description=None, journal_id=None,percentage=None):
        new_invoices = self.browse()
        for invoice in self:
            # create the new invoice
            values = self._prepare_refund(invoice, date_invoice=date_invoice, date=date,
                                    description=description, journal_id=journal_id,percentage=percentage)
            refund_invoice = self.create(values)
            invoice_type = {'out_invoice': ('customer invoices credit note'),
                'in_invoice': ('vendor bill credit note')}
            message = _("This %s has been created from: <a href=# data-oe-model=account.invoice data-oe-id=%d>%s</a>") % (invoice_type[invoice.type], invoice.id, invoice.number)
            refund_invoice.message_post(body=message)
            new_invoices += refund_invoice
        return new_invoices
    
    @api.model
    def invoice_line_move_line_get(self):
        res = []
        for line in self.invoice_line_ids:
            if line.quantity==0:
                continue
            tax_ids = []
            for tax in line.invoice_line_tax_ids:
                tax_ids.append((4, tax.id, None))
                for child in tax.children_tax_ids:
                    if child.type_tax_use != 'none':
                        tax_ids.append((4, child.id, None))
            analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

            move_line_dict = {
                'invl_id': line.id,
                'type': 'src',
                'name': line.name.split('\n')[0][:64],
                'price_unit': 1,
                'quantity': 1,
                #'price_unit': line.price_unit,
                #'quantity': line.quantity,
                #'price': line.price_subtotal,
                'price': self.amount_total,
                'account_id': line.account_id.id,
                'product_id': line.product_id.id,
                'uom_id': line.uom_id.id,
                'account_analytic_id': line.account_analytic_id.id,
                'tax_ids': tax_ids,
                'invoice_id': self.id,
                'analytic_tag_ids': analytic_tag_ids
            }
            res.append(move_line_dict)
        return res
    
class Batch(models.Model):
    _name = 'inv.batch'
    _rec_name = 'batch_id'
    
    batch_id = fields.Char("Enquiry ID") #sequence
    #obsolete fields
    creditor_id = fields.Many2one('creditor.id',string='Creditor ID') #removed
    comment = fields.Text("Comment")
    
    date_filter = fields.Boolean("Date Filter")
    status_filter = fields.Boolean("Status Filter")
    
    customerID = fields.Many2one('res.partner',string='Customer ID')
    #customerID = fields.Many2one('res.partner',related='customerID.id',string='Name') #removed
    
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
    transactions = fields.One2many('account.invoice','enquiry_id',string="Transactions")
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        record_obj = super(Batch, self).create(values)
        records = self.env['inv.batch'].sudo().search([])
        string_x = "000"
        x = len(records)
        if x >= 10 and x < 100:
            string_x = "00" + str(x)
        elif x >= 100 and x < 1000:
            string_x = "0" + str(x)
        elif x >= 1000:
            string_x = str(x)
        else:
            string_x = string_x + str(x)
        record_obj.batch_id = str(record_obj.customerID.name) + " " + string_x
        
        return record_obj
    
    @api.multi
    @api.depends('customerID','invoice_status','to_date')
    @api.onchange('customerID','invoice_status','to_date')
    def compute_voucher_value(self):
        if self.date_filter:
            for rec in self:
                result = self.env['account.invoice'].search([('user_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date)])
                rec['transactions'] = result
                for inv in result:
                    inv.enquiry_id = self.id 
        elif self.date_filter and self.status_filter:
            for rec in self:
                result = self.env['account.invoice'].search([('state','=',self.invoice_status),('user_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date)])
                rec['transactions'] = result
                for inv in result:
                    inv.enquiry_id = self.id
        elif self.status_filter:
            for rec in self:
                result = self.env['account.invoice'].search([('state','=',self.invoice_status),('user_id','=',self.customerID.id)])
                rec['transactions'] = result
                for inv in result:
                    inv.enquiry_id = self.id 
        else:
            for rec in self:
                result = self.env['account.invoice'].search([('user_id','=',self.customerID.id)])
                rec['transactions'] = result
                for inv in result:
                    inv.enquiry_id = self.id 
    
    @api.multi
    @api.depends('customerID','invoice_status','to_date')
    @api.onchange('customerID','invoice_status','to_date')
    def compute_voucher_value(self):
        if self.date_filter:
            for rec in self:
                result = self.env['account.invoice'].search([('partner_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date)])
                rec['transactions'] = result
                #for inv in result:
                #    inv.enquiry_id = self.id 
        elif self.status_filter and self.date_filter:
            for rec in self:
                result = self.env['account.invoice'].search([('state','=',self.invoice_status),('partner_id','=',self.customerID.id),('date_invoice','>=',self.from_date),('date_invoice','<=',self.to_date)])
                rec['transactions'] = result
                #for inv in result:
                #    inv.enquiry_id = self.id 
        elif self.status_filter:
            for rec in self:
                result = self.env['account.invoice'].search([('state','=',self.invoice_status),('partner_id','=',self.customerID.id)])
                rec['transactions'] = result
                #for inv in result:
                #    inv.enquiry_id = self.id 
        else:
            for rec in self:
                result = self.env['account.invoice'].search([('partner_id','=',self.customerID.id)])
                rec['transactions'] = result
                #for inv in result:
                #    inv.enquiry_id = self.id 
                   
                    
class AccountInvoiceRefund(models.TransientModel):
    """Credit Notes"""

    _inherit = "account.invoice.refund"

    partial = fields.Float(string='Percentage')
    
    @api.multi
    def compute_refund(self, mode='refund'):
        inv_obj = self.env['account.invoice']
        inv_tax_obj = self.env['account.invoice.tax']
        inv_line_obj = self.env['account.invoice.line']
        context = dict(self._context or {})
        xml_id = False

        for form in self:
            created_inv = []
            date = False
            description = False
            for inv in inv_obj.browse(context.get('active_ids')):
                if inv.state in ['draft', 'cancel']:
                    raise UserError(_('Cannot create credit note for the draft/cancelled invoice.'))
                if inv.reconciled and mode in ('cancel', 'modify'):
                    raise UserError(_('Cannot create a credit note for the invoice which is already reconciled, invoice should be unreconciled first, then only you can add credit note for this invoice.'))

                date = form.date or False
                description = form.description or inv.name
                if self.partial != 0:
                    refund = inv.refund(form.date_invoice, date, description, inv.journal_id.id,self.partial)
                else :
                    refund = inv.refund(form.date_invoice, date, description, inv.journal_id.id)
                
                created_inv.append(refund.id)
                if mode in ('cancel', 'modify'):
                    movelines = inv.move_id.line_ids
                    to_reconcile_ids = {}
                    to_reconcile_lines = self.env['account.move.line']
                    for line in movelines:
                        if line.account_id.id == inv.account_id.id:
                            to_reconcile_lines += line
                            to_reconcile_ids.setdefault(line.account_id.id, []).append(line.id)
                        if line.reconciled:
                            line.remove_move_reconcile()
                    refund.action_invoice_open()
                    for tmpline in refund.move_id.line_ids:
                        if tmpline.account_id.id == inv.account_id.id:
                            to_reconcile_lines += tmpline
                    to_reconcile_lines.filtered(lambda l: l.reconciled == False).reconcile()
                    if mode == 'modify':
                        invoice = inv.read(inv_obj._get_refund_modify_read_fields())
                        invoice = invoice[0]
                        del invoice['id']
                        invoice_lines = inv_line_obj.browse(invoice['invoice_line_ids'])
                        invoice_lines = inv_obj.with_context(mode='modify')._refund_cleanup_lines(invoice_lines)
                        tax_lines = inv_tax_obj.browse(invoice['tax_line_ids'])
                        tax_lines = inv_obj._refund_cleanup_lines(tax_lines)
                        invoice.update({
                            'type': inv.type,
                            'date_invoice': form.date_invoice,
                            'state': 'draft',
                            'number': False,
                            'invoice_line_ids': invoice_lines,
                            'tax_line_ids': tax_lines,
                            'date': date,
                            'origin': inv.origin,
                            'fiscal_position_id': inv.fiscal_position_id.id,
                        })
                        for field in inv_obj._get_refund_common_fields():
                            if inv_obj._fields[field].type == 'many2one':
                                invoice[field] = invoice[field] and invoice[field][0]
                            else:
                                invoice[field] = invoice[field] or False
                        inv_refund = inv_obj.create(invoice)
                        if inv_refund.payment_term_id.id:
                            inv_refund._onchange_payment_term_date_invoice()
                        created_inv.append(inv_refund.id)
                xml_id = inv.type == 'out_invoice' and 'action_invoice_out_refund' or \
                         inv.type == 'out_refund' and 'action_invoice_tree1' or \
                         inv.type == 'in_invoice' and 'action_invoice_in_refund' or \
                         inv.type == 'in_refund' and 'action_invoice_tree2'
                # Put the reason in the chatter
                subject = _("Credit Note")
                body = description
                refund.message_post(body=body, subject=subject)
        if xml_id:
            result = self.env.ref('account.%s' % (xml_id)).read()[0]
            invoice_domain = safe_eval(result['domain'])
            invoice_domain.append(('id', 'in', created_inv))
            result['domain'] = invoice_domain
            return result
        return True

    @api.multi
    def invoice_refund(self):
        data_refund = self.read(['filter_refund'])[0]['filter_refund']
        return self.compute_refund(data_refund)

class Journal(models.Model):
    _inherit = 'account.move.line'
    
    batch_id = fields.Many2one('batch.entry')

class Journal(models.Model):
    _inherit = 'account.move'
    
    batch_id = fields.Many2one('batch.entry')

class BatchEntry(models.Model):
    _name = 'batch.entry'
    _rec_name = 'batch_id'
    
    batch_type = fields.Selection([
            ('sale','Sales'),
            ('credit','Credit Notes'),
            ('customer','Customer Batch')],
        default='sale', string="Type")
    batch_id = fields.Char("Batch ID") #sequence
    comment = fields.Text("Description")
    origin = fields.Selection([
            ('transaction','Transaction Entry'),
        ], string='Origin')
    posting_date = fields.Date('Posting Date')
    date_due = fields.Date('Due Date')
    
    #Customer Batch Fields
    source = fields.Many2one('res.partner')
    
    ##PR MOHAPI 07/05/2022
    #customer_id = fields.Char('Customer ID',related='source.customer_id')
    customer_id = fields.Char('Customer ID')

    account_id = fields.Many2one('account.account',related="source.property_account_receivable_id")
    trade_discount = fields.Float('Trade Discount',related="source.trade_discount")
    
    
    #account_id = fields.Many2one('account.account')
    #checkbookID = fields.Many2one('customer.account',related='account_id.checkbook_id',string="Checkbook ID")
    
    
    last_posting_date = fields.Date('Last Date Posted')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    
    journal_ids = fields.One2many('account.move', 'batch_id',string="Journal Entries")
    journal_line_ids = fields.One2many('account.move.line','batch_id',string="Journal Entries")
    
    #controls
    transactions_control = fields.Integer("Trn Control")
    batch_control = fields.Monetary('Batch Total Control')
    
    #actual 
    
    transactions_actual = fields.Integer("Trn Actual",compute="compute_voucher_value")
    batch_actual = fields.Monetary('Batch Total Actual',compute="compute_voucher_value")
    control = fields.Boolean("Control")
    invoice_status = fields.Selection([
            ('draft','Draft'),
            ('review','Review'),
            ('approve','Approved'),
            ('reject','Rejected'),
            ('posted', 'Posted'),
            #('paid', 'Paid'),
            ('cancel', 'Cancelled'),
            ('reviewed','Reviewed')],
        default='draft', string="Batch State")
    
    approvalUser = fields.Many2one('res.users', string='Approved by')
    review_date = fields.Date("Review Date")
    last_update_user = fields.Many2one('res.users', string='Last updated by')
    review_user = fields.Many2one('res.users', string='Reviewed by')
    approval_date = fields.Date('Approval Date')
    
    transactions = fields.One2many('account.invoice', 'batch_id',string="Transactions")
    
    '''@api.multi
    @api.depends('source')
    @api.onchange('source')
    def customerID_select(self):
        customer_id = self.env['res.partner'].sudo().search([('id','=',self.source.id)])
        for each in customer_id:
            self.customer_id = each.id'''
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        if values:
            if values['batch_type'] == 'sale':
                values['batch_id'] = self.env['ir.sequence'].next_by_code('batch.entry')
            if values['batch_type'] == 'credit':
                values['batch_id'] = self.env['ir.sequence'].next_by_code('credit.entry')
                
        record_obj = super(BatchEntry, self).create(values)
        
        if record_obj.batch_type == 'customer':
            record_obj.batch_id = record_obj.source.name
            
        return record_obj
    
    @api.multi
    def write(self, values):
        record_obj = super(BatchEntry, self).write(values)
        '''inv_counter = 1
        for rec in self.transactions:
            if not rec.inv_identifier:
                string_number = str(inv_counter)
                rec.inv_identifier = "SLS"+string_number.zfill(7)
            inv_counter += 1'''
                
        return self.env.ref('account_receivables.action_report_batch_entry').report_action(self)
    
        return record_obj
    @api.multi
    @api.depends('transactions')
    @api.onchange('transactions')
    def compute_voucher_value(self):
        self.last_update_user = self.env.user.id
        sum = 0.0
        for record in self:
            for inv in record.transactions:
                inv.batch_id = record.id
                if record.batch_type == 'customer':
                    if not inv.partner_id:
                        inv.partner_id = record.source
                        inv.discount = record.trade_discount
                sum = sum + inv.amount_total
                
        for record in self:                    
            record.batch_actual = sum
            record.transactions_actual = len(record.transactions)
            if record.transactions_actual >= record.transactions_control or record.batch_actual >= record.batch_control:
                record.control = True
            else:
                record.control = False
                
            res = {}
            if record.transactions_actual > record.transactions_control:
                '''i = 1
                dictt = []
                for inv in self.transactions:
                    try:
                        if not (i == self.transactions_actual):
                            dictt.append(inv.id)
                    except:
                        pass
                    i = i+1
                self.transactions = [(6, 0, dictt)]
                '''
                res = {'warning': {
                    'title': _('Warning'),
                    'message': _('Actual Transactions limit reached transactions control')
                }}
                if res:
                    return res
                
            if record.batch_actual > record.batch_control:
                '''i = 1
                dictt = []
                for inv in self.transactions:
                    try:
                        if not(i == self.transactions_actual):
                            dictt.append(inv.id)
                    except:
                        pass
                    i = i+1
                self.transactions = [(6, 0, dictt)]
                '''
                res = {'warning': {
                    'title': _('Warning'),
                    'message': _('Actual Batch Total limit reached Batch Control')
                }}
                if res:
                    return res
        
    @api.multi
    def set_review(self):
        res = {}
        if self.transactions_actual > self.transactions_control:
            res = {'Warning': {
                'title': _('Warning'),
                'message': _('Actual Transactions limit reached transactions control')
            }}
            if res:
                return res
            
        if self.batch_actual > self.batch_control:
            res = {'warning': {
                'title': _('Warning'),
                'message': _('Actual Batch Total limit reached Batch Control')
            }}
            if res:
                return res
        
        self.invoice_status = 'review'
        
        #populate journal entries
        journals = []
        jids = []
        for inv in self.transactions:
            inv.date_due = self.date_due
            inv.action_invoice_open()
            if inv.move_id:
                journals.append(inv.move_id.id)
        
        self.journal_ids = [(6, 0, journals)]
        
        if self.journal_ids:       
            for inv in self.journal_ids:
                if inv.line_ids:
                    for line in inv.line_ids:
                        jids.append(line.id)
            self.journal_line_ids = [(6, 0, jids)]
        
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoices have been successfully moved to open status."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }
        
    @api.multi
    def set_approve_reject(self):
        #self.approvalUser = self.env.user.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Review Batch',
            'res_model': 'batch.review',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
    
    @api.multi
    def review_final(self):
        #self.approvalUser = self.env.user.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Review',
            'res_model': 'batch.review.final',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.multi
    def set_post(self):
        for inv in self.transactions:
            inv.state = 'paid'
        
        self.invoice_status = 'posted'
        self.last_posting_date = date.today()
        if not self.posting_date:
            self.posting_date = date.today()
        return self.env.ref('account_receivables.action_general_post_journal_entry').report_action(self)
        #return self.env.ref('account_receivables.action_report_batch_entry').report_action(self)
    
    def sales_journal(self):
        return self.env.ref('account_receivables.action_report_batch_entry').report_action(self)
    
    @api.multi
    def get_batch_entries(self):
        system_time = datetime.now()
        create_date = self.create_date
        create_user = self.env.user.name
        batch_id = self.batch_id
        posting_date = self.posting_date
        comment = self.comment
        transactions_actual = self.transactions_actual
        transactions_control = self.transactions_control
        batch_actual = self.batch_actual
        batch_control = self.batch_control
        state = self.invoice_status
        approvalUser = self.approvalUser.name
        approval_date = self.approval_date
        
        debit_totals = 0
        credit_totals = 0
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
                        temp_ledger.append(ledger)
                    
                vdata = {
                         'number': invoice.number, 
                         'date_invoice': invoice.date_invoice,
                         'due_date': invoice.date_due,
                         'parnter_id': invoice.partner_id.name,
                         'name': invoice.partner_id.name,
                         'sales_person': "",
                         'amount_total_signed': invoice.amount_total_signed,
                         #'write_off': "0.00",
                         'discount': invoice.discount * invoice.sales_amount,
                         'ledger_data':temp_ledger,
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
        
        new_state = ""
        if self.approvalUser:
            new_state = "YES"
        else:
            new_state = "NO"
        
        dict_custom = {
                'system_time':system_time, 
                'create_user':create_user,
                'create_date':create_date,
                'batch_id':batch_id,
                'posting_date':posting_date,
                'comment':comment,
                'transactions_actual':transactions_actual,
                'transactions_control':transactions_control,
                'batch_actual':batch_actual,
                'batch_control':batch_control,
                'state':new_state,
                'approval_date':approval_date,
                'approvalUser':approvalUser,
                'invoice_status':self.invoice_status,
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
        
    '''@api.multi
    def set_paid(self):
        for inv in self.transactions:
            inv.state = 'paid'
        
        self.invoice_status = 'paid' '''

    @api.multi
    def set_cancel(self):
        self.invoice_status = 'cancel'

    def general_post(self):
        return self.env.ref('account_receivables.action_general_post_journal_entry').report_action(self)
    
    @api.multi
    def get_general_post_journal(self):
        system_time = datetime.now()
        create_date = self.create_date
        create_user = self.env.user.name
        batch_id = self.batch_id
        posting_date = self.posting_date
        comment = self.comment
        transactions_actual = self.transactions_actual
        transactions_control = self.transactions_control
        batch_actual = self.batch_actual
        batch_control = self.batch_control
        state = self.invoice_status
        approvalUser = self.approvalUser.name
        approval_date = self.approval_date
        total_entries = len(self.journal_ids)
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
        for invoice in self.journal_ids:
            temp_ledger = []
            debit_totals = 0
            credit_totals = 0
            distributions = 0
            for line in invoice.line_ids:
                debit_totals = debit_totals + line.debit
                credit_totals = credit_totals+ line.credit
                distributions= distributions +1
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
                         'jid': invoice.id, 
                         'journal_id': invoice.journal_id.name,
                         'date': invoice.date,
                         'reverse_date': "",    #invoice.reverse_date,
                         'name': invoice.name,
                         'reference': invoice.ref,
                         'audit_trail_code': "",#invoice.audit_trail_code,
                         #'write_off': "0.00",
                         'rev_audit_trail_code': "", #invoice.discount * invoice.sales_amount,
                         'ledger_data':temp_ledger,
                         'debit_totals':debit_totals,
                         'credit_totals':credit_totals,
                         'total_distributions':distributions,
                         #'unapplied': invoice.amount_total_signed - (invoice.amount_total_signed * invoice.percentage),
            }
                       
            final_list.append(vdata)
            new_state = ""
            if self.approvalUser:
                new_state = "YES"
            else:
                new_state = "NO"
            
        dict_custom = {
                'system_time':system_time, 
                'create_user':create_user,
                'create_date':create_date,
                'batch_id':batch_id,
                'posting_date':posting_date,
                'comment':comment,
                'transactions_actual':transactions_actual,
                'transactions_control':transactions_control,
                'batch_actual':batch_actual,
                'batch_control':batch_control,
                'state':new_state,
                'approval_date':approval_date,
                'approvalUser':approvalUser,
                'invoice_status':self.invoice_status,
                'invoice_ids':final_list,
                'ledger_ids':ledger_data,
                #'applied_distribution_ids':applied_distribution_ids,
                #'total_invoices_amount':total_invoices_amount,
                #'total_discounts':total_discounts,
                #'total_unapplied_amount':total_unapplied_amount,
                #'total_write_off':total_write_off,
                'total_entries': str(total_entries),
                #'discount_total':total_discounts,
                #'write_off_total':total_write_off,
                #'total_applied':total_applied_,
                #'debit_totals':debit_totals,
                #'credit_totals':credit_totals,
            }
        
        return dict_custom

class CashReceipt(models.Model):
    _inherit = 'account.payment'
    
    def print_cash_receipt(self):
        return self.env.ref('account_receivables.action_cash_receipt_journal').report_action(self)
    
    @api.multi
    def get_cash_receipt_journal(self):
        system_time = datetime.now()                #
        doc_date = datetime.now()                   #
        create_user = self.env.user.name            #
        customer_id = self.partner_id.name
        
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
        invoice = self
        vdata = {
                    'number': invoice.name, 
                    'date_invoice': invoice.create_date,
                    'due_date': invoice.payment_date,
                    'customer_id': customer_id.id,
                    'name': customer_id.name,
                    'comment': "N/A",
                    'amount_total_signed': invoice.amount,
                         'write_off': "0.00",
                         'discount': "0.00",
                         'unapplied': "0.00",
        }
        final_list.append(vdata)
        if self.move_line_ids:
            for line in self.move_line_ids:
                debit_totals = debit_totals+ line.debit
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
                         'type': "RECV", 
                         'inv_name': invoice.name,
                         'date_inv': invoice.payment_date,
                         'discount_amount': "0.00",
                         'write_off_amount': "0.00",
                         'amount_applied': invoice.amount,
        }
        applied_distribution_ids.append(app_data)
        total_invoices_amount = total_invoices_amount + invoice.amount
        
        total_applied_ = total_applied_+invoice.amount
        dict_custom = {
                'system_time':system_time, 
                'doc_date':doc_date,
                'create_user':create_user,
                'customer_id':customer_id,
                #'from_date':self.from_date,
                #'to_date':self.to_date,
                #'invoice_status':self.invoice_status,
                'name':self.partner_id.name,
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
    
    
    
    