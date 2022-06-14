# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError

GENDER_SELECTION = [('male', 'Male'),
                    ('female', 'Female'),
                    ('other', 'Other')]

class EmployeeManagement(models.Model):
    _inherit = 'hr.employee'

    personal_mobile                 = fields.Char(string='Mobile', related='address_home_id.mobile', store=True)
    emergency_contact               = fields.One2many('hr.emergency.contact', 'employee_obj', string='Emergency Contact')
    relative_ids                    = fields.One2many('hr.employee.relative', 'employee_id', string='Employee Relative')
    education_ids                   = fields.One2many('hr.employee.education', 'employee_id', string='Employee Education')
    
    joining_date                    = fields.Date(string='Joining Date')
    termination_date                = fields.Date(string='Termination Date')
    id_expiry_date                  = fields.Date(string='Expiry Date', help='Expiry date of Identification ID')
    passport_expiry_date            = fields.Date(string='Expiry Date', help='Expiry date of Passport ID')
    id_attachment_id                = fields.Many2many('ir.attachment', 'id_attachment_rel', 'id_ref', 'attach_ref',
                                        string="Attachment", help='You can attach the copy of your Id')
    passport_attachment_id          = fields.Many2many('ir.attachment', 'passport_attachment_rel', 'passport_ref', 'attach_ref1',
                                        string="Attachment", help='You can attach the copy of Passport')
    fam_ids                         = fields.One2many('hr.employee.family', 'employee_id', 
                                        string='Family', help='Family Information')
    #Personal Information
    title                           = fields.Selection([('Mr', 'Mr'), ('Ms', 'Ms'), ('Miss', 'Miss'), ('Mrs', 'Mrs'), ('Prof', 'Prof'), ('Dr', 'Dr')], string="Title")
    preferred_name                  = fields.Char(string='Preferred Name')
    home_language                   = fields.Char(string='Home Language')
    disability                      = fields.Selection([('Yes','Yes'),('No','No')], string="Disability")
        
        
    disability_details              = fields.Char(string='Disability Details')
    initials                        = fields.Char(string='Initials')
    first_name                      = fields.Char(string='First Name')
    second_name                     = fields.Char(string='Second Name')
    employee_number                 = fields.Char(string='Employee Number')
    receivers_office                = fields.Char(string='Receivers Office')
    drivers_licence_code            = fields.Char(string='Drivers Licence Code')
    religion                        = fields.Char(string='Religion')
    citizenship                     = fields.Char(string='Citizenship')
    race                            = fields.Selection([('African', 'African'),('Coloured', 'Coloured'),('Indian', 'Indian'),('White', 'White'),('Chinese', 'Chinese')], string="Race")
    marital                         = fields.Selection([
                                            ('single', 'Single'),
                                            ('married', 'Married'),
                                            ('cohabitant', 'Legal Cohabitant'),
                                            ('widower', 'Widower'),
                                            ('widow', 'Widow'),
                                            ('divorced', 'Divorced')
                                        ], string='Marital Status', groups="hr.group_hr_user", default='single')

    membership_affiliation          = fields.Char(string='Membership Affiliation')
    race_other                      = fields.Char(string='Race Other')
    
    #Visa Details
    visa_issue_date                 = fields.Char(string='Visa Issue Date')
    residence_type                  = fields.Char(string='Residence Type')
    passport_held                   = fields.Char(string='Passport Held')
    
    #address_information
    street_address_1                = fields.Char(string='Street Address 1')
    suburb                          = fields.Char(string='Suburb')
    city                            = fields.Char(string='City')
    postal_code                     = fields.Char(string='Postal_code')
    municipality                    = fields.Char(string='Municipality')
    province                        = fields.Char(string='Province')
    
    postal_address_1                = fields.Char(string='Postal Address')
    postal_ad_city                  = fields.Char(string='Postal City')
    postal_ad_code                  = fields.Char(string='Postal Code')
    email                           = fields.Char(string='Email')
    home_tel                        = fields.Char(string='Home Tel')
    
    #Emergency Information - emergency_contact
    doctor_name                     = fields.Char(string='Doctor Name')
    allergies                       = fields.Char(string='Allergies')
    doctor_phone_number             = fields.Char(string='Doctor Phone Number')
    known_conditions                = fields.Char(string='Known Conditions')
    
    # name="public" string="Position Information"
    years_of_service                = fields.Char(string='Years of Service')
    branch_id                       = fields.Many2one(string="Branch", help='Select Branch', comodel_name='res.branch', invisible=0)
    
    position_code                   = fields.Char(string='Position Code')
    position_start                  = fields.Char(string='Position Start')
    cost_center                     = fields.Char(string='Cost Center')
    reports_to                      = fields.Many2one(string="Report To", help='Report To', comodel_name='hr.job', invisible=0)
    
    #name="bank_details" string="Payment Information"
    payment_intervals               = fields.Char(string='Payment Intervals')
    payment_method                  = fields.Char(string='Payment Method')
    payment_point                   = fields.Char(string='Payment Point')
    payment_point_description       = fields.Char(string='Payment Point Description')
    bank_name                       = fields.Char(string='Bank Name')
    bank_account_number             = fields.Char(string='Bank Account Number')
    bank_account_type               = fields.Char(string='Bank Account Type')
    bank_account_name               = fields.Char(string='Bank Account Name')
    bank_branch_name                = fields.Char(string='Bank Branch Name')
    bank_branch_code                = fields.Char(string='Bank Branch Code')
    tax_status                      = fields.Char(string='Tax Status')
    tax_method                      = fields.Char(string='Tax Method')
    tax_directive                   = fields.Char(string='Tax Directive')
    tax_depends                     = fields.Char(string='Tax Depends')
    company_car_value               = fields.Char(string='Company Car Value')
    nature_person                   = fields.Char(string='Nature Person')
    tax_number                      = fields.Char(string='Tax Number')
    tax_office                      = fields.Char(string='Tax Office')
    tax_certificate_issued_date     = fields.Char(string='Tax Certificate Issued Date')
    tax_certificate_number          = fields.Char(string='Preferred Name')
    prev_tax_certificate_no         = fields.Char(string='Previous Tax Certificate No.')
    company_no                      = fields.Char(string='Company No.')
    foreign_income_tax_emp          = fields.Char(string='Foreign Income Tax')
    
    #Funeral Contact
    funeral_contact_name            = fields.Char(string='Funeral Contact Name')
    funeral_contact_relationship    = fields.Char(string='Funeral Contact Relationship')
    funeral_contact_number          = fields.Char(string='Funeral Contact Number')
    funeral_contact_email           = fields.Char(string='Funeral Contact Email')
    employee_funeral_beneficiary    = fields.One2many('hr.funeral.beneficiary', 'employee_id', string='Funeral Beneficiary')

    def mail_reminder(self):
        """Sending expiry date notification for ID and Passport"""

        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            if i.id_expiry_date:
                exp_date = fields.Date.from_string(i.id_expiry_date) - timedelta(days=14)
                if date_now >= exp_date:
                    mail_content = "  Hello  " + i.name + ",<br>Your ID " + i.identification_id + "is going to expire on " + \
                                   str(i.id_expiry_date) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('ID-%s Expired On %s') % (i.identification_id, i.id_expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.work_email,
                    }
                    self.env['mail.mail'].sudo().create(main_content).send()
        match1 = self.search([])
        for i in match1:
            if i.passport_expiry_date:
                exp_date1 = fields.Date.from_string(i.passport_expiry_date) - timedelta(days=180)
                if date_now >= exp_date1:
                    mail_content = "  Hello  " + i.name + ",<br>Your Passport " + i.passport_id + "is going to expire on " + \
                                   str(i.passport_expiry_date) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('Passport-%s Expired On %s') % (i.passport_id, i.passport_expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.work_email,
                    }
                    self.env['mail.mail'].sudo().create(main_content).send()


