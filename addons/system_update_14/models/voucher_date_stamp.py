# coding=utf-8
from odoo import api, fields, models
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo import http
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class IctCheck(models.TransientModel):
    _inherit = 'ict.wiz'
    _description = 'ITC Report'

    #ict_report = fields.Binary('ITC Report')
    #ict_report_name = fields.Char('File Name')

    @api.multi
    def ict_report_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'ict_checked'
        grant_application.ict_report_name = self.ict_report_name
        grant_application.ict_report = self.ict_report
        grant_application.ict_report_upload_date = datetime.now()
        grant_application.ict_uploaded_by = self.env.user.id
        return True

class ScheduleGrantAppointmentWizard(models.TransientModel):
    _inherit = 'schedule.grant.appointment'
    _description = 'Opens up a wizard for creating appointment and changes state'

    @api.multi
    def create_appointment(self):
        active_id = self._context.get('active_id')
        vals = {
            'name': self.name.name,
            'bdo_name': self.bdo_name.id,
            'appointment_date': self.appointment_date,
            'appointment_location': self.appointment_location
        }
        if active_id:
            fetched_record = self.env['grant.application'].browse(active_id)
            fetched_record.user_name = vals['name']
            fetched_record.bdo_name = vals['bdo_name']
            fetched_record.appointment_date = vals['appointment_date']
            fetched_record.appointment_location = vals['appointment_location']
            fetched_record.status = 'inspected'
            fetched_record.schedule_date = datetime.now()
            fetched_record.schedule_by = self.env.user.id
        # template_id = self.env.ref('nyda_grant_and_voucher.schedule_appointment_mail_template').id
        mail_template_id = self.env.ref('nyda_grant_and_voucher.grant_application_wizard_mail_template')
        if mail_template_id:
           mail_template_id.with_context(user=self.env.user).send_mail(active_id, force_send=True)


'''class ScheduleAppointmentWizard(models.TransientModel):
    _inherit = 'schedule.appointment.wizard'
    _description = 'Opens up a wizard for creating appointment and changes state'
    
    @api.multi
    def create_appointment(self):
        active_id = self.env.context.get('current_id')
        vals = {
            'name': self.name.name,
            'bdo_name': self.bdo_name.id,
            'appointment_date': self.appointment_date,
            'x_location': self.x_location
        }
        if active_id:
            fetched_record = self.env['voucher.application'].browse(active_id)
            fetched_record.user_name = vals['name']
            fetched_record.bdo_name = vals['bdo_name']
            fetched_record.appointment_date = vals['appointment_date']
            fetched_record.x_location = vals['x_location']
            fetched_record.status = 'appointment_drafted'
            fetched_record.schedule_date = datetime.now()
            fetched_record.schedule_by = self.env.user.id
        mail_template_id = self.env.ref('nyda_grant_and_voucher.schedule_appointment_mail_template')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).send_mail(active_id, force_send=True)
        return True
'''

class ApproveLetter(models.TransientModel):
    _inherit = 'approve.letter.wiz'
    _description = 'Apprival Pack'

    @api.multi
    def approve_letter_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))

        grant_application.approval_letter_name = self.approval_letter_name
        grant_application.approval_letter = self.approval_letter
        # grant_application.declaration_of_interest_name = self.declaration_of_interest_name
        # grant_application.declaration_of_interest = self.declaration_of_interest
        # grant_application.minutes_name = self.minutes_name
        # grant_application.minutes = self.minutes
        grant_application.approval_letter_upload_date = datetime.now()
        grant_application.approval_letter_upload_by = self.env.user.id
        if not grant_application.gr_number:
            grant_application.gr_number = self.env['ir.sequence'].next_by_code('gr.number')


        attachment = {
            'name': str(self.approval_letter_name),
            'datas': self.approval_letter,
            'datas_fname': self.approval_letter_name,
            'res_model': grant_application._name,
            'type': 'binary'
        }
        ir_attechment_id = self.env['ir.attachment'].create(attachment)
        approve_mail_wiz_template = self.env.ref('nyda_grant_and_voucher.approve_latter_wizard_mail_template')
        if approve_mail_wiz_template:
            approve_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]
            approve_mail_wiz_template.with_context(user=self.env.user, bda=grant_application.email).send_mail(
                grant_application.id, force_send=True)
        grant_application.status = 'sent_approval_letter'

        return True

