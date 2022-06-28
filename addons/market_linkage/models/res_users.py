from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    beneficiary_count = fields.Integer(compute='_get_beneficiary',string= 'Beneficiary Count')

    @api.multi
    def _get_beneficiary(self):
        for res in self:
            beneficiary_count = self.env['register.opportunity'].search_count([('match_b_ids', 'in', res.id)])
            res.beneficiary_count = beneficiary_count

    def btn_get_beneficiary(self):
        return True

    @api.multi
    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        self.env['ir.rule'].sudo().clear_cache()
        return res