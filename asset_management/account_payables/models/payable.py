# coding=utf-8
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.safe_eval import safe_eval
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)
# mapping invoice type to refund type
TYPE2REFUND = {
    'out_invoice': 'out_refund',        # Customer Invoice
    'in_invoice': 'in_refund',          # Vendor Bill
    'out_refund': 'out_invoice',        # Customer Credit Note
    'in_refund': 'in_invoice',          # Vendor Credit Note
}

class SPEnhance(models.Model):
    _inherit = 'res.partner'
    
    creditor_id = fields.Char('Creditor ID')
    
class PinvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    
    pog_number = fields.Char('PO Number')
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    pog_number = fields.Char('PO Number',related="order_id.name")

class PinvoiceLine(models.Model):
    """ Override Pinvoice_line to add the link to the purchase order line it is related to"""
    _inherit = 'account.invoice.line'

    purchase_line_id = fields.Many2one('purchase.order.line', 'Purchase Order Line', ondelete='set null', index=True, readonly=True)
    purchase_id = fields.Many2many('purchase.order', 'rel_purchase_orders_supplier_lines','number','name', string='Purchase Order', store=True, readonly=True,
        help='Associated Purchase Order. Filled in automatically when a PO is chosen on the vendor bill.')

class Pinvoice(models.Model):
    """ Model to inherit/extend the PO"""
    _inherit = 'account.invoice'
    
    invoice_number_entry = fields.Char('Invoice Number')
    #invoice for payables fields
    invoice_idetifier = fields.Boolean('Is Batch')
    creditor_id = fields.Char(related="partner_id.creditor_id")
    purchase_id = fields.Many2many('purchase.order','rel_purchase_orders_supplier','number','name',        
        string='Add Purchase Order',
        readonly=True, states={'draft': [('readonly', False)]},
        help='Encoding help. When selected, the associated purchase order lines are added to the vendor bill. Several PO can be selected.'
    )
    receipt_num = fields.Char('Receipt Number')
    ivoice_item = fields.Char("Item")
    
    def print_invoice_document(self):
        return self.env.ref('account_payables.action_invoice_pdf').report_action(self)
    
    @api.onchange('state', 'partner_id', 'invoice_line_ids')
    def _onchange_allowed_purchase_ids(self):
        '''
        The purpose of the method is to define a domain for the available
        purchase orders.
        '''
        result = {}

        # A PO can be selected only if at least one PO line is not already in the invoice
        purchase_line_ids = self.invoice_line_ids.mapped('purchase_line_id')
        purchase_ids = self.invoice_line_ids.mapped('purchase_id').filtered(lambda r: r.order_line <= purchase_line_ids)

        result['domain'] = {'purchase_id': [
            ('invoice_status', '=', 'to invoice'),
            ('partner_id', 'child_of', self.partner_id.id),
            ('id', 'not in', purchase_ids.ids),
            ]}
        return result

    def _prepare_invoice_line_from_po_line(self, line):
        if line.product_id.purchase_method == 'purchase':
            qty = line.product_qty - line.qty_invoiced
        else:
            qty = line.qty_received - line.qty_invoiced
        if float_compare(qty, 0.0, precision_rounding=line.product_uom.rounding) <= 0:
            qty = 0.0
        taxes = line.taxes_id
        invoice_line_tax_ids = line.order_id.fiscal_position_id.map_tax(taxes)
        invoice_line = self.env['account.invoice.line']
        data = {
            'purchase_line_id': line.id,
            'name': line.order_id.name+': '+line.name,
            'origin': line.order_id.origin,
            'uom_id': line.product_uom.id,
            'product_id': line.product_id.id,
            'account_id': invoice_line.with_context({'journal_id': self.journal_id.id, 'type': 'in_invoice'})._default_account(),
            'price_unit': line.order_id.currency_id.with_context(date=self.date_invoice).compute(line.price_unit, self.currency_id, round=False),
            'quantity': qty,
            'discount': 0.0,
            'account_analytic_id': line.account_analytic_id.id,
            'analytic_tag_ids': line.analytic_tag_ids.ids,
            'invoice_line_tax_ids': invoice_line_tax_ids.ids,
            'pog_number':line.pog_number,
        }
        account = invoice_line.get_invoice_line_account('in_invoice', line.product_id, line.order_id.fiscal_position_id, self.env.user.company_id)
        if account:
            data['account_id'] = account.id
        return data

    def _onchange_product_id(self):
        domain = super(Pinvoice, self)._onchange_product_id()
        for rec in self.purchase_id:
            if self.purchase_id:
                # Use the purchase uom by default
                self.uom_id = self.product_id.uom_po_id
        return domain

    # Load all unsold PO lines
    @api.onchange('purchase_id')
    def purchase_order_change(self):
        if not self.purchase_id:
            return {}
        if not self.partner_id:
            for rec in self.purchase_id:
                self.partner_id = rec.partner_id.id

        new_lines = self.env['account.invoice.line']
        for rec in self.purchase_id:
            for line in rec.order_line - self.invoice_line_ids.mapped('purchase_line_id'):
                data = self._prepare_invoice_line_from_po_line(line)
                new_line = new_lines.new(data)
                new_line._set_additional_fields(self)
                new_lines += new_line
            self.invoice_line_ids += new_lines
            self.payment_term_id = rec.payment_term_id
            
        self.env.context = dict(self.env.context, from_purchase_order_change=True)
        return {}

    def _prepare_invoice_line_from_voucher(self, line):
        
        invoice_line = self.env['account.invoice.line']
        
        data = {
            'purchase_line_id': line.id,
            'name': line.serial_number,
            'origin': 'Application',
            'product_id': line.x_recommended_service.x_product_id.id,
            'account_id': 1779,
            'price_unit': line.x_voucher_value,
            'quantity': 1,
            'discount': 0.0,
            'account_analytic_id': 54,
            'invoice_line_tax_ids': line.x_recommended_service.x_product_id.supplier_taxes_id
        }
        
        return data
    
    # Load service lines from Voucher object
    @api.onchange('x_voucher_id')
    def voucher_link_change(self):
        if not self.x_voucher_id:
            return {}
        if not self.partner_id:
            self.partner_id = self.x_voucher_id.x_service_provider.id

        self.reference = self.x_voucher_id.serial_number
        
        new_lines = self.env['account.invoice.line']
        
        data = self._prepare_invoice_line_from_voucher(self.x_voucher_id)
        
        new_line = new_lines.new(data)
        new_line._set_additional_fields(self)
        new_lines += new_line

        self.invoice_line_ids += new_lines
        self.payment_term_id = self.purchase_id.payment_term_id
        #self.env.context = dict(self.env.context, from_purchase_order_change=True)

        return {}
    
    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        if self.currency_id:
            for rec in self.purchase_id:
                for line in self.invoice_line_ids.filtered(lambda r: r.purchase_line_id):
                    line.price_unit = line.rec.currency_id.with_context(date=self.date_invoice).compute(line.purchase_line_id.price_unit, self.currency_id, round=False)

    @api.onchange('invoice_line_ids')
    def _onchange_origin(self):
        purchase_ids = self.invoice_line_ids.mapped('purchase_id')
        for rec in purchase_ids:
            if rec:
                self.origin = ', '.join(purchase_ids.mapped('name'))

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        payment_term_id = self.env.context.get('from_purchase_order_change') and self.payment_term_id or False
        res = super(Pinvoice, self)._onchange_partner_id()
        if payment_term_id:
            self.payment_term_id = payment_term_id
        if not self.env.context.get('default_journal_id') and self.partner_id and self.currency_id and\
                self.type in ['in_invoice', 'in_refund'] and\
                self.currency_id != self.partner_id.property_purchase_currency_id:
            journal_domain = [
                ('type', '=', 'purchase'),
                ('company_id', '=', self.company_id.id),
                ('currency_id', '=', self.partner_id.property_purchase_currency_id.id),
            ]
            default_journal_id = self.env['account.journal'].search(journal_domain, limit=1)
            if default_journal_id:
                self.journal_id = default_journal_id
        return res

    @api.model
    def invoice_line_move_line_get(self):
        res = super(Pinvoice, self).invoice_line_move_line_get()

        if self.env.user.company_id.anglo_saxon_accounting:
            if self.type in ['in_invoice', 'in_refund']:
                for i_line in self.invoice_line_ids:
                    res.extend(self._anglo_saxon_purchase_move_lines(i_line, res))
        return res
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        '''if values:
            values['unique_credit_no'] = self.env['ir.sequence'].next_by_code('account.invoice.receivable')
        '''
        if values:
            values['receipt_num'] = self.env['ir.sequence'].next_by_code('receipt.number')
            #replace lines with defaul line
            
        record_obj = super(Pinvoice, self).create(values)
        
        try:
            if record_obj.type == 'out_invoice':
                record_obj.inv_identifier = self.env['ir.sequence'].next_by_code('batch.invoice')
            elif record_obj.type == 'out_refund':
                record_obj.inv_identifier = self.env['ir.sequence'].next_by_code('credit.invoice')
            '''elif record_obj.type == 'in_invoice':
                record_obj.inv_identifier = self.env['ir.sequence'].next_by_code('pur.batch.invoice')
            elif record_obj.type == 'in_refund':
                record_obj.inv_identifier = self.env['ir.sequence'].next_by_code('debit.invoice')'''
        except:
            pass
            
        #{'default_type': 'in_invoice', 'type': 'in_invoice', 'journal_type': 'purchase'}
        #if record_obj.invoice_idetifier:
        if record_obj.type == 'out_invoice' or record_obj.type == 'out_refund':
            products = self.env['product.product'].sudo().search([('name','=','Generic')])
            accounts = self.env['account.account'].sudo().search([('name','=','Sales Account')])
            if not accounts:
                type = self.env['account.account.type'].sudo().search([('name','=','Income')])
                accounts = self.env['account.account'].create({'code':'000-000',
                                                               'name':'Customer Sales',
                                                               'user_type_id':type.id,
                                                                })
            _logger.info(products)
        
            default_lines = self.env['account.invoice.line'].create({ 'product_id': products.id,
                                                                 'name':'Deferred Income',
                                                                 'account_id': accounts.id,
                                                                 'price_unit':self.amount_total,
                                                                 'quantity':1})
        elif record_obj.type == 'in_invoice' or record_obj.type == 'in_refund':
            products = self.env['product.product'].sudo().search([('name','=','Generic')])
            accounts = self.env['account.account'].sudo().search([('name','=','Purchase Accounts')])
            if not accounts:
                type = self.env['account.account.type'].sudo().search([('name','=','Expense')])
                accounts = self.env['account.account'].create({'code':'111-111',
                                                               'name':'Vendor Payments',
                                                               'user_type_id':type.id
                                                                })
            _logger.info(products)
        
            default_lines = self.env['account.invoice.line'].create({ 'product_id': products.id,
                                                                 'name':'VENDOR PAYMENT',
                                                                 'account_id': accounts.id,
                                                                 'price_unit':self.amount_total,
                                                                 'quantity':1})
        
            record_obj.invoice_line_ids = [(4,default_lines.id)]
                
        if not record_obj.date_invoice:
            record_obj.date_invoice = date.today()
    
        return record_obj

