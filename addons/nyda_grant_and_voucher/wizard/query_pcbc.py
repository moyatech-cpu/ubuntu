from odoo import api, fields, models

class QueryPcbc(models.TransientModel):
    _name = 'query.pcbc'
    _description = 'Query PCBC'

    query_pcbc = fields.Text(string='Any Query')

    @api.multi
    def querypcbc(self):
        grant_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        reject_v = grant_application.write({
            'query_pcbc': self.query_pcbc,
        })
        return True