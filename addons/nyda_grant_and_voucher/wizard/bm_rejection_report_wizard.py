from datetime import date
from odoo import api, fields, models


class BmRejectionReportWizard(models.TransientModel):
    _name = 'bm.rejection.report.wizard'
    _description = 'BM Rejection report  Wizard'

    bm_rejection_report = fields.Text(string="Reason for Rejection")
    bm_rejection_report_date = fields.Date(string="Date", default=date.today())

    @api.multi
    def submit_bm_rejection_report(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        submit_bm_rej = grant_application.write({
            'bm_rejection_report': self.bm_rejection_report,
            'bm_rejection_report_date': self.bm_rejection_report_date,
            'nyda_branch_manager_r_bool': True,
            'nyda_branch_manager_bool': False,
            'nyda_bdo_bool': False,
            'nyda_bdo_r_bool': False

        })
        grant_application.status = 'bdo_review'

        return True
