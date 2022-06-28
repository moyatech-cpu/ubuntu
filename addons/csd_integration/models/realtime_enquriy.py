# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit
import logging
_logger = logging.getLogger(__name__)
import requests

class RealTime(models.Model):
    _name = 'realtime.enquiry'
    _description = "Realtime CSD Search"
    
    name = fields.Char("Name", required=True, translate=True)
    
    def run_realtime(self):
        xml = """<AuthenticationRequest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <AcceptTermsandConditions>true</AcceptTermsandConditions>
    <Email>Zinhle.Bhengu@nyda.gov.za</Email>
    <Password>Nyda@2021</Password>
</AuthenticationRequest>"""
        response = requests.post(
                    "https://api.csd.gov.za/api/Authenticate",
                    headers={"Content-Type": "application/xml"},
        data=xml)
        _logger.info(str(response.text))
        token = response.text[10:46]
        _logger.info(token)
        
        xml = """<GetSupplierDetailRequest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <SupplierNumber>MAAA1116120</SupplierNumber>
</GetSupplierDetailRequest>"""
        response = requests.post(
                    "https://api.csd.gov.za/api/Supplier/GetSupplierDetailSI",
                    headers={"Authorization":"Bearer "+token,
                            "Content-Type": "text/xml",
                             "Accept":"application/xml",
                             "csdversion":"2"
                             },
        data=xml)
        _logger.info(str(response.text))