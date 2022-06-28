from datetime import date
from odoo import api, fields, models



class Invoice(models.Model):
    _name='grant.quotation'
    _rec_name='supplier_name'
    
    partner_id = fields.Many2one('res.partner',string='Supplier')
    supplier_name = fields.Char('Supplier Name')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    total_amount = fields.Monetary('Total Quotation Amount')
    bank_account_ids = fields.Many2one('res.partner.bank',string="Bank Account Details")
    date_invoice = fields.Date('Quotation Date')
    description = fields.Text('Description')
    
    percentage = fields.Integer('%')
    quantity = fields.Integer("Quantity")
    doc_number = fields.Char('Document Number')
    
    grant_id = fields.Many2one('grant.application',string='Grant Application ID')
    
    
class GrantApplication(models.Model):
    _inherit = 'grant.application'
    
    quotation_records = fields.One2many('grant.quotation','grant_id',string="Quotation Details")
    #quotation_records = fields.Many2many('grant.quotation',string="Quotation Details")
    quotation_sum = fields.Float('Quotation Sum', compute="_compute_sum")
    
    @api.multi
    @api.onchange('quotation_records')
    @api.depends('quotation_records')
    def _compute_sum(self):
        
        for record in self:
            total_sum = 0
            for rec in record['quotation_records']:
                total_sum = total_sum + rec['total_amount']
            record['quotation_sum'] = total_sum
            
class DisbursementPack(models.TransientModel):
    _inherit = 'disbursement.pack.wiz'

    #quatation_attech_ids = fields.Many2many('ir.attachment', string='Quotation')
    quotation_records = fields.One2many('grant.quotation','grant_id',string="Quotation Details")
    #quotation_records = fields.Many2many('grant.quotation',string="Quotation Details")
    
    @api.multi
    def disbursement_pack_req(self):
        #This will be sorted by active_id on field context
        gapp = self.env['grant.application'].browse(self._context.get('active_id'))
        for record in self:
            for rec in record['quotation_records']:
                rec.grant_id = gapp.id        
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
            'quotation_records':[(6, 0, self.quotation_records.ids)],
            
        })
        return True