class Batch(models.Model):
    _inherit = 'inv.batch'
    
    creditor_id = fields.Char('Creditor ID',related='customerID.creditor_id')
    
    batch_type = fields.Selection([
            ('sale','Sales'),
            ('credit','Credit Notes'),
            ('customer','Customer Batch'),('return','Returns Batch'),('pay','Payable Batch')],
        default='sale', string="Type")
    
class BatchEntry(models.Model):
    _inherit = 'batch.entry'
    
    batch_type = fields.Selection([
            ('sale','Sales'),
            ('credit','Credit Notes'),
            ('customer','Customer Batch'),('return','Returns Batch'),('pay','Payable Batch')],
        default='sale', string="Type")
    doc_number = fields.Char("Doc Number")
    date = fields.Date("Document Date")
    creditor_id = fields.Char(related="source.creditor_id")
    apply_controls = fields.Boolean("Transaction Control")
    receipt_num = fields.Char('Receipt Number')
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term',
        readonly=True, states={'draft': [('readonly', False)]},
        help="If you use payment terms, the due date will be computed automatically at the generation "
             "of accounting entries. If you keep the payment terms and the due date empty, it means direct payment. "
             "The payment terms may compute several due dates, for example 50% now, 50% in one month.")
    total_amount = fields.Monetary("Total Amount")
    batch_ref = fields.Char("Batch ID")
    audit_trail_code_ref = fields.Char("Batch ID")
    voucher_number = fields.Char('Voucher No.')
    transactions = fields.One2many('account.invoice','batch_id',string="Transactions")
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        '''if values:
            if values['batch_type'] == 'sale':
                values['batch_id'] = self.env['ir.sequence'].next_by_code('batch.entry')
            if values['batch_type'] == 'credit':
                values['batch_id'] = self.env['ir.sequence'].next_by_code('credit.entry')
            if values['batch_type'] == 'return':
                values['batch_id'] = self.env['ir.sequence'].next_by_code('batch.entry')
            if values['batch_type'] == 'pay':
                values['batch_id'] = self.env['ir.sequence'].next_by_code('pay.batch.entry')'''
        if values:
            values['receipt_num'] = self.env['ir.sequence'].next_by_code('receipt.batch.number')
            
        record_obj = super(BatchEntry, self).create(values)
        
        '''if record_obj.batch_type == 'customer':
            record_obj.batch_id = record_obj.source.name'''
            
        return record_obj
    
    @api.multi
    @api.depends('source')
    @api.onchange('source')
    def populate_po_invoice(self):
        for batch in self:
            invoices = []
            invoices_detail = []
            creditors_po = self.env['purchase.order'].sudo().search([('partner_id','=',self.source.id)])
            #create invoices per PO
            for po in creditors_po:
                accounts = self.env['account.account'].sudo().search([('code','like','000-000-000-9100')])
                account_id = self.env['account.account']
                journal_id = self.env['account.journal']
                for acc in accounts:
                    account_id = acc
                journals = self.env['account.journal'].sudo().search([('name','=','Vendor Invoices')])
                for jn in journals:
                    journal_id = jn
                item_ordered = ''
                for order_line in po['order_line']:
                    item_ordered = order_line.name
                
                new_lines = self.env['account.invoice.line']
                
                    
                invoice_id = self.env['account.invoice'].create({
                    'invoice_number_entry':po['name'],
                    'name' : po['name'],
                    'number': po['name'],
                    'date_invoice' : batch['date'],
                    'partner_id': batch['source']['id'],
                    'user_id': self.env.uid,
                    'type':'in_invoice',
                    #'ivoice_item': item_ordered,
                    'account_id':account_id.id,
                    'journal_id':journal_id.id
                    })
                for line in po['order_line']:
                    self.env['account.invoice.line'].create({
                            'invoice_id' : invoice_id.id,
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'account_id': journal_id.default_debit_account_id.id,
                            'price_unit': line.price_unit,
                            'quantity': line.product_qty,
                            'discount': 0.0,
                        })
                invoices_detail.append(invoice_id)
                invoices.append(invoice_id.id)
            for inv in invoices_detail:
                _logger.info("--> Partner: "+str(inv.partner_id.id)+ " PO:"+str(inv.number))
            
            batch['transactions'] = [(6,0,invoices)]
        
            
    def post_journal(self):
        for inv in self.transactions:
            inv.date_due = self.date_due
            inv.action_invoice_open()
            if inv.move_id:
                journals.append(inv.move_id.id)
        batch_ref = self.env['ir.sequence'].next_by_code('audit.trail.code')
        audit_trail_code_ref = self.env['ir.sequence'].next_by_code('audit.trail.code')
        voucher_number = self.env['ir.sequence'].next_by_code('voucher.number')
        #self.journal_ids = [(6, 0, journals)]
        return self.env.ref('account_payables.action_print_posting_journal').report_action(self)
    
    @api.multi
    @api.depends('transactions')
    @api.onchange('transactions')
    def compute_batch_value(self):
        self.last_update_user = self.env.user.id
        sum = 0.0
        for record in self:
            for inv in record.transactions:
                sum = sum + inv.amount_total
            record['total_amount'] = sum
        '''for record in self:                    
            record.batch_actual = sum
            record.transactions_actual = len(record.transactions)
            if record.apply_controls and (record.transactions_actual >= record.transactions_control or record.batch_actual >= record.batch_control):
                record.control = True
            else:
                record.control = False
                
            res = {}
            if (record.transactions_actual > record.transactions_control) and record.apply_controls:
                i = 1
                dictt = []
                for inv in self.transactions:
                    try:
                        if not (i == self.transactions_actual):
                            dictt.append(inv.id)
                    except:
                        pass
                    i = i+1
                self.transactions = [(6, 0, dictt)]
                
                res = {'warning': {
                    'title': _('Warning'),
                    'message': _('Actual Transactions limit reached transactions control')
                }}
                if res:
                    return res
                
            if (record.batch_actual > record.batch_control) and record.apply_controls:
                i = 1
                dictt = []
                for inv in self.transactions:
                    try:
                        if not(i == self.transactions_actual):
                            dictt.append(inv.id)
                    except:
                        pass
                    i = i+1
                self.transactions = [(6, 0, dictt)]
                res = {'warning': {
                    'title': _('Warning'),
                    'message': _('Actual Batch Total limit reached Batch Control')
                }}
                if res:
                    return res'''

