# -*- coding: utf-8 -*-

from odoo import models, fields, api

class partners(models.Model):
    _name = 'nationalyouth.specialist'

    subject = fields.Char('Subject')
    name = fields.Char('Customer Contact Name')
    email = fields.Char('Email')
    phone = fields.Char('Contact Number')
    assign_person = fields.Many2one('nationalyouth.partnerz.profile', string = "Assign to person")
    assign_team = fields.Many2one('nationalyouth.partnerz.profile', string = "Assign to team")
    priority = fields.Selection([('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], string="Previous Volunteer Experience")
    notes = fields.Text()
    info = fields.Text()