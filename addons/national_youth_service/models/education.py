# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class Primary(models.Model):
    _name = 'nationalyouth.primaryeducation'

    name = fields.Char('Name', required=True)
    subjects = fields.Text('Major Subjects')
    year = fields.Char('Year Completed')
    
    candidate_id = fields.Many2one('nationalyouth.partner', ondelete='cascade', string = "Candidate")

    @api.constrains('year','name')
    def _primary_education_constraints(self):
        for r in self:
            if r.year != False:
                if not r.year.isnumeric():
                    raise exceptions.ValidationError( "Invalid phone year")
                if len(r.year) != 4:
                    raise exceptions.ValidationError( "Invalid phone year")
            if r.name == False or r.name == None:
                raise exceptions.ValidationError( "Name of the primary school is required")

class HighSchool(models.Model):
    _name = 'nationalyouth.secondaryeducation'

    subject = fields.Selection([('Accounting', 'Accounting'), ('Agricultural Management Practices', 'Agricultural Management Practices'),
     ('Agricultural science', 'Agricultural science'), ('Agricultural Technology', 'Agricultural Technology'), ('Business Studies', 'Business Studies'),
     ('Civil Technology', 'Civil Technology'), ('Computer Applications Technology', 'Computer Applications Technology'), ('Consumer Studies','Consumer Studies'),
     ('Dance Studies', 'Dance Studies'), ('Design', 'Design'), ('Dramatic Arts','Dramatic Arts'), ('Economics','Economics'), ('Electrical Technology','Electrical Technology'),
     ('Engineering Graphics & Design', 'Engineering Graphics & Design'), ('Geography','Geography'), ('Hospitality Studies','Hospitality Studies'),
     ('Information Technology', 'Information Technology'), ('Life Sciences','Life Sciences'), ('Mechanical Technology', 'Mechanical Technology'),
     ('Music','Music'),('Physical Science', 'Physical Science'), ('Religion Studies', 'Religion Studies'),('Second Additional Language','Second Additional Language'),
     ('Third Additional Language', 'Third Additional Language'), ('Tourism','Tourism'), ('Visual Arts', 'Visual Arts'), ('English (HL/FAL)', 'English (HL/FAL)'),
     ('Isizulu (HL/FAL)','Isizulu (HL/FAL)'), ('IsiXhosa (HL/FAL)','IsiXhosa (HL/FAL)'), ('Afrikaans (FAL)', 'Afrikaans (FAL)'), ('Mathematics','Mathematics'),
     ('Mathematical Literacy', 'Mathematical Literacy'), ('Accounting','Accounting'), ('Economics','Economics')], string="Subjects", required=True)

    achievement_level = fields.Selection([('Level 7: 80 - 100%', 'Level 7: 80 - 100%'), ('Level 6: 70 - 80%', 'Level 6: 70 - 80%'), ('Level 5: 60 - 70%', 'Level 5: 60 - 70%'),
    ('Level 4: 50 - 60%', 'Level 4: 50 - 60%'), ('Level 3: 40 - 50%', 'Level 3: 40 - 50%'), ('Level 2: 30 - 40%', 'Level 2: 30 - 40%'), ('Level 1: 0 - 30%', 'Level 1: 0 - 30%'), 
    ], string="Achievement Level")

    #symbol = fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),('E', 'E'),('F','F'),('G','G')], string="Symbol", readonly=True)
    symbol = fields.Char( string="Symbol", readonly=True, compute = '_get_symbol')
    
    candidate_id = fields.Many2one('nationalyouth.partner', ondelete='cascade', string = "Candidate", readonly = True)

    @api.depends('achievement_level')
    def _get_symbol(self):
        for r in self:
            if r.achievement_level == 'Level 7: 80 - 100%':
                r.symbol = 'A'
            elif r.achievement_level == 'Level 6: 70 - 80%':
                r.symbol = 'B'
            elif r.achievement_level == 'Level 5: 60 - 70%':
                r.symbol = 'C'
            elif r.achievement_level == 'Level 4: 50 - 60%':
                r.symbol = 'D'
            elif r.achievement_level == 'Level 3: 40 - 50%':
                r.symbol = 'E'
            elif r.achievement_level == 'Level 2: 30 - 40%':
                r.symbol = 'F'
            elif r.achievement_level == 'Level 1: 0 - 30%':
                r.symbol = 'G'