class Capture_statement(models.Model):
    _name='capture.line'
    _rec_name = 'doc_number'
    
    doc_number = fields.Char('Doc Number')
    creditor = fields.Many2one('res.partner')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    amount = fields.Monetary(string='Amount')
    date = fields.Date('Date')
    recon = fields.Many2one('creditor.recon')
    authorize = fields.Boolean('EFT')
    
class Reconciliation(models.Model):
    _name='creditor.recon'
    _rec_name = 'creditor_id'
    
    reconcile_check = fields.Boolean('Ready to reconcile')
    partner_id = fields.Many2one('res.partner',domain="[('supplier','=',True)]",string="Supplier")
    creditor_id = fields.Char(related='partner_id.creditor_id',string='Creditor ID')
    statement_date = fields.Date('Statement Date')
    payment_date =  fields.Date('Payment Date')
    balance = fields.Monetary(string='Balance',required=False)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    description = fields.Text('Description')
    statement = fields.Binary('Statement')
    statement_name = fields.Char('File Name')
    transactions = fields.Many2many('capture.line',string="Capture Statement")
    unreconciled = fields.Many2many('capture.line','rel_unreconciled_items','batch_number','doc_number',string="Capture Statement")
    captured_balance = fields.Monetary('Captured Balance')
    difference = fields.Monetary('Difference')
    state = fields.Selection([
            ('new','New'),
            ('reconciled','Ready to Authorize')],
        default='new', string="State")
    other_statements = fields.Float("total other statemets")
    auth = fields.Many2one('creditor.authorize',string='Authorization')
    num_of_payments = fields.Integer("Count")
    num_of_payments_other = fields.Integer("Unreconciled Count")
    batch_number = fields.Char('Batch number')
    authorize = fields.Boolean('EFT')
    authorized = fields.Boolean('EFT')
    
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence"""
        '''if values:
            values['unique_credit_no'] = self.env['ir.sequence'].next_by_code('account.invoice.receivable')
        '''
        if values:
            values['batch_number'] = self.env['ir.sequence'].next_by_code('creditor.recon')
            #replace lines with defaul line
            
        record_obj = super(Reconciliation, self).create(values)
        return record_obj
    
    '''@api.multi
    @api.constrains('authorized')
    def check_authorization(self):
        for record in self:
            if record['state'] != 'authorization':
                raise Warning(_('Cannot proceed with EFT. Reconciliation pending.'))
        return'''
    
    @api.multi
    @api.depends('partner_id')
    @api.onchange('partner_id')
    def compute_voucher_value(self):
        invoices = self.env['payable.batch'].sudo().search([('source','=',self.partner_id.id),('state','=','posted')])
        
        #Fill up the list of captured statement
        '''txs = []
        unreconciled_list = []
        for record in invoices:
            transaction = self.env['capture.line']
            unreconciled = self.env['capture.line']
            transaction = self.env['capture.line'].create({
                    'doc_number': record['doc_number'],
                    'amount': record['total_amount'],
                    'date': record['date'],
                    'recon':self.id,
                })
            
            unreconciled_list.append(unreconciled.id)
            #txs.append(transaction.id)
        
        #self.transactions = [(6, 0, txs)]'''
        #self.unreconciled = self.env['capture.line'].sudo().search([])
        
    @api.multi
    @api.depends('transactions','balance')
    @api.onchange('transactions','balance')
    def compute_totals(self):
        total = 0
        balance = self.balance
        for record in self.transactions:
            total = total + record['amount']
            
        self.captured_balance = total
        #self.captured_balance = self.balance
        self.difference = total - balance
        
        
    
    @api.multi
    @api.depends('balance')
    @api.onchange('balance')
    def cpature_compute(self):
        self.captured_balance = self.balance
        
    '''@api.onchange('reconcile_check')
    def check_recons(self):
        if self.balance <= 0 or self.difference != 0 :
            self.reconcile_check = False'''
        
        
    def get_recon_report(self):
        return self.env.ref('account_payables.action_print_reconciliation_report').report_action(self)
    
    @api.onchange('state')
    def print_report_change(self):
        if self.state == 'reconciled':
            return self.env.ref('account_payables.action_print_reconciliation_report').report_action(self)
    
    
    @api.multi
    def reconcile(self):
        if self.reconcile_check:
            if self.balance <= 0 or self.difference != 0 :
                raise Warning(_('Cannot reconcile documents, please ensure difference is zero'))
                return
        if self.reconcile_check:
            sum = 0.0
            usum = 0.0
            c = 0
            for sta in self.transactions:
                c += 1
            self.num_of_payments = c
            
            uc = 0
            #self.unreconciled = self.unreconciled - self.transactions
            tot = []
            for item in self.transactions:
                tot.append(item.id)
            self.unreconciled = self.env['capture.line'].sudo().search([('id','not in',tot),('creditor','=',self.partner_id.id)])
            
            for statement in self.unreconciled:
                usum += statement.amount
                uc += 1
            
            self.other_statements = usum
            self.num_of_payments_other = uc
            
            self.state = 'reconciled'
            view = self.env.ref('sh_message.sh_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = " Statements have been successfully reconciled"
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
        else:
            raise Warning(_('Please mark this document as Ready to reconcile first.'))
        
    @api.multi
    def authorize_statement(self):
        if self.reconcile_check:
            context = {'default_statement':[self.id]}
            return{
                    'type': 'ir.actions.act_window',
                    'name': 'New Authorization',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'creditor.authorize',
                    'views': [(self.env.ref("account_payables.views_payable_authorization").id, 'form')],
                    'context': context,
                    'target': 'new',
            }
    
    
    
    
    
    
    
    
    
    
    
    
    
    