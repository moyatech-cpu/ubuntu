# coding=utf-8
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
from lxml import etree

_logger = logging.getLogger(__name__)

class RFQProcureStage(models.Model):
    _name = "scm.rfq.stage"
    _description = "Stage of RFQ"
    _order = 'sequence'

    name        = fields.Char("Stage name", required=True, translate=True)
    sequence    = fields.Integer("Sequence", default=10,help="Gives the sequence order when displaying a list of stages.")
    fold        = fields.Boolean("Folded in RFQ Pipe",
                          help="This stage is folded in the kanban view when there are no records in that stage to display.")

class RFQProcurement(models.Model):
    """ Model for SCM RFQ processes """
    _inherit = 'purchase.requisition'
    
    @api.multi
    def default_employee_id(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.id

    @api.multi
    def default_division(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.department_id.id     

    @api.multi
    def default_work_phone(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.work_phone
            
    state                       = fields.Selection([('new', 'Determine what to procure'),
                                                    ('select_suppliers', 'Select suppliers from database'), 
                                                    ('solicit_quotations', 'Solicit quotations'),
                                                    ('receive_quotations', 'Receive quotations'),
                                                    ('check_compliance', 'Check compliance'),
                                                    ('functional_evaluation', 'Functional evaluation'),
                                                    ('bee_price_evaluation', 'BEE plus Price evaluation'),
                                                    ('recommendation', 'Recommendation'),
                                                    ('review_recommendation', 'Review Recommendation'),
                                                    ('raise_purchase_order', 'Raise purchase order'),
                                                    ('purchase_order_approval', 'Purchase order approval'),
                                                    ('send_servie_provider_po', 'Send PO to service provider'),
                                                    ('administer_contracts', 'Administer contracts'),
                                                    ('confirm_delivery', 'Confirm delivery'),
                                                    ('report_on_delivery', 'Report on delivery'),
                                                    ('finished', 'Finished'),
                                                    ('rejected', 'Rejected'),('cancelled', 'Cancelled')],string='Status', default='new',
                                                    group_expand='_expand_states', index=True)

    name                        = fields.Char("Name", required=True, translate=True)
    rfq_number                  = fields.Char("RFQ Number")
    supplier_shortlist          = fields.One2many('scm.rfq.supplier.shortlist','rfq_id',string='Suppliers Shortlist')
    employee                    = fields.Many2one('hr.employee', string="Requester", related_sudo=False, default=lambda self: self.default_employee_id())
    contact_no                  = fields.Char("Contact No", default=lambda self: self.default_work_phone())
    division_id                 = fields.Many2one('hr.department', string="Division", related_sudo=False, default=lambda self: self.default_division())
    request_date                = fields.Datetime(string='Request Date', default=fields.Datetime.now)
    rfq_validity_period         = fields.Selection([('30 days', '30 days'), ('60 days', '60 days'), 
                                                    ('90 days', '90 days'),('180 days', '180 days')],
                                                   string="Validity Period")
    description                 = fields.Text(string='Description')
    recommendation              = fields.Text(string='Recommendation')
    cancel_reason               = fields.Text(string='Cancel Reason')
    reject_reason               = fields.Text(string='Reject Reason')
    submission_method           = fields.Selection([('Email', 'Email'), ('Physical', 'Physical')],string="Submission Method")
    
    functional_evaluation       = fields.Boolean(default=False)
    preference_point_system     = fields.Selection([('80', '80/20'), ('90', '90/10')],
                                                   string="Preference Points System")    
    closing_date_time           = fields.Datetime(string='Closing Date')
    color                       = fields.Integer(string='Color Index', default=4)
    active                      = fields.Boolean(default=True)    
    
    @api.onchange('state')
    def onchange_state(self):
        if self.state == 'new':
            self.color = 10
        if self.state == 'check_compliance':
            self.color = 1
        if self.state == 'recommendation':
            self.color = 4
        if self.state == 'finished':
            self.color = 3
                
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]    

    @api.model
    def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['rfq_number'] = self.env['ir.sequence'].next_by_code('scm.rfq.seq')
        rec_obj = super(RFQProcurement, self).create(values)
       
        return rec_obj   
    
    @api.multi
    def import_csv(self):
        # this will get executed when you click the import button in your form
        return {}
                                                        
    def new_completed(self):
        res = self.write({'state': 'select_suppliers'})    
        return res

    def select_suppliers_completed(self):
        res = self.write({'state': 'solicit_quotations'})    
        return res
    
    def solicit_quotations_completed(self):
        res = self.write({'state': 'receive_quotations'})    
        return res
    
    def receive_quotations_completed(self):
        res = self.write({'state': 'check_compliance'})    
        return res
    
    def compliance_evaluation_completed(self):
        res = self.write({'state': 'functional_evaluation'})    
        return res
    
    def functional_evaluation_completed(self):
        res = self.write({'state': 'bee_price_evaluation'})    
        return res
    
    def price_evaluation_completed(self):
        res = self.write({'state': 'recommendation'})    
        return res
    
    def recommendation_completed(self):
        res = self.write({'state': 'raise_purchase_order'})    
        return res
    
    def raise_po_completed(self):
        res = self.write({'state': 'purchase_order_approval'})    
        return res                        

    def po_approval_completed(self):
        res = self.write({'state': 'send_servie_provider_po'})    
        return res
    
    def send_po_completed(self):
        res = self.write({'state': 'administer_contracts'})    
        return res
    
    def administer_contract_completed(self):
        res = self.write({'state': 'confirm_delivery'})    
        return res
    
    def delivery_completed(self):
        res = self.write({'state': 'report_on_delivery'})    
        return res
    
    def delivery_report_completed(self):
        res = self.write({'state': 'finished'})    
        return res

    
class RFQSupplierShortlist(models.Model):    
    _name = 'scm.rfq.supplier.shortlist'
    
    rfq_id                  = fields.Many2one('purchase.requisition',string='RFQ')
    legal_name              = fields.Char(string="Legal Name")
    supplier_number         = fields.Char(string="Supplier Number")
    name                    = fields.Char(string="Name")
    surname                 = fields.Char(string="Surname")
    cellphone_number        = fields.Char(string="Cellphone Number")
    email_address           = fields.Char(string="Email Address")
    local_address           = fields.Char(string="Local Address")
    tax_status              = fields.Char(string="Tax Status")
    quotation_submitted     = fields.Boolean(string="Quotation Submitted")
    restricted_supplier     = fields.Char(string="Restricted Supplier")
    trading_name            = fields.Char(string="Trading Name")
    compliance_eligibility  = fields.Boolean(string='Compliance Eligibility')    
    
    functionality_score         = fields.Float(string='Functionality Score')   
    functionality_score_pass    = fields.Boolean(string='Functionality Pass')
    
    price_total                 = fields.Float(string='Price Total')
    price_score                 = fields.Float(string='Price Score')
    
    bee_level                   = fields.Integer(string='BEE Level')
    bee_score                   = fields.Integer(string='BEE Score')
        
    total_score                 = fields.Float(string='Total Score')
    
    
    def calculate_price_bee_score(self):
    
        #1.Get the RFQ Submission to Update
        submissions = self.env['scm.rfq.supplier.shortlist'].sudo().search([('rfq_id', '=', self.rfq_id.id)])
        
        prices = []
        for submission in submissions:
            #Add prices to list
            prices.append(submission.price_total)
          
        #Deduce the minimum from list
        minimum_price = min(prices)
        bee_score = 0
        for submission_item in submissions:
            #Calculate Price Score base on scoring system
            if self.rfq_id.preference_point_system == '80':
                price_score = 80*(1-((submission_item.price_total - minimum_price)/minimum_price))
            
                #Calculate BEE Score base on 80/20 scoring system
                if submission_item.bee_level == 1:
                  bee_score = 20
                elif submission_item.bee_level == 2:
                  bee_score = 18
                elif submission_item.bee_level == 3:
                  bee_score = 14
                elif submission_item.bee_level == 4:
                  bee_score = 12
                elif submission_item.bee_level == 5:
                  bee_score = 8
                elif submission_item.bee_level == 6:
                  bee_score = 6
                elif submission_item.bee_level == 7:
                  bee_score = 4
                elif submission_item.bee_level == 8:
                  bee_score = 2
                else:
                  bee_score = 0    
            
            else:
                price_score = 90*(1-((submission_item.price_total - minimum_price)/minimum_price))
            
                #Calculate BEE Score base on 90/10 scoring system
                if submission_item.bee_level == 1:
                  bee_score = 10
                elif submission_item.bee_level == 2:
                  bee_score = 8
                elif submission_item.bee_level == 3:
                  bee_score = 6
                elif submission_item.bee_level == 4:
                  bee_score = 5
                elif submission_item.bee_level == 5:
                  bee_score = 4
                elif submission_item.bee_level == 6:
                  bee_score = 3
                elif submission_item.bee_level == 7:
                  bee_score = 2
                elif submission_item.bee_level == 8:
                  bee_score = 1
                else:
                  bee_score = 0    
          
        total_score = (price_score + bee_score)
          
        submission_item.write({'bee_score': bee_score})
        submission_item.write({'price_score': price_score})
        submission_item.write({'total_score': total_score})    
    