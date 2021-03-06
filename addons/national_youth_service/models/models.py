# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

# nys beneficiary
class Person(models.Model):
    _name = 'nationalyouth.partner'

    #benificiary_id = fields.Many2one('youth.enquiry', string="Hello World")
    partner_id = fields.Many2one('youth.enquiry', default=lambda self: self.env['youth.enquiry'].sudo().search([('user_id','=',self.env.user.id)]))

    # Personal details fields
    title = fields.Selection([('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr', 'Dr'), ('Prof', 'Prof')], string="Title")
    name = fields.Char(string='Name',related="partner_id.name")
    surname = fields.Char('Surname',related="partner_id.surname")
    id_no = fields.Char(string="Id Numbers", related="partner_id.id_number")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('not_specify', 'Not Specify')], string="Gender", related = "partner_id.gender")
    disability = fields.Char(string="Disability")
    cell_phone_number = fields.Char('Cell Phone No', related = "partner_id.cell_phone_number")
    email = fields.Char('Email', related = "partner_id.email")
    home_language = fields.Selection([('English', 'English'), ('Afrikaans', 'Afrikaans'), ('Zulu', 'Zulu'),('Swati', 'Swati'), 
    ('Xhosa', 'Xhosa'), ('Ndebele','Ndebele'), ('Pedi','Pedi'), ('Sotho','Sotho'), ('Venda','Venda'), ('Tswana','Tswana'), ('Tsonga','Tsonga')], string="Home Language")
    employment_status = fields.Selection([('Unemployed', 'Unemployed'), ('Employed', 'Employed')], string="Employment Status")
    occupation = fields.Char('Occupation') 
    location_type = fields.Selection([('Urban', 'Urban'), ('Rural', 'Rural'), ('Peri Urban', 'Peri Urban')], string="Location Type")
    population_group = fields.Selection([('African', 'African'), ('Coloured', 'Coloured'), ('White', 'White'), ('Indian', 'Indian'), ('Asian', 'Asian'),
    ('Other','Other')], string="Population Group")
    highest_education = fields.Selection([('None', 'None'), ('Primary', 'Primary'), ('Secondary', 'Secondary'), 
    ('Tertiary','Tertiary'), ('Post Graduate','Post Graduate')], string="Highest Education")
    alternative_number = fields.Char('Alternative Number')

    # Address details fields
    drivers_license = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Drivers License")
    license_code = fields.Char('License Code')
    marital_status = fields.Selection([('Single', 'Single'), ('Married', 'Married'),('Divorced', 'Divorced'), ('Widowed', 'Widowed')], string="Martital Status")
    branch_id = fields.Many2one(comodel='res.branch', string="Branch", related = "partner_id.nearest_branch")
    municipality = fields.Many2one('res.municipality', string="Municipality", related = "partner_id.municipality")
    # address fields
    address_line1 = fields.Char('Address')
    address_line2 = fields.Char(' ')
    address_line3 = fields.Char(' ')
    address_line4 = fields.Selection([('Mpumalanga', 'Mpumalanga'), ('Gauteng', 'Gauteng'), ('Free State', 'Free State'), ('Kwazulu-natal', 'Kwazulu-natal'),
    ('North West', 'North West'), ('Northern Cape', 'Northern Cape'), ('Western Cape', 'Western Cape'), ('Eastern Cape', 'Eastern Cape')
    , ('Limpopo', 'Limpopo')], string=" ")
    address_line5 = fields.Char(' ')
    
    # Education
    primary_education = fields.One2many('nationalyouth.primaryeducation', 'candidate_id', string ="Primary School")
    secondary_education = fields.One2many('nationalyouth.secondaryeducation', 'candidate_id', string ="Secondary School")
    work_experience = fields.One2many('nationalyouth.workexperience', 'candidate_id', string ="Work Experience")
    references = fields.One2many('nationalyouth.references', 'candidate_id', string ="Telephone")
    tertiary_education = fields.One2many('nationalyouth.tertiary', 'candidate_id', string ="Tertiary Education")
    computer_skills = fields.One2many('nationalyouth.computerskills', 'candidate_id', string ="Computer Skills")

    # for kanaban view
    color = fields.Integer()

    # validation rules
    @api.constrains('alternative_number','address_line5')
    def _check_defined_number(self):
        for r in self:
            if not r.alternative_number.isnumeric():
                raise exceptions.ValidationError( "Invalid phone number")
            if len(r.alternative_number) != 10:
                raise exceptions.ValidationError( "Invalid phone number")
            if not r.address_line5.isnumeric():
                raise exceptions.ValidationError( "Invalid phone postal code")
            if len(r.address_line5) != 4:
                raise exceptions.ValidationError( "Invalid phone postal code")
                