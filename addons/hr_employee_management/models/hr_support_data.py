# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError

'''
class Province(models.Model):
    """This class is to add province table"""

    _name = 'province'
    _description = 'Province'

    area        = fields.Char(string='Area', help='Area')
    code        = fields.Char(string='Code', help='Code')
    district    = fields.Char(string='District', help='District')
    name        = fields.Char(string='Name', help='Name')
    population  = fields.Char(string='Population', help='Population')
    population_density = fields.Char(string='Population Density', help="Population Density")
    province    = fields.Char(string='province', help="province")
    seat        = fields.Char(string='Seat', help="Seat")
    sno         = fields.Char(string='SNO', help="SNO")
    type        = fields.Char(string='Type', help="Type")
    
class District(models.Model):
    """This class is to add district table"""

    _name = 'district'
    _description = 'District'

    area        = fields.Char(string='Area', help='Area')
    code        = fields.Char(string='Code', help='Code')
    district    = fields.Char(string='District', help='District')
    name        = fields.Char(string='Name', help='Name')
    population  = fields.Char(string='Population', help='Population')
    population_density = fields.Char(string='Population Density', help="Population Density")
    province    = fields.Char(string='province', help="province")
    seat        = fields.Char(string='Seat', help="Seat")
    sno         = fields.Char(string='SNO', help="SNO")
    type        = fields.Char(string='Type', help="Type")
'''
        
class Municipalities(models.Model):
    """This class is to add municipalities table"""

    _name = 'municipalities'
    _description = 'Municipalities'

    area        = fields.Char(string='Area', help='Area')
    code        = fields.Char(string='Code', help='Code')
    district    = fields.Char(string='District', help='District')
    name        = fields.Char(string='Name', help='Name')
    population  = fields.Char(string='Population', help='Population')
    population_density = fields.Char(string='Population Density', help="Population Density")
    province    = fields.Char(string='Province', help="province")
    seat        = fields.Char(string='Seat', help="Seat")
    sno         = fields.Char(string='SNO', help="SNO")
    type        = fields.Char(string='Type', help="Type")

class Branch(models.Model):
    """This class is to add branch table"""

    _name = 'branch'
    _description = 'Branch'

    name                = fields.Char(string='Name', help='Name')
    communication_agent = fields.Many2one('res.users', string='Communication Agent', help='Communication Agent')
    municipality        = fields.Many2one('municipalities', string='Municipality', help='Municipality')
