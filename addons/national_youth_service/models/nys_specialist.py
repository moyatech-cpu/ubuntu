# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

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


class ProjectOpportunities(models.Model):
    _name = 'nationalyouth.specialist.events'

    due = fields.Datetime('date')
    title = fields.Char('Event Name')
    country = fields.Char('Country', default="South Africa")
    attendees =  fields.Many2one('nationalyouth.partnerz.profile')
    color = fields.Integer()
    organiser = fields.Selection([('National Youth Development Agency', 'National Youth Development Agency'), ('Low', 'low'), ('Medium', 'Medium'), 
    ('High', 'High')], string="Priority", default="National Youth Development Agency")
    # address fields
    address_line1 = fields.Char('Address')
    address_line2 = fields.Char(' ')
    address_line3 = fields.Char(' ')
    address_line4 = fields.Selection([('Mpumalanga', 'Mpumalanga'), ('Gauteng', 'Gauteng'), ('Free State', 'Free State'), ('Kwazulu-natal', 'Kwazulu-natal'),
    ('North West', 'North West'), ('Northern Cape', 'Northern Cape'), ('Western Cape', 'Western Cape'), ('Eastern Cape', 'Eastern Cape')
    , ('Limpopo', 'Limpopo')], string=" ")
    address_line5 = fields.Char(' ')

    responsible = fields.Many2one('nationalyouth.partnerz', string="Responsible")
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')

    category = fields.Char('Category')
    twitter = fields.Char('Twitter')
    project = fields.Many2one('nationalyouth.partnerz', string="Project")

    min_att = fields.Integer('Minimum Attendees')
    max_att = fields.Selection([('Limited', 'Limited'), ('Unlimited', 'Unlimited')], string="Maximum Attendees")