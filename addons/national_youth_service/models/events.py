# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time
# from odoo.addons.http_routing.models.ir_http import slug

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

    # these fields for time munipulation
    month = fields.Char('Month',default=datetime.now().strftime("%B"))

    @api.onchange('create_date')
    def _get_day(self):
        for r in self:
            date = datetime.strptime(r.create_date, "%d/%m/%Y %H:%M:%S")
            month = date.month
            year = date.year

class Events(models.Model):
    _inherit = 'event.event'

    project = fields.Many2one('nationalyouth.partnerz', string="Project")
    date_begin = fields.Datetime(
        string='Start Date', required=True,
        track_visibility='onchange', states={'done': [('readonly', True)]})
    date_end = fields.Datetime(
        string='End Date', required=True,
        track_visibility='onchange', states={'done': [('readonly', True)]})

    def ApplyForEvent(self):
        self.ensure_one()
        # return self._compute_website_url()
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': '/event',
        }

class Attendees(models.Model):
    _inherit = 'event.registration'

    signature = fields.Binary(string = 'signature')
