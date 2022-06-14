# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import  _
from datetime import date, datetime
from odoo.exceptions import UserError

class ThusanoFundApplication(models.Model):
     _name = 'thusano.fund'
     _inherit = ['mail.thread']
     _rec_name = 'serial_number'
     
     #Personal Details
     serial_number = fields.Char('Serial Number')
     name = fields.Char('First Name')
     partner_job_title = fields.Char('Job Title')
     application_date = fields.Date('Date of Application', default=fields.Date.today())
     cell_phone_number = fields.Char('Phone Number')
     alternative_number = fields.Char('Alternative Number')
     email = fields.Char('Email')
     reg_fees = fields.Boolean("Registration Fees",default=False)
     outstanding_fees = fields.Boolean(default=False)
     ngo_ngo_funding = fields.Boolean("NGO/ NPO funding",default=False)
     short_courses_technical_training = fields.Boolean(default=False)
     other_related_funding = fields.Boolean(default=False)
     has_sponsor = fields.Boolean(default=False)
     empl_sector = fields.Char(string="Employment Status")
     npo_ngo_number = fields.Integer('NPO/ NGO number    ')
     employment_status = fields.Selection([('unemployed', 'Unemployed'), ('employed', 'Employed'),
                                           ('self-employed', 'Self-Employed'),('other','Other')], string="Employment Status")
     parent_name = fields.Char('Parent/Guardian Name')
     parent_id_number = fields.Char('First Parent ID Number')
     second_parent_name = fields.Char('Second Parent/Guardian Name')
     parent_id_number = fields.Char('First Parent ID Number')
     second_parent_id_number = fields.Char('Second Parent/Guardian ID Number')
     sponsor_name = fields.Char('Sponsor Name')
     sponsor_amount = fields.Monetary('Sponsor Amount', currency_field='currency_id')
     self_support_statement = fields.Char('Self Support Explanation')
     motivation_statement  = fields.Char('Application Motivation')
     user_type = fields.Selection([('student','Student'),('ngo','NGO')],string="Applicant Type", default='student')
     currency_id = fields.Many2one('res.currency', string='Currency')
     gross_income = fields.Monetary('Gross Income', currency_field='currency_id')
     color = fields.Integer(string='Color Index', default=4)

     appl_amount = fields.Monetary('Required Amount', currency_field='currency_id')
     approved_amount = fields.Monetary('Approved Amount', currency_field='currency_id')
     total_amount = fields.Monetary('Total of all applications', currency_field='currency_id')

     position = fields.Char('Position')
     postal_address = fields.Char('Postal Address')
     surname = fields.Char('Surname')
     gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
     physical_address = fields.Char('Physical address')
     id_number = fields.Char('ID Number')
     state = fields.Selection([('new', 'New'), ('shortlisted', 'Shortlisted'),
                                ('accepted', ' Accepted'), ('decline', ' Decline')],string='Application Status', default='new',
                               group_expand='_expand_states', index=True)
     certified_identity_document_applicant = fields.Binary(string='Identity Document')
     letter_stating_financial_need = fields.Binary(string='Financial Need Letter')
     academic_record_acceptance_letter = fields.Binary(string='Academic Record / Acceptance Letter')
     income_proof = fields.Binary(string='Guardian or Parent Income Proof')
     affidavit = fields.Binary(string='Affidavit')
     institution_invoice_quotation = fields.Binary(string='Institution Invoice quotation')
     npo_ngo_reg_docs   = fields.Binary(string='NPO/NGO Registration Documents')
     proposal_w_budget = fields.Binary(string='Proposal With Budget')
     tax_exemption_docs = fields.Binary(string='Tax Exemption Documents')
     npo_invoice    = fields.Binary(string='NPO/NGO Invoice')

    #submission declarations
     has_invoice = fields.Boolean(default=False)
     has_proof_of_income = fields.Boolean(default=False)
     has_npo_ngo_reg_doc = fields.Boolean(default=False)
     has_id_copies = fields.Boolean(default=False)
     has_proposal_budget = fields.Boolean(default=False)
     has_tax_exemption = fields.Boolean(default=False)
     
     def _expand_states(self, states, domain, order):
         return [key for key, val in type(self).state.selection]
     
     @api.onchange('state')
     def onchange_state(self):
        if self.state == 'accepted':
            self.color = 10
        if self.state == 'decline':
            self.color = 1
        if self.state == 'new':
            self.color = 4
            
     @api.onchange("self_support_statement")
     def onchange_support_statement(self):
         self.self_support_statement = self.self_support_statement.strip()
     
     @api.onchange("physical_address")
     def onchange_physical_address(self):
         self.physical_address = self.physical_address.strip()
     
     @api.onchange("postal_address")
     def onchange_postal_address(self):
         self.postal_address = self.postal_address.strip()
     
     @api.onchange('approved_amount')
     def onchange_state(self):
        
        total = self.total_amount
        
        total += self.approved_amount
        
        total_id = self.env['thusano.fund'].write({
            
                'total_amount' : total
            })

     @api.model
     def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['serial_number'] = self.env['ir.sequence'].next_by_code('thusano.fund')
        rec_obj = super(ThusanoFundApplication, self).create(values)
       
        return rec_obj
            
     def shortlist_state(self):
        res = self.write({'state': 'shortlisted'})    
        return res
    
     def accept_state(self):
        res = self.write({'state': 'accepted'})    
        return res
    
     def decline_state(self):
         for rec in self:
             rec.write({'state': 'decline'})
             
         return {
            'type': 'ir.actions.act_window',
            'name': 'Application Rejection Reason',
            'res_model': 'thusano.reject.reason',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('thusano_fund.thusano_reject_form').id),
            'target': 'new',
            'context': {'default_applicant_name':self.name,'default_email_recipient':self.email,'default_applicaiton_id': self.id}
        }

     @api.onchange('id_number')
     def onchange_id_number(self):
        """ South African Identity number validation."""
        if self.id_number:
            try:
                if int(self.id_number[:2]) < 50:
                    date = "20" + self.id_number[:2] + "-" + self.id_number[2:4] + "-" + self.id_number[4:6]
                    b_date = datetime.strptime(date, '%Y-%m-%d')
                    temp_date = datetime.today().strftime('%Y-%m-%d')
                    current_date = datetime.strptime(temp_date, '%Y-%m-%d')
                    difference_in_years = relativedelta(current_date, b_date).years
                    if difference_in_years < 14 or difference_in_years > 35:
                        raise UserError(_('You are not on our age group'))
                    else:
                        self.age = difference_in_years
                else:
                    date = "19" + self.id_number[:2] + "-" + self.id_number[2:4] + "-" + self.id_number[4:6]
                    b_date = datetime.strptime(date, '%Y-%m-%d')
                    temp_date = datetime.today().strftime('%Y-%m-%d')
                    current_date = datetime.strptime(temp_date, '%Y-%m-%d')
                    difference_in_years = relativedelta(current_date, b_date).years
                    if difference_in_years < 14 or difference_in_years > 34:
                        raise UserError(_('You are not on our age group'))
                    else:
                        self.age = difference_in_years
            except Exception:
                raise UserError(_('You are not on our age group'))

    # validation for mobile field
     @api.onchange('cell_phone_number')
     def onchange_cell_phone_number(self):
        """ Phone validation for only digits and 10 length """
        if self.cell_phone_number:
            if self.cell_phone_number.isdigit():
                if len(self.cell_phone_number) != 10:
                    raise UserError(_('Number Must be 10 digits'))
            else:
                raise UserError(_("Phone number should only contain digits."))

    # validation for mobile field
     @api.onchange('alternative_number')
     def onchange_alternative_number(self):
        """ Alternative phone validation for only digits and 10 length """
        if self.alternative_number:
            if self.alternative_number.isdigit():
                if len(self.alternative_number) != 10:
                    raise UserError(_('Number Must be 10 digits'))
            else:
                raise UserError(_("Alternative Phone number should only contain digits."))

     @api.onchange('email')
     def onchange_email(self):
        """ Email validation """
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if self.email:
            if not re.search(regex, self.email):
                raise UserError(_("Please Enter valid email address."))