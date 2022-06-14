# coding=utf-8
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

'''    
Greenfield Database:

branch_admin_id = fields.Many2one('res.users', string="Branch Admin")
is_enabled = fields.Boolean(string="Enabled")
sequence = fields.Integer('Branch ID', default=0)
name = fields.Char('Branch Name')
name = fields.DateTime('Branch Name')
    
'''


class sup_supplierheader(models.Model):
    """ sup_supplierheader """
    _name = 'sup_supplierheader'
    _description = 'sup_supplierheader'

    UserRequestedApproval    = fields.Char('UserRequestedApproval')
    VatRegisteredYN = fields.Char('VatRegisteredYN')
    AlternateID = fields.Char('AlternateID')
    VATRegistrationNr = fields.Char('VATRegistrationNr')
    RegistrationNr = fields.Char('RegistrationNr')
    B_BBEE_ID = fields.Char('B_BBEE_ID')
    GPVATRate = fields.Char('GPVATRate')
    BankName = fields.Char('BankName')
    BankBranch = fields.Char('BankBranch')
    BranchCode = fields.Char('BranchCode')
    BankAccountNumber = fields.Char('BankAccountNumber')
    BankAccountType = fields.Char('BankAccountType')
    currencyID = fields.Char('currencyID')
    OTP = fields.Char('OTP')
    AccSysInterfaceStatus = fields.Char('AccSysInterfaceStatus')
    Status_AccountingSystemID = fields.Char('Status_AccountingSystemID')
    PortalUpdatePending = fields.Char('PortalUpdatePending')
    PaymentMethodID = fields.Char('PaymentMethodID')
    VendorCode = fields.Char('VendorCode')
    Deleted = fields.Char('Deleted')
    ClassificationID = fields.Char('ClassificationID')
    LastCommodityChangeVP = fields.Char('LastCommodityChangeVP')
    LastCommodityChangeGF = fields.Char('LastCommodityChangeGF')
    CSDNumber = fields.Char('CSDNumber')
    CSDUniqueNr = fields.Char('CSDUniqueNr')
    LastCSDCheck = fields.Datetime('LastCSDCheck')
    CSDStatus = fields.Char('CSDStatus')
    PaymentTermsID = fields.Char('PaymentTermsID')
    F43 = fields.Char('F43')
 
 
class CSD_DirectorFlag(models.Model):
    """ CSD_DirectorFlag """
    _name = 'CSD_DirectorFlag'
    _description = 'CSD_DirectorFlag'    
    ID = fields.Char('MemberId')
    CSD_SupplierDirectorID = fields.Char('MemberId')
    SupplierID = fields.Char('MemberId')
    SupplierFlagType = fields.Char('MemberId')
    SupplierFlagDescription = fields.Char('MemberId')
    SupplierFlagValue = fields.Char('MemberId')
    SupplierFlagDetails = fields.Char('MemberId')
    SupplierFlagLastVerificationDate = fields.Char('MemberId')
    DirectorFlags_Id = fields.Char('MemberId')

class CSD_Status(models.Model):
    """ CSD_Status """
    _name = 'CSD_Status'
    _description = 'CSD_Status'
    ID = fields.Char('ID')
    StatusType = fields.Char('StatusType')
    StatusCode = fields.Char('StatusCode')
    StatusDescription = fields.Char('StatusDescription')
    ImportInfoGF = fields.Char('ImportInfoGF')

class CSD_StatusCheck_Details(models.Model):
    """ CSD_StatusCheck_Details """
    _name = 'CSD_StatusCheck_Details'
    _description = 'CSD_StatusCheck_Details'
    ID = fields.Char('ID')
    CSD_StatusCheck_HeaderID = fields.Char('CSD_StatusCheck_HeaderID')
    StatusType = fields.Char('StatusType')
    okStatus = fields.Char('okStatus')
    StatusMessage = fields.Char('StatusMessage')

class CSD_StatusCheck_Header(models.Model):
    """ CSD_StatusCheck_Header """
    _name = 'CSD_StatusCheck_Header'
    _description = 'CSD_StatusCheck_Header'
    ID = fields.Char('ID')
    VendorNumber = fields.Char('MemberId')
    UniqueNr = fields.Char('MemberId')
    DateChecked = fields.Char('MemberId')
    TransactionType = fields.Char('MemberId')
    ActionUser = fields.Char('MemberId')
    TransactionAllowed = fields.Char('MemberId')

class CSD_SupplierAccreditation(models.Model):
    """ CSD_SupplierAccreditation """
    _name = 'CSD_SupplierAccreditation'
    _description = 'CSD_SupplierAccreditation'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    AccreditationID = fields.Char('AccreditationID')
    AccreditationBodyParentName = fields.Char('AccreditationBodyParentName')
    AccreditationBodyParentCode = fields.Char('AccreditationBodyParentCode')
    AccreditationBodyName = fields.Char('AccreditationBodyName')
    AccreditationBodyCode = fields.Char('AccreditationBodyCode')
    AccreditationNumber = fields.Char('AccreditationNumber')
    RegistrationDate = fields.Datetime('ID')
    ExpiryDate = fields.Datetime('ExpiryDate')
    Description = fields.Char('Description')
    IsVerified = fields.Char('IsVerified')
    StatusName = fields.Char('StatusName')
    StatusCode = fields.Char('StatusCode')
    IsActive = fields.Char('IsActive')
    CreatedDate = fields.Datetime('ID')
    EditDate = fields.Datetime('EditDate')
    MasterSupplierAccreditationList_Id = fields.Char('MasterSupplierAccreditationList_Id')

class CSD_SupplierAddress(models.Model):
    """ CSD_SupplierAddress """
    _name = 'CSD_SupplierAddress'
    _description = 'CSD_SupplierAddress'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    AddressID = fields.Char('AddressID')
    IsPreferred = fields.Char('IsPreferred')
    AddressTypeCode = fields.Char('AddressTypeCode')
    AddressTypeName = fields.Char('AddressTypeName')
    AddressLine1 = fields.Char('AddressLine1')
    AddressLine2 = fields.Char('AddressLine2')
    CountryCode = fields.Char('CountryCode')
    CountryName = fields.Char('CountryName')
    ProvinceCode = fields.Char('ProvinceCode')
    ProvinceName = fields.Char('ProvinceName')
    DistrictCode = fields.Char('DistrictCode')
    DistrictName = fields.Char('DistrictName')
    MunicipalityCode = fields.Char('MunicipalityCode')
    MunicipalityName = fields.Char('MunicipalityName')
    CityCode = fields.Char('CityCode')
    CityName = fields.Char('CityName')
    SuburbCode = fields.Char('SuburbCode')
    SuburbName = fields.Char('SuburbName')
    WardCode = fields.Char('WardCode')
    WardName = fields.Char('WardName')
    PostalCode = fields.Char('PostalCode')
    IsPostalAddress = fields.Char('IsPostalAddress')
    IsDeliveryAddress = fields.Char('IsDeliveryAddress')
    IsPhysicalAddress = fields.IsPhysicalAddress('ID')
    IsPaymentAddress = fields.IsPaymentAddress('ID')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('ID')
    SupplierAddressList_Id = fields.Char('ID')

class CSD_SupplierAssociation(models.Model):
    """ CSD_SupplierAssociation """
    _name = 'CSD_SupplierAssociation'
    _description = 'CSD_SupplierAssociation'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    AssociationID = fields.Char('AssociationID')
    SupplierNumberRequestor = fields.Char('SupplierNumberRequestor')
    SupplierNumberRequested = fields.Char('SupplierNumberRequested')
    AssociationTypeCode = fields.Char('AssociationTypeCode')
    AssociationTypeName = fields.Char('AssociationTypeName')
    AssociationStatusTypeCode = fields.Char('AssociationStatusTypeCode')
    AssociationStatusTypeName = fields.Char('AssociationStatusTypeName')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')
    SupplierAssociations_Id = fields.Char('SupplierAssociations_Id')

