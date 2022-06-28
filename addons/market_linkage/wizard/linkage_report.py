from odoo import api, fields, models
from odoo.exceptions import UserError

class LinkageReport(models.TransientModel):
    _name = 'linkage.report'
    _description = 'Linkage Report'

    # linkage_report = fields.Binary('Linkage Report')
    # file_name = fields.Char('File Name')
    signed_contrct_report = fields.Binary('Signed Contract/Invoice/Letter of Appointment')
    signed_contrct_file_name = fields.Char('Linkage File Name')
    beneficiary_ver_report = fields.Binary('Beneficiary Verification Form')
    beneficiary_ver_file_name = fields.Char('Linkage File Name')
    jobs_ver_report = fields.Binary('Jobs Verification Form')
    jobs_ver_name = fields.Char('Linkage File Name')
    monthly_report = fields.Binary('Monthly Report')
    monthly_file_name = fields.Char('Linkage File Name')
    # linkage_report_ids = fields.One2many('linkage.report',Sting="Linkage Report")

    @api.multi
    def linkage_report_req(self):
        user = self.env['register.opportunity'].browse(self._context.get('active_id'))
        # user.state = 'linkage_report'
        # user.linkage_file_name =  self.file_name
        # user.linkage_report = self.linkage_report
        user.signed_contrct_file_name = self.signed_contrct_file_name
        user.signed_contrct_report = self.signed_contrct_report
        user.beneficiary_ver_file_name = self.beneficiary_ver_file_name
        user.beneficiary_ver_report = self.beneficiary_ver_report
        user.jobs_ver_name =  self.jobs_ver_name
        user.jobs_ver_report = self.jobs_ver_report
        user.monthly_file_name = self.monthly_file_name
        user.monthly_report = self.monthly_report
        if user.signed_contrct_file_name or user.beneficiary_ver_file_name or user.jobs_ver_name or user.monthly_file_name:
        	user.state = 'linkage_report'
        else :
        	raise UserError('Please upload a report')
        return True

