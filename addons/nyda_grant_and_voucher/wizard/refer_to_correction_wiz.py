from datetime import date
from odoo import api, fields, models


class ReferToCorrection(models.TransientModel):
    _name = 'refer.correction'
    _description = 'refer to correction in HOGAC Approve'

    refer_correction = fields.Text(string="Description")
    correction_date = fields.Date(string="Date", default=date.today())


    @api.multi
    def rejection_submit_reason(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.refer_correction = self.refer_correction
        grant_application.correction_date = self.correction_date

        grant_application.status = 'bgarg_review'
        return True
