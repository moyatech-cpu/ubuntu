from odoo import api, fields, models


class ClientApproveRejectWizaed(models.TransientModel):
    _name = 'recommendation.note'
    _description = 'recommendation note'
    x_recommended_service = fields.Many2many('business.development.assistance',string="Service")
    recommendationnote = fields.Char(string='Recommendation Note')

    @api.multi
    def default_recommendationnote(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        print('-----...', voucher_application)
        voucher_application.write({
            'x_recommended_service': [(6, 0, self.x_recommended_service.ids)],
            'recommendationnote': self.recommendationnote,
        })
        return True