class CSD_SupplierBankAccountDetail(models.Model):
    """ CSD_SupplierBankAccountDetail """
    _name = 'CSD_SupplierBankAccountDetail'
    _description = 'CSD_SupplierBankAccountDetail'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    BankAccountID = fields.Char('BankAccountID')
    AccountHolder = fields.Char('AccountHolder')
    BankAccountStatusName = fields.Char('BankAccountStatusName')
    BankAccountTypeCode = fields.Char('BankAccountTypeCode')
    BankAccountTypeName = fields.Char('BankAccountTypeName')
    IsForeignBankAccount = fields.Char('IsForeignBankAccount')
    BankName = fields.Char('BankName')
    BranchName = fields.Char('BranchName')
    BranchNumber = fields.Char('BranchNumber')
    AccountNumber = fields.Char('AccountNumber')
    CountryCode = fields.Char('CountryCode')
    CountryName = fields.Char('CountryName')
    AddressLine1 = fields.Char('AddressLine1')
    AddressLine2 = fields.Char('AddressLine2')
    ZipCode = fields.Char('ZipCode')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')
    BankAccountList_Id = fields.Char('BankAccountList_Id')
    IsPreferred = fields.Char('IsPreferred')
    BankAccountStatusCode = fields.Char('BankAccountStatusCode')

class CSD_SupplierBBBEEDetails(models.Model):
    """ CSD_SupplierBBBEEDetails """
    _name = 'CSD_SupplierBBBEEDetails'
    _description = 'CSD_SupplierBBBEEDetails'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    CertificateTypeCode = fields.Char('CertificateTypeCode')
    CertificateTypeName = fields.Char('CertificateTypeName')
    VerificationRegulatorCode = fields.Char('VerificationRegulatorCode')
    VerificationRegulatorName = fields.Char('VerificationRegulatorName')
    CertificateNumber = fields.Char('CertificateNumber')
    CertificateIssueDate = fields.Datetime('CertificateIssueDate')
    CertificateExpiryDate = fields.Datetime('CertificateExpiryDate')
    StatusLevelOfContributorCode = fields.Char('StatusLevelOfContributorCode')
    StatusLevelOfContributorName = fields.Char('StatusLevelOfContributorName')
    BlackOwnership = fields.Char('BlackOwnership')
    BlackWomanOwnership = fields.Char('BlackWomanOwnership')
    IsAcceptUnderstandAffidavid = fields.Char('IsAcceptUnderstandAffidavid')
    CertificateSignedBy = fields.Char('CertificateSignedBy')
    CertificateSignDate = fields.Char('CertificateSignDate')
    SectorCharterCode = fields.Char('SectorCharterCode')
    SectorCharterName = fields.Char('SectorCharterName')
    SubSectorCharterCode = fields.Char('SubSectorCharterCode')
    SubSectorCharterName = fields.Char('SubSectorCharterName')
    ValueAddingSupplier = fields.Char('ValueAddingSupplier')
    EmpoweringSupplier = fields.Char('EmpoweringSupplier')
    IRBARegisteredAuditorCode = fields.Char('IRBARegisteredAuditorCode')
    IRBARegisteredAuditorName = fields.Char('IRBARegisteredAuditorName')
    SANASAccreditedAgencyCode = fields.Char('SANASAccreditedAgencyCode')
    SANASAccreditedAgencyName = fields.Char('SANASAccreditedAgencyName')
    OwnershipScore = fields.Char('OwnershipScore')
    ManagementControlScore = fields.Char('ManagementControlScore')
    EmploymentEquityScore = fields.Char('EmploymentEquityScore')
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
    TotalAnnualTurnoverCode = fields.Char('TotalAnnualTurnoverCode')
    TotalAnnualTurnoverName = fields.Char('TotalAnnualTurnoverName')
    FinancialYearStartDate = fields.Datetime('FinancialYearStartDate')
    FinancialYearEndDate = fields.Datetime('FinancialYearEndDate')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')

class CSD_SupplierCommodity(models.Model):
    """ CSD_SupplierCommodity """
    _name = 'CSD_SupplierCommodity'
    _description = 'CSD_SupplierCommodity'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    CommodityGroupID = fields.Char('CommodityGroupID')
    Name = fields.Char('Name')
    Description = fields.Char('Description')
    NationWide = fields.Char('NationWide')
    ProvinceWide = fields.Char('ProvinceWide')
    IsActive = fields.Char('IsActive')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')
    SupplierCommodity_Id = fields.Char('SupplierCommodity_Id')
    SupplierCommodityList_Id = fields.Char('SupplierCommodityList_Id')
    
class CSD_SupplierCommodityItem(models.Model):
    """ CSD_SupplierCommodityItem """
    _name = 'CSD_SupplierCommodityItem'
    _description = 'CSD_SupplierCommodityItem'
    ID = fields.Char('ID')
    CSD_SupplierCommodity_ID = fields.Char('CSD_SupplierCommodity_ID')
    SupplierID = fields.Char('SupplierID')
    CommodityCode = fields.Char('CommodityCode')
    CommodityName = fields.Char('CommodityName')
    ClassName = fields.Char('ClassName')
    ClassCode = fields.Char('ClassCode')
    FamilyName = fields.Char('FamilyName')
    FamilyCode = fields.Char('FamilyCode')
    SegmentName = fields.Char('SegmentName')
    SegmentCode = fields.Char('SegmentCode')
    SupplierCommodityItems_Id = fields.Char('SupplierCommodityItems_Id')

class CSD_SupplierCommodityLocation(models.Model):
    """ CSD_SupplierCommodityLocation """
    _name = 'CSD_SupplierCommodityLocation'
    _description = 'CSD_SupplierCommodityLocation'
    ID = fields.Char('ID')
    CSD_SupplierCommodity_ID = fields.Char('CSD_SupplierCommodity_ID')
    SupplierID = fields.Char('SupplierID')
    WardNumber = fields.Char('WardNumber')
    WardCode = fields.Char('WardCode')
    SuburbName = fields.Char('SuburbName')
    SuburbCode = fields.Char('SuburbCode')
    CityName = fields.Char('CityName')
    CityCode = fields.Char('CityCode')
    MunicipalityName = fields.Char('MunicipalityName')
    MunicipalityCode = fields.Char('MunicipalityCode')
    DistrictName = fields.Char('DistrictName')
    DistrictCode = fields.Char('DistrictCode')
    ProvinceName = fields.Char('ProvinceName')
    ProvinceCode = fields.Char('ProvinceCode')
    SupplierCommodityLocations_Id = fields.Char('SupplierCommodityLocations_Id')

class CSD_SupplierContactDetail(models.Model):
    """ CSD_SupplierContactDetail """
    _name = 'CSD_SupplierContactDetail'
    _description = 'CSD_SupplierContactDetail'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    ContactID = fields.Char('ContactID')
    ContactTypeCode = fields.Char('ContactTypeCode')
    ContactTypeName = fields.Char('ContactTypeName')
    IsPreferred = fields.Char('IsPreferred')
    Name = fields.Char('Name')
    Surname = fields.Char('Surname')
    IdentificationTypeCode = fields.Char('IdentificationTypeCode')
    IdentificationTypeName = fields.Char('IdentificationTypeName')
    SAIDNumber = fields.Char('SAIDNumber')
    ForeignIDNumber = fields.Char('ForeignIDNumber')
    ForeignPassportNumber = fields.Char('ForeignPassportNumber')
    WorkPermit = fields.Char('WorkPermit')
    PreferCellphone = fields.Char('PreferCellphone')
    PreferEmail = fields.Char('PreferEmail')
    PreferFax = fields.Char('PreferFax')
    PreferPostal = fields.Char('PreferPostal')
    PreferSMS = fields.Char('PreferSMS')
    PreferTelephone = fields.Char('PreferTelephone')
    EmailAddress = fields.Char('EmailAddress')
    CellphoneNumber = fields.Char('CellphoneNumber')
    FaxNumber = fields.Char('FaxNumber')
    TelephoneNumber = fields.Char('TelephoneNumber')
    CSDUser = fields.Char('CSDUser')
    IsActive = fields.Char('IsActive')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')
    SupplierContacts_Id = fields.Char('SupplierContacts_Id')