class DeligenceReport(models.TransientModel):
    _inherit = 'deligence.wiz'
    _description = 'Due Deligence Report'

    @api.multi
    def deligence_report_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'deligence_done'
        deligence_rr = grant_application.write({
            'inspection_report_name': self.inspection_report_name,
            'inspection_report': self.inspection_report,
            'financial_assessment_name': self.financial_assessment_name,
            'financial_assessment': self.financial_assessment,
            'business_plan_name': self.business_plan_name,
            'business_plan': self.business_plan,
            'deligence_date': datetime.now(),
            'deligence_by': self.env.user.id,
        })

        return True

class InvestmentUploadMemo(models.TransientModel):
    _inherit = 'investment.memo.wiz'
    _description = 'Investment Upload Memo'

    upload_investiment_memo = fields.Binary(string='Investment memo')
    upload_investiment_memo_name = fields.Char(string='File Name')

    @api.multi
    def btn_upload_investiment_memo_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'investment_memo_upload'
        grant_application.upload_investiment_memo = self.upload_investiment_memo
        grant_application.upload_investiment_memo_name = self.upload_investiment_memo_name
        grant_application.investment_memo_upload_date = datetime.now()
        grant_application.investment_memo_upload_by = self.env.user.id
        return True

class BGARGApproveWizard(models.TransientModel):
    _inherit = 'bgarg.approve.wizard'
    _description = 'BGARC Approve Letter'

    @api.multi
    def bgarg_approve_submit(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        if not grant_application.gr_number:
            grant_application.gr_number = self.env['ir.sequence'].next_by_code('gr.number')

        bgarg_as = grant_application.write({
            'brarg_declaration_of_interest_name': self.brarg_declaration_of_interest_name,
            'bgarg_declaration_of_interest': self.bgarg_declaration_of_interest,
            'bgarg_minutes_name': self.bgarg_minutes_name,
            'bgarg_minutes': self.bgarg_minutes,
            'bgarg_approval_letter_send_date': self.bgarg_approval_letter_send_date,
            'bgarg_approve_date': datetime.now(),
            'bgarg_approve_by': self.env.user.id,
        })
        grant_application.status = 'approved'
        return True

class BGARGRejectLetter(models.TransientModel):
    _inherit = 'bgarg.reject.report.wiz'
    _description = 'BGARG Reject Reason Wizard'

    
    @api.multi
    def bgarg_reject_letter_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        bgarg_reject_lq = grant_application.write({
            'bgarg_rejection_report': self.bgarg_rejection_report,
            'bgarg_rejection_report_date': self.bgarg_rejection_report_date,
            'bgarc_declaration_of_interest_reject': self.bgarc_declaration_of_interest_reject,
            'bgarc_declaration_of_interest_name_reject': self.bgarc_declaration_of_interest_name_reject,
            'bgarc_minutes_reject': self.bgarc_minutes_reject,
            'bgarc_minutes_name_reject': self.bgarc_minutes_name_reject,
            'bgarg_reject_date': datetime.now(),
            'bgarg_reject_by': self.env.user.id,
        })
        grant_application.status = 'send_letter'

        return True

class HOGACApproveLetter(models.TransientModel):
    _inherit = 'hogac.approve.letter.wiz'
    _description = 'HOGAC Approve Letter'

    @api.multi
    def hogac_approve_letter_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'sent_approval_letter'
        # grant_application.hogac_approval_letter_name = self.hogac_approval_letter_name
        # grant_application.hogac_approval_letter = self.hogac_approval_letter
        grant_application.hogac_declaration_of_interest_name = self.hogac_declaration_of_interest_name
        grant_application.hogac_declaration_of_interest = self.hogac_declaration_of_interest
        grant_application.hogac_minutes_name = self.hogac_minutes_name
        grant_application.hogac_minutes = self.hogac_minutes
        grant_application.hogac_approval_letter_send_date = self.hogac_approval_letter_send_date
        grant_application.hogac_minutes = self.hogac_minutes
        grant_application.hogac_approve_date = datetime.now()
        grant_application.hogac_approve_by = self.env.user.id
        if not grant_application.gr_number:
            grant_application.gr_number = self.env['ir.sequence'].next_by_code('gr.number')
        attachment = {
            'name': str(self.hogac_declaration_of_interest_name),
            'datas': self.hogac_declaration_of_interest,
            'datas_fname': self.hogac_declaration_of_interest_name,
            'res_model': grant_application._name,
            'type': 'binary'
        }
        ir_attechment_id = self.env['ir.attachment'].create(attachment)
        approve_mail_wiz_template = self.env.ref('nyda_grant_and_voucher.hogac_declaration_interest_mail_template')
        if approve_mail_wiz_template:
            approve_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]
            #approve_mail_wiz_template.with_context(user=self.env.user, bda=grant_application.email).send_mail(
            #    grant_application.id, force_send=True)
        return True

