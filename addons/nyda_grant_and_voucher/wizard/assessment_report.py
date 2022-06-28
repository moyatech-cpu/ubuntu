from odoo import api, fields, models

class AssessmentReport(models.TransientModel):
    _name = 'assessment.report'
    _description = 'BMT Certificate Upload'

    assessment_report = fields.Binary('Assessment Report')
    assessment_report_name = fields.Char('File Name')

    @api.multi
    def assessment_report_req(self):
        grant_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        print('---', self._context.get('active_id'))
        assessment_rq = grant_application.write({
            'assessment_report_name': self.assessment_report_name,
            'assessment_report': self.assessment_report,
        })
        grant_application.status = 'assessment_report'
        return True

    @api.multi
    def attendance_register_req(self):
        grant_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        print('---', self._context.get('active_id'))
        assessment_rq = grant_application.write({
            'x_attendance_register_name': self.x_attendance_register_name,
            'x_attendance_register': self.x_attendance_register,
        })
        return True
    
    @api.multi
    def bmt_certificate_req(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        print('---', self._context.get('active_id'))
        assessment_rq = voucher_application.write({
            'x_bmt_certificate_name': self.x_bmt_certificate_name,
            'x_bmt_certificate': self.x_bmt_certificate,
        })

        voucher_application.x_voucher_number = self.env['ir.sequence'].next_by_code('voucher.issuance.number') or _('New')
        voucher_application.status = 'work_plan'
        return True    