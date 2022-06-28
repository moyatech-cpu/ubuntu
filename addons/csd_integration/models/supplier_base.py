# -*- coding: utf-8 -*-

from odoo import models, fields, api
#sfrom pygments.lexer import _inherit
import logging
_logger = logging.getLogger(__name__)
import requests
import xml.etree.ElementTree as Xet
#import pandas as pd

class Supplier(models.Model):
    _name = 'supplier.master'
    _description = "supplier base model"
    #_inherit = 'res.partner'
    _rec_name = "UniqueRegistrationReferenceNumber"
    
    UniqueRegistrationReferenceNumber = fields.Char("UniqueRegistrationReferenceNumber")#0
    IsActive = fields.Char("IsActive")#2
    SupplierInactiveReason = fields.Text("SupplierInactiveReasonn")#3
    SupplierInactiveDate = fields.Char("SupplierInactiveDate")#4
    #Codes to be converted to real type values
    SupplierStateCode = fields.Char("SupplierStateCode")#5
    IsAssociated = fields.Char("IsAssociated")#6
    SupplierTypeCode =  fields.Char("SupplierTypeCode")#7
    SupplierSubTypeCode = fields.Char("SupplierSubTypeCode")#8
    GovernmentTypeCode = fields.Char("GovernmentTypeCode")#9
    CountryOfOriginCode = fields.Char("CountryOfOriginCode")#10
    IDTypeCode = fields.Char("IDTypeCode")#13
    BusinessStatusCode = fields.Char("BusinessStatusCode")#27
    TotalAnnualTurnoverCode = fields.Char("TotalAnnualTurnoverCode")#31
    #Real type values
    LegalName = fields.Char("LegalName")#11
    TradingName = fields.Char("TraidingName")#12
    SAIDNumber = fields.Char("SAIDNumber")#14
    ForeignIDNumber = fields.Char("ForeignIDNumber")#15
    ForeignPassportNumber = fields.Char("ForeignPassportNumber")#16
    WorkPermitNumber = fields.Char("WorkPermitNumber")#17
    SACompanyNumber = fields.Char("SACompanyNumber")#18
    RegistrationDate = fields.Char("RegistrationDate")#19
    ForeignCompanyRegistrationNumber = fields.Char("ForeignCompanyRegistrationNumber")#20
    SATrustRegistrationNumber = fields.Char("SATrustRegistrationNumber")#21
    ForeignTrustRegistrationNumber = fields.Char("ForeignTrustRegistrationNumber")#22
    NonProfitOrganisationNumber = fields.Char("NonProfitOrganisationNumber")#23
    OoSIDNumber = fields.Char("OoSIDNumber")#24
    DateOperationsStarted = fields.Char("DateOperationsStarted")#25
    HaveBankAccount = fields.Char("HaveBankAccount")#26
    BusinessStatusLastVerificationDate = fields.Char("BusinessStatusLastVerificationDate")#28
    IsListedOnStockExchange = fields.Char(string="IsListedOnStockExchange")#29
    #isListedOnStockLabel = fields.Selection([('yes', 'Yes'), ('no', 'No')],default='active',string="Is the Supplier listed on stock Exchange",compute='_compute_stock_exchange',store=True)
    IsOwnedByNaturalSAPerson = fields.Boolean("IsOwnedByNaturalSAPerson")#30
    #isListedOnStockLabel = fields.Selection([('yes', 'Yes'), ('no', 'No')],default='yes',string="Is the Supplier listed on stock Exchange",compute='_computeownedByNaturalSAPerson',store=True)
    FinancialYearStartDate = fields.Text("FinancialYearStartDate")#32
    
    #relational fields
    user_id = fields.Many2one('res.users', string='User')
    tax_certificate = fields.Many2one("tax.certificate",compute='_get_tax_certificate',store=False, string="Tax Certificate")
    bbbee_certificate = fields.Many2one("bbbee.certificate",compute='_get_tax_certificate',store=False, string="BBBEE Certificate")
    contacts = fields.One2many("contact.detail","ContactID",compute='_get_tax_certificate',store=False, string="Contacts")
    addresses = fields.One2many("address.details","AddressID",compute='_get_tax_certificate',store=False, string="Addresses")
    directors = fields.One2many("supplier.director","DirectorID",compute='_get_tax_certificate',store=False, string="Directors")
    #owners = fields.One2many("sup.owner",,string="Owner") # can be two either natural or non natural owner
    bank_accounts = fields.One2many('bank.account',"BankAccountID",compute='_get_tax_certificate',store=False,string="Banking Accounts")
    industry = fields.One2many('industry.classification',"UniqueRegistrationReferenceNumber",compute='_get_tax_certificate',store=False, string="Industry")
    accreditations = fields.One2many('accreditation.model',"AccreditationID",compute='_get_tax_certificate',store=False,string='Accreditations')
    association = fields.One2many('supplier.association',"AssociationID",compute='_get_tax_certificate',store=False,string="Association")
    commodoties = fields.One2many('commodity.group',"CommodityGroupID",compute='_get_tax_certificate',store=False,string="Commodoties")
    
    @api.multi
    def search_csd(self, mi_number,link):
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
                <SupplierNumber>{ma_id}</SupplierNumber>
                </GetSupplierDetailRequest>""".format(ma_id=str(mi_number))
                
        response = requests.post(
                    "https://api.csd.gov.za/api/Supplier/"+link,
                    headers={"Authorization":"Bearer "+token,
                            "Content-Type": "text/xml",
                             "Accept":"application/xml",
                             "csdversion":"2"
                             },
        data=xml)
        _logger.info(str(response.text))
        return str(response.text)
        
    
    @api.depends('user_id')
    def _get_tax_certificate(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        tax_cert = self.env['tax.certificate'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        bbbee_certificate = self.env['bbbee.certificate'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        contacts = self.env['contact.detail'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        addresses = self.env['address.details'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        directors = self.env['supplier.director'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        bank_accounts = self.env['bank.account'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        industry = self.env['industry.classification'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        accreditations = self.env['accreditation.model'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        association = self.env['supplier.association'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        commodoties = self.env['commodity.group'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        
        
        for a in self:
            for tax in tax_cert:
                a.tax_certificate = tax
            for bbbee in bbbee_certificate:
                a.bbbee_certificate = bbbee
            a.contacts = contacts
            a.addresses = addresses
            a.directors = directors
            a.bank_accounts = bank_accounts
            a.industry = industry
            a.accreditations = accreditations
            a.association = association
            a.commodoties = commodoties
            
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Supplier, self).fields_view_get(view_id=view_id,view_type=view_type,toolbar=toolbar,submenu=submenu)
        
        supplier_number = self.UniqueRegistrationReferenceNumber
        try:
            self.tax_certificate = self.env['tax.certificate'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        try:
            self.bbbee_certificate = self.env['bbbee.certificate'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        try:
            self.contacts = self.env['contact.detail'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        try:
            self.addresses = self.env['address.details'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        try:
            self.directors = self.env['supplier.director'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        try:
            self.bank_accounts = self.env['bank.account'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        try:
            self.industry = self.env['industry.classification'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        try:
            self.accreditations = self.env['accreditation.model'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        try:
            self.association = self.env['supplier.association'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        
        try:
            self.commodoties = self.env['commodity.group'].search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        except:
            pass
        
        return res

    @api.multi
    def update_records(self):
        #start update procedure
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailSI")
        root = Xet.fromstring(csd_result)
                    
        for item in root.iter('SupplierIdentification'):
            self.UniqueRegistrationReferenceNumber =  str(item.find('SupplierNumber').text)
            self.IsActive =  str(item.find('IsActive').text)
            self.SupplierInactiveReason =  str(item.find('SupplierInactiveReason').text)
            self.SupplierInactiveDate =  str(item.find('SupplierInactiveDate').text)
            self.SupplierStateCode =  str(item.find('SupplierStateCode').text)
            self.IsAssociated =  str(item.find('IsAssociated').text)
            self.SupplierTypeCode =  str(item.find('SupplierTypeCode').text)
            self.SupplierSubTypeCode =  str(item.find('SupplierSubTypeCode').text)
            self.GovernmentTypeCode =  str(item.find('GovernmentTypeCode').text)
            self.CountryOfOriginCode =  str(item.find('CountryOfOriginCode').text)
            self.IDTypeCode =  str(item.find('IDTypeCode').text)
            self.BusinessStatusCode =  str(item.find('BusinessStatusCode').text)
            self.TotalAnnualTurnoverCode =  str(item.find('TotalAnnualTurnoverCode').text)
            self.LegalName =  str(item.find('LegalName').text)
            self.TradingName =  str(item.find('TradingName').text)
            self.SAIDNumber =  str(item.find('SAIDNumber').text)
            self.ForeignIDNumber =  str(item.find('ForeignIDNumber').text)
            self.ForeignPassportNumber =  str(item.find('ForeignPassportNumber').text)
            self.WorkPermitNumber =  str(item.find('WorkPermitNumber').text)
            self.SACompanyNumber =  str(item.find('SACompanyNumber').text)
            self.RegistrationDate =  str(item.find('RegistrationDate').text)
            self.ForeignCompanyRegistrationNumber =  str(item.find('ForeignCompanyRegistrationNumber').text)
            self.SATrustRegistrationNumber =  str(item.find('SATrustRegistrationNumber').text)
            self.ForeignTrustRegistrationNumber =  str(item.find('ForeignTrustRegistrationNumber').text)
            self.NonProfitOrganisationNumber =  str(item.find('NonProfitOrganisationNumber').text)
            self.OoSIDNumber =  str(item.find('OoSIDNumber').text)
            self.DateOperationsStarted =  str(item.find('DateOperationsStarted').text)
            self.HaveBankAccount =  str(item.find('HaveBankAccount').text)
            self.BusinessStatusLastVerificationDate =  str(item.find('BusinessStatusLastVerificationDate').text)
            self.IsListedOnStockExchange =  str(item.find('IsListedOnStockExchange').text)
            self.IsOwnedByNaturalSAPerson =  str(item.find('IsOwnedByNaturalSAPerson').text)
            self.FinancialYearStartDate =  str(item.find('FinancialYearStartDate').text)
        
        record = self.env['tax.certificate'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsTax")
        root = Xet.fromstring(csd_result)
        
        for item in root.iter('Tax'):
            self.env['tax.certificate'].create({
                        'UniqueRegistrationReferenceNumber': self.UniqueRegistrationReferenceNumber,
                        'IsRegistered' :  str(item.find('IsRegistered').text),
                        'IncomeTaxNumber' :  str(item.find('IncomeTaxNumber').text),
                        'IsVATVendor' :  str(item.find('IsVATVendor').text),
                        'PAYENumber' :  str(item.find('PAYENumber').text),
                        'VATNumber' :  str(item.find('VATNumber').text),
                        'IsValidCertificate' :  str(item.find('IsValidCertificate').text),
                        'ValidationResponse' :  str(item.find('ValidationResponse').text),
                        'LastVerificationDate' :  str(item.find('LastVerificationDate').text),
                        'EditDate' :  str(item.find('EditDate').text)
                    })
        
        #Delete old accreditations
        record = self.env['accreditation.model'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsAccreditation")
        root = Xet.fromstring(csd_result)
        
        for item in root.iter('Accreditation'):
            self.env['accreditation.model'].create({
                        'UniqueRegistrationReferenceNumber': self.UniqueRegistrationReferenceNumber,
                        'AccreditationID' :str(item.find('AccreditationID').text),
                        'AccreditationNumber' : str(item.find('AccreditationNumber').text),
                        'Description' :  str(item.find('Description').text),
                        'RegistrationDate' :  str(item.find('RegistrationDate').text),
                        'ExpiryDate' :  str(item.find('ExpiryDate').text),
                        'IsVerified' :  str(item.find('IsVerified').text),
                        'LastVerificationDate' :  str(item.find('LastVerificationDate').text),
                        'StatusCode' :  str(item.find('StatusCode').text),
                        'CreatedDate' :  str(item.find('CreatedDate').text),
                        'EditDate' :  str(item.find('EditDate').text),
                    })

        record = self.env['address.details'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsAddress")
        root = Xet.fromstring(csd_result)
        
        for item in root.iter('Address'):
            self.env['address.details'].create({
                        'UniqueRegistrationReferenceNumber': self.UniqueRegistrationReferenceNumber,
                        'AddressID': str(item.find('AddressID').text),
                        'AddressTypeCode':str(item.find('AddressTypeCode').text),
                        'AddressLine1':str(item.find('AddressLine1').text),
                        'AddressLine2':str(item.find('AddressLine2').text),
                        'CountryCode':str(item.find('CountryCode').text),
                        'ProvinceCode':str(item.find('ProvinceCode').text),
                        'DistrictCode':str(item.find('DistrictCode').text),
                        'MunicipalityCode':str(item.find('MunicipalityCode').text),
                        'CityCode':str(item.find('CityCode').text),
                        'SuburbCode':str(item.find('SuburbCode').text),
                        'WardCode':str(item.find('WardCode').text),
                        'PostalCode':str(item.find('PostalCode').text),
                        'IsPostalAddress':str(item.find('IsPostalAddress').text),
                        'IsDeliveryAddress':str(item.find('IsDeliveryAddress').text),
                        'IsPhysicalAddress':str(item.find('IsPhysicalAddress').text),
                        'IsPaymentAddress':str(item.find('IsPaymentAddress').text),
                    })

        record = self.env['bbbee.certificate'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsBBBEE")
        root = Xet.fromstring(csd_result)
        
        for item in root.iter('BBBEE'):
            self.env['bbbee.certificate'].create({
                'CertificateTypeCode' : str(item.find('CertificateTypeCode').text),
                'VerificationRegulatorCode' : str(item.find('VerificationRegulatorCode').text),
                'StatusLevelOfContributorCode' : str(item.find('StatusLevelOfContributorCode').text),
                'SectorCharterCode' : str(item.find('SectorCharterCode').text),
                'SubSectorCharterCode' : str(item.find('SubSectorCharterCode').text),
                'IRBARegisteredAuditorCode' : str(item.find('IRBARegisteredAuditorCode').text),
                'SANASAccreditedAgencyCode' : str(item.find('SANASAccreditedAgencyCode').text),
                'CertificateNumber' : str(item.find('CertificateNumber').text),
                'CertificateIssueDate' : str(item.find('CertificateIssueDate').text),
                'CertificateExpiryDate' : str(item.find('CertificateExpiryDate').text),
                'BlackOwnership' : str(item.find('BlackOwnership').text),
                'BlackWomanOwnership' : str(item.find('BlackWomanOwnership').text),
                'IsAcceptUnderstandAffidavid' : str(item.find('IsAcceptUnderstandAffidavid').text),
                'CertificateSignedBy' : str(item.find('CertificateSignedBy').text),
                'CertificateSignDate' : str(item.find('CertificateSignDate').text),
                'ValueAddingSupplier' : str(item.find('ValueAddingSupplier').text),
                'EmpoweringSupplier' : str(item.find('EmpoweringSupplier').text),
                'OwnershipScore' : str(item.find('OwnershipScore').text),
                'ManagementControlScore' : str(item.find('ManagementControlScore').text),
                'EmploymentEquityScore' : str(item.find('EmploymentEquityScore').text),
                'SkillsDevelopmentScore' : str(item.find('SkillsDevelopmentScore').text),
                'PreferentialProcurementScore' : str(item.find('PreferentialProcurementScore').text),
                'EnterpriseDevelopmentScore' : str(item.find('EnterpriseDevelopmentScore').text),
                'SocioEconomicDevelopmentScore' : str(item.find('SocioEconomicDevelopmentScore').text),
                'EnterpriseSupplierDevelopmentScore' : str(item.find('EnterpriseSupplierDevelopmentScore').text),
                'LandOwnershipScore' : str(item.find('LandOwnershipScore').text),
                'EmpowermentFinancingScore' : str(item.find('EmpowermentFinancingScore').text),
                'AccessFinancialServicesScore' : str(item.find('AccessFinancialServicesScore').text),
                'EconomicDevelopmentScore' : str(item.find('EconomicDevelopmentScore').text),
                'ForeignOwnershipScore' : str(item.find('ForeignOwnershipScore').text),
                'StatusTypeCode' : str(item.find('StatusTypeCode').text),
                'LastVerificationDate' : str(item.find('LastVerificationDate').text),
                        
            })

        
        record = self.env['supplier.association'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsAssociation")
        root = Xet.fromstring(csd_result)

        for item in root.iter('Association'):
            self.env['contact.detail'].create({
                        'UniqueRegistrationReferenceNumber': self.UniqueRegistrationReferenceNumber,
                        'IsActive': str(item.find('IsActive').text),
                        'LastVerficationDate':str(item.find('LastVerficationDate').text),
                        'EditDate':str(item.find('EditDate').text),
                        'CreatedDate':str(item.find('CreatedDate').text),
                        'AssociationID':str(item.find('AssociationID').text),
                        'SupplierNumberRequestor':str(item.find('SupplierNumberRequestor').text),
                        'SupplierNumberRequested':str(item.find('SupplierNumberRequested').text),
                        'AssociationTypeCode':str(item.find('AssociationTypeCode').text),
                        'AssociationStatusTypeCode':str(item.find('AssociationStatusTypeCode').text),
                    })
        
        record = self.env['accreditation.model'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsAccreditation")
        root = Xet.fromstring(csd_result)
        
        for item in root.iter('Accreditation'):
            self.env['accreditation.model'].create({
                        'UniqueRegistrationReferenceNumber': self.UniqueRegistrationReferenceNumber,
                        'AccreditationID': str(item.find('AccreditationID').text),
                        'AccreditationNumber':str(item.find('AccreditationNumber').text),
                        'Description':str(item.find('Description').text),
                        'RegistrationDate':str(item.find('RegistrationDate').text),
                        'ExpiryDate':str(item.find('ExpiryDate').text),
                        'IsVerified':str(item.find('IsVerified').text),
                        'LastVerificationDate':str(item.find('LastVerificationDate').text),
                        'StatusCode':str(item.find('StatusCode').text),
                        'CreatedDate':str(item.find('CreatedDate').text),
                        'EditDate':str(item.find('EditDate').text),
                    })
        
        record = self.env['commodity.group'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsCommodities")
        root = Xet.fromstring(csd_result)

        for item in root.iter('CommodityGroup'):
            self.env['commodity.group'].create({
                        'UniqueRegistrationReferenceNumber': self.UniqueRegistrationReferenceNumber,
                        'CommodityGroupID': str(item.find('CommodityGroupID').text),
                        'Name':str(item.find('Name').text),
                        'Description':str(item.find('Description').text),
                        'NationWide':str(item.find('NationWide').text),
                        'Field1':str(item.find('Field1').text),
                        'CreatedDate':str(item.find('CreatedDate').text),
                        'EditDate':str(item.find('EditDate').text),
                    })
        
        record = self.env['supplier.director'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsDirectors")
        root = Xet.fromstring(csd_result)
        
        for item in root.iter('Director'):
            self.env['supplier.director'].create({
                        'UniqueRegistrationReferenceNumber': self.UniqueRegistrationReferenceNumber,
                        'IsActive': str(item.find('IsActive').text),
                        #'LastVerficationDate':str(item.find('LastVerificationDate').text),
                        'EditDate':str(item.find('EditDate').text),
                        #'IsPreferred':str(item.find('IsPreferred').text),
                        'CreatedDate':str(item.find('CreatedDate').text),
                        'DirectorID':str(item.find('DirectorID').text),
                        'Name':str(item.find('Name').text),
                        'Surname':str(item.find('Surname').text),
                        'AppointmentDate':str(item.find('AppointmentDate').text),
                        'CountryTypeCode':str(item.find('CountryTypeCode').text),
                        'IDTypeCode':str(item.find('IDTypeCode').text),
                        'DirectorStatusTypeCode':str(item.find('DirectorStatusTypeCode').text),
                        'SAIDNumber':str(item.find('SAIDNumber').text),
                        'ForeignIDNumber':str(item.find('ForeignIDNumber').text),
                        'ForeignPassportNumber':str(item.find('ForeignPassportNumber').text),
                        'WorkPermitNumber':str(item.find('WorkPermitNumber').text),
                        'LastVerificationDate':str(item.find('LastVerificationDate').text),
                        #'DirectorTypeCode':str(item.find('DirectorTypeCode').text),
                        'IsOwner':str(item.find('IsOwner').text),
                        'CellphoneNumber':str(item.find('CellphoneNumber').text),
                        'EmailAddress':str(item.find('EmailAddress').text),
                        'GenderCode':str(item.find('GenderCode').text),
                        'EthnicGroupCode':str(item.find('EthnicGroupCode').text),
                        'OwnershipPercentage':str(item.find('OwnershipPercentage').text),
                        'OwnershipDemographics':str(item.find('OwnershipDemographics').text),
                        #'SupplierFlagType':str(item.find('SupplierFlagType').text),
                        #'SupplierFlagDescription':str(item.find('SupplierFlagDescription').text),
                        #'SupplierFlagValue':str(item.find('SupplierFlagValue').text),
                        #'SupplierFlagLastVerificationDate':str(item.find('SupplierFlagLastVerificationDate').text),
                        
                    })
            
        record = self.env['bank.account'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsBanking")
        root = Xet.fromstring(csd_result)
        
        for item in root.iter('BankAccount'):
            self.env['bank.account'].create({
                        'UniqueRegistrationReferenceNumber': self.UniqueRegistrationReferenceNumber,
                        'IsActive': str(item.find('IsActive').text),
                        'EditDate':str(item.find('EditDate').text),
                        'IsPreferred':str(item.find('IsPreferred').text),
                        'CreatedDate':str(item.find('CreatedDate').text),
                        'BankAccountID':str(item.find('BankAccountID').text),
                        'IsForeignBankAccount':str(item.find('IsForeignBankAccount').text),
                        'AccountHolder':str(item.find('AccountHolder').text),
                        'BankAccountTypeCode':str(item.find('BankAccountTypeCode').text),
                        'BankName':str(item.find('BankName').text),
                        'BankCode':str(item.find('BankCode').text),
                        'BranchName':str(item.find('BranchName').text),
                        'BranchNumber':str(item.find('BranchNumber').text),
                        'AccountNumber':str(item.find('AccountNumber').text),
                        'BankAccountStatusCode':str(item.find('BankAccountStatusCode').text),
                        'BankAccountVerificationDate':str(item.find('BankAccountVerificationDate').text),
                        'AddressLine1':str(item.find('AddressLine1').text),
                        'AddressLine2':str(item.find('AddressLine2').text),
                        'CountryCode':str(item.find('CountryCode').text),
                        'ZipCode':str(item.find('ZipCode').text),
                        'FirstName':str(item.find('FirstName').text),
                        'Initials':str(item.find('Initials').text),
                        'LastName':str(item.find('LastName').text),
                        'Title':str(item.find('Title').text),
                        'IsIdentifierLinkedAtBank':str(item.find('IsIdentifierLinkedAtBank').text),
                        'IsSharedFundingAccount':str(item.find('IsSharedFundingAccount').text),
                        'FundingContacts':str(item.find('FundingContacts').text),
                        
                    })

                
        record = self.env['contact.detail'].sudo().search([('UniqueRegistrationReferenceNumber','=',self.UniqueRegistrationReferenceNumber)]).unlink()
        csd_result = self.search_csd(self.UniqueRegistrationReferenceNumber,"GetSupplierDetailsContact")
        root = Xet.fromstring(csd_result)
        
        for item in root.iter('Contact'):
            self.env['contact.detail'].create({
                        'UniqueRegistrationReferenceNumber': self.UniqueRegistrationReferenceNumber,
                        'IsActive': str(item.find('IsActive').text),
                        'EditDate':str(item.find('EditDate').text),
                        'IsPreferred':str(item.find('IsPreferred').text),
                        'CreatedDate':str(item.find('CreatedDate').text),
                        'ContactID':str(item.find('ContactID').text),
                        #'ContactTypeCode':str(item.find('ContactTypeCode').text),
                        'Name':str(item.find('Name').text),
                        'Surname':str(item.find('Surname').text),
                        'IdentificationTypeCode':str(item.find('IdentificationTypeCode').text),
                        'SAIDNumber':str(item.find('SAIDNumber').text),
                        'ForeignIDNumber':str(item.find('ForeignIDNumber').text),
                        'ForeignPassportNumber':str(item.find('ForeignPassportNumber').text),
                        'WorkPermitNumber':str(item.find('WorkPermitNumber').text),
                        'PreferCellphone':str(item.find('PreferCellphone').text),
                        'PreferEmail':str(item.find('PreferEmail').text),
                        'PreferFax':str(item.find('PreferFax').text),
                        'PreferPostal':str(item.find('PreferPostal').text),
                        'PreferSMS':str(item.find('PreferSMS').text),
                        'PreferTelephone':str(item.find('PreferTelephone').text),
                        'EmailAddress':str(item.find('EmailAddress').text),
                        'CellphoneNumber':str(item.find('CellphoneNumber').text),
                        'FaxNumber':str(item.find('FaxNumber').text),
                        'TelephoneNumber':str(item.find('TelephoneNumber').text),
                        'TollFreeNumber':str(item.find('TollFreeNumber').text),
                        'WebsiteAddress':str(item.find('WebsiteAddress').text),
                        #'FundingPartnerLegalName':str(item.find('FundingPartnerLegalName').text),
                        
                    })                
    
    
    
    
    
    
    
    
    