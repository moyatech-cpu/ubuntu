# coding=utf-8

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Company(models.Model):
    """ Company model """
    _name = 'company'
    _rec_name = 'name'
    _description = "Company"

    name = fields.Char("Name")
    contact_number = fields.Char(string="Contact Number")
    e_mail = fields.Char(string="E-mail")
    physical_address = fields.Text(string="Physical Address")

    _sql_constraints = [
        ('email_address', 'unique(e_mail)',
         'E-mail address should be unique.'),
    ]

    #Validation for mobile field
    @api.onchange('contact_number')
    def onchange_of_contact_number(self):
        if self.contact_number:
            if self.contact_number.isdigit():
                if len(self.contact_number) != 10:
                    raise UserError(_('Number Must be 10 digits'))
            else:
                raise UserError(_("Phone number should only contain digits."))