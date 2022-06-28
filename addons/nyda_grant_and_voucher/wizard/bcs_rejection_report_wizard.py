from datetime import date
from odoo import api, fields, models


class BCSRejectionReasonWizard(models.TransientModel):
    _name = 'bcs.rejection.reason.wizard'
    _description = 'BCS Rejection reason  Wizard'

    bcs_rejection_report = fields.Text(string="Reason for Rejection")
    bcs_rejection_report_date = fields.Date(string="Date", default=date.today())


    @api.multi
    def bcs_rejection_submit_reason(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        bsc_rsr = grant_application.write({
            'bcs_rejection_report': self.bcs_rejection_report,
            'nyda_bcs_r_bool': True,
            'nyda_bcs_bool': False,
            'nyda_branch_manager_bool': False,
            'nyda_branch_manager_r_bool': False,
        })

        grant_application.status = 'send_letter'
        return True
