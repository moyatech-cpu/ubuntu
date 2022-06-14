# coding=utf-8

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ComplimentSuggestions(models.Model):
    """ Compliment Suggestions model """
    _name = 'compliments.suggestions'
    _rec_name = 'user_id'
    _description = "Compliment Suggestions"

    user_id = fields.Many2one('res.users', string="User", default= lambda self: self.env.user.id)
    send_to_user_id = fields.Many2one('res.users',string="Send to")
    facility_officer_id = fields.Many2one('res.users', string="Facility Officer",
                                          domain=lambda self: [
                                              ('groups_id', '=', self.env.ref('facility.facility_officer').id)])
    contact_number = fields.Char(string="Contact Number",related="send_to_user_id.mobile")
    e_mail = fields.Char(string="E-mail", related="send_to_user_id.login")
    type = fields.Selection(
        [('Suggestions', 'Suggestions'), ('Compliments', 'Compliments'), ('Complain', 'Complain')], string="Type")
    comment= fields.Text(string="Comment")

    def send_mail(self):
        mail_template = self.env.ref('facility.compliments_and_suggestions_email_template')
        if mail_template:
            email = self.e_mail + ", " + self.facility_officer_id.login
            mail_template.send_mail(self.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': email
                                    })