class CSD_SupplierDirector(models.Model):
    """ CSD_SupplierDirector """
    _name = 'CSD_SupplierDirector'
    _description = 'CSD_SupplierDirector'

    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    DirectorID = fields.Char('DirectorID')
    CountryTypeCode = fields.Char('CountryTypeCode')
    CountryTypeName = fields.Char('CountryTypeName')
    IDTypeCode = fields.Char('IDTypeCode')
    IDTypeName = fields.Char('IDTypeName')
    DirectorStatusTypeCode = fields.Char('DirectorStatusTypeCode')
    DirectorStatusTypeName = fields.Char('DirectorStatusTypeName')
    SAIDNumber = fields.Char('SAIDNumber')
    ForeignIDNUmber = fields.Char('ForeignIDNUmber')
    ForeignPassportNumber = fields.Char('ForeignPassportNumber')
    WorkPermitNumber = fields.Char('WorkPermitNumber')
    Name = fields.Char('Name')
    Surname = fields.Char('Surname')
    AppointmentDate = fields.Datetime('AppointmentDate')
    IsActive = fields.Char('IsActive')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')
    LastVerificationDate = fields.Datetime('LastVerificationDate')
    SupplierDirector_Id = fields.Char('SupplierDirector_Id')
    SupplierDirectors_Id = fields.Char('SupplierDirectors_Id')

class CSD_SupplierFlag(models.Model):
    """ CSD_SupplierFlag """
    _name = 'CSD_SupplierFlag'
    _description = 'CSD_SupplierFlag'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    SupplierFlagType = fields.Char('SupplierFlagType')
    SupplierFlagDescription = fields.Char('SupplierFlagDescription')
    SupplierFlagValue = fields.Char('SupplierFlagValue')
    SupplierFlagDetails = fields.Char('SupplierFlagDetails')
    SupplierFlagLastVerificationDate = fields.Datetime('SupplierFlagLastVerificationDate')
    SupplierFlags_Id = fields.Char('SupplierFlags_Id')

class CSD_SupplierIdentificationDetails(models.Model):
    """ CSD_SupplierIdentificationDetails """
    _name = 'CSD_SupplierIdentificationDetails'
    _description = 'CSD_SupplierIdentificationDetails'
    ID = fields.Char('ID')
    UniqueRegistrationReferenceNumber = fields.Char('UniqueRegistrationReferenceNumber')
    SupplierNumber = fields.Char('SupplierNumber')
    SupplierInactiveReason = fields.Char('SupplierInactiveReason')
    SupplierInactiveDate = fields.Datetime('SupplierInactiveDate')
    IsAssociated = fields.Char('IsAssociated')
    IsActive = fields.Char('IsActive')
    SupplierTypeCode = fields.Char('SupplierTypeCode')
    SupplierTypeName = fields.Char('SupplierTypeName')
    SupplierSubTypeCode = fields.Char('SupplierSubTypeCode')
    SupplierSubTypeName = fields.Char('SupplierSubTypeName')
    GovernmentTypeCode = fields.Char('GovernmentTypeCode')
    GovernmentTypeName = fields.Char('GovernmentTypeName')
    IDTypeCode = fields.Char('IDTypeCode')
    IDTypeName = fields.Char('IDTypeName')
    CountryOfOriginCode = fields.Char('CountryOfOriginCode')
    CountryOfOriginName = fields.Char('CountryOfOriginName')
    BusinessStatusCode = fields.Char('BusinessStatusCode')
    BusinessStatusName = fields.Char('BusinessStatusName')
    BusinessStatusLastVerificationDate = fields.Char('BusinessStatusLastVerificationDate')
    IndustryClassificationCode = fields.Char('IndustryClassificationCode')
    IndustryClassificationName = fields.Char('IndustryClassificationName')
    LegalName = fields.Char('LegalName')
    TradingName = fields.Char('TradingName')
    SAIDNumber = fields.Char('SAIDNumber')
    ForeignIDNumber = fields.Char('ForeignIDNumber')
    ForeignPassportNumber = fields.Char('ForeignPassportNumber')
    WorkPermitNumber = fields.Char('WorkPermitNumber')
    SACompanyNumber = fields.Char('SACompanyNumber')
    ForeignCompanyRegistrationNumber = fields.Char('ForeignCompanyRegistrationNumber')
    SATrustRegistrationNumber = fields.Char('SATrustRegistrationNumber')
    ForeignTrustRegistrationNumber = fields.Char('ForeignTrustRegistrationNumber')
    RegistrationDate = fields.Datetime('RegistrationDate')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')
    HaveBankAccount = fields.Char('HaveBankAccount')
    SupplierIdentificationDetails_Id = fields.Char('SupplierIdentificationDetails_Id')

class CSD_SupplierTaxDetails(models.Model):
    """ CSD_SupplierTaxDetails """
    _name = 'CSD_SupplierTaxDetails'
    _description = 'CSD_SupplierTaxDetails'

    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    IncomeTaxNumber = fields.Char('IncomeTaxNumber')
    VATNumber = fields.Char('VATNumber')
    PAYENumber = fields.Char('PAYENumber')
    IsValidCertificate = fields.Char('IsValidCertificate')
    TaxClearanceCertificateExpiryDate = fields.Datetime('TaxClearanceCertificateExpiryDate')
    IsRegistered = fields.Char('IsRegistered')
    LastVerificationDate = fields.Datetime('LastVerificationDate')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')
    ValidationResponse = fields.Char('ValidationResponse')

class Req_Commodities(models.Model):
    """ Req_Commodities """
    _name = 'Req_Commodities'
    _description = 'Req_Commodities'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    Commodity = fields.Char('Commodity')
    ReferenceID = fields.Char('ReferenceID')
    ActiveYN = fields.Char('ActiveYN')
    DateCreated = fields.Datetime('DateCreated')
    fkiReqItemTypeID = fields.Char('fkiReqItemTypeID')
    ParentID = fields.Char('ParentID')