class EmergencyContact(models.Model):
    """This class is to add emergency contact table"""

    _name = 'hr.emergency.contact'
    _description = 'HR Emergency Contact'

    name            = fields.Char(string='Name', help='Contact Name')
    number          = fields.Char(string='Number', help='Contact Number')
    relation        = fields.Char(string='Contact', help='Relation with employee')
    employee_obj    = fields.Many2one(string="Employee", help='Select corresponding Employee', comodel_name='hr.employee',
                                  invisible=1)
    id_number       = fields.Char(string='ID Number', help="Kin's identity number")

class RelativeContact(models.Model):
    """This class is to add relative contact table"""

    _name = 'hr.employee.relative'
    _description = 'HR Employee Relative'

    employee_id     = fields.Many2one(string="Employee", help='Select corresponding Employee', comodel_name='hr.employee',
                                  invisible=1)
    relative_type   = fields.Char(string='Relative Type', help='Relative Type')
    name            = fields.Char(string='Name', help='Name')
    birthday        = fields.Char(string='Birthday', help='birthday')    
    id_number       = fields.Char(string='ID Number', help="Kin's identity number")

class EmployeeEducation(models.Model):
    """This class is to add Employee Education table"""

    _name = 'hr.employee.education'
    _description = 'HR Employee Education'

    employee_id         = fields.Many2one(string="Employee", help='Select corresponding Employee', comodel_name='hr.employee',
                                  invisible=1)
    grade               = fields.Char(string='Grade', help='Grade')
    qualification_type  = fields.Char(string='Name', help='Qualification Type')
    school_name         = fields.Char(string='School Name', help='School Name')    
    to_date             = fields.Date(string='Date', help="Completed")
            
class FuneralBeneficiary(models.Model):
    """This class is to add emergency contact table"""

    _name = 'hr.funeral.beneficiary'
    _description = 'HR Funeral Beneficiary'

    name            = fields.Char(string='Name', help='Contact Name')
    relationship    = fields.Char(string='Contact', help='Relation with employee')
    contact_no      = fields.Char(string='Contact No', help='Contact Number')
    contact_email   = fields.Char(string='Contact Email', help='Contact Email')
    employee_id     = fields.Many2one(string="Employee", help='Select corresponding Employee', comodel_name='hr.employee',
                                  invisible=1)
    relative_type   = fields.Char(string='Relative', help="Relative")


class HrEmployeeFamilyInfo(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.family'
    _description = 'HR Employee Family'

    member_name     = fields.Char(string='Name', related='employee_ref.name', store=True)
    employee_ref    = fields.Many2one(string="Is Employee", help='If family member currently is an employee of same company, ''then please tick this field', 
                                comodel_name='hr.employee')
    employee_id     = fields.Many2one(string="Employee", help='Select corresponding Employee', 
                                comodel_name='hr.employee', invisible=1)
    relation        = fields.Selection([('father', 'Father'),
                                        ('mother', 'Mother'),
                                        ('daughter', 'Daughter'),
                                        ('son', 'Son'),
                                        ('wife', 'Wife')], string='Relationship', help='Relation with employee')
    member_contact  = fields.Char(string='Contact No', related='employee_ref.personal_mobile', store=True)