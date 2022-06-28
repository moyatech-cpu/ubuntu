# coding=utf-8
import re
import datetime

from odoo import api, fields, models, _


class PartnerEnquiryInherit(models.Model):
    _inherit = 'partner.enquiry'

    # partner_service_idss = fields.One2many('partner.service', 'partner_enquiry_id', string='Partner Service')
    partner_service_ids = fields.Many2many('business.development.assistance', string= 'Partner Servicers')

# class PartnerService(models.Model):
#     _name = 'partner.service'
#     # rec_name = 'service_name'
#
#     voucher_application_id = fields.Many2one('', string='Voucher Application')
#     partner_enquiry_id = fields.Many2one('partner.enquiry', string='Partner Enquiry')
#
#     service_name = fields.Many2one('business.development.assistance', string='Service Provided')
#     service_item_seq = fields.Char(string="Service Item ID", related='service_name.service_item_seq')
#     voucher_value = fields.Integer(string="Voucher Value", related='service_name.voucher_value')
#     min_dur = fields.Integer(string="Minimum Duration(Hours)", related='service_name.min_dur')