class Req_Document_Line(models.Model):
    """ Req_Document_Line """
    _name = 'Req_Document_Line'
    _description = 'Req_Document_Line'
    DocumentLineID = fields.Char('DocumentLineID')
    CompanyID = fields.Char('CompanyID')
    DocumentHeaderID = fields.Char('DocumentHeaderID')
    ReqItemID = fields.Char('ReqItemID')
    ItemID = fields.Char('ItemID')
    ItemDescription = fields.Char('ItemDescription')
    CommodityID = fields.Char('CommodityID')
    Quantity = fields.Char('Quantity')
    UnitPrice = fields.Char('UnitPrice')
    VATAmount = fields.Char('VATAmount')
    SubTotal = fields.Char('SubTotal')
    TAXInput = fields.Char('TAXInput')
    ItemTaxSchedule = fields.Char('ItemTaxSchedule')
    VATPer = fields.Char('VATPer')
    GLAccount = fields.Char('GLAccount')
    Comments = fields.Char('Comments')
    SiteID = fields.Char('SiteID')
    RequiredByDate = fields.Datetime('RequiredByDate')
    RequestedByAlias = fields.Char('RequestedByAlias')
    BudgetAmount = fields.Char('BudgetAmount')
    ActualAmount = fields.Char('ActualAmount')
    Commited1 = fields.Char('Commited1')
    Commited2 = fields.Char('Commited2')
    AvailableAmount = fields.Char('AvailableAmount')
    DateCreated = fields.Datetime('DateCreated')
    SupplierID = fields.Char('SupplierID')
    SupplierName = fields.Char('SupplierName')
    SupplierAddress1 = fields.Char('SupplierAddress1')
    SupplierAddress2 = fields.Char('SupplierAddress2')
    SupplierAddress3 = fields.Char('SupplierAddress3')
    SupplierAddress4 = fields.Char('SupplierAddress4')
    SupplierAddress5 = fields.Char('SupplierAddress5')
    ShippingMethod = fields.Char('ShippingMethod')
    DeliveryAddress1 = fields.Char('DeliveryAddress1')
    DeliveryAddress2 = fields.Char('DeliveryAddress2')
    DeliveryAddress3 = fields.Char('DeliveryAddress3')
    DeliveryAddress4 = fields.Char('DeliveryAddress4')
    DeliveryAddress5 = fields.Char('DeliveryAddress5')
    ProjectID = fields.Char('ProjectID')
    CostCategoryID = fields.Char('CostCategoryID')
    PONumber = fields.Char('PONumber')
    UnitOfMeasure = fields.Char('UnitOfMeasure')
    OverBudget = fields.Char('OverBudget')
    ContractID = fields.Char('ContractID')
    ContractInstallmentID = fields.Char('ContractInstallmentID')
    ReferenceNumber = fields.Char('ReferenceNumber')
    ContractItemID = fields.Char('ContractItemID')
    ClassificationID = fields.Char('ClassificationID')
    OrignalUnitPrice = fields.Char('OrignalUnitPrice')
    OriginalSubTotal = fields.Char('OriginalSubTotal')
    EstimateExceeded = fields.Char('EstimateExceeded')
    DemandPlanLineID = fields.Char('DemandPlanLineID')
    ApprovalForExceedingRequested = fields.Char('ApprovalForExceedingRequested')
    WBS_ELEMENT = fields.Char('WBS_ELEMENT')
    PackageNo = fields.Char('PackageNo')
    LineSeqNr = fields.Char('LineSeqNr')
    RecommendedSupplierID = fields.Char('RecommendedSupplierID')
    RecommendedContractID = fields.Char('RecommendedContractID')
    ReCommendedSelected = fields.Char('ReCommendedSelected')
    OrderNr = fields.Char('OrderNr')
    StandardPrice = fields.Char('StandardPrice')
    AvePrice = fields.Char('AvePrice')
    VariancePercentage = fields.Char('VariancePercentage')
    Fund = fields.Char('Fund')
    FunctionalArea = fields.Char('FunctionalArea')
    FundedProgram = fields.Char('FundedProgram')
    CommitmentItemGLAccount = fields.Char('CommitmentItemGLAccount')
    mSCOARegional = fields.Char('mSCOARegional')
    mSCOACosting = fields.Char('mSCOACosting')

class Req_Document_Line_Addhoc(models.Model):
    """ Req_Document_Line_Addhoc """
    _name = 'Req_Document_Line_Addhoc'
    _description = 'Req_Document_Line_Addhoc'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    ReqLineID = fields.Char('ReqLineID')
    SysAddHocFieldID = fields.Char('SysAddHocFieldID')
    SysAddHocFieldValueID = fields.Char('SysAddHocFieldValueID')
    SysAddhocFieldName = fields.Char('SysAddhocFieldName')
    SysAddHocFieldCode = fields.Char('SysAddHocFieldCode')
    SysAddhocFieldValue = fields.Char('SysAddhocFieldValue')
    DateCreated = fields.Char('DateCreated')

class Req_DocumentHeader(models.Model):
    """ Req_DocumentHeader """
    _name = 'Req_DocumentHeader'
    _description = 'Req_DocumentHeader'
    DocumentID = fields.Char('DocumentID')
    CompanyID = fields.Char('CompanyID')
    DocumentNumber = fields.Char('DocumentNumber')
    DocumentDate = fields.Char('DocumentDate')
    DateCreated = fields.Datetime('DateCreated')
    ReqTypeID = fields.Char('ReqTypeID')
    Title = fields.Char('Title')
    UserAliasCreated = fields.Char('UserAliasCreated')
    Comments = fields.Char('Comments')
    Status = fields.Char('Status')
    DepartmentID = fields.Char('DepartmentID')
    CurrentApprovalStructureID = fields.Char('CurrentApprovalStructureID')
    PurchaseOrderDate = fields.Char('PurchaseOrderDate')
    SubTotal = fields.Char('SubTotal')
    VATAmount = fields.Char('VATAmount')
    GUID1 = fields.Char('GUID1')
    ReqExceptionType = fields.Char('ReqExceptionType')
    SubmitDate = fields.Char('SubmitDate')
    FinalApproveUser = fields.Char('FinalApproveUser')
    FinalApproveDate = fields.Datetime('FinalApproveDate')
    ApprovalDays = fields.Char('ApprovalDays')
    ContractRequisition = fields.Char('ContractRequisition')
    ContractID = fields.Char('ContractID')
    Contract_InstallmentID = fields.Char('Contract_InstallmentID')
    TransferredtoAccountingSystem = fields.Char('TransferredtoAccountingSystem')
    FinalFinancialApproveDate = fields.Datetime('FinalFinancialApproveDate')
    FinalFinancialApprover = fields.Char('FinalFinancialApprover')
    QueriesContactName = fields.Char('QueriesContactName')
    QueriesContactPhone = fields.Char('QueriesContactPhone')
    QueriesContactEmail = fields.Char('QueriesContactEmail')
    QueriesContactComment = fields.Char('QueriesContactComment')
    QueriesContactAlternative = fields.Char('QueriesContactAlternative')
    PanelContract = fields.Char('PanelContract')

class Req_DocumentHeader_Assigned(models.Model):
    """ Req_DocumentHeader_Assigned """
    _name = 'Req_DocumentHeader_Assigned'
    _description = 'Req_DocumentHeader_Assigned'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    DocumentID = fields.Char('DocumentID')
    UserAlias = fields.Char('UserAlias')
    AssignedDate = fields.Datetime('AssignedDate')
    Status = fields.Char('Status')
    DateLastAccessed = fields.Datetime('DateLastAccessed')
    DateCreated = fields.Datetime('DateCreated')

class Req_DocumentHeader_Comment(models.Model):
    """ Req_DocumentHeader_Comment """
    _name = 'Req_DocumentHeader_Comment'
    _description = 'Req_DocumentHeader_Comment'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    DocumentHeaderID = fields.Char('DocumentHeaderID')
    EventDate = fields.Char('EventDate')
    UserAlias = fields.Char('UserAlias')
    UserComment = fields.Char('UserComment')
    DateCreated = fields.Datetime('DateCreated')

class Req_DocumentHeader_Log(models.Model):
    """ Req_DocumentHeader_Log """
    _name = 'Req_DocumentHeader_Log'
    _description = 'Req_DocumentHeader_Log'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    DocumentHeaderID = fields.Char('DocumentHeaderID')
    UserAlias = fields.Char('UserAlias')
    EventDate = fields.Datetime('EventDate')
    EventDescription = fields.Char('EventDescription')
    DateCreated = fields.Datetime('DateCreated')

class Req_DocumentHeader_RFQ(models.Model):
    """ Req_DocumentHeader_RFQ """
    _name = 'Req_DocumentHeader_RFQ'
    _description = 'Req_DocumentHeader_RFQ'
    ID = fields.Char('ID')
    ReqDocumentID = fields.Char('ReqDocumentID')
    Status = fields.Char('Status')
    Subject = fields.Char('Subject')
    ExpiryDate = fields.Datetime('ExpiryDate')
    ExpiryTime = fields.Char('ExpiryTime')
    RFQMessage = fields.Char('RFQMessage')
    UserCreated = fields.Datetime('UserCreated')
    DateCreated = fields.Datetime('DateCreated')
    OpeningDate = fields.Datetime('OpeningDate')
    ManualRFQ = fields.Char('ManualRFQ')

