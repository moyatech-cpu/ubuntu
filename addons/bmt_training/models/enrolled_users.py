# coding=utf-8

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError


class EnrolledUsers(models.Model):
    """ Enrolled Users """
    _name = 'enrolled.users'
    _rec_name = 'benificiary_id'
    _description = "Company"

    benificiary_id = fields.Many2one('youth.enquiry', string="Benificiary")
    surname = fields.Char(string="Surname", related="benificiary_id.surname")
    id_number = fields.Char(string="ID Number", related="benificiary_id.id_number")
    contact_number = fields.Char(string="Contact Number", related="benificiary_id.cell_phone_number")
    e_mail = fields.Char(string="E-mail", related="benificiary_id.email")
    population_group = fields.Selection(
        [('african', 'African'), ('asian', 'Asian'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Population Group", related="benificiary_id.population_group")
    gender = fields.Selection([('male','Male'),('female','Female')], string="Gender", related="benificiary_id.gender")
    geographic_location = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri-Urban'), ('rural-area-villages', 'Rural Area - Villages'),
         ('rural-area-farms', 'Rural area - Farms'), ('informa-settlement', 'Informa settlement')],
        string="Geographic Location", related="benificiary_id.geographic_location")
    technical_training_id = fields.Many2one('technical.training', string="Technical Training")
    technical_training_apprenticeship_id = fields.Many2one('technical.training.apprenticeship',
                                            string="Technical Training Apprenticeship")
    year = fields.Selection(
        [('first_year', 'First year'), ('second_year', 'Second Year'), ('third_year', 'Third Year')],
        string="Current Year")
    passed = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Passed")
    work_placement_id = fields.Char(string="Work Placement")
    certificate = fields.Binary(string="Certificate")
    certificate_name = fields.Char(string="Certificate Name")
    trade_certi = fields.Binary(string="Trade Certificate")
    trade_certificate_name = fields.Char(string="Certificate Name")
    mentorship_report_log_book = fields.Binary(string="Mentorship report/Log book", copy=False)
    log_book_file_name = fields.Char(string="Mentorship report/Log book File name", copy=False)

    # _sql_constraints = [
    #     ('email_address', 'unique(e_mail)',
    #      'E-mail address should be unique.'),
    # ]

class LinkServiceProvider(models.Model):
    """ Link Service Provider """
    _name = 'link.service.provider'
    _rec_name = 'service_provider_id'
    _description = "Link Service Provider"

    service_provider_id = fields.Many2one('res.users', string="Service Provider", domain=lambda self: [
        ("groups_id", "=", self.env.ref("client_management.group_partner_service_provider").id)])
    nyda_specialist_id = fields.Many2one('res.users', string="NYDA Specialist", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_nyda_specialist").id)])

    @api.constrains('service_provider_id')
    @api.one
    def restrict_service_provider(self):
        service_provider_exists = self.env['link.service.provider'].sudo().search(
            [('service_provider_id', '=', self.service_provider_id.id), ('id', '!=', self.id)])
        print ("\n\n\n", service_provider_exists, self, self.id)
        if service_provider_exists:
            raise ValidationError(_("Service Provider is already linked !!"))