class HOGACRejectLetter(models.TransientModel):
    _inherit = 'hogac.reject.report.wiz'
    _description = 'HOGAC Reject Reason Wizard'

    @api.multi
    def hogac_reject_letter_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        reject_lr = grant_application.write({
            'hogac_rejection_report': self.hogac_rejection_report,
            'hogac_rejection_report_date': self.hogac_rejection_report_date,
            'hogac_minutes_name': self.hogac_minutes_file_name,
            'hogac_minutes': self.hogac_minutes_file,
            'hogac_declaration_of_interest': None,
            'hogac_approval_letter_send_date': None,
            'hogac_reject_date': datetime.now(),
            'hogac_reject_by': self.env.user.id,

        })
        grant_application.status = 'send_letter'
        return True

class UploadSentApprovalLetter(models.TransientModel):
    _inherit = 'upload.approval.wiz'
    _description = 'Contracting'

    @api.multi
    def uploaded_approve_letter_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'uploaded_approval_letter'
        upload_alr = grant_application.write({
            'contract_name': self.contract_name,
            'contract': self.contract,
            'uploaded_approval_letter1_name': self.uploaded_approval_letter1_name,
            'uploaded_approval_letter1': self.uploaded_approval_letter1,
            'contracting_date': datetime.now(),
            'contracting_by': self.env.user.id,
        })

        return True

class DisbursementPack(models.TransientModel):
    _inherit = 'disbursement.pack.wiz'
    _description = 'Disbursement Pack'

    disbursement_amount = fields.Float('Grant Amount')

    @api.multi
    def disbursement_pack_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id')).write({
            'cover_letter' : self.cover_letter,
            'cover_letter_name' : self.cover_letter_name,
            'supplier_checklist' : self.supplier_checklist,
            'supplier_checklist_name' : self.supplier_checklist_name,
            'quatation_attech_ids' : [(6, 0, self.quatation_attech_ids.ids)],
            'bank_confirmation_ids' : [(6, 0, self.bank_confirmation_ids.ids)],
            'directors_attech_ids' : [(6, 0, self.directors_attech_ids.ids)],
            'company_registration_attech_ids' : [(6, 0, self.company_registration_attech_ids.ids)],
            'nyda_bdo_bool' : False,
            'nyda_branch_manager_bool' : False,
            'nyda_bcs_bool' : False,
            'nyda_qao_bool' : False,
            'nyda_edm_bool' : False,
            'nyda_bdo_r_bool' : False,
            'nyda_branch_manager_r_bool' : False,
            'nyda_bcs_r_bool' : False,
            'nyda_qao_r_bool' : False,
            'nyda_edm_r_bool' : False,
            'disbursement_upload_date' : datetime.now(),
            'disbursement_upload_by' : self.env.user.id,
            'disbursement_amount': self.disbursement_amount,
            'status': 'bdo_review',
        })
        # grant_application.status = 'disbursement'
        # grant_application.cover_letter = self.cover_letter
        # grant_application.cover_letter_name = self.cover_letter_name
        # grant_application.supplier_checklist = self.supplier_checklist
        # grant_application.supplier_checklist_name = self.supplier_checklist_name
        # grant_application.quatation_attech_ids = [(6, 0, self.quatation_attech_ids.ids)]
        # grant_application.bank_confirmation_ids = [(6, 0, self.bank_confirmation_ids.ids)]
        # grant_application.directors_attech_ids = [(6, 0, self.directors_attech_ids.ids)]
        # grant_application.company_registration_attech_ids = [(6, 0, self.company_registration_attech_ids.ids)]
        #
        # grant_application.nyda_bdo_bool = False
        # grant_application.nyda_branch_manager_bool = False
        # grant_application.nyda_bcs_bool = False
        # grant_application.nyda_qao_bool = False
        # grant_application.nyda_edm_bool = False
        #
        # grant_application.nyda_bdo_r_bool = False
        # grant_application.nyda_branch_manager_r_bool = False
        # grant_application.nyda_bcs_r_bool = False
        # grant_application.nyda_qao_r_bool = False
        # grant_application.nyda_edm_r_bool = False
        # grant_application.status = 'bdo_review'


        # grant_application.quatation_attech_name = self.quatation_attech_name
        # grant_application.bank_confirmation_name = self.bank_confirmation_name
        # grant_application.director_ide_name = self.director_ide_name
        # grant_application.company_registration_doc = self.company_registration_doc
        # grant_application.company_registration_doc_name = self.company_registration_doc_name
        # grant_application.tax_clearance_doc = self.tax_clearance_doc
        # grant_application.tax_clearance_doc_name = self.tax_clearance_doc_name

        return True

