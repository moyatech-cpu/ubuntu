from datetime import date
from odoo import api, fields, models


class BdoRejectWiz(models.TransientModel):
    _name = 'qao.accept.confirm.wizard'
    _description = 'QAO Accept Confirm Wizard'

    qao_confirm_text = fields.Text(default="I hereby confirm that I have reviewed all the documents neccesary or required by the program to the best of my knowledge. I confirm that all the documents reviewed under my authority are present and are appropriate. I hereby confirm that the applicant's application review was conducted by myself.")


    @api.multi
    def submit_confirm(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.nyda_qao_bool = True
        grant_application.nyda_qao_r_bool = False
        grant_application.nyda_edm_r_bool = False
        grant_application.nyda_edm_bool = False
        grant_application.status = 'qao_approved'
        return True
