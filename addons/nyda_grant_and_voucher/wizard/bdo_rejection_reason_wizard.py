from datetime import date
from odoo import api, fields, models


class BdoRejectionReasonWizard(models.TransientModel):
    _name = 'bdo.rejection.reason.wizard'
    _description = 'BDO Rejection reason  Wizard'

    bdo_rejection_report = fields.Text(string="Reason for Rejection")
    bdo_rejection_report_date = fields.Date(string="Date", default=date.today())


    @api.multi
    def submit_reason(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        # grant_application.reason_text = self.bdo_rejection_reason
        submit_r = grant_application.write({
            'bdo_rejection_report': self.bdo_rejection_report,
            'nyda_bdo_r_bool': True,
            'nyda_bdo_bool': False,
        })
        #grant_application.status = 'send_letter'        
        #grant_application.status = 'reject'
        # LM Mahasha 2021/11/05
        grant_application.status = 'approved'
        
        return True