class Req_GLAccount(models.Model):
    """ Req_GLAccount """
    _name = 'Req_GLAccount'
    _description = 'Req_GLAccount'
    CompanyID = fields.Char('CompanyID')
    GLAccount = fields.Char('GLAccount')
    AccountDescription = fields.Char('AccountDescription')
    DateCreated = fields.Datetime('DateCreated')
    Disabled = fields.Char('Disabled')
    AdditionalSegment = fields.Char('AdditionalSegment')
    AdditionalSegment_Name = fields.Char('AdditionalSegment_Name')

class Req_Inventory(models.Model):
    """ Req_Inventory """
    _name = 'Req_Inventory'
    _description = 'Req_Inventory'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    ItemID = fields.Char('ItemID')
    ItemDescription = fields.Char('ItemDescription')
    UnitOfMeasure = fields.Char('UnitOfMeasure')
    ItemTypeID = fields.Char('ItemTypeID')
    CommodityID = fields.Char('CommodityID')
    GLAccount = fields.Char('GLAccount')
    DateCreated = fields.Char('DateCreated')
    VATRate = fields.Char('VATRate')
    VATSchedule = fields.Char('VATSchedule')
    VATScheduleID = fields.Char('VATScheduleID')
    Comments = fields.Char('Comments')
    ServiceOrGoods = fields.Char('ServiceOrGoods')
    LastUnitPrice = fields.Char('LastUnitPrice')
    StandardPriceExcl = fields.Char('StandardPriceExcl')
    Deleted = fields.Char('Deleted')
    PlantCode = fields.Char('PlantCode')
    DefaultSiteID = fields.Char('DefaultSiteID')
    AllowedToChangeSite = fields.Char('AllowedToChangeSite')
    PurchaseGroup = fields.Char('PurchaseGroup')

class Req_RequisitionType(models.Model):
    """ Req_RequisitionType """
    _name = 'Req_RequisitionType'
    _description = 'Req_RequisitionType'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    RequisitionType = fields.Char('RequisitionType')
    TravelRequisition = fields.Char('TravelRequisition')
    BlockIfNoBudget = fields.Char('BlockIfNoBudget')
    MemoType = fields.Char('MemoType')
    Deleted = fields.Char('Deleted')
    visibleSmartview = fields.Char('visibleSmartview')
    AllowManualSupplierRFQSelection = fields.Char('AllowManualSupplierRFQSelection')
    RFQAttempts = fields.Char('RFQAttempts')
    MinRFQRequired = fields.Char('MinRFQRequired')
    RFQAllowManualCapture = fields.Char('RFQAllowManualCapture')
    RFQDefaultSelection = fields.Char('RFQDefaultSelection')
    RFQHideQuotesUntilExp = fields.Char('RFQHideQuotesUntilExp')
    RequireOrderNr = fields.Char('RequireOrderNr')
    Requisition_InformalTenderLowerLimit = fields.Char('Requisition_InformalTenderLowerLimit')
    Requisition_InformalTenderUpperLimit = fields.Char('Requisition_InformalTenderUpperLimit')
    Requisition_QuoteLowerLimit = fields.Char('Requisition_QuoteLowerLimit')
    Requisition_QuoteUpperLimit = fields.Char('Requisition_QuoteUpperLimit')
    Requisition_TenderLowerLimit = fields.Char('Requisition_TenderLowerLimit')
    CreatorApprovalWhenExceedingEstimate = fields.Char('CreatorApprovalWhenExceedingEstimate')
    ShowReferenceNr = fields.Char('ShowReferenceNr')
    AllowCreatorToSource = fields.Char('AllowCreatorToSource')
    SourcingType = fields.Char('SourcingType')
    MinRequiredAttachment = fields.Char('MinRequiredAttachment')
    AllowPRBackdating = fields.Char('AllowPRBackdating')
    EnableSupplierReview = fields.Char('PurchaseEnableSupplierReview')

class Req_Status(models.Model):
    """ Req_Status """
    _name = 'Req_Status'
    _description = 'Req_Status'
    ID = fields.Char('ID')
    Status = fields.Char('Status')
    StatusColor = fields.Char('StatusColor')
    CssClass = fields.Char('CssClass')

class Req_TravelDestinations(models.Model):
    """ Req_TravelDestinations """
    _name = 'Req_TravelDestinations'
    _description = 'Req_TravelDestinations'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    CountryID = fields.Char('CountryID')
    Destination = fields.Char('Destination')
    DateCreated = fields.Datetime('DateCreated')

class Req_TravelDetails(models.Model):
    """ Req_TravelDetails """
    _name = 'Req_TravelDetails'
    _description = 'Req_TravelDetails'

    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    ReqDocumentID = fields.Char('ReqDocumentID')
    TravellerName = fields.Char('TravellerName')
    IDNumber = fields.Char('IDNumber')
    Reason = fields.Char('Reason')
    VoyagerNr = fields.Char('VoyagerNr')
    FreqGuestNr = fields.Char('FreqGuestNr')
    ProCardNr = fields.Char('ProCardNr')
    CarHireAwardsNr = fields.Char('CarHireAwardsNr')
    AllowanceAmount = fields.Char('AllowanceAmount')
    AllowanceCurrency = fields.Char('AllowanceCurrency')
    DateCreated = fields.Datetime('DateCreated')

class Req_TravelDetails_Accomodation(models.Model):
    """ Req_TravelDetails_Accomodation """
    _name = 'Req_TravelDetails_Accomodation'
    _description = 'Req_TravelDetails_Accomodation'

    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    ReqTravelID = fields.Char('ReqTravelID')
    Accomodation_Name = fields.Char('Accomodation_Name')
    Check_In = fields.Char('Check_In')
    Check_Out = fields.Char('Check_Out')
    DateCreated = fields.Char('DateCreated')
    DateCreated = fields.Datetime('DateCreated')

class Req_TravelDetails_Carhire(models.Model):
    """ Req_TravelDetails_Carhire """
    _name = 'Req_TravelDetails_Carhire'
    _description = 'Req_TravelDetails_Carhire'

    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    ReqTravelID = fields.Char('ReqTravelID')
    Car_Hire_Company = fields.Char('Car_Hire_Company')
    Car_Hire_Group = fields.Char('Car_Hire_Group')
    Car_Hire_Pickup_Date = fields.Char('Car_Hire_Pickup_Date')
    Comments = fields.Char('Comments')
    DateCreated = fields.Datetime('DateCreated')

class Req_TravelDetails_FlightDetails(models.Model):
    """ Req_TravelDetails_FlightDetails """
    _name = 'Req_TravelDetails_FlightDetails'
    _description = 'Req_TravelDetails_FlightDetails'

    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    ReqTravelID = fields.Char('ReqTravelID')
    Departure_Name = fields.Char('Departure_Name')
    Departure_Date = fields.Datetime('Departure_Date')
    Arrive_Name = fields.Char('Arrive_Name')
    Arrive_Date = fields.Datetime('Arrive_Date')
    CountryFrom = fields.Char('CountryFrom')
    CountryTo = fields.Char('CountryTo')
    Comments = fields.Char('Comments')
    DateCreated = fields.Datetime('DateCreated')

class Req_TravelPurpose(models.Model):
    """ Req_TravelPurpose """
    _name = 'Req_TravelPurpose'
    _description = 'Req_TravelPurpose'

    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    Purpose = fields.Char('Purpose')
    DateCreated = fields.Datetime('DateCreated')

class Sup_B_BBEE_Status_Levels(models.Model):
    """ Sup_B_BBEE_Status_Levels """
    _name = 'Sup_B_BBEE_Status_Levels'
    _description = 'Sup_B_BBEE_Status_Levels'

    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    B_BBEE_Status_Level_Contributor = fields.Char('B_BBEE_Status_Level_Contributor')
    DateCreated = fields.Datetime('DateCreated')
    BEE_Recognition_Level = fields.Char('BEE_Recognition_Level')
    PP80_20 = fields.Char('PP80_20')
    PP90_10 = fields.Char('PP90_10')

