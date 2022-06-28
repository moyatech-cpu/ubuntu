from odoo import api, fields, models


class TeamWiz(models.TransientModel):
    _name = 'team.wiz'
    _description = 'Team Wizard'

    team_id = fields.Many2one('enquiry.team', string="Team")

    @api.multi
    def assign_team(self):
        active_model = self._context.get('active_model')
        active_id = self._context.get('active_id')
        browse_record = self.env[active_model].browse(active_id)
        browse_record.state = 'accepted'
        browse_record.team_id = self.team_id
        browse_record.is_pending = False
        return True
