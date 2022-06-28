# coding=utf-8

from odoo import api, fields, models, _
from odoo import http
from datetime import date, datetime


class GrantApplication(models.Model):
    """ Model to register all the applications for grant. """
    _inherit = 'grant.application'
    
    proof_of_residence = fields.Binary(string='Proof of Residence')
    proof_of_residence_name = fields.Char(string='Proof of Residence')
    
    curriculum_vitae = fields.Binary(string='Curriculum Vitae')
    curriculum_vitae_name = fields.Char(string='Curriculum Vitae')
    
    business_bank_account = fields.Binary(string='Business bank account')
    business_bank_account_name = fields.Char(string='Business bank account')
    
    supplier_quotations = fields.Binary(string='Supplier Quotations')
    supplier_quotations_name = fields.Char(string='Supplier Quotations')
    
    #Supplier quotations multiple 
    x_supplier_quotations_ids = fields.Many2many('ir.attachment',relation='x_supplier_quotations_rel',store=True,copy=True, string="Supplier Quotations")
    
    supplier_bank_details = fields.Binary(string='Supplier Bank Details')
    supplier_bank_details_name = fields.Char(string='Supplier Bank Details')
    
    six_month_personal_bs = fields.Binary(string='Six month personal Bank Statement')
    six_month_personal_bs_name = fields.Char(string='Six Month personal Bank Statement')
    
    six_month_business_bs = fields.Binary(string='Six month business Bank Statement')
    six_month_business_bs_name = fields.Char(string='six_month_business_bs')
    
    certificate_qualification = fields.Binary(string='Certificate Qualification')
    certificate_qualification_name = fields.Char(string='Certificate Qualification')
    
    six_twentyfour_bs = fields.Binary(string='Six to twenty-four month bank statement')
    six_twentyfour_bs_name = fields.Char(string='Six to twenty-four month bank statement')
    
    management_accounts = fields.Binary(string='Management Accounts')
    management_accounts_name = fields.Char(string='Management Accounts')
    
    buisness_asset_reg = fields.Binary(string='Business Asset Registration')
    buisness_asset_reg_name = fields.Char(string='Business Asset Registration')
    
    tax_certificate = fields.Binary(string='Tax Certificate')
    tax_certificate_name = fields.Char(string='Tax Certificate')
    
    
    