class Sup_Supplier_Address(models.Model):
    """ Sup_Supplier_Address """
    _name = 'Sup_Supplier_Address'
    _description = 'Sup_Supplier_Address'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    SupplierID = fields.Char('SupplierID')
    AddressType = fields.Char('AddressType')
    AddressLine1 = fields.Char('AddressLine1')
    AddressLine2 = fields.Char('AddressLine2')
    AddressLine3 = fields.Char('AddressLine3')
    AddressLine4 = fields.Char('AddressLine4')
    AddressLine5 = fields.Char('AddressLine5')
    Code = fields.Char('Code')
    Country = fields.Char('Country')
    PrimaryAddressYN = fields.Char('PrimaryAddressYN')
    PrimaryPostalAddressYN = fields.Char('PrimaryPostalAddressYN')
    DateCreated = fields.Datetime('DateCreated')
    ProvinceID = fields.Char('ProvinceID')
    MunicipalitiesID = fields.Char('MunicipalitiesID')
    RegionID = fields.Char('RegionID')
    CSDRecord = fields.Char('CSDRecord')

class Sup_Supplier_ApprovalRoute(models.Model):
    """ Sup_Supplier_ApprovalRoute """
    _name = 'Sup_Supplier_ApprovalRoute'
    _description = 'Sup_Supplier_ApprovalRoute'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    SupplierID = fields.Char('SupplierID')
    UserAlias = fields.Char('UserAlias')
    Status = fields.Char('Status')
    ApprovalDate = fields.Datetime('ApprovalDate')
    ApprovalOrder = fields.Char('ApprovalOrder')
    Comments = fields.Char('Comments')
    DateCreated = fields.Datetime('DateCreated')

class Sup_Supplier_ApprovalStatus(models.Model):
    """ Sup_Supplier_ApprovalStatus """
    _name = 'Sup_Supplier_ApprovalStatus'
    _description = 'Sup_Supplier_ApprovalStatus'
    ID = fields.Char('ID')
    Status = fields.Char('ID')
    DateCreated = fields.Datetime('DateCreated')

class Sup_Supplier_ApprovalStructure(models.Model):
    """ Sup_Supplier_ApprovalStructure """
    _name = 'Sup_Supplier_ApprovalStructure'
    _description = 'Sup_Supplier_ApprovalStructure'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    SupplierTypeID = fields.Char('SupplierTypeID')
    UsersToAlert = fields.Char('UsersToAlert')
    ApprovalOrder = fields.Char('ApprovalOrder')
    DateCreated = fields.Datetime('DateCreated')

class Sup_Supplier_Audit(models.Model):
    """ Sup_Supplier_Audit """
    _name = 'Sup_Supplier_Audit'
    _description = 'Sup_Supplier_Audit'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    ActionUser = fields.Char('ActionUser')
    ActionDate = fields.Datetime('ActionDate')
    EventDescription = fields.Char('SupplierID')
    DateCreated = fields.Datetime('DateCreated')

class Sup_Supplier_Audit_Warning_Types(models.Model):
    """ Sup_Supplier_Audit_Warning_Types """
    _name = 'Sup_Supplier_Audit_Warning_Types'
    _description = 'Sup_Supplier_Audit_Warning_Types'
    ID = fields.Char('ID')
    WarningType = fields.Char('WarningType')

class Sup_Supplier_Audit(models.Model):
    """ Sup_Supplier_Audit """
    _name = 'Sup_Supplier_Audit'
    _description = 'Sup_Supplier_Audit'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    ClassName = fields.Char('ClassName')
    ClassReference = fields.Datetime('ClassReference')
    DateCreated = fields.Datetime('DateCreated')

class Sup_Supplier_Classification(models.Model):
    """ Sup_Supplier_Classification """
    _name = 'Sup_Supplier_Classification'
    _description = 'Sup_Supplier_Classification'
    ID = fields.Char('ID')
    SupplierClassification = fields.Char('SupplierClassification')

class Sup_Supplier_Commodity(models.Model):
    """ Sup_Supplier_Commodity """
    _name = 'Sup_Supplier_Commodity'
    _description = 'Sup_Supplier_Commodity'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    CommodityID = fields.Char('CommodityID')
    DateCreated = fields.Datetime('DateCreated')
    CSDRecord = fields.Char('CSDRecord')

class Sup_Supplier_Contacts(models.Model):
    """ Sup_Supplier_Contacts """
    _name = 'Sup_Supplier_Contacts'
    _description = 'Sup_Supplier_Contacts'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    SupplierID = fields.Char('SupplierID')
    ContactTypeID = fields.Char('ContactTypeID')
    ContactName = fields.Char('ContactName')
    ContactSurname = fields.Char('ContactSurname')
    ContactPosition = fields.Char('ContactPosition')
    ContactTel = fields.Char('ContactTel')
    ContactFax = fields.Char('ContactFax')
    ContactCell = fields.Char('ContactCell')
    ContactEmail = fields.Char('ContactEmail')
    DateCreated = fields.Char('DateCreated')
    Quotation_Contact = fields.Char('Quotation_Contact')
    CSDRecord = fields.Char('CSDRecord')
    POContact = fields.Char('POContact')

class Sup_Supplier_ContactType(models.Model):
    """ Sup_Supplier_ContactType """
    _name = 'Sup_Supplier_ContactType'
    _description = 'Sup_Supplier_ContactType'
    ID = fields.Char('ID')    
    ContactType = fields.Char('ContactType')
    DateCreated = fields.Datetime('DateCreated')
    Compulsary = fields.Char('Compulsary')

class Sup_Supplier_CSD_Status(models.Model):
    """ Sup_Supplier_CSD_Status """
    _name = 'Sup_Supplier_CSD_Status'
    _description = 'Sup_Supplier_CSD_Status'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    StatusType = fields.Char('StatusType')
    okStatus = fields.Char('okStatus')
    StatusMessage = fields.Char('StatusMessage')
    CurrentStatus = fields.Char('CurrentStatus')
    StatusCheckDate = fields.Datetime('DateCreated')
    UserChecked = fields.Char('UserChecked')
    TransactionType = fields.Char('TransactionType')
    RefID = fields.Char('RefID')

class Sup_Supplier_Named_Attachments(models.Model):
    """ Sup_Supplier_Named_Attachments """
    _name = 'Sup_Supplier_Named_Attachments'
    _description = 'Sup_Supplier_Named_Attachments'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    SupplierDetailID = fields.Char('SupplierDetailID')
    DateCreated = fields.Datetime('DateCreated')
    UserAlias = fields.Char('UserAlias')
    FromDate = fields.Datetime('FromDate')
    ToDate = fields.Datetime('ToDate')
    Status = fields.Char('Status')
    ConfirmedUser = fields.Char('ConfirmedUser')
    ConfirmedDate = fields.Datetime('ConfirmedDate')

class Sup_Supplier_Owners(models.Model):
    """ Sup_Supplier_Owners """
    _name = 'Sup_Supplier_Owners'
    _description = 'Sup_Supplier_Owners'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    SupplierID = fields.Char('SupplierID')
    OwnerName = fields.Char('OwnerName')
    OwnerSurname = fields.Char('OwnerSurname')
    OwnerPosition = fields.Char('OwnerPosition')
    OwnerTel = fields.Char('OwnerTel')
    OwnerFax = fields.Char('OwnerFax')
    OwnerCell = fields.Char('OwnerCell')
    OwnerEmail = fields.Char('OwnerEmail')
    OwnerIDNumber = fields.Char('OwnerIDNumber')
    Shareholding = fields.Char('Shareholding')
    Race = fields.Char('Race')
    DisabilityYN = fields.Char('DisabilityYN')
    Gender = fields.Char('Gender')
    Citizen = fields.Char('Citizen')
    DateCreated = fields.Datetime('DateCreated')
    OwnerType = fields.Char('OwnerType')
    CompanyName = fields.Char('CompanyName')
    CompanyRegistrationNr = fields.Char('CompanyRegistrationNr')
    CSDRecord = fields.Char('CSDRecord')
    isOwner = fields.Char('isOwner')
    NonNaturalCSDNumber = fields.Char('NonNaturalCSDNumber')
    LegalName = fields.Char('LegalName')
    OwnershipDemographicCode = fields.Char('OwnershipDemographicCode')
    isActive = fields.Char('isActive')
    AppointmentDate = fields.Datetime('AppointmentDate')
    IDTypeCode = fields.Char('IDTypeCode')