class Tertiary(models.Model):
    _name = 'nationalyouth.tertiary'

    name = fields.Char('Name')
    subjects = fields.Text('Major Subjects')
    year = fields.Char('Year Completed')
    #qualification = fields.Many2one('ir.attachment', string="Attachment", required=True)
    qualification = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_identity_card_rel", column1="m2m_id", column2="attachment_id", string="Upload your file")
    
    
    candidate_id = fields.Many2one('nationalyouth.partner', ondelete='cascade', string = "Candidate")

    @api.constrains('year')
    def _tertiary_education_constraints(self):
        for r in self:
            if r.year != False:
                if not r.year.isnumeric():
                    raise exceptions.ValidationError( "Year must be a number")
                if len(r.year) != 4:
                    raise exceptions.ValidationError( "Year has 4 numbers")
            if r.name == False or r.name == None:
                raise exceptions.ValidationError( "Name of the tertiary institutiion is required")

class Skills(models.Model):
    _name = 'nationalyouth.computerskills'

    qualification = fields.Char('Qualification')
    ms_word = fields.Selection([('Excellent', 'Excellent'), ('Good', 'Good'), ('Satisfactory', 'Satisfactory'), ('Basic', 'Basic')], string="MS Word")
    excel = fields.Selection([('Excellent', 'Excellent'), ('Good', 'Good'), ('Satisfactory', 'Satisfactory'), ('Basic', 'Basic')], string="Excel")
    database = fields.Selection([('Excellent', 'Excellent'), ('Good', 'Good'), ('Satisfactory', 'Satisfactory'), ('Basic', 'Basic')], string="Database System(Oracle,CRM,Access,SAP,etc)")
    graphic_design = fields.Selection([('Excellent', 'Excellent'), ('Good', 'Good'), ('Satisfactory', 'Satisfactory'), ('Basic', 'Basic')], string="Graphic Design")
    outlook = fields.Selection([('Excellent', 'Excellent'), ('Good', 'Good'), ('Satisfactory', 'Satisfactory'), ('Basic', 'Basic')], string="Internet microsoft outlook")
    accounts = fields.Selection([('Excellent', 'Excellent'), ('Good', 'Good'), ('Satisfactory', 'Satisfactory'), ('Basic', 'Basic')], string="Accounts")
    attachments = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_qualifiucation_rel", column1="m2m_id", column2="attachment_id", string="Upload your file")
    
    
    candidate_id = fields.Many2one('nationalyouth.partner', ondelete='cascade', string = "Candidate")

class WorkExperience(models.Model):
    _name = 'nationalyouth.workexperience'

    name = fields.Char('Name of the organisation')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    position = fields.Char('Position held')
    reason_for_leaving = fields.Text('Reasons for leaving')

    candidate_id = fields.Many2one('nationalyouth.partner', ondelete='cascade', string = "Candidate")


class Reference(models.Model):
    _name = 'nationalyouth.references'

    organisation = fields.Char('Organisation')
    name = fields.Char('Name')
    job_title = fields.Char('Job Title')
    telephone = fields.Char('Telephone')
    Mobile = fields.Char('Mobile')

    candidate_id = fields.Many2one('nationalyouth.partner', ondelete='cascade', string = "Candidate")

    @api.constrains('telephone','name', 'mobile')
    def _reference_constraints(self):
        for r in self:
            if r.telephone != False:
                if not r.telephone.isnumeric():
                    raise exceptions.ValidationError( "Invalid phone telephone")
                if len(r.telephone) != 10:
                    raise exceptions.ValidationError( "Invalid phone telephone")
            if r.mobile != False:
                if not r.mobile.isnumeric():
                    raise exceptions.ValidationError( "Invalid phone mobile number")
                if len(r.mobile) != 10:
                    raise exceptions.ValidationError( "Invalid phone mobile number")
            if r.name == False or r.name == None:
                raise exceptions.ValidationError( "Name of the referee is required")