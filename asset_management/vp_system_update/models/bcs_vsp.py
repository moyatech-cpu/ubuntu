# coding=utf-8
from odoo import api, fields, models
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo import http
from odoo.exceptions import UserError, ValidationError
#from pdf2image import convert_from_path, convert_from_bytes
import base64

class Service(models.Model):
    _inherit = 'res.partner'
    
    payment_status = fields.Selection([('pending','Pending'),('paid','Paid')],default='pending',string="Voucher VP19 status")
    
    def payment_completed(self):
        self.payment_status = 'paid'

class POInvoice(models.Model):
    """ Model to inherit/extend the PO"""
    _inherit = 'account.invoice'
    
    related_vp = fields.Many2one('bcs.vsp',string="VP19 Batch")
    
class VSPform(models.Model):
    """ Model to populate voucher applications for specific service provider """
    _inherit = 'bcs.vsp'
    
    @api.model
    def service_provider_domain(self):
        sp = self.env["voucher.application"].sudo().search([('status','=','pending_payment')])
        #collect all users
        sp_ids = []
        for record in sp:
            sp_ids.append(record.x_service_provider.id)
        
        return [('x_voucher_vendor', '=', True),('id','in',sp_ids)]
    
    service_providers = fields.Many2many('res.partner','vp_bcs_service_providers_rel','bcs_number','name',domain=service_provider_domain, string="Service Provider(s)")
    voucher_application_ids = fields.One2many('voucher.application', 'vp_record',compute="_compute_service_provider_vouchers",
                                            string="Voucher Applications")
    
    voucher_invoices = fields.One2many('account.invoice', 'related_vp',string="Voucher Invoices")
    
    status = fields.Selection([('new', 'New'), ('sent2fin', 'EDM Review'),
         ('approved', 'Approved'),('completed', 'Completed'), ('query', 'Query')],
        default='new', string="status",group_expand='_expand_states', index=True)
    
    fin_status = fields.Selection([('new', 'New'), ('open', 'Invoice Open'),
         ('paid', 'Posted'),('query', 'Query')],
        default='new', string="status",group_expand='_expand_fin_states', index=True)
    
    query_comment = fields.Text("Query Comment")
    
    fold = fields.Selection([('new', 'New'), ('sent2fin', 'EDM Review'),
         ('approved', 'Approved'), ('completed', 'Completed'),('query', 'Query')],
                              string='Status', default='new', index=True)
    
    fin_fold = fields.Selection([('new', 'New'), ('open', 'Invoice Open'),
         ('paid', 'Posted'),('query', 'Query')],string='Status', default='new', index=True)
    
    #Process Flow Files
    vp_document = fields.Binary('VP19 Document',compute='generate_report_file')
    vp_document_fn = fields.Char('VP19',default='Internal Memorandum')
    sp_statements = fields.Binary('SP Statement Document')
    sp_statements_fn = fields.Char('SP Statement',default='SP Statement')
    
    
    @api.depends('service_providers')
    @api.onchange('service_providers')
    def generate_report_file(self):
        report_name = "bcs_vsp.action_report_bcs_vsp"
        for record in self:
            pdf = self.env.ref('bcs_vsp.action_report_bcs_vsp').sudo().render_qweb_pdf([record['id']])[0]
            record['vp_document'] = base64.b64encode(pdf)
      
    
    @api.model
    def _expand_fin_states(self, states, domain, order):
         return [key for key, val in type(self).fin_fold.selection]
    
    def query_finance(self):
        self.status = 'query'
        self.x_rejected_by_date = date.today()
        self.fin_status = 'query'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Query VP19',
            'res_model': 'query.vp',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }
    
    @api.onchange('repsonsible_edm_employee')
    def get_service_providers(self):
        return 0
        sp = self.env["voucher.application"].sudo().search([('status','=','pending_payment')])
        #collect all users
        sp_ids = []
        for record in sp:
            sp_ids.append(record.x_service_provider.id)
        
        self.service_providers = self.env['res.partner'].sudo().search([('id','in',sp_ids),('payment_status','!=','paid')])
        for rec in self:
            for svp in rec['service_providers']:
                if not svp.payment_status:
                    svp.payment_status = 'pending'
    
    def get_service_provider_report(self):
        return self.env.ref('vp_system_update.action_print_service_providers').report_action(self)
    
    def get_process_flow_report(self):
        return self.env.ref('vp_system_update.action_print_process_flow').report_action(self)
    
    def get_sp_report(self):
        return {
                'service_providers':self.service_providers,
            }
    
    
    @api.onchange('service_providers','from_date','to_date')
    @api.depends('service_providers','from_date','to_date')
    def _compute_total_grand(self):
        total = 0
        if self.service_providers:
            for record in self.voucher_application_ids:#calculate directly from many2many object onchange
                total = total + record.x_voucher_value
        for record in self:
            record['total_vouchers'] = total
        
    @api.onchange('service_providers','from_date','to_date')
    @api.depends("service_providers",'from_date','to_date')
    def _compute_total_vouchers(self):
        total = 0
        if self.service_providers and self.date_filter:
            temp = self.env["voucher.application"].sudo().search([('x_service_provider','in',self.service_providers.ids),('status', 'in',('payment_completed','pending_payment')),('x_finance_submission_date','>=',self.from_date),('x_finance_submission_date','<=',self.to_date)])
            for record in temp:
                total = total + 1
            self.num_of_applications = total
        elif self.service_providers:
            temp = self.env["voucher.application"].sudo().search([('x_service_provider','in',self.service_providers.ids),('status', 'in',('payment_completed','pending_payment'))])
            for record in temp:
                total = total + 1
            self.num_of_applications = total
                
    @api.onchange('service_providers','from_date','to_date')
    @api.depends("service_providers",'from_date','to_date')
    def _compute_service_provider_vouchers(self):
        if self.service_providers and self.date_filter:
            recordset = self.env["voucher.application"].sudo().search([('x_service_provider','in',self.service_providers.ids),('status', 'in',('payment_completed','pending_payment')),('x_finance_submission_date','>=',self.from_date),('x_finance_submission_date','<=',self.to_date)]) #("status", "=","new"),("branch_id", "=",self.branch)
            self.voucher_application_ids = recordset
        elif self.service_providers:
            recordset = self.env["voucher.application"].sudo().search([('x_service_provider','in',self.service_providers.ids),('status',  'in',('payment_completed','pending_payment'))]) #("status", "=","new"),("branch_id", "=",self.branch)
            self.voucher_application_ids = recordset
    
    def payment_completed(self):
        '''for sp in self.service_providers:
            if sp.payment_status != 'paid':
                raise ValidationError("Please ensure all Services Providers are Marked Paid")
                return
        for vp in self.voucher_application_ids:
            if vp.status != 'payment_completed':
                raise ValidationError("Please ensure all Vouchers are marked completed")
                return'''
        for record in self:
            for inv in record['voucher_invoices']:
                inv.action_date_assign()
                inv.action_move_create()
                inv.invoice_validate()
        self.status = 'completed'
        self.fin_status = 'paid'
    
    def send_to_verification(self):
        self.status = 'sent2fin'
        self.x_verified_by_date = datetime.now()
        self.verified_by = self.env.uid
        for record in self:
            for v in record['voucher_application_ids']:
                v['vp_record'] = record['id']
            
        email_list = []
        body = "<html>\
        <body><p>"+str(self.bcs_number)+" VP19 has been verified and brought to your attention to review</p>\
        <table width='100%' height='100%' style='border:1px solid black;'>\
        <tr style='border:1px solid black;'>\
        <td style='border:1px solid black;'>VP REF#</td><td style='border:1px solid black;'>"+str(self.bcs_number)+"</td></tr>"
        for record_mail in self.env['res.users'].search([]):
            if (record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_bscvp') or record_mail.id == self.responsible_bds_voucher) and record_mail.email:
                email_list.append(str(record_mail.email))
        mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
        
        body += "</table></body></html>"
        body += "<p><strong> Kind regards, </strong></p><br/>\
                <p>"+self.verified_by.name+"</p>"
        if email_list and mail_server_ids.smtp_user:
            email_to = ','.join(email_list)
            template = self.env['mail.mail'].create({
                'subject': 'VP19 Workflow',
                'body_html': body,
                'email_from': self.env.user.email or '',
            })
            template.write({'email_to': email_to})
            template.send()
    
    @api.multi
    def reject_record(self):
        self.status = 'query'
        self.x_rejected_by_date = date.today()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Query VP19',
            'res_model': 'query.vp',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }
        
    def approve_record(self):
        self.status = 'approved'
        self.fin_status = 'new'
        self.x_approved_by_date = datetime.now()
        self.approved_by = self.env.uid
    
    def send_back_to_finance(self):
        self.status = 'approved'
        self.fin_status = 'new'
    
    @api.multi
    def grant_bcs_vsp_data(self):
        dict_custom = {}
        vouchers = {}
        final_list = []
        sp_list = []
        recordset = self.voucher_application_ids
        rec_no = 0
        for sv in recordset:
            rec_no += 1
            for voucher in sv:
                temp = ""
                try:
                    for service in voucher.x_recommended_service:
                        temp = service.name + "\n"+ temp
                except:
                    print("Invalid value")
                    
                vdata = {'main_no': rec_no, 
                         'sp': voucher.x_service_provider.name, 
                         'vch_no': voucher.x_voucher_number,
                         'inv_no': voucher.invoice_number,
                         'services': temp,
                         'branch': voucher.branch_id.name,
                         'amount': voucher.x_voucher_value,
                         }
                final_list.append(vdata)  
        for sp in self.service_providers:
            spData = {'display_name': sp.name, 
                      'phone': sp.phone, 
                      'email': sp.email,
                      'payment_status': sp.payment_status
                         }
            sp_list.append(spData)  
        
        flag = ""
        if self.flag == '0':
            flag = "Normal"
        elif self.flag == '1':
            flag = "High"
        elif self.flag == '2':
            flag = "Urgent"
        elif self.flag == '3':
            flag = "Critical"
        
        '''for att in self.vp_attachments:
            statement_id = att'''
        '''file = base64.b64decode(statement_id)
        images = convert_from_bytes(file)
        attachments = []
        for pos in images:
            attachment.append({'image':pos})'''
        
        
        date = self.date
        dict_custom = {
                'bcs_number':self.bcs_number,
                'service_providers': sp_list,
                'edm':self.repsonsible_edm_employee.name,
                'bcs':self.responsible_bds_voucher.name,
                'date': date,
                'no_vouchers' : self.num_of_applications,
                'priority': flag,
                'sp': self.service_provider.name,
                'vouchers': final_list,
                'total': self.total_vouchers,
                'compiler':self.compiled_by.name,
                'verifier':self.verified_by.name,
                'approver': self.approved_by.name,
                #'attachments': statement_id,
            }
        
        return dict_custom
    
    @api.multi
    def post_invoices(self):
        self.payment_completed()
        
    @api.multi
    def generate_invoices(self):
        for rec in self:
            vps = rec['voucher_application_ids']
            for record in vps:
                accounts = self.env['account.account'].sudo().search([('code','=','1995')])
                account_id = self.env['account.account']
                journal_id = self.env['account.journal']
                for acc in accounts:
                    account_id = acc
                journals = self.env['account.journal'].sudo().search([('name','=','Vendor Invoices')])
                for jn in journals:
                    journal_id = jn
                inv_total = 0.0
                inv_des = ''
                for line in record['x_recommended_service']:
                    inv_total = inv_total + line['voucher_value']
                    inv_des = inv_des+line['name']+' '
                invoice_id = self.env['account.invoice'].create({
                    'name' : record['serial_number'] + ' ' + record['x_service_provider']['name']+ ' '+inv_des,
                    'number': record['x_service_provider']['name'][:4] + '/'+str(date.year)+'/'+str(date.month),
                    'date_invoice' : date.today(),
                    'partner_id': record['x_service_provider']['id'],
                    'user_id': self.env.uid,
                    'type':'in_invoice',
                    'account_id':account_id.id,
                    'journal_id':journal_id.id,
                    'related_vp':rec['id'],
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
                self.env['account.invoice.line'].create({
                        'invoice_id' : invoice_id.id,
                        'name' : 'VOUCHER ITEM',
                        'product_id' : product_id.id,
                        'price_unit' : inv_total,
                        'quantity' : 1.0,
                        'account_id': account_id.id,
                    })
                rec['voucher_invoices'] = rec['voucher_invoices'] + invoice_id
            rec['fin_status'] = 'open'
    
class VoucherApplication(models.Model):
    """ Model to inherit/extend the voucher application """
    _inherit = 'voucher.application'
    
    vp_comment_query = fields.Text("Query")
    vp_process_document = fields.Binary('Process Document',compute='generate_report_file')
    vp_process_fn = fields.Binary('Process Flow',default='Process Flow')
    
    def get_process_flow_report(self):
        return self.env.ref('vp_system_update.action_report_voucher_internal_audit').report_action(self)
    
    @api.depends('status')
    @api.onchange('status')
    def generate_report_file(self):
        report_name = "vp_system_update.action_report_voucher_internal_audit"
        for record in self:
            pdf = self.env.ref('vp_system_update.action_report_voucher_internal_audit').sudo().render_qweb_pdf([record['id']])[0]
            record['vp_process_document'] = base64.b64encode(pdf)
        #report
        #result, format = self.env.ref('hr_timesheet.timesheet_report).render_qweb_pdf(self.ids)
        #result = base64.b64encode(result) # Use this in attachment creation in datas field
        #df = self.env.ref('vp_system_update.action_report_voucher_internal_audit').render_qweb_pdf(self.id)[0]
        
class ProofOfPayment(models.TransientModel):
    _inherit = 'proof.of.payment.wiz'
    
    @api.multi
    def btn_submit_proof_of_payment(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        voucher_application.status = 'payment_completed'
        voucher_application.proof_of_payment = self.proof_of_payment
        voucher_application.proof_of_payment_name = self.proof_of_payment_name
        voucher_application.proof_of_payment_date = self.payment_date
        return True
    