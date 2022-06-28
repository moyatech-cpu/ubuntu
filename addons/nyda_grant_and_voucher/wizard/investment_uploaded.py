from datetime import date
from odoo import api, fields, models


class InvestmentUploadMemo(models.TransientModel):
    _name = 'investment.memo.wiz'
    _description = 'Investment Upload Memo'

    upload_investiment_memo = fields.Binary(string='Investment memo')
    upload_investiment_memo_name = fields.Char(string='File Name')

    @api.multi
    def btn_upload_investiment_memo_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id'))
        grant_application.status = 'investment_memo_upload'
        grant_application.upload_investiment_memo = self.upload_investiment_memo
        grant_application.upload_investiment_memo_name = self.upload_investiment_memo_name
        return True
