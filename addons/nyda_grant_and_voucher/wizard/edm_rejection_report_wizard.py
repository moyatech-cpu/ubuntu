from datetime import date
from odoo import api, fields, models


class EDMRejectionReasonWizard(models.TransientModel):
    _name = 'edm.rejection.reason.wizard'
    _description = 'EDM Rejection reason  Wizard'

    edm_rejection_report = fields.Text(string="Reason for Rejection")
    edm_rejection_report_date = fields.Date(string="Date", default=date.today())


    @api.multi
    def edm_rejection_submit_reason(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        # grant_application.reason_text = self.bdo_rejection_reason
        edm_rej = grant_application.write({
            'edm_rejection_report': self.edm_rejection_report,
            'nyda_edm_r_bool': True,
            'nyda_edm_bool': False,
            'nyda_qao_bool': False,
            'nyda_qao_r_bool': False
        })

        grant_application.status = 'bcs_approved'
        return True
