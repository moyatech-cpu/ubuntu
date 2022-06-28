from datetime import date
from odoo import api, fields, models


class QaoRejectionReasonWizard(models.TransientModel):
    _name = 'qao.rejection.report.wizard'
    _description = 'QAO Rejection reason  Wizard'

    qao_rejection_report = fields.Text(string="Reason for Rejection")
    qao_rejection_report_date = fields.Date(string="Date", default=date.today())


    @api.multi
    def qao_rejection_submit_reason(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.qao_rejection_report = self.qao_rejection_report
        grant_application.nyda_qao_r_bool = True
        grant_application.nyda_qao_bool = False
        grant_application.nyda_bcs_bool = False
        grant_application.nyda_bcs_r_bool = False
        grant_application.status = 'disbursement'
        return True
