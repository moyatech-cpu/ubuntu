# coding=utf-8
from odoo import api, fields, models
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo import http
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class ScheduleAppointment(models.TransientModel):
    _inherit = 'schedule.appointment.wizard'
    
    #sch_app_created_date = fields.Datetime('Scheduled Date',default=datetime.now())
    #sch_by = fields.Many2one('res.users','Scheduled By',default=lambda self: self.env.user)
    
    @api.multi
    def create_appointment(self):
        active_id = self.env.context.get('current_id')
        
        vals = {
            'name': self.name.name,
            'bdo_name': self.bdo_name.id,
            'appointment_date': self.appointment_date,
            'x_location': self.x_location,
            'sch_app_created_date': datetime.now(),
            'sch_by': self.env.user.id,
        }
        if active_id:
            fetched_record = self.env['voucher.application'].browse(active_id)
            fetched_record.user_name = vals['name']
            fetched_record.bdo_name = vals['bdo_name']
            fetched_record.appointment_date = vals['appointment_date']
            fetched_record.x_location = vals['x_location']
            fetched_record.sch_app_created_date = vals['sch_app_created_date']
            fetched_record.sch_by = vals['sch_by']
            fetched_record.status = 'appointment_drafted'
        mail_template_id = self.env.ref('nyda_grant_and_voucher.schedule_appointment_mail_template')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).send_mail(active_id, force_send=True)
        return True
        
class AttendanceRegister(models.TransientModel):
    _inherit = 'attendance.register'
    
    #attendance_created_date = fields.Date('Uploaded Date')
    #attendance_by = fields.Many2one('res.users','Uploaded By')
    
    @api.multi
    def attendance_reg_req(self):  #modified lines 23,34-38
        user = self.env['voucher.application'].browse(self._context.get('active_id'))
        
        # user.linkage_file_name =  self.file_name
        # user.linkage_report = self.linkage_report
        user.x_attendance_register = self.attendance_register_file
        user.x_attendance_register_name = self.attendance_register_name
        user.attendance_created_date = datetime.now()
        user.attendance_by = self.env.user.id
        return True
                                 
class AssessmentReport(models.TransientModel):
    _inherit = 'assessment.report'
    
    #assessment_upload_date = fields.Date('Uploaded Date')
    #assessment_uploaded_by = fields.Many2one('res.users','Uploaded By')
    
    @api.multi
    def assessment_report_req(self):
        grant_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        if grant_application.x_attendance_register:
            print('---', self._context.get('active_id'))
            assessment_rq = grant_application.write({
                'assessment_report_name': self.assessment_report_name,
                'assessment_report': self.assessment_report,
                'assessment_upload_date': datetime.now(),
                'assessment_uploaded_by': self.env.user.id,
            })
            grant_application.status = 'assessment_report'
        else:
            raise ValidationError("Please submit attendance register before proceeding with the assessment report.")
        return True
        
        
    @api.multi
    def attendance_register_req(self):
        grant_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        print('---', self._context.get('active_id'))
        assessment_rq = grant_application.write({
            'x_attendance_register_name': self.x_attendance_register_name,
            'x_attendance_register': self.x_attendance_register,
            'attendance_created_date': datetime.now(),
            'attendance_by':self.env.user.id,
        })
        return True

class Recommendation(models.TransientModel):
    _inherit = 'recommendation.note'
    
    #recommendation_date = fields.Date('Date Recommended')
    #recommendation_by = fields.Many2one('res.users','Recommended By')
    
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
            'recommendation_date': datetime.now(),
            'recommendation_by': self.env.user.id,
            'x_voucher_value': total,
        })
        return True

class ServiceProviderSelect(models.TransientModel):
    _inherit = 'select.service.provider.wizard'
    
    #service_provider_selected_date = fields.Date('SP Select Date')
    #selected_by = fields.Many2one('res.users','Selected By')
    
    @api.multi
    def confirm_service_provider(self):
        if self.x_service_provider_1:
            active_id = self._context.get('active_id')
            voucher_id = self.env['voucher.application'].browse([active_id])

            voucher_isurance_obj = self.env['voucher.isurance']
            today = datetime.now()
            next_month = today + relativedelta(months=+1)

            print({
                'start_date': datetime.today() or False,
                'end_date': (datetime.today() + relativedelta(months=3)) or False,
                'applicant_name': voucher_id.name or False,
                'applicant_email': voucher_id.email or False,
                'gender': voucher_id.gender or False,
                'mobile': voucher_id.mobile or False,
                'status': 'active' or False,
                'service_provider': self.x_service_provider_1.id or False,
                'voucher_applicant_id': voucher_id.id or False
            })

            jeck = voucher_isurance_obj.create({
                                        'start_date': datetime.today() or False,
                                        'end_date': (datetime.today() + relativedelta(months=3)) or False,
                                        'applicant_name': voucher_id.name or False,
                                        'applicant_email': voucher_id.email or False,
                                        'gender': voucher_id.gender or False,
                                        'mobile': voucher_id.mobile or False,
                                        'status': 'active' or False,
                                        'x_service_provider': self.x_service_provider_1.id or False,
                                        'voucher_applicant_id': voucher_id.id or False
                                        })

            voucher_id.status = 'voucher_isurance'
            voucher_id.service_provider_selected_date = datetime.now()
            voucher_id.selected_by = self.env.user.id
            if voucher_id.status == 'voucher_isurance':
                voucher_id.x_service_provider    = self.x_service_provider_1.id
                voucher_id.x_voucher_issued      = jeck.id
        else:
            print("Select Provider FIRST")

