# -*- coding: utf-8 -*-

from odoo import models, fields, api
#from pygments.lexer import _inherit

class BBBEECertificate(models.Model):
    _name = 'bbbee.certificate'
    _description = "BBBEE Certificate"
    _rec_name = "CertificateNumber"
    
    IsActive = fields.Char("IsActive")
    LastVerficationDate = fields.Char("LastVerificationDate")
    EditDate = fields.Char("EditDate")
    
    UniqueRegistrationReferenceNumber = fields.Char("Supplier Serial#")
    #code types
    CertificateTypeCode = fields.Char("CertificateTypeCode")
    VerificationRegulatorCode = fields.Char("VerificationRegulatorCode")
    StatusLevelOfContributorCode = fields.Char("StatusLevelOfContributorCode")
    CertificateSignedByvalue = fields.Char("CertificateSignedByvalue")
    SectorCharterCode = fields.Char("SectorCharterCodee")
    SubSectorCharterCode = fields.Char("SubSectorCharterCode")
    IRBARegisteredAuditorCode = fields.Char('IRBARegisteredAuditorCode')
    SANASAccreditedAgencyCode = fields.Char('SANASAccreditedAgencyCode')
    #real types
    CertificateNumber = fields.Char("CertificateNumber")
    CertificateIssueDate = fields.Char("CertificateIssueDate")
    CertificateExpiryDate = fields.Char("CertificateExpiryDate")
    BlackOwnership = fields.Char("BlackOwnership")
    BlackWomanOwnership = fields.Char("BlackWomanOwnership")
    IsAcceptUnderstandAffidavid = fields.Char("IsAcceptUnderstandAffidavid")
    CertificateSignedBy = fields.Char("CertificateSignedBy")
    CertificateSignDate = fields.Char("CertificateSignedDate") 
    ValueAddingSupplier = fields.Char(string="ValueAddingSupplier")
    EmpoweringSupplier = fields.Char(string="EmpoweringSupplier")
    OwnershipScore = fields.Char('OwnershipScore')
    ManagementControlScore = fields.Char('ManagementControlScore')
    EmploymentEquityScore = fields.Char('EmploymentEnquiryScore')
    SkillsDevelopmentScore = fields.Char('SkillsDevelopmentScore')
    PreferentialProcurementScore = fields.Char('PreferentialProcurementScore')
    EnterpriseDevelopmentScore = fields.Char('EnterpriseDevelopmentScore')
    SocioEconomicDevelopmentScore = fields.Char('SocioEconomicDevelopmentScore')
    EnterpriseSupplierDevelopmentScore = fields.Char('EnterpriseSupplierDevelopmentScore')
    LandOwnershipScore = fields.Char('LandOwnershipScore')
    EmpowermentFinancingScore = fields.Char('EmpowermentFinancingScore')
    AccessFinancialServicesScore = fields.Char('AccessFinancialServicesScore')
    EconomicDevelopmentScore = fields.Char('EconomicDevelopmentScore')
    ForeignOwnershipScore = fields.Char('ForeignOwnershipScore')
    StatusTypeCode = fields.Char('StatusTypeCode')
    LastVerificationDate = fields.Char('LastVerificationDate')
    EditDate = fields.Char('EditDate')
    
    user_id = fields.Many2one('res.users', string='User')
    supplier_identification = fields.Many2one("supplier.master",compute='_get_master',store=False, string="Supplier")
    
    @api.depends('user_id')
    def _get_master(self):
        supplier_number = self.UniqueRegistrationReferenceNumber
        
        s = self.env['supplier.master'].sudo().search([('UniqueRegistrationReferenceNumber','=',supplier_number)])
        for a in self:
            for x in s:
                a.supplier_identification = x
    