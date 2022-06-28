 # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError
import logging
from openerp.osv import orm

_logger = logging.getLogger(__name__)

class TravelRequestReport(models.TransientModel):
    """Travel Request Report"""
    _name           = "travel.request.report"
    _description    = 'Travel Request Report'

    start_date   = fields.Date(string="Start Date")
    end_date     = fields.Date(string="End Date")   
    programme    = fields.Many2one('hr.department', string='Division')
    emergency    = fields.Selection([('No', 'No'),('Yes', 'Yes')],string="Travel Emergency", default='No')
    
    region       = fields.Selection([('Local', 'Local'),
                                     ('Regional', 'Regional'),
                                     ('International', 'International')],string="Travel Region")

    status      = fields.Selection([('New', 'New'),('Pending', 'Pending'),
                                     ('Approved', 'Approved'),
                                     ('Rejected', 'Rejected')],string="Report Status")

    mode        = fields.Selection([('Air', 'Air'),
                                   ('Car', 'Car'),('Fleet', 'Fleet'),('Shuttle', 'Shuttle')],string="Travel Model")
            
    branch      = fields.Many2one('x_branch', string='Branch')
    
    accom_type  = fields.Selection([('Bed and Breakfast', 'Bed and Breakfast'),
                                    ('Hotel', 'Hotel'),
                                    ('Motel', 'Motel')],string="Accommodation Type")
         
    def get_travel_request_data(self):
        
        travel_request_list = []
        
        converted_start_date    = datetime.strptime(self.start_date, '%Y-%m-%d')
        converted_end_date      = datetime.strptime(self.end_date, '%Y-%m-%d')
        
        #Filter by programme
        if self.programme:
            travel_request_data = self.env['project.task'].search([('project_id', '=', 89),
                                                                   ('travel_programme', '=', self.programme)
                                                                   ])
         
        elif self.branch:
            travel_request_data = self.env['project.task'].search([('project_id', '=', 89),
                                                                   ('travel_branch', '=', self.travel_branch)
                                                                   ])
       
            
        elif self.region:
            travel_request_data = self.env['project.task'].search([('project_id', '=', 89),
                                                                   ('travel_region', '=', self.region)
                                                                   ])
        
        elif self.status:
            
            if self.status == 'Pending':
                travel_request_data = self.env['project.task'].search([('project_id', '=', 89),
                                                                   ('stage_id', '=', 488)
                                                                   ])
            else:
                travel_request_data = self.env['project.task'].search([('project_id', '=', 89),
                                                                   ('x_stage_name', '=', self.status)
                                                                   ])
     
            
        elif self.mode == 'Air':
            travel_request_data = self.env['project.task'].search([('project_id', '=', 89),
                                                                   ('travel_flight_id.flight_departure_from', '!=', False),
                                                                   ('travel_flight_id.flight_departure_to', '!=', False)])
          
            
        elif self.mode == 'Car':
            travel_request_data = self.env['project.task'].search([('project_id', '=', 89),
                                                                   ('travel_car_hire_id.car_hire_from', '!=', False),
                                                                   ('travel_car_hire_id.car_hire_to', '!=', False)])
          
        elif self.mode == 'Fleet':
            travel_request_data = self.env['project.task'].sudo().search([('project_id','=',89),
                                                                   ('travel_fleet_hire_id.fleet_hire_from', '!=', False),
                                                                   ('travel_fleet_hire_id.fleet_hire_to', '!=', False)])
  
        elif self.mode == 'Shuttle':
            travel_request_data = self.env['project.task'].sudo().search([('project_id','=',89),
                                                                   ('travel_shuttle_hire_id.shuttle_hire_from', '!=', False),
                                                                   ('travel_shuttle_hire_id.shuttle_hire_to', '!=', False)])
            
        else:
            travel_request_data = self.env['project.task'].search([('project_id', '=', 89)])
            
           
        
        if travel_request_data:
            for travel_request_data_date in travel_request_data:
                check_date = datetime.strptime(
                    datetime.strftime(datetime.strptime(travel_request_data_date.create_date, '%Y-%m-%d %H:%M:%S'),
                                      '%Y-%m-%d'), '%Y-%m-%d')
                if converted_start_date <= check_date <= converted_end_date:
                    temp={
                        'emp_name':travel_request_data_date.travel_employee.name,
                        'emp_position': travel_request_data_date.travel_position.name,
                        'emp_branch' : travel_request_data_date.travel_branch.x_name,
                        'travel_date':travel_request_data_date.travel_date,
                        'travel_region': travel_request_data_date.travel_region,
                        'travel_place_to_visit' :travel_request_data_date.travel_place_to_visit,
                        'travel_purpose_of_visit': travel_request_data_date.travel_purpose_of_visit,
                        'travel_emergency':travel_request_data_date.travel_emergency
                        }
            
                    travel_request_list.append(temp)

                    
        return {'start_date': self.start_date, 'end_date': self.end_date,
                'data': travel_request_list,
                'mode': self.mode
                }
        
    def get_travel_request_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_travel_management.action_travel_request_report').report_action(self)                                