# -*- coding: utf-8 -*-

from odoo import models, fields, api


class partners(models.Model):
    _name = 'nationalyouth.specialist'

    subject = fields.Char('Enquirer')
    name = fields.Char('Customer Contact Name')
    email = fields.Char('Email')
    phone = fields.Char('Contact Number')
    city = fields.Char('City')
    enquiry_channel = fields.Char('Enquiry Channel', default="NYS")
    assign_person = fields.Many2one('nationalyouth.partnerz.profile', string = "Assign to person")
    assign_team = fields.Many2one('nationalyouth.partnerz.profile', string = "Assign to team")
    priority = fields.Selection([('default', 'Default'), ('Low', 'low'), ('Medium', 'Medium'), ('High', 'High')], string="Priority")
    notes = fields.Text()
    info = fields.Text()

    state = fields.Selection([('new', 'New'), ('accepted', 'ACCEPTED FOR NYDA SERVICES'), ('declined', 'DECLINED')], default = 'accepted')

class ProjectManagement(models.Model):
    _name = 'nationalyouth.specialist.projectmanagment'

    name = fields.Char('Name', default="national")
