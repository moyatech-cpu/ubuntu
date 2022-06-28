from datetime import date
from odoo import api, fields, models


class BdoRejectWiz(models.TransientModel):
    _name = 'bdo.accept.confirm.wizard'
    _description = 'BDO Accept Confirm Wizard'

    bdo_confirm_text = fields.Text(default="I hereby confirm that I have reviewed all the documents neccesary or required by the program to the best of my knowledge. I confirm that all the documents reviewed under my authority are present and are appropriate. I hereby confirm that the applicant's application review was conducted by myself.")

    @api.multi
    def submit_confirm(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        submit_c = grant_application.write({
            'nyda_bdo_bool': True,
            'nyda_bdo_r_bool': False,
            'nyda_branch_manager_r_bool': False,
            'nyda_branch_manager_bool': False,

        })
        grant_application.status = 'branch_manager_review'
        return True
