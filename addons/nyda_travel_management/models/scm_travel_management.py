# coding=utf-8
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
from lxml import etree

_logger = logging.getLogger(__name__)

class SCMTravelManagement(models.Model):
    """ SCM Travel Management Module """
    _name       = 'scm.travel.management'
    _rec_name   = 'travel_employee'
    
    @api.multi
    def default_surname(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.name

    @api.multi
    def default_firstname(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.x_first_name

    @api.multi
    def default_secondname(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.x_second_name

    @api.multi
    def default_division(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.department_id.id

    @api.multi
    def default_position(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.job_id.id

    @api.multi
    def default_province(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.province_id.id

    @api.multi
    def default_qualification(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.previous_qualification

    @api.multi
    def default_id_num(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.app_identity_number

    @api.multi
    def default_manager(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.parent_id

    @api.multi
    def default_reports_to(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.x_reports_to
                
    @api.multi
    def default_employee_id(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.id
    
    
    traveller                               = fields.Many2many('hr.employee',string="Traveller(s)" , related_sudo=False)
    intl_travel_id                          = fields.One2many('intl.travel','intl_travel_task_id',string='International Travel Reference')
    accommodation_id                        = fields.One2many('travel.accommodation','accommodation_task_id',string='Travel Accommodation Reference')
    travel_shuttle_hire_id                  = fields.One2many('travel.shuttle.hire','shuttle_hire_task_id',string='Travel Shuttle Hire Reference')
    travel_flight_id                        = fields.One2many('travel.flight','flight_task_id',string='Travel Flight Reference')
    travel_fleet_hire_id                    = fields.One2many('travel.fleet.hire','fleet_hire_task_id',string='Travel Fleet Hire Reference')
    travel_car_hire_id                      = fields.One2many('travel.car.hire','car_hire_task_id',string='Travel Car Hire Reference')        
    travel_employee                         = fields.Many2one('hr.employee', string="Requester", related_sudo=False, default=lambda self: self.default_employee_id())
    state                                   = fields.Selection([('new', 'New'),
                                                                ('review', 'Review'), 
                                                                ('approved', 'Approved'),
                                                                ('authorised', 'Authorised'),
                                                                ('rejected', 'Rejected'),
                                                                ],string='Status', default='new')    
    
    #Employee Details
    travel_full_name                        = fields.Char(related='travel_employee.name', string='Full Name', readonly=True, related_sudo=False)
    travel_surname                          = fields.Char(related='travel_employee.surname', string='Surname', readonly=True, related_sudo=False)
    travel_identity_number                  = fields.Char(related='travel_employee.identification_id', string='Identity No', readonly=True, related_sudo=False)
    travel_branch                           = fields.Many2one(related='travel_employee.branch_id', string='Branch', readonly=True, related_sudo=False)
    travel_contact_details                  = fields.Char(related='travel_employee.work_phone', string='Contact Details', readonly=True, related_sudo=False)
    travel_position                         = fields.Many2one(related='travel_employee.job_id', string='Position', readonly=True, related_sudo=False)
    travel_signature                        = fields.Binary(string='Travel Signature')
    
    travel_completion_date                  = fields.Datetime(string='Completion Date', default=fields.Datetime.now)
    travel_budget_allocation                = fields.Float(string='Budget Allocation')
    #travel_division                        = fields.Many2one('hr.department', string='Division', default=lambda self: self.default_division())
    travel_programme                        = fields.Many2one('hr.department', string='Programme')
    travel_place_to_visit                   = fields.Char(string='Places to Visit')
    travel_purpose_of_visit                 = fields.Char(string='Purpose of visit')
    
    travel_admin                            = fields.Many2one('hr.employee', string='Travel Admin')
    travel_admin_signature                  = fields.Binary(string='Admin Signature')
    travel_admin_signature_date             = fields.Datetime(string='Signature Date')
    
    travel_reports_to                       = fields.Many2one(related='travel_employee.x_reports_to', string='Reporting Line', readonly=True, related_sudo=False, default=lambda self: self.default_reports_to())
    
    travel_line_manager                     = fields.Many2one(related='travel_employee.parent_id', string='Line Manager', readonly=True, related_sudo=False)
    travel_line_manager_signature           = fields.Binary(string='Admin Signature')
    travel_manager_signature_date           = fields.Datetime(string='Signature Date')
    travel_date                             = fields.Datetime(string='Travel Date')
    
    #Car Hire (Section A)    
    travel_car_hire_from                    = fields.Char(string='Hire From')
    travel_car_hire_to                      = fields.Char(string='Hire To')
    travel_car_hire_est_km                  = fields.Float(string='Estimated Km.')
    travel_car_hire_group                   = fields.Selection([('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D')],string="Car Hire Group?")
    travel_car_hire_departure_date          = fields.Datetime(string='Car Hire Departure Date')
    travel_car_hire_return_date             = fields.Datetime(string='Car Hire Return Date')
                
    #Flights (Section B)
    travel_flight_departure_from            = fields.Char(string='Departure From')
    travel_flight_departure_to              = fields.Char(string='Departure To')
    travel_flight_departure_date            = fields.Datetime(string='Departure Date')
    travel_flight_departure_arrival_date    = fields.Datetime(string='Depart Arrival Date')
    
    travel_flight_return_from               = fields.Char(string='Return From')
    travel_flight_return_to                 = fields.Char(string='Return To')
    travel_flight_return_departure_date     = fields.Datetime(string='Return Departure Date')
    travel_flight_return_arrival_date       = fields.Datetime(string='Return Arrival Date')
    
    #Accomodation (Section C)
    travel_accom_name                       = fields.Char(string='Accomodation Name')
    travel_accom_type                       = fields.Selection([('Bed and Breakfast', 'Bed and Breakfast'),
                                                                ('Hotel', 'Hotel'),
                                                                ('Motel', 'Motel')],string="Accomodation Type")
    travel_accom_meals_incl                 = fields.Selection([('Breakfast', 'Breakfast'),
                                                                ('Lunch', 'Lunch'),
                                                                ('Dinner', 'Dinner')],string="Accomodation Meals")
    travel_accom_check_in_date              = fields.Datetime(string='Check-in Date')
    travel_accom_checkout_date              = fields.Datetime(string='Check-out Date')
    travel_accom_shuttle_required           = fields.Selection([('No', 'No'),('Yes', 'Yes')],string="Shuttle Required")

    travel_emergency                        = fields.Selection([('Normal', 'Normal'),
                                                                ('Urgent', 'Urgent')],string="Travel Urgency", default='Normal')
        
    #Perdium
    travel_perdium_int_travel_depart_date   = fields.Datetime(string='Int. Departure Date')
    travel_perdium_int_travel_return_date   = fields.Datetime(string='Int. Return Date')
    travel_perdium_int_travel_num_nights    = fields.Float(string='Number of Nights')
    travel_perdium_int_travel_amount        = fields.Float(string='Amount')
    
    #Approval
    travel_approval_emp                     = fields.Many2one('hr.employee', string='Approver')
    travel_approval_emp_signature           = fields.Binary(string='Approver Signature')
    travel_approval_date                    = fields.Datetime(string='Approval Date')
    
    #Admin Authorisation
    travel_authorised_emp                   = fields.Many2one('hr.employee', string='Authoriser')
    travel_authorised_date                  = fields.Datetime(string='Authorised Date')
    
    travel_region                           = fields.Selection([('Local', 'Local'),
                                                                ('Regional', 'Regional'),
                                                                ('International', 'International')],string="Travel Region")   

    travel_delegated_authority              = fields.Selection([('Branch Manager', 'Branch Manager'),
                                                                ('Executive', 'Executive'),
                                                                ('CEO', 'CEO'),
                                                                ('Chairperson', 'Chairperson')],string="Delegated Authority", compute='get_delegated_authority')  
         
    travel_group_life_insurance             = fields.Boolean(string='Group Life Insurance')
    travel_international_travel_insurance   = fields.Boolean(string='International Travel Insurance')
    
    #For office use 
    travel_match_to_flight                  = fields.Boolean(string='Match to Flight')
    travel_match_to_accomodation            = fields.Boolean(string='Match to Accomodation')
    travel_match_to_car_hire                = fields.Boolean(string='Match to Car hire')
    travel_scm_officer                      = fields.Boolean(string="SCM Officer Check", compute='get_user')
    reject_reason                           = fields.Text(string="Reject Reason")

    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('nyda_travel_management.nyda_scm_travel_officer_user'):
            self.travel_scm_officer = True
        else:
            self.travel_scm_officer = False

    def get_delegated_authority(self):
        
        _logger.info(self.travel_reports_to.name)
        
        #2. Set Approval Authority based on Conditions of Travel
        if self.travel_reports_to.name == 'Branch Manager':
            self.travel_delegated_authority = 'Branch Manager'     
        elif self.travel_reports_to.name == 'Chief Executive Officer':
            self.travel_delegated_authority = 'CEO'
        elif self.travel_reports_to.name == 'Executive Chairperson':
            self.travel_delegated_authority = 'Chairperson'
        else:
            self.travel_delegated_authority = 'Executive'
        
        # All international to be approved by chairperson
        if self.travel_region == 'Regional' or self.travel_region == 'International':
            self.travel_delegated_authority = 'Chairperson'
            
    @api.onchange('travel_date')
    def validate_travel_date(self):
        
        #2. Set Approval Authority based on Conditions of Travel
        if self.travel_date:
            date_dt1 = datetime.strptime(self.travel_date, '%Y-%m-%d %H:%M:%S')
            date_dt2 = datetime.strptime(self.travel_completion_date, '%Y-%m-%d %H:%M:%S')
            #date_dt2 = datetime.now()
            delta = (date_dt1 - date_dt2)
            
            _logger.info(delta.days)
            
            #Validation - Cannot be less than five days if not emergency
            if self.travel_emergency == 'Normal':
                if delta.days < 5:
                    raise ValidationError(_("Travel requests must be logged 5 days prior the travel date."))
                         
    @api.model
    def create(self, vals):
        # context: no_log, because subtype already handle this
        context = dict(self.env.context, mail_create_nolog=True)
        
        #1. Create Unique Travel Number
        vals['name'] = self.env['ir.sequence'].next_by_code('scm.travel.seq') or _('New')
                
        #3. Stage change: Update date_end if folded stage
        if vals.get('stage_id'):
            vals.update(self.update_date_end(vals['stage_id']))
        travel = super(SCMTravelManagement, self.with_context(context)).create(vals)
        
        return travel
         
    def action_reject_travel(self):
        return {
            'name': _('Reject Reason'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('nyda_travel_management.scm_travel_reject_reason_form').id,
            'res_model': 'scm.travel.management',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
        }
        
   
    def has_car_hire(self):
        
        return self.travel_car_hire_id.travel_emp.id        
        
    
    def set_new(self):
        self.write({'state': 'new'})
        
    def set_internal_review(self):
        self.write({'state': 'review'})
        
    def set_approved(self):
        
        self.write({'state': 'approved', 'travel_approval_emp': self.default_employee_id(), 'travel_approval_date': datetime.now()})

        #Create a Purchase Order for Travel Cost Items
        po = self.env['purchase.order'].create({
                                                    'partner_id': 83551,
                                                    'date_planned': self.travel_date,
                                                    'x_scm_travel_id': self.id,
                                                    'origin': "Travel Request"
                                                })   

        #If Car Hire Booked then add product item
        for car_hire in self.travel_car_hire_id:
            po.write({
                        'order_line': [(0,0, {
                                                'product_id':2063,
                                                'name': "Local - Car Hire A",
                                                'product_qty':1,    
                                                'product_uom':1,  
                                                'price_unit':0,
                                                'account_analytic_id': 4210,
                                                'date_planned': self.travel_date,
                                        })]
                    })

        #If accomodation booked then add product item
        for accommodation_id in self.accommodation_id:
            po.write({
                        'order_line': [(0,0, {
                                                'product_id':2062,
                                                'name': "Local - Accommodation",
                                                'product_qty':1,
                                                'product_uom':1,
                                                'price_unit':0,
                                                'account_analytic_id': 4210,
                                                'date_planned': self.travel_date,
                                        })]
                    })

        #If flights booked then add product item
        for flight_id in self.travel_flight_id:
            po.write({
                        'order_line': [(0,0, {
                                                'product_id':2071,
                                                'name': "Local - Flights Economy Class",     
                                                'product_qty':1,      
                                                'product_uom':1,  
                                                'price_unit':0,                                                                                                                    
                                                'account_analytic_id': 4210,
                                                'date_planned': self.travel_date,
                                        })]
                    })                          

        #If flights booked then add product item
        for int_flight in self.intl_travel_id:
            po.write({
                        'order_line': [(0,0, {
                                                'product_id':2022,
                                                'name': "International - Flights Economy",   
                                                'product_qty':1,  
                                                'product_uom':1,      
                                                'price_unit':0,                                     
                                                'account_analytic_id': 4210,
                                                'date_planned': self.travel_date,
                                        })]
                    })   

    def action_purchase_order(self):
        return{
            
            'name': _('Travel Purchase Order'),
            "views": [[False, "tree"], [5421, "form"]],
            #'view_type': 'form',
            #'view_mode': 'form',
            #'view_id': self.env.ref('__export__.ir_ui_view_5421').id,
            'res_model': 'purchase.order',             
            'type': 'ir.actions.act_window',
            #'target': 'main',
            "domain": [["x_scm_travel_id", "=", self.id]],
            'context': {'default_x_scm_travel_id':self.id, 'default_partner_id':83551, 'no_breadcrumbs': True}
            
            }
                
    def set_rejected(self):
        self.write({'state': 'rejected', 'travel_approval_emp': self.default_employee_id(), 'travel_approval_date': datetime.now()})                                  

    def set_authorised(self):
        self.write({'state': 'authorised', 'travel_authorised_emp': self.default_employee_id(), 'travel_authorised_date': datetime.now()})