class Sup_Supplier_Owners_Demographics(models.Model):
    """ Sup_Supplier_Owners_Demographics """
    _name = 'Sup_Supplier_Owners_Demographics'
    _description = 'Sup_Supplier_Owners_Demographics'
    ID = fields.Char('ID')
    SupplierOwnerID = fields.Char('SupplierOwnerID')
    Demographic = fields.Char('Demographic')
    DemographicCode = fields.Char('DemographicCode')
    DemoGraphicValue = fields.Char('DemoGraphicValue')
    CSDRecord = fields.Char('CSDRecord')
    DateCreated = fields.Datetime('DateCreated')
    UserCreated = fields.Datetime('UserCreated')

class Sup_Supplier_Rotation_Items(models.Model):
    """ Sup_Supplier_Rotation_Items """
    _name = 'Sup_Supplier_Rotation_Items'
    _description = 'Sup_Supplier_Rotation_Items'
    ID = fields.Char('ID')
    ItemName = fields.Char('ItemName')
    Weight = fields.Char('Weight')
    MonthPeriod = fields.Char('MonthPeriod')

class Sup_Supplier_Sites(models.Model):
    """ Sup_Supplier_Sites """
    _name = 'Sup_Supplier_Sites'
    _description = 'Sup_Supplier_Sites'
    ID = fields.Char('ID')
    SiteID = fields.Char('ID')
    SupplierID = fields.Char('ID')

class Sup_Supplier_Status(models.Model):
    """ Sup_Supplier_Status """
    _name = 'Sup_Supplier_Status'
    _description = 'Sup_Supplier_Status'
    ID = fields.Char('ID')
    Status = fields.Char('Status')
    Description = fields.Char('Description')
    DateCreated = fields.Datetime('DateCreated')

class Sup_Supplier_Status_AccountingSystem(models.Model):
    """ Sup_Supplier_Status_AccountingSystem """
    _name = 'Sup_Supplier_Status_AccountingSystem'
    _description = 'Sup_Supplier_Status_AccountingSystem'
    ID = fields.Char('ID')
    SupplierStatusID = fields.Char('SupplierStatusID')
    StatusCode = fields.Char('StatusCode')
    StatusDescription = fields.Char('StatusDescription')
    ReasonDescription = fields.Char('ReasonDescription')
    ReasonCode = fields.Char('ReasonCode')
    ReasonCodeMapping = fields.Char('ReasonCodeMapping')

class Sup_Supplier_Type(models.Model):
    """ Sup_Supplier_Type """
    _name = 'Sup_Supplier_Type'
    _description = 'Sup_Supplier_Type'
    ID = fields.Char('ID')
    SupplierType = fields.Char('SupplierType')
    Description = fields.Char('Description')
    DisplayOrder = fields.Char('DisplayOrder')
    GPIDGeneration = fields.Char('GPIDGeneration')
    DateCreated = fields.Datetime('DateCreated')
    ReferenceID = fields.Char('ReferenceID')
    ReferenceCode = fields.Char('ReferenceCode')
    AllowManualRegistration = fields.Char('AllowManualRegistration')

class Sup_SupplierBBBEEDetails(models.Model):
    """ Sup_SupplierBBBEEDetails """
    _name = 'Sup_SupplierBBBEEDetails'
    _description = 'Sup_SupplierBBBEEDetails'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    CertificateTypeCode = fields.Char('CertificateTypeCode')
    CertificateTypeName = fields.Char('CertificateTypeName')
    VerificationRegulatorCode = fields.Char('VerificationRegulatorCode')
    VerificationRegulatorName = fields.Char('VerificationRegulatorName')
    CertificateNumber = fields.Char('CertificateNumber')
    CertificateIssueDate = fields.Datetime('CertificateIssueDate')
    CertificateExpiryDate = fields.Datetime('CertificateExpiryDate')
    StatusLevelOfContributorCode = fields.Char('StatusLevelOfContributorCode')
    StatusLevelOfContributorName = fields.Char('StatusLevelOfContributorName')
    BlackOwnership = fields.Char('BlackOwnership')
    BlackWomanOwnership = fields.Char('BlackWomanOwnership')
    IsAcceptUnderstandAffidavid = fields.Char('IsAcceptUnderstandAffidavid')
    CertificateSignedBy = fields.Char('CertificateSignedBy')
    CertificateSignDate = fields.Datetime('CertificateSignDate')
    SectorCharterCode = fields.Char('SectorCharterCode')
    SectorCharterName = fields.Char('SectorCharterName')
    SubSectorCharterCode = fields.Char('SubSectorCharterCode')
    SubSectorCharterName = fields.Char('SubSectorCharterName')
    ValueAddingSupplier = fields.Char('ValueAddingSupplier')
    EmpoweringSupplier = fields.Char('EmpoweringSupplier')
    IRBARegisteredAuditorCode = fields.Char('IRBARegisteredAuditorCode')
    IRBARegisteredAuditorName = fields.Char('IRBARegisteredAuditorName')
    SANASAccreditedAgencyCode = fields.Char('SANASAccreditedAgencyCode')
    SANASAccreditedAgencyName = fields.Char('SANASAccreditedAgencyName')
    OwnershipScore = fields.Char('OwnershipScore')
    ManagementControlScore = fields.Char('ManagementControlScore')
    EmploymentEquityScore = fields.Char('EmploymentEquityScore')
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
    TotalAnnualTurnoverCode = fields.Char('TotalAnnualTurnoverCode')
    TotalAnnualTurnoverName = fields.Char('TotalAnnualTurnoverName')
    FinancialYearStartDate = fields.Datetime('FinancialYearStartDate')
    FinancialYearEndDate = fields.Datetime('FinancialYearEndDate')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')

class Sup_SupplierHeader(models.Model):
    """ Sup_SupplierHeader """
    _name = 'Sup_SupplierHeader'
    _description = 'Sup_SupplierHeader'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    Name = fields.Char('Name')
    DateCreated = fields.Datetime('DateCreated')
    DateUpdated = fields.Datetime('DateUpdated')
    UserUpdated = fields.Datetime('UserUpdated')
    Status = fields.Char('Status')
    SupplierTypeID = fields.Char('SupplierTypeID')
    SupplierType = fields.Char('SupplierType')
    GPVendorID = fields.Char('GPVendorID')
    SupplierClass = fields.Char('SupplierClass')
    ApprovedYN = fields.Char('ApprovedYN')
    UserApproved = fields.Char('UserApproved')
    DateApproved = fields.Datetime('DateApproved')
    UserRequestedApproval = fields.Char('UserRequestedApproval')
    VatRegisteredYN = fields.Char('VatRegisteredYN')
    AlternateID = fields.Char('AlternateID')
    VATRegistrationNr = fields.Char('VATRegistrationNr')
    RegistrationNr = fields.Char('RegistrationNr')
    B_BBEE_ID = fields.Char('B_BBEE_ID')
    GPVATRate = fields.Char('GPVATRate')
    BankName = fields.Char('BankName')
    BankBranch = fields.Char('BankBranch')
    BranchCode = fields.Char('BranchCode')
    BankAccountNumber = fields.Char('BankAccountNumber')
    BankAccountType = fields.Char('BankAccountType')
    currencyID = fields.Char('currencyID')
    OTP = fields.Char('OTP')
    AccSysInterfaceStatus = fields.Char('AccSysInterfaceStatus')
    Status_AccountingSystemID = fields.Char('Status_AccountingSystemID')
    PortalUpdatePending = fields.Char('PortalUpdatePending')
    PaymentMethodID = fields.Char('PaymentMethodID')
    VendorCode = fields.Char('VendorCode')
    Deleted = fields.Char('Deleted')
    ClassificationID = fields.Char('ClassificationID')
    LastCommodityChangeVP = fields.Char('LastCommodityChangeVP')
    LastCommodityChangeGF = fields.Char('LastCommodityChangeGF')
    CSDNumber = fields.Char('CSDNumber')
    CSDUniqueNr = fields.Char('CSDUniqueNr')
    LastCSDCheck = fields.Char('LastCSDCheck')
    CSDStatus = fields.Char('CSDStatus')
    PaymentTermsID = fields.Char('PaymentTermsID')
    LegalName = fields.Char('LegalName')


