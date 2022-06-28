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
        [('new', 'New'), ('sent2fin', 'EDM Review'),
         ('approved', 'Approved'),('completed', 'Completed'), ('query', 'Query')],
        default='new', string="status",group_expand='_expand_states', index=True)
    flag = fields.Selection(
        [('0', 'Normal'), ('1', 'High'),
         ('2', 'Urgent'), ('3', 'Critical')],
        default='0', string="Urgency")
    
    repsonsible_edm_employee = fields.Many2one('res.users', string="To")
    responsible_bds_voucher = fields.Many2one('res.users', string="From")
    date = fields.Date('Date', default=fields.Date.today(),store=True)
    num_of_applications = fields.Integer("Total Grant'",compute="_compute_total_grants",store=True)
    
    grant_application_ids = fields.One2many('grant.application', 'gp_record',compute="_compute_service_provider_vouchers",
                                            string="Grant Applications")
    
    total_grants = fields.Integer("R",compute="_compute_total_grand",store=True)
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
    gp_attachments = fields.Many2many('ir.attachment', 'gp_statememts_rel', 'ref_number', 'attachment_id', 'Attachments')
    
    date_filter = fields.Boolean("Date Filter",default=True)
    from_date = fields.Date("From")
    to_date = fields.Date("To")
    
    color = fields.Integer(string='Color Index', default=4)
    active = fields.Boolean(default=True)
    fold = fields.Selection([('new', 'New'), ('sent2fin', 'EDM Review'),
         ('approved', 'Approved'), ('completed', 'Completed'),('query', 'Query')],
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
    
    @api.multi
    def bulk_grant_data(self):
        dict_custom = {}
        vouchers = {}
        final_list = []
        recordset = self.grant_application_ids
        rec_no = 0
        for grant in recordset:
            for quo in voucher['quotation_records']:
                rec_no += 1
                vdata = {'main_no': rec_no, 
                         'serial_number': grant['serial_number'], 
                         'supplier_name': quo['supplier_name'],
                         'description': quo['description'],
                         'date_invoice': quo['date_invoice'],
                         'total_amount': quo['total_amount'],
                         'branch': grant['serial_number'],
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
                'bcs_number':self.ref_number,
                #'service_providers': self.service_providers,
                'edm':self.repsonsible_edm_employee.name,
                'bcs':self.responsible_bds_voucher.name,
                'date': date,
                'no_vouchers' : self.num_of_applications,
                'priority': flag,
                #'sp': self.service_provider.name,
                'vouchers': final_list,
                'total': self.total_grants,
                'compiler':self.compiled_by.name,
                'verifier':self.verified_by.name,
                'approver': self.approved_by.name,
                }
        
        return dict_custom
    
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
        
    @api.onchange('from_date','to_date')
    @api.depends('from_date','to_date')
    def _compute_total_grants(self):
        total = 0
        if self.date_filter:
            temp = self.env["grant.application"].sudo().search([('status', '=','edm_approved')])
            for record in temp:
                total = total + 1
            self.num_of_applications = total
        else:
            temp = self.env["grant.application"].sudo().search([('status', '=','edm_approved')])
            for record in temp:
                total = total + 1
            self.num_of_applications = total
    
    @api.onchange('from_date','to_date')            
    @api.depends('from_date','to_date')
    def _compute_service_provider_vouchers(self):
        if self.date_filter:
            recordset = self.env["grant.application"].sudo().search([('status', '=','edm_approved')])
            self.grant_application_ids = recordset
        else:
            recordset = self.env["grant.application"].sudo().search([('status', '=','edm_approved')]) 
            self.grant_application_ids = recordset
    
    @api.multi
    def print_report(self, docids, data=None):
        return self.env.ref('vp_system_update.action_report_bulk_grant').report_action(self)
    
    def send_to_finance(self):
        self.status = 'sent2fin'
        email_list = []
    
    def reject_record(self):
        self.status = 'query'
        self.x_rejected_by_date = datetime.now()
        self.rejected_q = True
        self.if_rejected = self.env.uid
    
    def payment_completed(self):
        self.status = 'completed'
        self.fin_status = 'paid'
        
    def approve_record(self):
        self.status = 'approved'
        self.fin_status = 'new'
        self.x_approved_by_date = datetime.now()
        self.approved_by = self.env.uid
    
    def send_to_verification(self):
        self.status = 'sent2fin'
        self.x_verified_by_date = datetime.now()
        self.verified_by = self.env.uid
        for record in self:
            for v in record['grant_application_ids']:
                v['vp_record'] = record['id']
            
        email_list = []
        body = "<html>\
        <body><p>"+str(self.bcs_number)+" Grant Disbursement Pack has been verified and brought to your attention to review</p>\
        <table width='100%' height='100%' style='border:1px solid black;'>\
        <tr style='border:1px solid black;'>\
        <td style='border:1px solid black;'>REF#</td><td style='border:1px solid black;'>"+str(self.ref_number)+"</td></tr>"
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
                'subject': 'Grant Disbursement Pack Workflow',
                'body_html': body,
                'email_from': self.env.user.email or '',
            })
            template.write({'email_to': email_to})
            template.send()
    
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence to VSP19 forms """
        if values:
            values['ref_number'] = self.env['ir.sequence'].next_by_code('bulk.grant')
            print('---------\n\n\n', values['ref_number'])
        record_obj = super(GrantBulk, self).create(values)
        return record_obj


class GrantApplication(models.Model):
    """ Model to inherit/extend the voucher application """
    _inherit = 'grant.application'
    
    gp_record = fields.Many2one('bulk.grant.disbursment',string="related Grant Disbursment Bulk")
