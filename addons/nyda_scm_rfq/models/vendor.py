# coding=utf-8
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, exceptions, fields, models, _
import logging

'''
 Need to remove sql_constraints on these models to accomodate ome of the data anomalies 
'''

class VendorExtend(models.Model):
    """ Model to inherit/extend the res.partner model """
    _inherit    = 'res.partner'
    
    vendor_id       = fields.Char('Vendor ID')
    csd_number      = fields.Char('CSD Number')
    company_no      = fields.Char('Company No')
    vendor_contact  = fields.Char('Vendor Contact')
    tax_number      = fields.Char('Tax No')
    fax             = fields.Char('Fax')
    service1        = fields.Char("Service 1")
    service2        = fields.Char("Service 2")
    service3        = fields.Char("Service 3")
