from datetime import date
from odoo import api, fields, models


class ApproveLetter(models.TransientModel):
    _name = 'approve.letter.wiz'
    _description = 'Apprival Pack'

    approval_letter = fields.Binary(string='Approval Letter')
    approval_letter_name = fields.Char(string='File Name')
    # declaration_of_interest = fields.Binary(string='Declaration Of Interest')
    # declaration_of_interest_name = fields.Char(string='File Name')
    # minutes = fields.Binary(string='Minutes')
    # minutes_name = fields.Char(string='File Name')
    approval_letter_send_date = fields.Date(string="Date", default=date.today())

    @api.multi
    def approve_letter_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))

        grant_application.approval_letter_name = self.approval_letter_name
        grant_application.approval_letter = self.approval_letter
        # grant_application.declaration_of_interest_name = self.declaration_of_interest_name
        # grant_application.declaration_of_interest = self.declaration_of_interest
        # grant_application.minutes_name = self.minutes_name
        # grant_application.minutes = self.minutes
        grant_application.approval_letter_send_date = self.approval_letter_send_date

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
            approve_mail_wiz_template.attachment_ids = [(6, 0, [])]
            approve_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]
            approve_mail_wiz_template.with_context(user=self.env.user, bda=grant_application.email).send_mail(
                grant_application.id, force_send=True)
        grant_application.status = 'sent_approval_letter'

        return True


class HOGACApproveLetter(models.TransientModel):
    _name = 'hogac.approve.letter.wiz'
    _description = 'HOGAC Approve Letter'

    hogac_approval_letter = fields.Binary(string='Approval Letter')
    hogac_approval_letter_name = fields.Char(string='File Name')
    hogac_declaration_of_interest = fields.Binary(string='Declaration Of Interest')
    hogac_declaration_of_interest_name = fields.Char(string='File Name')
    hogac_minutes = fields.Binary(string='Minutes')
    hogac_minutes_name = fields.Char(string='File Name')
    hogac_approval_letter_send_date = fields.Date(string="Date", default=date.today())

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
        grant_application.status = 'approved'
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
            approve_mail_wiz_template.attachment_ids = [(6, 0, [])]
            approve_mail_wiz_template.attachment_ids = [(4, ir_attechment_id.id)]
            #approve_mail_wiz_template.with_context(user=self.env.user, bda=grant_application.email).send_mail(
            #    grant_application.id, force_send=True)
        return True


class HOGACRejectLetter(models.TransientModel):
    _name = 'hogac.reject.report.wiz'
    _description = 'HOGAC Reject Reason Wizard'

    hogac_rejection_report = fields.Text(string="HOGAC Rejection Reason")
    hogac_rejection_report_date = fields.Date(string="HOGAC Rejection Date", default=date.today())
    hogac_minutes_file = fields.Binary(string='Minutes')
    hogac_minutes_file_name = fields.Char(string='Minutes File Name')

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
        })
        grant_application.status = 'send_letter'
        return True


class BGARGRejectLetter(models.TransientModel):
    _name = 'bgarg.reject.report.wiz'
    _description = 'BGARG Reject Reason Wizard'

    bgarg_rejection_report = fields.Text(string="BGARC Rejection Reason")
    bgarc_declaration_of_interest_reject = fields.Binary(string='Declaration Of Interest')
    bgarc_declaration_of_interest_name_reject = fields.Char(string='File Name')
    bgarc_minutes_reject = fields.Binary(string='Minutes')
    bgarc_minutes_name_reject = fields.Char(string='File Name')

    bgarg_rejection_report_date = fields.Date(string="BGARC Rejection Date", default=date.today())

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
        })
        grant_application.status = 'send_letter'

        return True


class UploadSentApprovalLetter(models.TransientModel):
    _name = 'upload.approval.wiz'
    _description = 'Contracting'

    contract = fields.Binary(String='Contract')
    contract_name = fields.Char(String='File Name')

    uploaded_approval_letter1 = fields.Binary(String='Signed Letter')
    uploaded_approval_letter1_name = fields.Char(String='File Name')

    @api.multi
    def uploaded_approve_letter_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'uploaded_approval_letter'
        upload_alr = grant_application.write({
            'contract_name': self.contract_name,
            'contract': self.contract,
            'uploaded_approval_letter1_name': self.uploaded_approval_letter1_name,
            'uploaded_approval_letter1': self.uploaded_approval_letter1,
        })

        return True
