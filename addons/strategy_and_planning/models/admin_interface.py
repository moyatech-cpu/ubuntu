from odoo import api, fields, models


class Divisions(models.Model):
    _name = 'divisions'
    _rec_name = 'division_name'

    division_name = fields.Char(string='Division Name')
    programme_id = fields.Many2one('programme', string='Programme')
    responsible_user = fields.Many2one('res.users', string='Responsible User')


class BusinessUnits(models.Model):
    _name = 'business.units'
    _rec_name = 'unit_name'

    unit_name = fields.Char(string='Unit Name')
    sub_programme = fields.Char(string='Sub Programme')
    division_id = fields.Many2one('divisions', string='Division ID')
    responsible_user = fields.Many2one('res.users', string='Responsible User')


class Programme(models.Model):
    _name = 'programme'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    description = fields.Char(string='description')