'''class VoucherSupportingDocuments(models.TransientModel):
    _inherit = 'reissue.voucher'

    #voucher_re_sd_submitted_date = fields.Date('Reissue Document Date')
    #voucher_re_sd_submitted_by = fields.Many2one('res.users','Submitted By')
    
    @api.multi
    def voucher_resupporting_documents_seq(self):  #modified lines 23,34-38
        voucher_id = self.env['voucher.application'].browse(self._context.get('active_id'))
        
        voucher_id.x_voucher_reissue_start_date = self.start_date or False
        voucher_id.x_voucher_reissue_end_date = (datetime.strptime(self.start_date, '%Y-%m-%d').date() + relativedelta(months=3)) or False
        
        voucher_id.reissued_voucher_supporting_doc = self.reissued_voucher_supporting_doc
        voucher_id.reissued_voucher_supporting_doc_file_name = self.reissued_voucher_supporting_doc_file_name
        voucher_id.voucher_re_sd_submitted_date = datetime.now()#self.voucher_re_sd_submitted_date
        voucher_id.voucher_re_sd_submitted_by = self.env.user #self.voucher_re_sd_submitted_by
        voucher_id.status = 'work_plan'
        voucher_id.x_voucher_number = self.env['ir.sequence'].next_by_code('voucher.isurance')
        print('---------\n\n\n', voucher_id.x_voucher_number)
        mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_issued_sp')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)
        return True'''
                  
class VoucherSupportingDocuments(models.TransientModel):
    _inherit = 'voucher.supporting.documents'
    
    #voucher_sd_submitted_date = fields.Date('Voucher Supporting Document Date')
    #voucher_sd_submitted_by = fields.Many2one('res.users','Submitted By')
    
    @api.multi
    def voucher_supporting_documents_seq(self):  #modified lines 23,34-38
        voucher_id = self.env['voucher.application'].browse(self._context.get('active_id'))
        
        voucher_id.voucher_issuance_supporting_document = self.x_voucher_supporting_documents
        voucher_id.voucher_issuance_supporting_document_file_name = self.x_voucher_supporting_documents_file_name
        voucher_id.voucher_sd_submitted_date = datetime.now() #self.voucher_sd_submitted_date
        voucher_id.voucher_sd_submitted_by = self.env.user.id #self.voucher_sd_submitted_by
        voucher_id.status = 'work_plan'
        voucher_id.x_voucher_number = self.env['ir.sequence'].next_by_code('voucher.isurance')
        print('---------\n\n\n', voucher_id.x_voucher_number)
        mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_issued_sp')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)
        return True

class WorkPlan(models.TransientModel):
    _inherit = 'work.plan.submit.wizard'
    
    #work_plan_date = fields.Date('Workplan Submitted Date')
    #work_plan_by = fields.Many2one('res.users','Submitted By')
    
    @api.multi
    def submit_work_plan_report(self):
        
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        
        if(voucher_application):
            voucher_application.work_plan_report_name   = self.work_plan_report_name
            voucher_application.work_plan_report        = self.work_plan_report
            voucher_application.work_plan_date        = datetime.now() #self.work_plan_date
            voucher_application.work_plan_by        = self.env.user.id #self.work_plan_by
            voucher_application.status                  = 'work_plan_submitted'
            
            attachment = {
                       'name': str(self.work_plan_report_name),
                       'datas': self.work_plan_report,
                       'datas_fname': self.work_plan_report_name,
                       'res_model': voucher_application._name,
                       'type': 'binary'
                       }
            ir_attechment_id = self.env['ir.attachment'].create(attachment)
            approve_mail_wiz_template = self.env.ref('nyda_grant_and_voucher.send_voucher_work_plan_mail_template')
            if approve_mail_wiz_template:
                approve_mail_wiz_template.attachment_ids = [(6, 0, [])]
    
                approve_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]
    
                approve_mail_wiz_template.with_context(user=self.env.user,beneficiary=voucher_application.email).sudo().send_mail(voucher_application.id, force_send=True)
            return True      

