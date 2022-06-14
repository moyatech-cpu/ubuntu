# coding=utf-8
from odoo import api, fields, models, _


class MeetingInherit(models.Model):
    """ Inheriting Meeting model to add commette in calendar event. """
    _inherit = 'calendar.event'

    @api.model
    def _get_committee(self):
        """ Getting all the available committee records from database. """
        return self.env['res.committee'].search([]).ids

    committee_id = fields.Many2one('res.committee', string="Committee", default=_get_committee)

    @api.model
    def create(self, values):
        """ Adding selected committee members to participants. """
        if values['committee_id']:
            partner_ids = values['partner_ids'][0][-1]
            member_ids = self.env['res.committee'].browse(values['committee_id']).member_ids
            for member in member_ids:
                partner_ids.append(member.member_partner_id.id)
            values['partner_ids'][0][-1] = partner_ids
        return super(MeetingInherit, self).create(values)
