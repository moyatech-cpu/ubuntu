from odoo import api, fields, models
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception,content_disposition
import base64
import datetime


class ClientApproveRejectWizaed(models.TransientModel):
    _name = 'client.approve.reject.wizard'
    
    x_pc_comments = fields.Text(string="Comments")
    x_pc_state = fields.Selection(string="PC State",
                                   selection=[('Approved', 'Approved'),('Decline','Decline'), ('Query', 'Query')])
    x_timesheet_doc = fields.Binary(string="Timesheet")
    x_timesheet_doc_name = fields.Char("Timesheet name")     
    x_invoice_doc = fields.Binary(string="Invoice")
    x_invoice_doc_name = fields.Char("Invoice name")   
    x_bda_comments = fields.Text(string="Comments")
    x_bda_state = fields.Selection(string="State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_bdo_comments = fields.Text(string="Comments")
    x_bdo_state = fields.Selection(string="State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_branch_manager_comments = fields.Text(string="Comments")
    x_branch_manager_state = fields.Selection(string="State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_ed_manager_comments = fields.Text(string="Comments")
    x_ed_manager_state = fields.Selection(string="State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_ho_admin_comments = fields.Text(string="Comments")
    x_ho_admin_state = fields.Selection(string="State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])
    x_pc_bc_comments = fields.Text(string="PC Comments")
    x_pc_bc_state = fields.Selection(string="PC State",
                                   selection=[('Approved', 'Approved'),('Decline','Decline'), ('Query', 'Query')])
    x_qa_officer_comments = fields.Text(string="PC Comments")
    x_qa_officer_state = fields.Selection(string="PC State",
                                   selection=[('Approved', 'Approved'), ('Query', 'Query')])

    @api.model
    def default_get(self, fields):
        result = super(ClientApproveRejectWizaed, self).default_get(fields)
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        result.update({
            'final_product': voucher_application.product_doc,
            'final_product_name': voucher_application.product_doc_name,

            'x_timesheet_doc': voucher_application.timesheet_doc,
            'x_timesheet_doc_name': voucher_application.timesheet_doc_name,
            
            'x_invoice_doc': voucher_application.invoice_doc,
            'x_invoice_doc_name': voucher_application.invoice_doc_name,                
        })
        return result

    client_approve_reject_state = fields.Selection(string="Approve/Reject", selection=[('approve', 'Approve'), ('reject', 'Reject'), ('query', 'Query')])
    client_approve_reject_description = fields.Text(string="Explain in brief, reasons of your decision")
    client_redemption_pack = fields.Binary(string="Submit Work Plan Report")
    client_redemption_pack_name = fields.Char('File Name')
    final_product = fields.Binary(string="Final Product")
    final_product_name = fields.Char('File Name')

    def confirm_client_decision(self):
        return {
            "type": "ir.actions.nikesh"
        }

    def submit_pc_bc_decision(self):

        if self.x_pc_bc_state:
            active_id = self._context.get('active_id')
            voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            voucher_id = self.env['voucher.application'].browse([active_id])

            if voucher_id:
                
                if self.x_pc_bc_state == 'Approved':
                    voucher_id.status = 'approved'
                    
                    mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_approval_mail_template')
                    if mail_template_id and voucher_id.status == 'approved':
                        mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)

                elif self.x_pc_bc_state == 'Decline':
                    voucher_id.status = 'decline'          
                    
                    mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_declined_mail_template')
                    if mail_template_id and voucher_id.status == 'decline':
                        mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)   
                       
                else:
                    voucher_id.status = 'assessment_report'
                    
                voucher_id.x_pc_bc_state = self.x_pc_bc_state
                voucher_id.x_pc_bc_comments = self.x_pc_bc_comments
                
    def submit_client_decision(self):

        if self.client_approve_reject_state:
            print('----INSide iffffff--')
            active_id = self._context.get('active_id')
            voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            print('-------0\n\n', voucher_application)
            voucher_id = self.env['voucher.application'].browse([active_id])
            print('---------\n\n', voucher_id.product_doc)

            if voucher_id:
                voucher_id.client_approve_reject_state = self.client_approve_reject_state
                voucher_id.client_approve_reject_description = self.client_approve_reject_description
                voucher_id.client_redemption_pack = self.client_redemption_pack
                voucher_id.client_redemption_pack_name = self.client_redemption_pack_name


            if self.client_approve_reject_state == 'approve' and voucher_id.client_approve_reject_state == 'approve':
                
                voucher_id.status = 'bda_review'
                
                '''email_list = []
                for record_mail in self.env['res.users'].search([('branch_id','=',voucher_application.branch_id.id)]): #('branch_id','=',voucher_application.branch_id)
                    if (record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_bdo') or
                        record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_bda') or
                        record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_pc_bc')) and record_mail.email:
                        email_list.append(str(record_mail.email))

                mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

                if email_list and mail_server_ids.smtp_user:
                    email_send_list = ','.join(email_list)
                    attachment = {
                        'name': str(self.client_redemption_pack_name),
                        'datas': self.client_redemption_pack,
                        'datas_fname': self.client_redemption_pack_name,
                        'res_model': voucher_id._name,
                        'type': 'binary'
                    }
                    ir_attechment_id = self.env['ir.attachment'].create(attachment)
                    approve_mail_wiz_template = self.env.ref(
                        'nyda_grant_and_voucher.send_client_approve_product_mail_template')
                    if approve_mail_wiz_template:
                        approve_mail_wiz_template.attachment_ids = [(6, 0, [])]

                        approve_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]

                        approve_mail_wiz_template.with_context(user=self.env.user,
                                                               email_send_list=email_send_list).send_mail(voucher_id.id,
                                                                                                          force_send=True)'''
            elif self.client_approve_reject_state == 'reject':
                '''email_list = []
                for record_mail in self.env['res.users'].search([]):
                    if (record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_bdo') or
                        record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_bda') or
                        record_mail.has_group('nyda_grant_and_voucher.group_grant_voucher_pc_bc')) and record_mail.email:
                        email_list.append(str(record_mail.email))

                mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
                
                if mail_server_ids.smtp_user and mail_server_ids.smtp_user:
                    email_send_list = ','.join(email_list)
                    attachment = {
                        'name': str(self.client_redemption_pack_name),
                        'datas': self.client_redemption_pack,
                        'datas_fname': self.client_redemption_pack_name,
                        'res_model': voucher_id._name,
                        'type': 'binary'
                    }
                    ir_attechment_id = self.env['ir.attachment'].create(attachment)
                    reject_mail_wiz_template = self.env.ref(
                        'nyda_grant_and_voucher.send_client_reject_product_mail_template')
                    if reject_mail_wiz_template:
                        reject_mail_wiz_template.attachment_ids = [(6, 0, [])]

                        reject_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]

                        reject_mail_wiz_template.with_context(user=self.env.user,
                                                               email_send_list=email_send_list).send_mail(voucher_id.id,
                                                                                                          force_send=True)'''
                voucher_id.status = 'work_plan_submitted'
            else:
                voucher_id.status = 'work_plan_submitted'
                                                               
                                                               
    def submit_bda_decision(self):
        
        if self.x_bda_state:
            active_id = self._context.get('active_id')
            #voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            voucher_id = self.env['voucher.application'].browse([active_id])

            if voucher_id:
                
                if self.x_bda_state == 'Approved':
                    voucher_id.status = 'bdo_review'                 
                else:
                    voucher_id.status = 'work_plan_submitted'
                    
                voucher_id.x_bda_state = self.x_bda_state
                voucher_id.x_bda_comments = self.x_bda_comments
                
    def submit_bdo_decision(self):

        if self.x_bdo_state:
            active_id = self._context.get('active_id')
            #voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            voucher_id = self.env['voucher.application'].browse([active_id])

            if voucher_id:
                
                if self.x_bdo_state == 'Approved':
                    voucher_id.status = 'pc_review'
                    #mail_template_id = self.env.ref('nyda_voucher.voucher_status_mail_template')
                    #if mail_template_id and voucher_id.status == 'approved':
                    #   mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)                    
                else:
                    voucher_id.status = 'bda_review'
                    
                voucher_id.x_bdo_state = self.x_bdo_state
                voucher_id.x_bdo_comments = self.x_bdo_comments

    def submit_pc_decision(self):

        if self.x_pc_state:
            active_id = self._context.get('active_id')
            #voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            voucher_id = self.env['voucher.application'].browse([active_id])

            if voucher_id:
                
                if self.x_pc_state == 'Approved':
                    #26/08/20 
                    #voucher_id.status = 'branch_manager_review'
                    voucher_id.status = 'ho_admin_review'
                    #mail_template_id = self.env.ref('nyda_voucher.voucher_status_mail_template')
                    #if mail_template_id and voucher_id.status == 'approved':
                    #    mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)                    
                else:
                    voucher_id.status = 'bdo_review'
                    
                voucher_id.x_pc_state = self.x_pc_state
                voucher_id.x_pc_approval_date = datetime.datetime.now()
                voucher_id.x_pc_comments = self.x_pc_comments                             

    def submit_branch_manager_decision(self):

        if self.x_branch_manager_state:
            active_id = self._context.get('active_id')
            voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            voucher_id = self.env['voucher.application'].browse([active_id])

            if voucher_id:
                
                if self.x_branch_manager_state == 'Approved':
                    voucher_id.status = 'ho_admin_review'
                    voucher_id.x_branch_manager_approval_date = datetime.datetime.now()
                    #mail_template_id = self.env.ref('nyda_voucher.voucher_status_mail_template')
                    #if mail_template_id and voucher_id.status == 'approved':
                    #    mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)                    
                
                else:
                    voucher_id.status = 'pc_review'
                    
                voucher_id.x_branch_manager_state           = self.x_branch_manager_state
                voucher_id.x_branch_manager_comments        = self.x_branch_manager_comments  
                
    def submit_ho_admin_decision(self):

        if self.x_ho_admin_state:
            active_id = self._context.get('active_id')
            #voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            voucher_id = self.env['voucher.application'].browse([active_id])

            if voucher_id:
                
                if self.x_ho_admin_state == 'Approved':
                    voucher_id.status = 'qa_officer_review'
                    #mail_template_id = self.env.ref('nyda_voucher.voucher_status_mail_template')
                    #if mail_template_id and voucher_id.status == 'approved':
                    #    mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)                    
                
                else:
                    voucher_id.status = 'bdo_review'
                    
                voucher_id.x_ho_admin_state = self.x_ho_admin_state
                voucher_id.x_ho_admin_comments = self.x_ho_admin_comments                  

    def submit_qa_officer_decision(self):

        if self.x_qa_officer_state:
            active_id = self._context.get('active_id')
            #voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            voucher_id = self.env['voucher.application'].browse([active_id])

            if voucher_id:
                
                if self.x_qa_officer_state == 'Approved':
                    voucher_id.status = 'ed_manager_review'
                    #mail_template_id = self.env.ref('nyda_voucher.voucher_status_mail_template')
                    #if mail_template_id and voucher_id.status == 'approved':
                    #    mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)                    
                else:
                    voucher_id.status = 'ho_admin_review'
                    
                voucher_id.x_qa_officer_state = self.x_qa_officer_state
                voucher_id.x_qa_officer_comments = self.x_qa_officer_comments
                
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
                voucher_id.x_finance_submission_date    = datetime.datetime.now()
                voucher_id.x_ed_manager_comments        = self.x_ed_manager_comments