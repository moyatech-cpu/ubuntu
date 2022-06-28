from datetime import date
from odoo import api, fields, models


class BdoRejectWiz(models.TransientModel):
    _name = 'bdo.reject.wiz'
    _description = 'BDO Rejection Wizard'

    bdo_reason_text = fields.Text(string="Reason for Rejection")


    @api.multi
    def submit_reason(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        voucher_application.bdo_reason_text = self.bdo_reason_text
        voucher_application.status = 'new'
        return True
