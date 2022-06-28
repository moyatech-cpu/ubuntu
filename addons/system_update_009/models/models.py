from odoo import api, fields, models

class SystemUpdate_009(models.TransientModel):
    
    _inherit = 'query.pcbc'
    
    voucher_id = fields.Many2one('voucher.application', string='Voucher Application ID')
    email = fields.Char(string="Beneficiary Email", default=lambda self: self.get_beneficiary_email())

    @api.multi
    def get_beneficiary_email(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        if voucher_application:
            return voucher_application.email
    
    @api.multi
    def querypcbc(self):
        voucher_application = self.env['voucher.application'].browse(self._context.get('active_id'))
        reject_v = voucher_application.write({
            'query_pcbc': self.query_pcbc,
            'status'     : 'assessment_report',
        })
   
        return True
    
class SystemUpdate_009_Inherit_Voucher(models.Model):
    
    _inherit = 'voucher.application'
    
    @api.multi
    def set_refer(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Any Query',
            'res_model': 'query.pcbc',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_voucher_id': self.id}
        }