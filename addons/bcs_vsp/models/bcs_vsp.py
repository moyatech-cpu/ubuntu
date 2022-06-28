# coding=utf-8
from odoo import api, fields, models
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo import http

class VSPform(models.Model):
    """ Model to populate voucher applications for specific service provider """
    _name = 'bcs.vsp'
    _rec_name = 'bcs_number'
    
    bcs_number = fields.Char('BCS VP-19')
    status = fields.Selection(
        [('new', 'New'), ('sent2fin', 'EDM Review'),
         ('approved', 'Approved'),('completed', 'Completed'), ('reject', 'Rejected')],
        default='new', string="status",group_expand='_expand_states', index=True)
    flag = fields.Selection(
        [('0', 'Normal'), ('1', 'High'),
         ('2', 'Urgent'), ('3', 'Critical')],
        default='0', string="Urgency")
    service_provider = fields.Many2one('res.partner',domain=[('x_voucher_vendor', '=', True)], string="Service Provider")
    repsonsible_edm_employee = fields.Many2one('res.users', string="To")
    responsible_bds_voucher = fields.Many2one('res.users', string="From")
    date = fields.Date('Date', default=fields.Date.today(),store=True)
    num_of_applications = fields.Integer("Total Vouchers'",compute="_compute_total_vouchers",store=True)
    
    voucher_application_ids = fields.One2many('voucher.application', 'vp_record',compute="_compute_service_provider_vouchers",
                                            string="Voucher Applications",ondelete='restrict')
    
    total_vouchers = fields.Integer("R",compute="_compute_total_grand",store=True)
    branch = fields.Many2one('res.branch', string="Branch", default=lambda self: self.env.user.branch_id)
    
    compiled_by = fields.Many2one('res.users', string="Compiled By", default=lambda self: self.env.user)
    
    verified_by = fields.Many2one('res.users', string="Verified By")
    approved_by = fields.Many2one('res.users', string="Approved By")
    for_comment = fields.Boolean("For Comment")
    for_approve = fields.Boolean("For Approve")
    
    if_rejected = fields.Many2one('res.users', string="Rejected By", default=lambda self: self.env.user)
    rejected_q = fields.Boolean()
    x_verified_by_date = fields.Datetime('Verified Date')
    x_approved_by_date = fields.Datetime('Approved Date')
    x_rejected_by_date = fields.Datetime('Rejected Date')
    vp_attachments = fields.Many2many('ir.attachment', 'vp_bcs_statememts_rel', 'bcs_number', 'attachment_id', 'Attachments')
    #filters         x_finance_submission_date
    
    date_filter = fields.Boolean("Date Filter",default=True)
    from_date = fields.Date("From")
    to_date = fields.Date("To")
    
    color = fields.Integer(string='Color Index', default=4)
    active = fields.Boolean(default=True)
    fold = fields.Selection([('new', 'New'), ('sent2fin', 'EDM Review'),
         ('approved', 'Approved'), ('completed', 'Completed'),('reject', 'Rejected')],
                              string='Status', default='new', index=True)
      
    
    @api.model
    def _expand_states(self, states, domain, order):
         return [key for key, val in type(self).fold.selection]
    '''
         state = [
            'new',
            'pending',
            ]
         folded = {'in_progress': True, 'closed': True, 'delivered': True}
         return state,folded     
    '''
    
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
    
    @api.multi
    def grant_bcs_vsp_data(self):
        dict_custom = {}
        vouchers = {}
        final_list = []
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
                
        
        flag = ""
        if self.flag == '0':
            flag = "Normal"
        elif self.flag == '1':
            flag = "High"
        elif self.flag == '2':
            flag = "Urgent"
        elif self.flag == '3':
            flag = "Critical"
            
        date = self.date
        dict_custom = {
                'bcs_number':self.bcs_number,
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
            }
        
        return dict_custom
    
    @api.onchange('service_provider','date_filter','from_date','to_date')
    @api.depends('service_provider','date_filter','from_date','to_date')
    def _compute_total_grand(self):
        total = 0
        if self.service_provider:
            for record in self:#calculate directly from many2many object onchange
                for vpx in record['voucher_application_ids']:
                    total = total + vpx.x_voucher_value
            self.total_vouchers = total
        
    @api.onchange("service_provider",'from_date','to_date')
    @api.depends("service_provider",'from_date','to_date')
    def _compute_total_vouchers(self):
        total = 0
        if self.service_provider and self.date_filter:
            temp = self.env["voucher.application"].sudo().search([('x_service_provider','=',self.service_provider.id),('status', 'in',('pending_payment','payment_completed','payment_released')),('x_finance_submission_date','>=',self.from_date),('x_finance_submission_date','<=',self.to_date)])
            for record in temp:
                total = total + 1
            self.num_of_applications = total
        elif self.service_provider:
            temp = self.env["voucher.application"].sudo().search([('x_service_provider','=',self.service_provider.id),('status', 'in',('pending_payment','payment_completed','payment_released'))])
            for record in temp:
                total = total + 1
            self.num_of_applications = total
    
    @api.onchange("service_provider",'from_date','to_date')            
    @api.depends("service_provider",'from_date','to_date')
    def _compute_service_provider_vouchers(self):
        if self.service_provider and self.date_filter:
            recordset = self.env["voucher.application"].sudo().search([('x_service_provider','=',self.service_provider.id),('status', 'in',('pending_payment','payment_completed','payment_released')),('x_finance_submission_date','>=',self.from_date),('x_finance_submission_date','<=',self.to_date)]) #("status", "=","new"),("branch_id", "=",self.branch)
            self.voucher_application_ids = recordset
        elif self.service_provider:
            recordset = self.env["voucher.application"].sudo().search([('x_service_provider','=',self.service_provider.id),('status', 'in',('pending_payment','payment_completed','payment_released'))]) #("status", "=","new"),("branch_id", "=",self.branch)
            self.voucher_application_ids = recordset
    
    @api.multi
    def print_report(self, docids, data=None):
        return self.env.ref('bcs_vsp.action_report_bcs_vsp').report_action(self)
    
    def send_to_finance(self):
        self.status = 'sent2fin'
        email_list = []
        '''body = "<html>\
        <body><p>"+str(self.service_provider.name)+" VP19 has been brought to your attention</p>\
        <table width='100%' height='100%' style='border:1px solid black;'>\
        <tr style='border:1px solid black;'>\
        <td style='border:1px solid black;'>VP REF#</td><td style='border:1px solid black;'>"+str(self.bcs_number)+"</td></tr>"
        for record_mail in self.env['res.users'].search([]):
            if record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_edm') and record_mail.email:
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
            template.send()'''
    
    def reject_record(self):
        self.status = 'reject'
        self.x_rejected_by_date = datetime.now()
        self.rejected_q = True
        self.if_rejected = self.env.uid
    
    def payment_completed(self):
        self.status = 'completed'
    
    def approve_record(self):
        self.status = 'approved'
        self.x_approved_by_date = datetime.now()
        self.approved_by = self.env.uid
    
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
            if (record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_bscvp') or record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_edm')) and record_mail.email:
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
    
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence to VSP19 forms """
        if values:
            values['bcs_number'] = self.env['ir.sequence'].next_by_code('bcs.vsp')
            print('---------\n\n\n', values['bcs_number'])
        record_obj = super(VSPform, self).create(values)
        return record_obj


class VoucherApplication(models.Model):
    """ Model to inherit/extend the voucher application """
    _inherit = 'voucher.application'
    
    invoice_number = fields.Char("Invoice Number")
    vp_record = fields.Many2one('bcs.vsp',string='related VP19')
    x_voucher_value = fields.Integer(string="Voucher value",store=True,readonly=True)#deleted _compute_voucher_value
    #edm_approved_date = fields.Datetime("Approved Date")
    #x_voucher_value_copy = fields.Integer(string="Voucher value",store=True)
    
    """@api.multi
    @api.depends('x_recommended_service')
    def _compute_voucher_value(self):
        total = 0
        for rec in self:
            for x in rec.x_recommended_service:
                total = total + int(x.voucher_value)
        
        self.x_voucher_value = int(total)"""

class ClientApproveRejectWizaed(models.TransientModel):
    _inherit = 'client.approve.reject.wizard'
    
    def submit_ed_manager_decision(self):

        if self.x_ed_manager_state_correction:
            active_id = self._context.get('active_id')
            #voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            voucher_id = self.env['voucher.application'].browse([active_id])

            if voucher_id:
                
                if self.x_ed_manager_state_correction == 'Approved':
                    voucher_id.status = 'pending_payment'
                    #mail_template_id = self.env.ref('nyda_voucher.voucher_status_mail_template')
                    #if mail_template_id and voucher_id.status == 'approved':
                    #    mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)                    
                if self.x_ed_manager_state_correction == 'Query Invoice':
                    voucher_id.status = 'ho_admin_review'
                if self.x_ed_manager_state_correction == 'Query Product':
                    voucher_id.status = 'qa_officer_review'
                    
                voucher_id.x_ed_manager_state           = self.x_ed_manager_state_correction
                voucher_id.x_finance_submission_date    = datetime.now()
                voucher_id.x_ed_manager_comments        = self.x_ed_manager_comments

class SubmitProductWiz(models.TransientModel):
    _inherit = 'submit.product.wiz'
    _description = 'Submit Product'

    invoice_number = fields.Char('Invoice Number')
    

    @api.multi
    def submit_product_req(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        #voucher_application.status = 'submitted_product'
        voucher_application.status = 'client_review'
        #newly added field
        voucher_application.invoice_number = self.invoice_number
        voucher_application.product_doc_name = self.product_doc_name
        voucher_application.product_doc = self.product_doc
        voucher_application.invoice_doc_name = self.invoice_doc_name
        voucher_application.invoice_doc = self.invoice_doc
        voucher_application.x_invoice_date = datetime.now()
        voucher_application.timesheet_doc_name = self.timesheet_doc_name
        voucher_application.timesheet_doc = self.timesheet_doc
        if voucher_application.email:
            voucher_product_submit_mail_template = self.env.ref('nyda_grant_and_voucher.voucher_product_submit_mail_template')
            voucher_product_submit_mail_template.with_context(user=self.env.user).send_mail(voucher_application.id, force_send=True)
        return True
    
class ClientApproveRejectWizaed(models.TransientModel):
    _inherit = 'recommendation.note'
    _description = 'recommendation note'
    #x_recommended_service = fields.Many2many('business.development.assistance',string="Service")
    #recommendationnote = fields.Char(string='Recommendation Note')

    @api.multi
    def default_recommendationnote(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        print('-----...', voucher_application)
        total = 0
        
        for x in voucher_application.x_recommended_service:
                total = total + int(x.voucher_value)
                
        voucher_application.write({
            'x_recommended_service': [(6, 0, self.x_recommended_service.ids)],
            'recommendationnote': self.recommendationnote,
            'x_voucher_value': total,
        })
        return True