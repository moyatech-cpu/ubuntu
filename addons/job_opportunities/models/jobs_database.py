# -*- coding: utf-8 -*-

from odoo import models, fields, api

class JobsDatabase(models.Model):
    _name = 'jobs.database'
    _description = 'Jobs Database'

    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    title = fields.Selection(
        [('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr', 'Dr'), ('Prof', 'Prof')],
        string="Title")
    surname = fields.Char(string="Surname")
    id_no = fields.Char(string="ID No")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    disability = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Disability")
    home_language = fields.Selection(
        [('sepedi', 'Sepedi'), ('sesotho', 'Sesotho'), ('setswana', 'Setswana'), ('siswati', 'siSwati'),
         ('tshivenda', 'Tshivenda'), ('xitsonga', 'Xitsonga'), ('afrikaans', 'Afrikaans'),
         ('english', 'English'), ('isindebele', 'isiNdebele'), ('isixhosa', 'isiXhosa'),
         ('isizulu', 'isiZulu')], string="Home Language")
    employment_status = fields.Selection([('yes','Yes'), ('no', 'No')],string="Employment Status")
    location = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Rural area - Villages'),
         ('rural-area-farms', 'Rural area - Farms')], string="Location")
    cell_phone = fields.Char(string="Cell Phone Number")
    alt_number = fields.Char(string="Alternative Number")
    email = fields.Char(string="E-mail")
    product_info = fields.Char(string="Product Info") #change type
    population_group = fields.Selection(
        [('african', 'African'), ('asian', 'Asian'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Population Group")
    highest_education = fields.Selection([('secondary', 'Secondary'), ('territory', 'Territory')],
                                         string="Highest Education")
    drivers_license = fields.Selection([('yes', 'Yes'), ('no', 'No')],string="Drivers License")
    license_code = fields.Char(string="License Code")
    marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried')], string="Marital Status")
    occupation = fields.Char(string="Occupation")
    scholar_level = fields.Text(string="If Scholar, state which level")
    completed_job_preparedeness = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                   string="Have you completed NYDA Job Preparedness ?")
    branch_id = fields.Many2one('res.branch', string="Branch")
    municipality_id = fields.Many2one('res.municipality', string="Municipality")
    district = fields.Many2one('res.district', string="District")
    street = fields.Char(string="Street...")
    street2 = fields.Char(string="Street 2...")
    town = fields.Char(string="Town")
    province_id = fields.Many2one('res.country.state', string="Province")
    postal_code = fields.Integer(string="Postal Code")
    is_matric_certificate = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Do you have matric certificate ?")
    matric_Result_ids = fields.One2many('matric.results', 'jobs_database_id', string="Matric Results")
    is_teritory_higher_education = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                    string="Do you have a Tertiary or Higher education qualification ?")
    teritory_higher_education_ids = fields.One2many('teritory.higher.education', 'jobs_database_id',
                                                    string="Teritory Higher Education")
    computer_skills_ids = fields.One2many('computer.skills', 'jobs_database_id',
                                                    string="Computer Skills")
    organisations_ids = fields.One2many('organisations', 'jobs_database_id',
                                                    string="Organisations")
    referees_ids = fields.One2many('referees', 'jobs_database_id',
                                                    string="Referees")
    benificiary_signature = fields.Binary(string="Signature")
    user_id = fields.Many2one('res.users', string="User")
    youth_enquiry_id = fields.Many2one('youth.enquiry', string="Youth")
    active = fields.Boolean(string="Active", default=True)
