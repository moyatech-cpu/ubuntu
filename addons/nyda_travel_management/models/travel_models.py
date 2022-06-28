# -*- coding: utf-8 -*-

from odoo import models, fields, api

class travelCarHire(models.Model):
    
    _name = 'travel.car.hire'
    
    name                             = fields.Char(string="Travel Car Hire")
    travel_emp                       = fields.Many2many('hr.employee',relation='travel_car_hire_request',column1='name',column2='user_id',string='Travel Employee',store=True,copy=True)
    car_hire_task_id                 = fields.Many2one('scm.travel.management',string='Travel Car Hire Task Reference')
    car_hire_from                    = fields.Char(string='Hire From')
    car_hire_to                      = fields.Char(string='Hire To')
    car_hire_est_km                  = fields.Float(string='Estimated Km.')
    car_hire_group                   = fields.Selection([('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D')],string="Fleet Hire Group?")
    car_hire_departure_date          = fields.Datetime(string='Departure Date')
    car_hire_return_date             = fields.Datetime(string='Return Date')

class travelFleetHire(models.Model):
    
    _name = 'travel.fleet.hire'
    
    name                               = fields.Char(string="Travel Fleet Hire")
    travel_emp                         = fields.Many2many('hr.employee',relation='travel_fleet_hire_request',column1='name',column2='user_id',string='Travel Employee',store=True,copy=True)
    fleet_hire_task_id                 = fields.Many2one('scm.travel.management',string='Travel Fleet Hire Task Reference')
    fleet_hire_from                    = fields.Char(string='Hire From')
    fleet_hire_to                      = fields.Char(string='Hire To')
    fleet_hire_est_km                  = fields.Float(string='Estimated Km.')
    fleet_hire_group                   = fields.Selection([('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D')],string="Fleet Hire Group?")
    fleet_hire_departure_date          = fields.Datetime(string='Departure Date')
    fleet_hire_return_date             = fields.Datetime(string='Return Date')

class travelShuttleHire(models.Model):
    
    _name = 'travel.shuttle.hire'

    name                                = fields.Char(string="Travel Shuttle Hire")
    travel_emp                          = fields.Many2many('hr.employee',relation='travel_shuttle_hire_request',column1='name',column2='user_id',string='Travel Employee',store=True,copy=True)
    shuttle_hire_task_id                = fields.Many2one('scm.travel.management',string='Travel Shuttle Hire Task Reference')
    shuttle_hire_from                   = fields.Char(string='Hire From')
    shuttle_hire_to                     = fields.Char(string='Hire To')
    shuttle_hire_est_km                 = fields.Float(string='Estimated Km.')
    shuttle_hire_group                  = fields.Selection([('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D')],string="Fleet Hire Group?")
    shuttle_hire_departure_date         = fields.Datetime(string='Departure Date')
    shuttle_hire_return_date            = fields.Datetime(string='Return Date')

class travelFlight(models.Model):
    
    _name = 'travel.flight'

    name                           = fields.Char(string="Travel Flight")
    travel_emp                     = fields.Many2many('hr.employee',relation='travel_flight_request',column1='name',column2='user_id',string='Travel Employee',store=True,copy=True)
    flight_task_id                 = fields.Many2one('scm.travel.management',string='Travel Flight Task Reference')
    flight_from                    = fields.Char(string='Fly From')
    flight_to                      = fields.Char(string='Fly To')
    flight_departure_date          = fields.Datetime(string='Departure Date')
    flight_return_date             = fields.Datetime(string='Return Date')


class intlTravel(models.Model):
    
    _name = 'intl.travel'
    
    name                            = fields.Char(string="International Travel")
    travel_emp                      = fields.Many2many('hr.employee',relation='international_travel_request',column1='name',column2='user_id',string='Travel Employee',store=True,copy=True)
    intl_travel_task_id             = fields.Many2one('scm.travel.management',string='International Travel Task Reference')
    perdium_int_travel_depart_date  = fields.Datetime(string='Int. Departure Date')
    perdium_int_travel_return_date  = fields.Datetime(string='Int. Return Date')
    perdium_int_travel_num_nights   = fields.Float(string='Number of Nights')
    perdium_int_travel_amount       = fields.Float(string='Amount')
    

class travelAccommodation(models.Model):
    
    _name = 'travel.accommodation'
    
    name                                    = fields.Char(string="Travel Accommodation")
    travel_emp                              = fields.Many2many('hr.employee',relation='travel_accommodation_request',column1='name',column2='user_id',string='Travel Employee',store=True,copy=True)
    accommodation_task_id                   = fields.Many2one('scm.travel.management',string='Travel Accommodation Task Reference')
    accommodation_name                      = fields.Char(string='Accomodation Name')
    accommodation_type                      = fields.Selection([('Bed and Breakfast', 'Bed and Breakfast'),
                                                                ('Hotel', 'Hotel'),
                                                                ('Motel', 'Motel')],string="Accomodation Type")
    accommodation_meals_incl                = fields.Selection([('Breakfast', 'Breakfast'),
                                                                ('Lunch', 'Lunch'),
                                                                ('Dinner', 'Dinner')],string="Accomodation Meals")
    accommodation_check_in_date             = fields.Datetime(string='Check-in Date')
    accommodationtravel_accom_checkout_date = fields.Datetime(string='Check-out Date')
    accommodation_shuttle_required          = fields.Selection([('No', 'No'),('Yes', 'Yes')],string="Shuttle Required")
    travel_emergency                        = fields.Selection([('Normal', 'Normal'),
                                                                ('Urgent', 'Urgent')],string="Travel Urgency", default='Normal')