class SubmitProduct(models.TransientModel):
    _inherit = 'submit.product.wiz'
    
    #product_submitted_date = fields.Date('Product Submitted Date')
    #product_submitted_by = fields.Many2one('res.users','Submitted By')
    
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
        voucher_application.product_submitted_date = datetime.now() #self.product_submitted_date
        voucher_application.product_submitted_by = self.env.user.id #self.product_submitted_by
        voucher_application.x_invoice_date = datetime.now()
        voucher_application.timesheet_doc_name = self.timesheet_doc_name
        voucher_application.timesheet_doc = self.timesheet_doc
        if voucher_application.email:
            voucher_product_submit_mail_template = self.env.ref('nyda_grant_and_voucher.voucher_product_submit_mail_template')
            voucher_product_submit_mail_template.with_context(user=self.env.user).send_mail(voucher_application.id, force_send=True)
        return True
                          
class BDAReview(models.TransientModel):
    _inherit = 'client.approve.reject.wizard'
    
    #bda_approve_query_reject_date = fields.Date('Reviewed Date')
    #bda_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
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
                    
                voucher_id.bda_approve_query_reject_date = datetime.now() #self.bda_approve_query_reject_date
                voucher_id.bda_approve_reject_by = self.env.user.id #self.bda_approve_reject_by
                voucher_id.x_bda_state = self.x_bda_state
                voucher_id.x_bda_comments = self.x_bda_comments

                                   
