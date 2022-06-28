# coding=utf-8
from odoo import api, fields, models
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo import http

class GrantBulk(models.Model):
    """ Model to populate voucher applications for specific service provider """
    _name = 'bulk.grant.disbursment'
    _rec_name = 'ref_number'
    
    ref_number = fields.Char('Serial#')
    status = fields.Selection(
        [('new', 'New'), ('sent2fin', 'Send To Finance'),
        ('completed', 'Completed'), ('query', 'Query')],
        default='new', string="status",group_expand='_expand_states', index=True)
    flag = fields.Selection(
        [('0', 'Normal'), ('1', 'High'),
         ('2', 'Urgent'), ('3', 'Critical')],
        default='0', string="Urgency")
    
    #repsonsible_edm_employee = fields.Many2one('res.users', string="To")
    #responsible_bds_voucher = fields.Many2one('res.users', string="From")
    date = fields.Date('Date', default=fields.Date.today(),store=True)
    num_of_applications = fields.Integer("Total Grant'",compute="_compute_total_grants",store=True)
    
    grant_application_ids = fields.One2many('grant.application', 'gp_record',compute="_compute_service_provider_vouchers",
                                            string="Grant Applications")
    
    total_grants = fields.Float("R",compute="_compute_total_grand",store=True)
    branch = fields.Many2one('res.branch', string="Branch", default=lambda self: self.env.user.branch_id)
    
    compiled_by = fields.Many2one('res.users', string="Compiled By", default=lambda self: self.env.user)
    
    verified_by = fields.Many2one('res.users', string="Verified By")
    #approved_by = fields.Many2one('res.users', string="Approved By")
    #for_comment = fields.Boolean("For Comment")
    #for_approve = fields.Boolean("For Approve")
    voucher_invoices = fields.One2many('account.invoice', 'related_gp',string="Voucher Invoices")
    
    
    completed_by = fields.Many2one('res.users', string="Completed By", default=lambda self: self.env.user)
    completed_date = fields.Datetime('Completed Date')
    verified_by_date = fields.Datetime('Verified Date')
    #x_approved_by_date = fields.Datetime('Approved Date')
    #x_rejected_by_date = fields.Datetime('Rejected Date')
    gp_attachments = fields.Many2many('ir.attachment', 'gp_statememts_rel', 'ref_number', 'attachment_id', 'Attachments')
    
    date_filter = fields.Boolean("Date Filter",default=False)
    from_date = fields.Date("From")
    to_date = fields.Date("To")
    
    color = fields.Integer(string='Color Index', default=4)
    active = fields.Boolean(default=True)
    fold = fields.Selection([('new', 'New'), ('sent2fin', 'Send To Finance'),
        ('completed', 'Completed'), ('query', 'Query')],
                              string='Status', default='new', index=True)
      
    
    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).fold.selection]
    
    @api.onchange('flag')
    def onchange_state(self):
        if self.flag == 0:
            self.color = 10
        if self.flag == 1:
            self.color = 1
        if self.flag == 2:
            self.color = 4
        if self.flag == 3:
            self.color = 6
    
    
    @api.onchange('date_filter','from_date','to_date')
    @api.depends('date_filter','from_date','to_date')
    def _compute_total_grand(self):
        total = 0
        for record in self:
            for vpx in record['grant_application_ids']:
                if vpx['quotation_records']:
                    for quotation in vpx['quotation_records']:
                        total = total + quotation['total_amount']
        self.total_grants = total
        
    @api.onchange('date_filter','from_date','to_date')
    @api.depends('date_filter','from_date','to_date')
    def _compute_total_grants(self):
        total = 0
        if self.date_filter:
            temp = self.env["grant.application"].sudo().search([('status', '=','edm_approved'),('create_date','>=',self.from_date),('create_date','<=',self.to_date)])
            for record in temp:
                total = total + 1
            self.num_of_applications = total
        else:
            temp = self.env["grant.application"].sudo().search([('status', '=','edm_approved')])
            for record in temp:
                total = total + 1
            self.num_of_applications = total
    
    @api.onchange('date_filter','from_date','to_date')
    @api.depends('date_filter','from_date','to_date')
    def _compute_service_provider_vouchers(self):
        if self.date_filter:
            recordset = self.env["grant.application"].sudo().search([('status', '=','edm_approved'),('create_date','>=',self.from_date),('create_date','<=',self.to_date)])
            self.grant_application_ids = recordset
        else:
            recordset = self.env["grant.application"].sudo().search([('status', '=','edm_approved')]) 
            self.grant_application_ids = recordset
    
    @api.multi
    def print_report(self, docids, data=None):
        return self.env.ref('vp_system_update.action_report_bulk_grant').report_action(self)
    
    def send_to_finance(self):
        self.status = 'sent2fin'
        #Send emails and compute invoices
        self.generate_invoices()
        self.post_invoices()
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = " Grant Disbursement Pack Sent to Finance for processing"
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
    
    def payment_completed(self):
        self.status = 'completed'
    
    @api.multi
    def post_invoices(self):
        line_totals = 0
        move_totals = 0
        journals=[]
        #create payable batch
        payable_batch = self.env['payable.batch'].create({
            'date': self.date,
            'batch_id':self.ref_number,
            'comment': "Grant Disbursement Pack",
            'total_amount': self.total_grants,
            'batch_type':'grant',
            'gp_link': self.id,
            })
        
        for inv in self.voucher_invoices:
            #inv.action_invoice_open()
            inv.batch_id_payables = payable_batch.id
        
    
    @api.multi
    def generate_invoices(self):
        for rec in self:
            vps = rec['grant_application_ids']
            for record in vps:
                accounts = self.env['account.account'].sudo().search([('code','=','000-000-000-9100-0000000')])
                account_id = self.env['account.account']
                journal_id = self.env['account.journal']
                for acc in accounts:
                    account_id = acc
                journals = self.env['account.journal'].sudo().search([('name','=','Vendor Invoices')])
                for jn in journals:
                    journal_id = jn
                inv_total = 0.0
                inv_data = []
                for line in record['quotation_records']:
                    #partner_id = self.env['res.partner'].sudo().search(['|',('name','=',line['supplier_name']),('email','=',line['email'])])
                    partner = self.env['res.partner'].create({
                                'name': line['supplier_name'],
                                'mobile':line['mobile_number'],
                                'email':line['email'],
                                'bank_ids': line['bank_account_ids'],
                                'property_account_payable_id': account_id.id,
                            })
                            
                    qa_line = {
                        'partner_id':partner.id,
                        'date_invoice':line['date_invoice'],
                        'description':line['description'],
                        'total_amount':line['total_amount'],
                        'doc_number':line['doc_number']
                    }
                    inv_data.append(qa_line)
                for inv in inv_data:
                    invoice_id = self.env['account.invoice'].create({
                        'name' : inv['doc_number'],
                        'invoice_number_entry': inv['doc_number'],
                        'date_invoice' : inv['date_invoice'],
                        'sales_amount' :inv['total_amount'],
                        'partner_id': inv['partner_id'],
                        'user_id': self.env.uid,
                        'type':'in_invoice',
                        #'account_id':2356,
                        'account_id':account_id.id,
                        'journal_id':journal_id.id,
                        'related_gp':rec['id'],
                        'state':'draft',
                        
                    })
                
                    product_ids = self.env['product.product'].sudo().search([('name','=','VOUCHER ITEM')])
                    product_id = self.env['product.product']
                    if not product_ids:
                        category_id = self.env['product.category'].sudo().search([('name','=','All')])
                        for cat in category_id:
                            product_id = self.env['product.product'].create({
                                'type' : 'service',
                                'name' : 'VOUCHER ITEM',
                                'default_code' : 'VOUCHER ITEM',
                                'categ_id' : cat.id,
                            })
                    else:
                        for prod in product_ids:
                            product_id = prod
                    prod_accounts = self.env['account.account'].sudo().search([('code','=','1995')])
                    self.env['account.invoice.line'].create({
                            'invoice_id' : invoice_id.id,
                            'name' : 'VOUCHER ITEM',
                            'product_id' : product_id.id,
                            'price_unit' : invoice_id.sales_amount,
                            'quantity' : 1.0,
                            'account_id': prod_accounts.id,
                        })
                    rec['voucher_invoices'] = rec['voucher_invoices'] + invoice_id
    
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence to VSP19 forms """
        if values:
            values['ref_number'] = self.env['ir.sequence'].next_by_code('bulk.grant')
            print('---------\n\n\n', values['ref_number'])
        record_obj = super(GrantBulk, self).create(values)
        return record_obj


class POInvoice(models.Model):
    """ Model to inherit/extend the PO"""
    _inherit = 'account.invoice'
    
    related_gp = fields.Many2one('bulk.grant.disbursment',string="Grant Disbursement Batch")
    
class GrantApplication(models.Model):
    """ Model to inherit/extend the voucher application """
    _inherit = 'grant.application'
    
    gp_record = fields.Many2one('bulk.grant.disbursment',string="Grant Disbursment Statements")
