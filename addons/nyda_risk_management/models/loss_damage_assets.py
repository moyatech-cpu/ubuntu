# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class ParticularClaims(models.Model):
    """ Particular Claims """
    _name = "particular.claims"
    _description = "Particular Claims"
    _rec_name = "description_of_property_damaged"

    description_of_property_damaged = fields.Char(string="Description of Property Damaged")
    date_of_purchase = fields.Datetime(string="Date Of Purchase")
    cost_price = fields.Char(string="Cost Price")
    depreciation =fields.Char(string="Depreciation")
    depreciated_value_of_property = fields.Char(string="Depreciated Value of Property at time of Damage")
    value_of_salvage = fields.Char(string="Value of Salvage")
    amount_claimed = fields.Char(string="Amount Claimed including VAT")
    loss_damage_assets_id = fields.Many2one('loss.damage.assets', string="Loss Damage Assets")


class LossDamageAssets(models.Model):
    """ Loss/Damage Assets model to capture claims by user """
    _name = "loss.damage.assets"
    _description = "Loss/Damage Assets Claim"
    _rec_name = "name"

    @api.multi
    def default_employee_id(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.id

    @api.multi
    def default_phone(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.work_phone

    @api.multi
    def default_branch(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.x_branch_id.id
                        
    # General Data
    name = fields.Char('Name')
    state = fields.Selection([('new', 'New'),
                              ('submitted', 'Submitted'),
                              ('approved_by_lm', 'Approved by Line Manager'),
                              ('rejected_by_lm', 'Rejected by Line Manager'),
                              ('review_by_lm', 'Review by Line Manager'),
                              ('approved_by_bm', 'Approved by Branch Manager'),
                              ('approved_by_hod', 'Approved by Head of Department'),
                              ('submitted_to_rm', 'Submitted to Risk Manager'),
                              ('review_by_rm', 'Review by Risk Manager'),
                              ('submitted_to_ed', 'Submitted to Executive director'),
                              ('approved_by_ed', 'Approved by Executive Director'),
                              ('req_cfo', 'Request Permission the CFO'),
                              ('app_cfo', 'CFO Approved'),
                              ('rej_cfo', 'CFO Rejected'),
                              ('rev_ceo', 'CEO Review'),
                              ('rej_ceo', 'CEO Reject'),
                              ('app_ceo', 'CEO Approved'),
                              ('waiver', 'Waiver'),
                              ('recovery', 'Recovery'),
                              ('finance', 'Submitted to Finance'),
                              ('ass_dis_rec', 'Assets Disposes/Recovered'),
                              ('review_by_am', 'Reviewing by Asset Manager'),
                              ('review_by_ro', 'Review by Risk Officer')]
                             , string='States', default='new')
    report_type = fields.Selection([('internal', 'Internal'),
                                    ('debt', 'Debt Acknowledgement'),
                                    ('waiver', 'Waiver of Debt Payment Form'),
                                    ('general', 'General')],
                                   string="Report Type")
    type_of_incident = fields.Selection([('loss_theft', 'Loss/Theft'), ('damaged', 'Damaged')],
                                        default='damaged', string="Type of Incident")
    poe_for_damaged_incident = fields.Binary(string="POE For Damaged Incident")
    poe_for_damaged_incident_filename = fields.Char(string="Damaged POE File name")
    
    employee_id = fields.Many2one('hr.employee', string="Name of Staff Member", readonly=True, default = lambda self: self.default_employee_id())
    phone = fields.Char('Phone Number', related="employee_id.mobile_phone", readonly=True, default = lambda self: self.default_phone())
    branch_id = fields.Many2one('res.branch', strign="Branch", readonly=True, default = lambda self: self.default_branch())
    
    loss_damage_assets_ids = fields.One2many('particular.claims', 'loss_damage_assets_id', string="Loss Damage Assets")
    insured_signature = fields.Binary(string="Insured Signature")
    insureds_vat_reg_number = fields.Char(string="Insureds VAT Registration Number")
    claim_date = fields.Datetime(string="Claim Date")

    # Banking details
    acc_holders_full_name = fields.Char(string="Account holder’s full name")
    bank_name = fields.Char(string="Bank Name")
    acc_number = fields.Char(string="Account Number")
    branch_code = fields.Integer(string="Branch Code")

    # Details of Loss/Damage
    date_of_loss = fields.Datetime('Date and time of Loss/Damage', default=fields.datetime.now())
    time_of_discovery = fields.Datetime('When was the Loss/Damage discovered?', default=fields.datetime.now())
    place_where_occurred = fields.Text('Place where loss/Damage Occurred?')
    entry = fields.Char('How was entry gained?')
    doors_locked = fields.Boolean('Were all doors locked?', default=False)
    last_location = fields.Char('Where was the device at the time of theft or damage?')
    previously_lodged_claim = fields.Boolean('Have you previously lodge claim?', default=False)
    description_previous_claim = fields.Text('Description of previous claim')
    by_whom = fields.Text(string="If so by whom ?")
    when_occupied = fields.Text(string="If not, when last occupied ?")
    address_premises =  fields.Char(string="Address of the premises at which the theft/loss/fire/damage occurred")
    cause_of_the_loss = fields.Text(
        string="Describe the cause of the loss or damage and the manner in which it occurred")
    were_premises_inhabited = fields.Text(
        string="Were the premises inhabited at the time of the theft/loss/fire/damage ?")
    how_the_premises_were_occupied = fields.Text(
        string="Please state exactly how the premises were occupied at the time of the theft/loss/fire/damage.")
    sole_onwer = fields.Boolean(string="Are you the sole owner of the property which is the subject of this claim ?")
    insured_against_the_loss_or_damage = fields.Boolean(
        string="Is the property which is the subject of this claim insured against the loss or damage described above by any other insurance?")
    amount_of_fire_insurance = fields.Char(string="amount_of_fire_insurance")
    name_of_fire_ins_company = fields.Char(string="Name Of Fire Insurance Company")
    steps_taken_to_prevent_loss = fields.Text(string="What steps are being taken to prevent a recurrence of loss ?")
    details_of_previous_losses = fields.Text(string="Please give details of previous losses")

    # Cause of Loss/Damage
    full_description = fields.Text('Describe fully how the loss / damage occurred stating how (if applicable) entry was gained to premises')
    is_by_someone = fields.Boolean('Is Loss/Damage done by another party?', default=False)
    description_another_party = fields.Text('Name and Address of another party')

    # Police Case Details
    is_police_reported = fields.Boolean('Reported to Police')
    not_reported_reason = fields.Text("Please provide proper reason for not reporting to Police")
    police_station = fields.Char('Police Station')
    police_reference_no = fields.Char('Police Reference Number')
    date_reported = fields.Date('Date Reported', default=fields.Date.today())
    police_report_affidavit = fields.Binary('Affidavit from Police')
    payment_method = fields.Selection(
        [('excess_payable_by_employee', 'Excess is payable by the employee which is 10% of the insurance claim'),
         ('ceo_request_to_waiver_off_excess',
          'Risk Management Unit may write to the CEO requesting to waiver off excess amount in certain instances'),
         ('amt_payable_by_emp',
          'Employees will be responsible to pay full replacement amount for lost or damaged assets due to negligence'),
         ('card', '3G Card (Full replacement cost once off payment)'),
         ('laptop charger', 'Laptop charger (Full replacement cost)')
         ], string="Payment Method")
    payment_option = fields.Selection(
        [('once_off_payment', 'Once off Payment (full excess amount as per the insurance loss agreement form)'),
         ('installment', '3 months’ instalment [(excess amount as per the insurance loss agreement form/3 months)]')],
        string="Payment Option")
    payment_description = fields.Text(string="Description")

    #  Signatures and Dates
    employee_sign = fields.Binary('Employee Signature')
    employee_sign_date = fields.Date('Employee Signature Date')
    line_manager_sign = fields.Binary('Line Manager Signature')
    line_manager_sign_date = fields.Date('Line Manager Signature Date')
    branch_manager_sign = fields.Binary('Branch Manager Signature')
    branch_manager_sign_date = fields.Date('Branch Manager Signature Date')
    hod_sign = fields.Binary('Head of Division Signature')
    hod_sign_date = fields.Date('Head of Division Signature Date')
    risk_manager_sign = fields.Binary('Risk Manager Signature')
    risk_manager_sign_date = fields.Date('Risk Manager Signature Date')

    # employee checklist
    is_proof_of_forcible_entry = fields.Boolean(string="Proof Of Forcible Entry Submitted")
    is_police_case_number = fields.Boolean(string="Police Case Number Submitted")
    is_affidavit_from_police = fields.Boolean(string="Affidavit From the Police")
    is_copy_of_invoice = fields.Boolean(string="Copy of Invoice for repairs due to forcible entry")
    is_assets_general_information = fields.Boolean(string="Assets Genral Information")
    is_quotation_of_similar_asset = fields.Boolean(string="Quotation Of Similar Asset")
    is_itc_number = fields.Boolean(string="ITC number (Blacklisting ref – Cellphone)")
    is_damaged_report = fields.Boolean(string="Damaged Report")

    @api.multi
    def create_view_insurance_excess(self):
        rec = self.env['insurance.excess'].sudo().search([('loss_damage_assets_id', '=', self.id)])
        view_id = self.env.ref('nyda_risk_management.insurance_excess_form').id
        if not rec:
            return {'name': 'Insurance Excess',
                    'view_type': 'form',
                    'view_mode': 'tree',
                    'views': [(view_id or False, 'form')],
                    'res_model': 'insurance.excess',
                    'view_id': view_id or False,
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                    'context': {'default_loss_damage_assets_id': self.id, 'default_employee_id': self.employee_id.id}
                    }
        elif len(rec) == 1:
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form,tree',
                'views': [(view_id or False, 'form')],
                'res_model': 'insurance.excess',
                'view_id': view_id or False,
                'target': 'current',
                'res_id': rec.id,
                'domain': [('id', '=', rec.id)],
            }
        else:
            raise UserError(_("There are multiple records of insurance for %s!!") % (self.name))

    @api.model
    def create(self, values):
        """ test """
        res = super(LossDamageAssets, self).create(values)
        res.name = self.env['ir.sequence'].next_by_code('loss.damage.assets') or _("New")
        return res

    @api.onchange('employee_id')
    def onchnage_staff_member(self):
        """Number will change on change of staff member"""
        if self.employee_id:
            self.phone = self.employee_id.mobile_phone
        else:
            self.phone = ''

    def line_manager_submitted(self):
        """Submitted to line manager"""
        self.state = "submitted"

    def line_manager_approved(self):
        """Approved by line manager"""
        self.state = "review_by_ro"

    def line_manager_rejected(self):
        """Rejected by line manager"""
        self.state = "rejected_by_lm"

    def line_manager_review(self):
        """Review by line manager"""
        self.state = "review_by_lm"

    def risk_officer_review(self):
        """Review by risk officer"""
        self.state = "review_by_ro"

    def risk_manager_submit(self):
        """Review by risk officer"""
        rec = self.env['insurance.excess'].sudo().search([('loss_damage_assets_id', '=', self.id)])
        if rec and len(rec) == 1:
            self.state = "review_by_rm"
        elif len(rec) > 1:
        	self.state = "review_by_rm"
        elif not rec:
        	self.state = "review_by_rm"

    @api.multi
    def create_view_assessment(self):
        rec = self.env['recovery'].sudo().search([('loss_damage_assets_id', '=', self.id)])
        view_id = self.env.ref('nyda_risk_management.recovery_form').id
        if not rec:
            return {'name': 'Recovery',
                    'view_type': 'form',
                    'view_mode': 'tree',
                    'views': [(view_id or False, 'form')],
                    'res_model': 'recovery',
                    'view_id': view_id or False,
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                    'context': {'default_loss_damage_assets_id': self.id,
                                'default_employee_id': self.employee_id.id}
                    }
        elif len(rec) == 1:
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form,tree',
                'views': [(view_id or False, 'form')],
                'res_model': 'recovery',
                'view_id': view_id or False,
                'target': 'current',
                'res_id': rec.id,
                'domain': [('id', '=', rec.id)],
            }
        else:
            raise UserError(_("There are multiple records of debt for %s!!") % (self.name))

    def req_perm_cfo(self):
        """Review by risk officer"""
        rec = self.env['recovery'].sudo().search([('loss_damage_assets_id', '=', self.id)])
        if rec and len(rec) == 1:
            self.state = "req_cfo"
        elif len(rec) > 1:
        	self.state = "req_cfo"
        elif not rec:
        	self.state = "req_cfo"

    def risk_manager_review(self):
        """Review by risk manager"""
        self.state = "review_by_rm"

    def submit_to_ed(self):
        """Submitted to ED"""
        self.state = "submitted_to_ed"

    def approved_by_exe_dir(self):
        """Approved to ED"""
        self.state = "review_by_am"

    def review_by_asset_man(self):
        """Reviewed by asset manager"""
        self.state = "review_by_am"

    def cfo_rejected(self):
        """Rejected by CFO"""
        self.state = "rej_cfo"

    def cfo_approved(self):
        """Approved by CFO"""
        self.state = "rev_ceo"

    def review_ceo(self):
        """Reviewing by CEO"""
        self.state = "rev_ceo"

    def approve_ceo(self):
        """Approved by CEO"""
        self.state = "app_ceo"

    def reject_ceo(self):
        """Reject by CEO"""
        self.state = "rej_ceo"

    def asset_dis_rec(self):
        """Assets Disposes Recovered"""
        self.state = "ass_dis_rec"

    def ceo_waiver(self):
        """Employee doesnt have to pay."""
        self.state = "waiver"     	

    def ceo_recovery(self):
        """Employee has to pay either a portion or full amount as determined by process"""
        self.state = "recovery"
                	
    def submit_finance(self):
        """The recovery details are sent to finance for processing"""
        self.state = "finance"                	
