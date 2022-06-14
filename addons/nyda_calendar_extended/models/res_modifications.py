# coding=utf-8
from odoo import api, fields, models, _


class ResCommittee(models.Model):
    """ Committee model for NYDA to add calendar events. """
    _name = 'res.committee'

    name = fields.Char('Name')
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    member_ids = fields.One2many('res.committee.members', 'committee_id', string="Committee Members")


class ResCommitteeMembers(models.Model):
    """ Committee Members model """
    _name = 'res.committee.members'

    committee_id = fields.Many2one('res.committee', string="Committee")
    member_id = fields.Many2one('res.users', string="Member")
    member_partner_id = fields.Many2one('res.partner', related='member_id.partner_id', string="Member")