class ClientReview(models.TransientModel):
    _inherit = 'client.approve.reject.wizard'
    
    #client_approve_query_reject_date = fields.Date('Reviewed Date')
    #client_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
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
                voucher_id.client_approve_query_reject_date = datetime.now() #self.client_approve_query_reject_date
                voucher_id.client_approve_reject_by = self.env.user.id #self.client_approve_reject_by
                voucher_id.client_approve_reject_description = self.client_approve_reject_description
                voucher_id.client_redemption_pack = self.client_redemption_pack
                voucher_id.client_redemption_pack_name = self.client_redemption_pack_name


            if self.client_approve_reject_state == 'approve' and voucher_id.client_approve_reject_state == 'approve':
                
                voucher_id.status = 'bda_review'
                
                '''email_list = []
                for record_mail in self.env['res.users'].search([]):
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

                  
class BDOReview(models.TransientModel):
    _inherit = 'client.approve.reject.wizard'
    
    #bdo_approve_query_reject_date = fields.Date('Reviewed Date')
    #bdo_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
    def submit_bdo_decision(self):

        if self.x_bdo_state:
            active_id = self._context.get('active_id')
            #voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
            voucher_id = self.env['voucher.application'].browse([active_id])

            if voucher_id:
                
                if self.x_bdo_state == 'Approved':
                    voucher_id.status = 'branch_manager_review'
                    #mail_template_id = self.env.ref('nyda_voucher.voucher_status_mail_template')
                    #if mail_template_id and voucher_id.status == 'approved':
                    #   mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)                    
                else:
                    voucher_id.status = 'bda_review'
                    
                voucher_id.x_bdo_state = self.x_bdo_state
                voucher_id.bdo_approve_query_reject_date = datetime.now() #self.bdo_approve_query_reject_date
                voucher_id.bdo_approve_reject_by = self.env.user.id #self.bdo_approve_reject_by
                voucher_id.x_bdo_comments = self.x_bdo_comments
     
class PCReview(models.TransientModel):
    _inherit = 'client.approve.reject.wizard'
    
    #pc_approve_query_reject_date = fields.Date('Reviewed Date')
    #pc_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
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
                voucher_id.pc_approve_query_reject_date = datetime.now() #self.pc_approve_query_reject_date
                voucher_id.pc_approve_reject_by = self.env.user.id #self.pc_approve_reject_by
                voucher_id.x_pc_approval_date = datetime.now()
                voucher_id.x_pc_comments = self.x_pc_comments  

class HOReview(models.TransientModel):
    _inherit = 'client.approve.reject.wizard'
    
    #ho_approve_query_reject_date = fields.Date('Reviewed Date')
    #ho_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
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
                voucher_id.ho_approve_query_reject_date = datetime.now() #self.ho_approve_query_reject_date
                voucher_id.ho_approve_reject_by = self.env.user.id #self.ho_approve_reject_by
                voucher_id.x_ho_admin_comments = self.x_ho_admin_comments


class QAOReview(models.TransientModel):
    _inherit = 'client.approve.reject.wizard'
    
    #qa_approve_query_reject_date = fields.Date('Reviewed Date')
    #qa_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
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
                voucher_id.qa_approve_query_reject_date = datetime.now() #self.qa_approve_query_reject_date
                voucher_id.qa_approve_reject_by = self.env.user.id #self.qa_approve_reject_by
                voucher_id.x_qa_officer_comments = self.x_qa_officer_comments

class ProofPayment(models.TransientModel):
    _inherit = 'proof.of.payment.wiz'
    
    #proof_submitted_date = fields.Date('Product Submitted Date')
    #proof_submitted_by = fields.Many2one('res.users','Submitted By')
    
    @api.multi
    def btn_submit_proof_of_payment(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        voucher_application.status = 'payment_completed'
        voucher_application.proof_of_payment = self.proof_of_payment
        voucher_application.proof_submitted_date = datetime.now() #self.proof_submitted_date
        voucher_application.proof_submitted_by = self.env.user.id #self.proof_submitted_by
        voucher_application.proof_of_payment_name = self.proof_of_payment_name
        voucher_application.proof_of_payment_date = self.payment_date
        return True


class VoucherApplication(models.Model):
    _inherit = 'voucher.application'
    
    approved_date = fields.Datetime('Approve Date')
    approved_by = fields.Many2one('res.users','Approved By')
    
    decline_date = fields.Datetime('Decline Date')
    decline_by = fields.Many2one('res.users','Decline By')
    
    query_date = fields.Datetime('Query Date')
    query_by = fields.Many2one('res.users','Query By')
    
    sch_app_created_date = fields.Datetime('Scheduled Date')
    sch_by = fields.Many2one('res.users','Scheduled By')
    
    attendance_created_date = fields.Datetime('Uploaded Date')
    attendance_by = fields.Many2one('res.users','Uploaded By')
    
    assessment_upload_date = fields.Datetime('Uploaded Date')
    assessment_uploaded_by = fields.Many2one('res.users','Uploaded By')
    
    recommendation_date = fields.Datetime('Date Recommended')
    recommendation_by = fields.Many2one('res.users','Recommended By')
    
    approved_date = fields.Datetime('Approve Date')
    approved_by = fields.Many2one('res.users','Approved By')
    
    decline_date = fields.Datetime('Query Date')
    decline_by = fields.Many2one('res.users','Query By')
    
    query_date = fields.Datetime('Query Date')
    query_by = fields.Many2one('res.users','Query By')
    
    service_provider_selected_date = fields.Datetime('SP Select Date')
    selected_by = fields.Many2one('res.users','Selected By')
    
    voucher_sd_submitted_date = fields.Datetime('Voucher Supporting Document Date')
    voucher_sd_submitted_by = fields.Many2one('res.users','Submitted By')
    
    work_plan_date = fields.Datetime('Workplan Submitted Date')
    work_plan_by = fields.Many2one('res.users','Submitted By')
    
    product_submitted_date = fields.Datetime('Product Submitted Date')
    product_submitted_by = fields.Many2one('res.users','Submitted By')
    
    bda_approve_query_reject_date = fields.Datetime('Reviewed Date')
    bda_approve_reject_by = fields.Many2one('res.users','Reviewed By')
         
    client_approve_query_reject_date = fields.Datetime('Reviewed Date')
    client_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
    bdo_approve_query_reject_date = fields.Datetime('Reviewed Date')
    bdo_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
    pc_approve_query_reject_date = fields.Datetime('Reviewed Date')
    pc_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
    ho_approve_query_reject_date = fields.Datetime('Reviewed Date')
    ho_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
    qa_approve_query_reject_date = fields.Datetime('Reviewed Date')
    qa_approve_reject_by = fields.Many2one('res.users','Reviewed By')
    
    proof_submitted_date = fields.Datetime('Product Submitted Date')
    proof_submitted_by = fields.Many2one('res.users','Submitted By')
        
    @api.multi
    def set_approve(self):
        """ Sets state to approved and sends mail to applicant. Add logic if need anything once application is moved to approved state. """
        for rec in self:
            rec.write({'status': 'approved', 'x_pc_status': 'Approved','approved_date':datetime.now(),'approved_by':self.env.user.id})

        mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_approval_mail_template')
        if mail_template_id and self.status == 'approved':
            mail_template_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)

    @api.multi
    def set_decline(self):
        """ Sets state to declied and sends mail to applicant. Add logic if need anything once application is moved to reject state. """
        for rec in self:
            rec.write({'status': 'decline', 'x_pc_status': 'Declined','decline_date':datetime.now(),'decline_by':self.env.user.id})

            mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_declined_mail_template')
            if mail_template_id and self.status == 'decline':
                mail_template_id.with_context(user=self.env.user).send_mail(self.id, force_send=True)







    
    