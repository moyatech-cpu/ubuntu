from datetime import date
from odoo import api, fields, models


class BdoRejectWiz(models.TransientModel):
    _name = 'bm.accept.confirm.wizard'
    _description = 'BM Accept Confirm Wizard'

    bm_confirm_text = fields.Text(default="I hereby confirm that I have reviewed all the documents neccesary or required by the program to the best of my knowledge. I confirm that all the documents reviewed under my authority are present and are appropriate. I hereby confirm that the applicant's application review was conducted by myself.")


    @api.multi
    def submit_confirm(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        submit_c = grant_application.write({
            'nyda_branch_manager_bool': True,
            'nyda_branch_manager_r_bool': False,
            'nyda_bcs_r_bool': False,
            'nyda_bcs_bool': False,

        })
        grant_application.status = 'disbursement'
        return True
