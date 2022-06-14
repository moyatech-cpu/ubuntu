# coding=utf-8
from odoo import api, fields, models, _


class ResDistrict(models.Model):
    """ Districts as per Provinces """
    _name = 'res.district'
    _description = 'Districts per Province for more in-depth localizations. '

    name = fields.Char('Name')
    state_id = fields.Many2one('res.country.state', string="Province", domain="[('country_id.name', '=', 'South Africa')]")
    country_id = fields.Many2one('res.country', related="state_id.country_id", string="Country")


class ResMunicipality(models.Model):
    """Municipality as per Districts"""
    _name = 'res.municipality'
    _description = 'Municipality per Districts for more in-depth localizations. '

    name = fields.Char('Name')
    district_id = fields.Many2one('res.district', string="District")
    state_id = fields.Many2one('res.country.state', related="district_id.state_id", string="State")
    country_id = fields.Many2one('res.country', related="district_id.country_id", string="Country")


class ResBranch(models.Model):
    """ Branches for Beneficiary Data. """
    _name = 'res.branch'
    _description = 'Branch data for Beneficiary departments. '

    name                = fields.Char('Name')
    sequence            = fields.Integer('Number', default=0)
    state_id            = fields.Many2one('res.country.state', string="Province", domain="[('country_id.name', '=', 'South Africa')]")
    country_id          = fields.Many2one('res.country', related="state_id.country_id", string="Country")
    manager_id          = fields.Many2one('res.users', string="Branch Manager")
    branch_admin_id     = fields.Many2one('res.users', string="Branch Admin")
    communication_agent = fields.Many2one('res.users', string="Communication Agent")


class EnquiryTeam(models.Model):
    """ Teams that are created to attend Enquiry. """
    _name = "enquiry.team"
    _description = "Teams object created to apply on Enquiry."

    name = fields.Char('Team Name')
    team_member_ids = fields.One2many('enquiry.team.members', 'enquiry_team_id', string="Team Members")


class ResUsersInherit(models.Model):
    """ Add Users to Teams. """
    _name = "enquiry.team.members"
    _description = "Add Users to teams"

    user_id = fields.Many2one('res.users', string="Member")
    enquiry_team_id = fields.Many2one('enquiry.team', string='Enquiry Team')


class ResMetroMunicipality(models.Model):
    """ Metro municipality model."""
    _name = "res.metro.municipality"
    _description = "Metro Municipality object."

    name = fields.Char("Metro Municipality")
    state_id = fields.Many2one('res.country.state', string="Province", domain="[('country_id.name', '=', 'South Africa')]")
    country_id = fields.Many2one('res.country', related="state_id.country_id", string="Country")
