# -*- coding: utf-8 -*-

from odoo import models, fields, api

class partners(models.Model):
    _name = 'nationalyouth.partnerz'

    name = fields.Char('Name')
    date = fields.Datetime('Date')
    color = fields.Integer()

    state = fields.Selection([('new', 'New'), ('review', 'Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], group_expand = '_expand_states', default = 'new')

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

class partner_profile(models.Model):
    _name = 'nationalyouth.partnerz.profile'

    reg_no = fields.Char('Registration Number')
    tax_no = fields.Char('Tax No')
    vat_vendor = fields.Char('VAT Vendor')
    vat = fields.Char('VAT')
    inst_type = fields.Char('Institution Type')
    org_sector = fields.Char('Organisation Sector')
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    address = fields.Char(string="Address")

    # contacts = fields.One2many('hr.employee',string = "Contacts")