class BdoRejectWiz(models.TransientModel):
    _inherit = 'bdo.accept.confirm.wizard'
    _description = 'BDO Accept Confirm Wizard'

    @api.multi
    def submit_confirm(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        submit_c = grant_application.write({
            'nyda_bdo_bool': True,
            'nyda_bdo_r_bool': False,
            'nyda_branch_manager_r_bool': False,
            'nyda_branch_manager_bool': False,
            'bdo_approve_date': datetime.now(),
            'bdo_approver': self.env.user.id,

        })
        grant_application.status = 'branch_manager_review'
        return True

class BdoRejectionReasonWizard(models.TransientModel):
    _inherit = 'bdo.rejection.reason.wizard'
    _description = 'BDO Rejection reason  Wizard'

    @api.multi
    def submit_reason(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        # grant_application.reason_text = self.bdo_rejection_reason
        submit_r = grant_application.write({
            'bdo_rejection_report': self.bdo_rejection_report,
            'nyda_bdo_r_bool': True,
            'nyda_bdo_bool': False,
            'bdo_reject_date': datetime.now(),
            'bdo_reject_by': self.env.user.id,
            
        })
        #grant_application.status = 'send_letter'        
        grant_application.status = 'uploaded_approval_letter'
        
        return True

class BdoRejectWiz(models.TransientModel):
    _inherit = 'bm.accept.confirm.wizard'
    _description = 'BM Accept Confirm Wizard'

    @api.multi
    def submit_confirm(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        submit_c = grant_application.write({
            'nyda_branch_manager_bool': True,
            'nyda_branch_manager_r_bool': False,
            'nyda_bcs_r_bool': False,
            'nyda_bcs_bool': False,
            'bm_approve_date': datetime.now(),
            'bm_approve_user': self.env.user.id,

        })
        grant_application.status = 'disbursement'
        return True

class BmRejectionReportWizard(models.TransientModel):
    _inherit = 'bm.rejection.report.wizard'
    _description = 'BM Rejection report  Wizard'

    @api.multi
    def submit_bm_rejection_report(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        submit_bm_rej = grant_application.write({
            'bm_rejection_report': self.bm_rejection_report,
            'bm_rejection_report_date': self.bm_rejection_report_date,
            'nyda_branch_manager_r_bool': True,
            'nyda_branch_manager_bool': False,
            'nyda_bdo_bool': False,
            'nyda_bdo_r_bool': False,
            'bm_reject_date': datetime.now(),
            'bm_reject_user': self.env.user.id,

        })
        grant_application.status = 'bdo_review'

        return True

class BdoRejectWiz(models.TransientModel):
    _inherit = 'bsc.accept.confirm.wizard'
    _description = 'BCS Accept Confirm Wizard'


    @api.multi
    def submit_confirm(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        submit_c = grant_application.write({
            'nyda_bcs_bool': True,
            'nyda_bcs_r_bool': False,
            'nyda_qao_r_bool': False,
            'nyda_qao_bool': False,
            'bcs_approve_date': datetime.now(),
            'bcs_approve_by': self.env.user.id,

        })
        grant_application.status = 'bcs_approved'
        return True

class BCSRejectionReasonWizard(models.TransientModel):
    _inherit = 'bcs.rejection.reason.wizard'
    _description = 'BCS Rejection reason  Wizard'

    @api.multi
    def bcs_rejection_submit_reason(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        bsc_rsr = grant_application.write({
            'bcs_rejection_report': self.bcs_rejection_report,
            'nyda_bcs_r_bool': True,
            'nyda_bcs_bool': False,
            'nyda_branch_manager_bool': False,
            'nyda_branch_manager_r_bool': False,
            'bcs_reject_date': datetime.now(),
            'bcs_reject_user': self.env.user.id,

        })

        grant_application.status = 'send_letter'
        return True


class BdoRejectWiz(models.TransientModel):
    _inherit = 'qao.accept.confirm.wizard'
    _description = 'QAO Accept Confirm Wizard'

    @api.multi
    def submit_confirm(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.nyda_qao_bool = True
        grant_application.nyda_qao_r_bool = False
        grant_application.nyda_edm_r_bool = False
        grant_application.nyda_edm_bool = False
        grant_application.qao_approve_date = datetime.now()
        grant_application.qao_approve_by = self.env.user.id
        grant_application.status = 'qao_approved'
        return True

class QaoRejectionReasonWizard(models.TransientModel):
    _inherit = 'qao.rejection.report.wizard'
    _description = 'QAO Rejection reason  Wizard'

    @api.multi
    def qao_rejection_submit_reason(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.qao_rejection_report = self.qao_rejection_report
        grant_application.nyda_qao_r_bool = True
        grant_application.nyda_qao_bool = False
        grant_application.nyda_bcs_bool = False
        grant_application.nyda_bcs_r_bool = False
        grant_application.status = 'disbursement'
        grant_application.qao_reject_date = datetime.now()
        grant_application.qao_reject_by = self.env.user.id
        return True

class BdoRejectWiz(models.TransientModel):
    _inherit = 'edm.accept.confirm.wizard'
    _description = 'EDM Accept Confirm Wizard'


    @api.multi
    def submit_confirm(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.nyda_edm_bool = True
        grant_application.nyda_edm_r_bool = False
        grant_application.status = 'edm_approved'
        grant_application.edm_approve_date = datetime.now()
        grant_application.edm_approve_by = self.env.user.id

        return True

class EDMRejectionReasonWizard(models.TransientModel):
    _inherit = 'edm.rejection.reason.wizard'
    _description = 'EDM Rejection reason  Wizard'

    @api.multi
    def edm_rejection_submit_reason(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        # grant_application.reason_text = self.bdo_rejection_reason
        edm_rej = grant_application.write({
            'edm_rejection_report': self.edm_rejection_report,
            'nyda_edm_r_bool': True,
            'nyda_edm_bool': False,
            'nyda_qao_bool': False,
            'nyda_qao_r_bool': False,
            'edm_reject_date': datetime.now(),
            'edm_reject_user': self.env.user.id,
        })

        grant_application.status = 'bcs_approved'
        return True

class GrantApplication(models.Model):
    _inherit = 'grant.application'
    
    hogac_approve_date = fields.Datetime('Approve date')
    hogac_approve_by = fields.Many2one('res.users','Approve by')

    ict_report_upload_date = fields.Datetime('Upload Date')
    ict_uploaded_by = fields.Many2one('res.users','Uploaded By')
    
    schedule_date = fields.Datetime('Scheduled Date')
    schedule_by = fields.Many2one('res.users','Scheduled By')
    
    approval_letter_upload_date = fields.Datetime('Upload Date')
    approval_letter_upload_by = fields.Many2one('res.users','Uploaded By')

    deligence_date = fields.Datetime('Deligence Date')
    deligence_by = fields.Many2one('res.users','Deligence By')

    investment_memo_upload_date = fields.Datetime('Upload Date')
    investment_memo_upload_by = fields.Many2one('res.users','Uploaded By')

    bgarg_approve_date = fields.Datetime('Approve Date')
    bgarg_approve_by = fields.Many2one('res.users','Approve By')

    bgarg_reject_date = fields.Datetime('Reject Date')
    bgarg_reject_by = fields.Many2one('res.users','Reject By')

    hogac_reject_date = fields.Datetime('Reject Date')
    hogac_reject_by = fields.Many2one('res.users','Reject By')

    contracting_date = fields.Datetime('Contracting Date')
    contracting_by = fields.Many2one('res.users','Contracting By')
    
    disbursement_upload_date = fields.Datetime('Disbursement Date')
    disbursement_upload_by = fields.Many2one('res.users','Disbursement By')
    disbursement_amount = fields.Float('Grant Amount')


    bdo_approve_date = fields.Datetime('BDO Approve Date')
    bdo_approver = fields.Many2one('res.users','Bod Approve By')

    bdo_reject_date = fields.Datetime('BDO Reject Date')
    bdo_reject_by = fields.Many2one('res.users','BDO Reject By')
    
    bm_approve_date = fields.Datetime('BM Approve Date')
    bm_approve_user = fields.Many2one('res.users','BM Approve By')

    bm_reject_date = fields.Datetime('BM Approve Date')
    bm_reject_user = fields.Many2one('res.users','BM Approve By')

    bcs_approve_date = fields.Datetime('BCS Approve Date')
    bcs_approve_by = fields.Many2one('res.users','BCS Approve By')

    bcs_reject_date = fields.Datetime('BCS Reject Date')
    bcs_reject_user   = fields.Many2one('res.users','BCS Reject By')
    
    qao_approve_date = fields.Datetime('QAO Approve Date')
    qao_approve_by  = fields.Many2one('res.users','QAO Approve By')

    qao_reject_date = fields.Datetime('QAO reject date')
    qao_reject_by = fields.Many2one('res.users','QAO reject By')

    edm_approve_date = fields.Datetime('EDM Approve Date')
    edm_approve_by = fields.Many2one('res.users','EDM Approved By')

    edm_reject_date = fields.Datetime('EDM Reject Date')
    edm_reject_user = fields.Many2one('res.users','EDM Reject By')

    gr_number = fields.Char('GR #',store=True)

class YouthEnquiry(models.Model):
    _inherit = 'youth.enquiry'
    
    bmt_training_certificate = fields.Binary('BMT Certificate')
    bmt_training_certificate_name = fields.Char('BMT File Name')
    bmt_certi_upload_date = fields.Datetime('Upload Date')
    training_type = fields.Selection(
        [('gyb', 'GYBI - 3 days'),('syb', 'SYB - 5 days'),
         ('iyb_one', 'IYB 1 - 5 days'),
         ('iyb_two', 'IYB 2 - 5 days'), ('syb_coops', 'SYB/Co-ops - 3 days')],
        string="Course")

class ClientPreassessment(models.Model):
    _inherit = 'client.preassessment'

    state = fields.Selection(selection_add=[('cancelled', 'Cancelled')])

class CancelledPreassessment(models.TransientModel):
    _inherit = 'client.preassessment.cancel.wizard'

    @api.multi
    def cancel_assessment(self):
        assessment = self.env['client.preassessment'].browse(self._context.get('active_id'))
        cancel_assess = assessment.write({
            'cancel_assessment_reason': self.cancel_assessment_reason,
            'current_state': assessment.state,
            'state': 'cancelled'
        })
        
    @api.multi
    def reinstate_assessment(self):
        assessment = self.env['client.preassessment'].browse(self._context.get('active_id'))
        reinstate_assess = assessment.write({
            'reinstate_assessment_reason': self.reinstate_assessment_reason,
            'state': assessment.current_state,
            'cancel_state': False,
        })



