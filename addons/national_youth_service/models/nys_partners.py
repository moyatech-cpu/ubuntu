# -*- coding: utf-8 -*-

from odoo import models, fields, api

class partners(models.Model):
    _name = 'nationalyouth.partnerz'
    _inherit = ['mail.thread','mail.activity.mixin']

    #partner_id = fields.Many2one('partner.enquiry', default=lambda self: self.env['partner.enquiry'].sudo().search([('user_id','=',self.env.user.id)]), readonly=True)

    name = fields.Char('Project Title')
    date = fields.Datetime('Date')
    color = fields.Integer()
    
    another_id = fields.Many2one('partner.enquiry', string = "Partner", default=lambda self: self.env['partner.enquiry'].sudo().search([('user_id','=',self.env.user.id)]), readonly=True)
    partner_id = fields.Char(string="Partner", related = "another_id.entity_name")
    # project details
    project_type = fields.Selection([('Category 1 - Learning Community Service and Linkages', 'Category 1 - Learning Community Service and Linkages'), 
    ('Category 2 - Voluntary Service', 'Category 2 - Voluntary Service'), ('Category 3 - Gap Year', 'Category 3 - Gap Year')], string="Project Type")

    partner_type = fields.Selection([('Institution of Higher Education', 'Institution of Higher Education'), 
    ('International Institution', 'International Institution'), ('National Department', 'National Department'),
    ('Provincial Department', 'Provincial Department'), ('District Municipality', 'District Municipality'), ('Local Authority', 'Local Authority'),
    ('Private Business', 'Private Business'), ('State Owned Enterprise', 'State Owned Enterprise'), ('NGO', 'NGO'), ('Other', 'Other')], string="Partner Type")
    
    project_application = fields.Date(string="Project Application Deadline")

    Branch = fields.Selection([('Head Office', 'Head Office'), ('Johannesburg', 'Johannesburg'), ('Tshwane', 'Tshwane'), ('Soweto', 'Soweto'),
    ('Emalahleni', 'Emalahleni'),('Nelspruit', 'Nelspruit'), ('Secunda', 'Secunda'), ('Polokwane', 'Polokwane'), ('Thulamela', 'Thulamela'),
    ('East London', 'East London'), ('Port Elizabeth', 'Port Elizabeth'), ('Durban', 'Durban'),('Empangeni', 'Empangeni'), ('Rustenburg', 'Rustenburg'),
    ('Bloemfontein','Bloemfontein'), ('Cape Town', 'Cape Town'), ('Kimberly', 'Kimberly')], string="Branch")
    project_summary = fields.Html()

    state = fields.Selection([('new', 'New'), ('review', 'Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], readonly=True, group_expand = '_expand_states', default = 'new')

    # Project info
    program_sector = fields.Many2one('res.partner.industry', string = "Programme Sector")

    nature = fields.Text('Nature of Programme')

    province = fields.Selection([('Mpumalanga', 'Mpumalanga'), ('Gauteng', 'Gauteng'), ('Free State', 'Free State'), ('Kwazulu-natal', 'Kwazulu-natal'),
    ('North West', 'North West'), ('Northern Cape', 'Northern Cape'), ('Western Cape', 'Western Cape'), ('Eastern Cape', 'Eastern Cape')
    , ('Limpopo', 'Limpopo')], string="Province")

    age_cohort = fields.Selection([('14 - 18', '14 - 18'), ('18 - 21', '18 - 21'), ('21 - 26', '21 - 26'), ('26 - 30', '30 - 35')], string="Age Cohort")

    male_req = fields.Selection([('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'),('60', '60'), ('70', '70'), 
    ('80', '80'), ('90', '90'), ('100', '100')], string="Male Requirement (%)")

    female_req = fields.Selection([('10', '10'), ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'),('60', '60'), ('70', '70'), 
    ('80', '80'), ('90', '90'), ('100', '100')], string="Female Requirement (%)")

    educational_req = fields.Selection([('National Youth Service', 'National Youth Service'), ('Not Applicable', 'Not Applicable'), 
    ('Less than grade 9', 'Less than grade 9'), ('Some FET credits', 'Some FET credits'), ('Grade 12 or Equivalent', 'Grade 12 or Equivalent'), 
    ('Graduate or Post Graduate',  'Graduate or Post Graduate')], string="Educational Requirements")

    previous_volunteer = fields.Selection([('N/A', 'N/A'), ('Yes', 'Yes'), ('No', 'No')], string="Previous Volunteer Experience")

    other_criteria = fields.Text('Other Criteria')

    project_duration = fields.Selection([('< 3 months', '< 3 months'), ('3 months', '3 months'), ('< 6 months', '< 6 months'), ('6 months', '6 months'),
    ('< 12 months', '< 12 months'), ('12 months +', '12 months +'), ], string="Project Duration")

    # Project Description Fields
    describe_nature = fields.Text()
    describe_beneficiaries = fields.Text()
    project_objectives = fields.Selection([('Further Education And Training', 'Further Education and Training'),('Employment', 'Employment'), 
    ('Enterprise Development', 'Enterprise Development'), ('Other', 'Other')], string="Project Duration")
    exit_pathways = fields.Text()

    # for kanban view
    kanban_state = fields.Selection([('normal', 'In Progress'),('blocked', 'Blocked'),('done', 'Ready for next stage')],'Kanban State',default='normal')
    priority = fields.Selection([('Lelev 1', 'Level 1'), ('Lelev 2', 'Level 2')])

    # status bar function 
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    # functions for NYS specialist
    def Proceed_to_review(self):
        self.state = 'review'

    # functions for NYS manager
    def Proceed_to_accepted(self):
        self.state = 'approved'

    def Proceed_to_rejected(self):
        self.state = 'rejected'

    def run_action1(self):
        views = [(self.env.ref('event.view_event_kanban').id, 'kanban'), (self.env.ref('event.view_event_form').id, 'form')]
        return{
                'name': 'Physical Events',
                'view_type': 'form',
                'view_mode': 'kanban,form',
                'view_id': False,
                'res_model': 'event.event',
                'views': views,
                'domain': [('project','=',self.id),('event_type_id','=','Physical Event')],
                'type': 'ir.actions.act_window',
            }

    def run_action2(self):
        action = self.run_action1()
        action['domain'][1] = ('event_type_id','=','Training')
        return action


class partner_profile(models.Model):
    _name = 'nationalyouth.partnerz.profile'

    partner_id = fields.Many2one('partner.enquiry', default=lambda self: self.env['partner.enquiry'].sudo().search([('user_id','=',self.env.user.id)]))
    image = fields.Binary('res.partner')
    name = fields.Char(related = "partner_id.entity_name")
    reg_no = fields.Char('Registration Number', related = "partner_id.company_reg_number")
    tax_no = fields.Char('Name of Entity', related = "partner_id.name_entity_representative")
    vat_vendor = fields.Char('Surname', related = "partner_id.surname")
    # vat = fields.Char('VAT')
    inst_type = fields.Char('Institution Type')
    org_sector = fields.Char('Organisation Sector')
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    # address fields
    address_line1 = fields.Char('Address')
    address_line2 = fields.Char(' ')
    address_line3 = fields.Char(' ')
    address_line4 = fields.Selection([('Mpumalanga', 'Mpumalanga'), ('Gauteng', 'Gauteng'), ('Free State', 'Free State'), ('Kwazulu-natal', 'Kwazulu-natal'),
    ('North West', 'North West'), ('Northern Cape', 'Northern Cape'), ('Western Cape', 'Western Cape'), ('Eastern Cape', 'Eastern Cape')
    , ('Limpopo', 'Limpopo')], string=" ")
    address_line5 = fields.Char(' ')

    contacts = fields.One2many('res.partner','related_nys_partner',string = "Contacts")

class Contact(models.Model):
    _inherit = 'res.partner'
    
    related_nys_partner = fields.Many2one('nationalyouth.partnerz.profile')