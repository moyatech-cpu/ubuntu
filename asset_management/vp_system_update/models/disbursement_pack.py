from datetime import date
from odoo import api, fields, models


class DisbursementPack(models.TransientModel):
    _name = 'disbursement.pack.wiz'
    _description = 'Disbursement Pack'

    cover_letter = fields.Binary(string='Cover Letter')
    cover_letter_name = fields.Char(string='File Name')
    supplier_checklist = fields.Binary(string='Supplier Checklist')
    supplier_checklist_name = fields.Char(string='File Name')
    quatation_attech_ids = fields.Many2many('ir.attachment', string='Quotation')
    bank_confirmation_ids = fields.Many2many('ir.attachment', string='Bank Confirmation')
    directors_attech_ids = fields.Many2many('ir.attachment', string="Director's ID")
    company_registration_attech_ids = fields.Many2many('ir.attachment', string="Company Registration Doc")
    # quatation_attech = fields.Binary(string='Quatation')
    # quatation_attech_name = fields.Char(string='File Name')
    # bank_confirmation = fields.Binary(string='Bank Confirmation')
    # bank_confirmation_name = fields.Char(string='File Name')
    # director_ide = fields.Binary(string="Director's ID")
    # director_ide_name = fields.Char(string='File Name')
    # company_registration_doc = fields.Binary(string='Company Registration Doc')
    # company_registration_doc_name = fields.Char(string='File Name')
    tax_clearance_doc = fields.Binary(string='Tax Clearance Certificate')
    tax_clearance_doc_name = fields.Char(string='File Name')

    @api.multi
    def disbursement_pack_req(self):
        grant_application = self.env['grant.application'].browse(self._context.get('active_id')).write({
            'cover_letter' : self.cover_letter,
            'cover_letter_name' : self.cover_letter_name,
            'supplier_checklist' : self.supplier_checklist,
            'supplier_checklist_name' : self.supplier_checklist_name,
            'quatation_attech_ids' : [(6, 0, self.quatation_attech_ids.ids)],
            'bank_confirmation_ids' : [(6, 0, self.bank_confirmation_ids.ids)],
            'directors_attech_ids' : [(6, 0, self.directors_attech_ids.ids)],
            'company_registration_attech_ids' : [(6, 0, self.company_registration_attech_ids.ids)],
            'x_disbursement_date':self.x_disbursement_date,
            'nyda_bdo_bool' : False,
            'nyda_branch_manager_bool' : False,
            'nyda_bcs_bool' : False,
            'nyda_qao_bool' : False,
            'nyda_edm_bool' : False,
            'nyda_bdo_r_bool' : False,
            'nyda_branch_manager_r_bool' : False,
            'nyda_bcs_r_bool' : False,
            'nyda_qao_r_bool' : False,
            'nyda_edm_r_bool' : False,
            'status': 'bdo_review',
        })
        # grant_application.status = 'disbursement'
        # grant_application.cover_letter = self.cover_letter
        # grant_application.cover_letter_name = self.cover_letter_name
        # grant_application.supplier_checklist = self.supplier_checklist
        # grant_application.supplier_checklist_name = self.supplier_checklist_name
        # grant_application.quatation_attech_ids = [(6, 0, self.quatation_attech_ids.ids)]
        # grant_application.bank_confirmation_ids = [(6, 0, self.bank_confirmation_ids.ids)]
        # grant_application.directors_attech_ids = [(6, 0, self.directors_attech_ids.ids)]
        # grant_application.company_registration_attech_ids = [(6, 0, self.company_registration_attech_ids.ids)]
        #
        # grant_application.nyda_bdo_bool = False
        # grant_application.nyda_branch_manager_bool = False
        # grant_application.nyda_bcs_bool = False
        # grant_application.nyda_qao_bool = False
        # grant_application.nyda_edm_bool = False
        #
        # grant_application.nyda_bdo_r_bool = False
        # grant_application.nyda_branch_manager_r_bool = False
        # grant_application.nyda_bcs_r_bool = False
        # grant_application.nyda_qao_r_bool = False
        # grant_application.nyda_edm_r_bool = False
        # grant_application.status = 'bdo_review'


        # grant_application.quatation_attech_name = self.quatation_attech_name
        # grant_application.bank_confirmation_name = self.bank_confirmation_name
        # grant_application.director_ide_name = self.director_ide_name
        # grant_application.company_registration_doc = self.company_registration_doc
        # grant_application.company_registration_doc_name = self.company_registration_doc_name
        # grant_application.tax_clearance_doc = self.tax_clearance_doc
        # grant_application.tax_clearance_doc_name = self.tax_clearance_doc_name

        return True
