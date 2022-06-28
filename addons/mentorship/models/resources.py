# coding=utf-8
from odoo import api, fields, models, _


class legalEntity(models.Model):
    _name = 'legal.entity'

    name = fields.Char(string='Name')


class areasSupport(models.Model):
    _name = 'areas.support'

    name = fields.Char(string='Name')


class mentoringSupport(models.Model):
    _name = 'mentoring.support'

    name = fields.Char(string='Name')


class skillsTraining(models.Model):
    _name = 'skills.training'

    menteeApplication_id = fields.Many2one('mentee.application', string='')
    course = fields.Char(string='Course')
    institutionOrganisation = fields.Char(string='Institution/ Organisation')
    duration = fields.Char(string='Duration')
    when = fields.Date(string="When")


class motivation(models.Model):
    _name = 'motivation'

    menteeApplication_id = fields.Many2one('mentee.application', string='')
    motivationText = fields.Text(string='Write Something that motivates you !!! ')