class Sup_SupplierHeader_BankdetailsHistory(models.Model):
    """ Sup_SupplierHeader_BankdetailsHistory """
    _name = 'Sup_SupplierHeader_BankdetailsHistory'
    _description = 'Sup_SupplierHeader_BankdetailsHistory'
    ID = fields.Char('ID')
    SupplierID = fields.Char('SupplierID')
    BankName = fields.Char('BankName')
    BankBranch = fields.Char('BankBranch')
    BranchCode = fields.Char('BranchCode')
    BankAccountNumber = fields.Char('BankAccountNumber')
    BankAccountType = fields.Char('BankAccountType')
    UserChanged = fields.Char('UserChanged')
    Status = fields.Char('Status')
    DateChanged = fields.Datetime('DateChanged')
    DateCreated = fields.Datetime('DateCreated')

class Sup_SupplierTaxDetails(models.Model):
    """ Sup_SupplierTaxDetails """
    _name = 'Sup_SupplierTaxDetails'
    _description = 'Sup_SupplierTaxDetails'
    ID = fields.Char('ID')
    SupplierHeaderID = fields.Char('SupplierHeaderID')
    IncomeTaxNumber = fields.Char('IncomeTaxNumber')
    VATNumber = fields.Char('VATNumber')
    PAYENumber = fields.Char('PAYENumber')
    IsValidCertificate = fields.Char('IsValidCertificate')
    IsRegistered = fields.Char('IsRegistered')
    LastVerificationDate = fields.Datetime('LastVerificationDate')
    CreatedDate = fields.Datetime('CreatedDate')
    EditDate = fields.Datetime('EditDate')
    ValidationResponse = fields.Char('ValidationResponse')
    IsVATVendor = fields.Char('IsVATVendor')
    TaxClearanceExpiryDate = fields.Datetime('TaxClearanceExpiryDate')

class Sys_Attachments(models.Model):
    """ Sys_Attachments """
    _name = 'Sys_Attachments'
    _description = 'Sys_Attachments'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    RefID = fields.Char('RefID')
    FileType = fields.Char('FileType')
    Attachment = fields.Char('Attachment')
    AttachmentName = fields.Char('AttachmentName')
    AttachmentTypeRef = fields.Char('AttachmentTypeRef')
    Comments = fields.Char('Comments')
    UserUploaded = fields.Char('UserUploaded')
    DateCreated = fields.Datetime('DateCreated')
    PhysicalLocation = fields.Char('PhysicalLocation')
    isVisible = fields.Char('isVisible')
    isArchived = fields.Char('isArchived')
    isOnFileSystem = fields.Char('isOnFileSystem')
    PathOnDisk = fields.Char('PathOnDisk')

class Sys_Audit(models.Model):
    """ Sys_Audit """
    _name = 'Sys_Audit'
    _description = 'Sys_Audit'
    ID = fields.Char('ID')
    PrimaryEntityName = fields.Char('ID')
    UserAlias = fields.Char('ID')
    EventDate = fields.Char('ID')
    EventDescripiton = fields.Char('ID')
    IPAddress = fields.Char('ID')

class Sys_Bank_AccountTypes(models.Model):
    """ Sys_Bank_AccountTypes """
    _name = 'Sys_Bank_AccountTypes'
    _description = 'Sys_Bank_AccountTypes'
    ID = fields.Char('ID')
    BankAccountType = fields.Char('BankAccountType')
    Description = fields.Char('Description')
    ReferenceID = fields.Char('ReferenceID')
    ReferenceNumID = fields.Char('ReferenceNumID')
    Enabled = fields.Char('Enabled')

class Sys_Department(models.Model):
    """ Sys_Department """
    _name = 'Sys_Department'
    _description = 'Sys_Department'
    ID = fields.Char('ID')
    DepartmentID = fields.Char('DepartmentID')
    CompanyID = fields.Char('CompanyID')
    DepartmentName = fields.Char('DepartmentName')
    DepartmentReference = fields.Char('DepartmentReference')
    GLAccountMask = fields.Char('GLAccountMask')
    DateCreated = fields.Datetime('DateCreated')
    DeletedYN = fields.Char('DeletedYN')
    BusinessUnitID = fields.Char('BusinessUnitID')

class Sys_Emails(models.Model):
    """ Sys_Emails """
    _name = 'Sys_Emails'
    _description = 'Sys_Emails'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    EmailTo = fields.Char('EmailTo')
    EmailSubject = fields.Char('EmailSubject')
    EmailBody = fields.Char('EmailBody')
    Status = fields.Char('Status')
    UserSent = fields.Char('UserSent')
    HasAttachmentYN = fields.Char('HasAttachmentYN')
    DateCreated = fields.Datetime('DateCreated')

class Sys_Menu(models.Model):
    """ Sys_Menu """
    _name = 'Sys_Menu'
    _description = 'Sys_Menu'
    ID = fields.Char('ID')
    MenuID = fields.Char('MenuID')
    ModuleID = fields.Char('ModuleID')
    MenuName = fields.Char('MenuName')
    PageURL = fields.Char('PageURL')
    ParentID = fields.Char('ParentID')
    DisplayOrder = fields.Char('DisplayOrder')
    DateCreated = fields.Datetime('DateCreated')

class Sys_Municipalities(models.Model):
    """ Sys_Municipalities """
    _name = 'Sys_Municipalities'
    _description = 'Sys_Municipalities'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    ProviceID = fields.Char('ProviceID')
    Municipalities = fields.Char('Municipalities')
    DateCreated = fields.Datetime('DateCreated')

class Sys_Province(models.Model):
    """ Sys_Province """
    _name = 'Sys_Province'
    _description = 'Sys_Province'
    ID = fields.Char('ID')
    ProvinceName = fields.Char('ProvinceName')
    ProvinceCode = fields.Char('ProvinceCode')

class Sys_Province_Municipalities(models.Model):
    """ Sys_Province_Municipalities """
    _name = 'Sys_Province_Municipalities'
    _description = 'Sys_Province_Municipalities'
    ID = fields.Char('ID')
    ProvinceID = fields.Char('ProvinceID')
    Municipality = fields.Char('Municipality')

class Sys_Province_Municipalities_Regions(models.Model):
    """ Sys_Province_Municipalities_Regions """
    _name = 'Sys_Province_Municipalities_Regions'
    _description = 'Sys_Province_Municipalities_Regions'
    ID = fields.Char('ID')
    MunicipalityID = fields.Char('MunicipalityID')
    RegionCode = fields.Char('RegionCode')

class Sys_Race(models.Model):
    """ Sys_Race """
    _name = 'Sys_Race'
    _description = 'Sys_Race'
    ID = fields.Char('ID')
    RaceDescription = fields.Char('RaceDescription')
    DisplayOrder = fields.Char('DisplayOrder')

class Sys_Reports(models.Model):
    """ Sys_Reports """
    _name = 'Sys_Reports'
    _description = 'Sys_Reports'
    ID = fields.Char('ID')
    CompanyID = fields.Char('CompanyID')
    Section = fields.Char('Section')
    ReportName = fields.Char('ReportName')
    ReportPath = fields.Char('ReportPath')
    ReportDescription = fields.Char('ReportDescription')