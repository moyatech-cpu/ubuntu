# coding=utf-8
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class Branch(models.Model):
    """ NYDA Branches """
    _name = 'branches'
    _description = 'NYDA Branches Data'

    code = fields.Char('Branch Code')
    name = fields.Char('Branch Name')
    description = fields.Char('Description')
    sequence = fields.Integer('Branch ID', default=0)
    state_id = fields.Many2one('res.country.state', string="Province", domain="[('country_id.name', '=', 'South Africa')]")
    manager_id = fields.Many2one('res.users', string="Branch Manager")
    branch_admin_id = fields.Many2one('res.users', string="Branch Admin")
    is_enabled = fields.Boolean(string="Enabled")

'''
class JobCodes(models.Model):
    """ Job Codes """
    _name = 'job_codes'
    _description = 'HR Job Codes Data'

    ID = fields.Char('ID')
    code = fields.Char('Job Code')
    name = fields.Char('Job Name')
    description = fields.Char('Description')    
'''    
class ContractTypes(models.Model):
    """ Contract Types """
    _name = 'contract_types'
    _description = 'Contract Types Data'

    code = fields.Char('Contract Code')
    name = fields.Char('Contract Name')
    description = fields.Char('Description')
    
class Departments(models.Model):
    """ Departments """
    _name = 'departments'
    _description = 'Departments Data'

    code = fields.Char('Code')
    name = fields.Char('Name')
    description = fields.Char('Description')
    
class Committees(models.Model):
    """ Committees """
    _name = 'committees'
    _description = 'Committees Data'

    ID = fields.Char('ID')
    code = fields.Char('Code')
    name = fields.Char('Name')
    description = fields.Char('Description')
    
class EmployeeCodes(models.Model):
    """ Employee Codes """
    _name = 'employee_codes'
    _description = 'EmployeeCodes Data'
    
    name                    = fields.Char(related="LastName", string='Name', readonly=True)
    Company                 = fields.Char('Company')
    Title                   = fields.Char('Title')
    Initials                = fields.Char('Initials')
    FirstName               = fields.Char('FirstName')
    LastName                = fields.Char('LastName')
    KnownAsName             = fields.Char('KnownAsName')
    EmployeeID              = fields.Char('EmployeeID')
    BirthDate               = fields.Char(string="BirthDate")
    DateJoinedGroup         = fields.Char(string="DateJoinedGroup")
    DateJoinedCompany       = fields.Char(string="DateJoinedCompany")
    Gender                  = fields.Selection([('M', 'Male'), ('F', 'Female')],string="Gender")
    MaritalStatus           = fields.Selection([('S', 'Single'), ('M', 'Married'), ('D', 'Divorced'), ('W', 'Widow'), ('P', 'P')],string="Marital Status")
    EmploymentStatusVIP     = fields.Char('EmploymentStatusVIP')
    NewEmploymentStatusGen  = fields.Char('NewEmploymentStatusGen')
    EmploymentStatusGen     = fields.Char('EmploymentStatusGen')
    PostalAddress01         = fields.Char('PostalAddress01')
    PostalAddress02         = fields.Char('PostalAddress02')
    PostalAddress03         = fields.Char('PostalAddress03')
    PostalCode              = fields.Char('PostalCode')
    StreetAddress01         = fields.Char('StreetAddress01')
    StreetAddress02         = fields.Char('StreetAddress02')
    StreetAddress03         = fields.Char('StreetAddress03')
    StreetPostalCode        = fields.Char('StreetPostalCode')
    TelephoneNumber         = fields.Char('TelephoneNumber')
    FaxNumber               = fields.Char('FaxNumber')
    CellphoneNumber         = fields.Char('CellphoneNumber')
    WorkphoneNumber         = fields.Char('WorkphoneNumber')
    EmailAddress            = fields.Char('EmailAddress') 
    GroupCode               = fields.Char('GroupCode')
    LanguageCode            = fields.Char('LanguageCode')
    PeriodForBonus          = fields.Char('PeriodForBonus')
    HoursPerDay             = fields.Char('HoursPerDay')
    HoursPerPeriod          = fields.Char('HoursPerPeriod')
    Internship              = fields.Char('Internship')
    TerminationDate         = fields.Char('TerminationDate')
    TerminationDate2        = fields.Char('TerminationDate2')
    MedicalAidRefNo         = fields.Char('MedicalAidRefNo')
    MedicalAidDependants    = fields.Char('MedicalAidDependants')
    MedicalAidStartDate     = fields.Char('MedicalAidStartDate')
    MedicalAidCode          = fields.Char('MedicalAidCode')
    PensionFundStartDate    = fields.Char('PensionFundStartDate')
    ProvidentFundStartDate  = fields.Char('ProvidentFundStartDate')
    DoctorName              = fields.Char('DoctorName')
    DoctorTelephoneNumber   = fields.Char('DoctorTelephoneNumber')
    BloodGroupCode          = fields.Char('BloodGroupCode')
    Disabled                = fields.Char('Disabled')
    NatureOfDisablility     = fields.Char('NatureOfDisablility')
    ContractNumber          = fields.Char('ContractNumber')
    ContractType            = fields.Char('ContractType')
    ContractStartDate       = fields.Char('ContractStartDate')
    ContractExpiryDate      = fields.Char('ContractExpiryDate')
    ResidencePermitNumber   = fields.Char('ResidencePermitNumber')
    ResidencePermitExpiryDate   = fields.Char('ResidencePermitExpiryDate')
    SecurityClearanceCode       = fields.Char('SecurityClearanceCode')
    SecurityClearanceIssueDate  = fields.Char('SecurityClearanceIssueDate')
    SecurityClearanceExpiryDate = fields.Char('SecurityClearanceExpiryDate')
    WorkPermitNumber        = fields.Char('WorkPermitNumber')
    WorkPermitDate          = fields.Char('WorkPermitDate')
    DirectiveNumber         = fields.Char('DirectiveNumber')
    DirectivePercentage     = fields.Char('DirectivePercentage')
    Passport1Number         = fields.Char('Passport1Number')
    Passport1ExpiryDate     = fields.Char('Passport1ExpiryDate')
    Passport1Country        = fields.Char('Passport1Country')
    Passport2Number         = fields.Char('Passport2Number')
    Passport2ExpiryDate     = fields.Char('Passport2ExpiryDate')
    Passport2Country        = fields.Char('Passport2Country')
    TaxNumber               = fields.Char('TaxNumber')
    TaxOffice               = fields.Char('TaxOffice')
    TaxStatus               = fields.Char('TaxStatus') 
    UIFStatus               = fields.Char('UIFStatus')
    Identifier              = fields.Char('Identifier')
    LastChanged             = fields.Char('LastChanged')
    NewEmployeeType         = fields.Char('NewEmployeeType')
    EmployeeType            = fields.Char('EmployeeType')
    TransferCompany         = fields.Char('TransferCompany')
    CompanyVIP              = fields.Char('CompanyVIP')
    TerminationDateVIP      = fields.Char('TerminationDateVIP')
    ZoneCode                = fields.Char('ZoneCode')
    NewZoneCode             = fields.Char('NewZoneCode')
    SecondName              = fields.Char('SecondName')
    StreetAddress04         = fields.Char('StreetAddress04')
    StreetAddress05         = fields.Char('StreetAddress05')
    StreetAddress06         = fields.Char('StreetAddress06')
    PostalAddress04         = fields.Char('PostalAddress04')
    PostalAddress05         = fields.Char('PostalAddress05')
    PostalAddress06         = fields.Char('PostalAddress06')
    PassportNumber          = fields.Char('PassportNumber')
    PassportCountry         = fields.Char('PassportCountry')
    DoNotReEmploy           = fields.Char('DoNotReEmploy')
    MaidenName              = fields.Char('MaidenName')
    SundryAfr1              = fields.Char('SundryAfr1')
    SundryAfr2              = fields.Char('SundryAfr2')
    SundryAfr3              = fields.Char('SundryAfr3')
    SundryAfr4              = fields.Char('SundryAfr4')
    SundryAfr5              = fields.Char('SundryAfr5')
    EmergencyContactName    = fields.Char('EmergencyContactName')
    EmergencyContactCellNumber  = fields.Char('EmergencyContactCellNumber')
    EmergencyContactWorkNumber  = fields.Char('EmergencyContactWorkNumber')
    ExcludedForSkillsLevy       = fields.Char('ExcludedForSkillsLevy')
    TypeOfService               = fields.Char('TypeOfService')
    CareOfPostalAddress         = fields.Char('CareOfPostalAddress')
    CareOfPostalAddressDetail   = fields.Char('CareOfPostalAddressDetail')
    PostalAddressCountryCode    = fields.Char('PostalAddressCountryCode')
    StreetAddressCountryCode    = fields.Char('StreetAddressCountryCode')
    SocialSecurityStatus        = fields.Char('SocialSecurityStatus')
    SocialSecurityNumber        = fields.Char('SocialSecurityNumber')
    CorrectedSocialSecurityNumber   = fields.Char('CorrectedSocialSecurityNumber')
    PensionFundNumber               = fields.Char('PensionFundNumber')
    ProvidentFundNumber             = fields.Char('ProvidentFundNumber')
    NatureofEmploymentCode          = fields.Char('NatureofEmploymentCode')
    CreateDate                      = fields.Char('CreateDate')
    EditDate                        = fields.Char('EditDate')
    BankLinkSplitType               = fields.Char('BankLinkSplitType')
    NationalHousingFundNumber       = fields.Char('NationalHousingFundNumber')
    NationalHealthInsuranceFundNumber   = fields.Char('NationalHealthInsuranceFundNumber')
    NumberOfChildDependants             = fields.Char('NumberOfChildDependants')
    NumberOfRelativeDependants          = fields.Char('NumberOfRelativeDependants')
    PensionFundCode                     = fields.Char('PensionFundCode')

class EmployeeDisciplinaryGrievanceDescription(models.Model):
    """ employee_disciplinary_grievance_description"""
    _name = 'employee_disciplinary_grievance_description'
    _description = 'Employee Disciplinary Grievance Description'
    
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    EmployeeDisciplinaryGrievanceTypeCode = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class EmployeeDisciplinaryGrievanceDescription(models.Model):
    """ EmployeeDisciplinaryGrievanceType """
    _name = 'employee_disciplinary_grievance_type'
    _description = 'Employee Disciplinary Grievance Type'
    
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    EmployeeDocumentTypeCode = fields.Char('EmployeeDocumentTypeCode')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class EmployeeDisciplinaryGrievanceDescription(models.Model):
    """ EmployeeDocumentDescription """
    _name = 'employee_document_description'
    _description = 'Employee Document Description'
    
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    EmployeeDocumentTypeCode = fields.Char('EmployeeDocumentTypeCode')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class EmployeeFamilyRelationship(models.Model):
    """ EmployeeFamilyRelationship """
    _name = 'employee_family_relationship'
    _description = 'Employee Family Relationship'
    
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class EmployeeItemsIssuedDescription(models.Model):
    """ Employee Items Issued Description """
    _name = 'employee_items_issued_description'
    _description = 'Employee Items Issued Description'

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    EmployeeItemsIssuedTypeCode = fields.Many2one('employee_items_issued_type', string="employee_items_issued_type")
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class EmployeeItemsIssuedType(models.Model):
    """ Employee Items Issued Type """
    _name = 'employee_items_issued_type'
    _description = 'Employee Items Issued Type'
    
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class EmployeePositionHistory(models.Model):
    """ Employee Position History """
    _name = 'employee_position_history'
    _description = 'EmployeePositionHistory'

    ID = fields.Char('Code')
    EmployeeID = fields.Many2one('employee_codes', string='EmployeeID')
    PositionID = fields.Many2one('position_codes', string='PositionID')
    PositionNumber = fields.Char('PositionNumber')
    CompanyID = fields.Char('CompanyID')
    StartDate = fields.Char('StartDate')
    TerminateDate = fields.Char('TerminateDate')
    LastChanged = fields.Char('LastChanged')

class EmployeevsBankLink(models.Model):
    """ EmployeevsBankLink """
    _name = 'employee_bank_link'
    _description = 'EmployeevsBankLink'
    
    EmployeeID = fields.Many2one('employee_codes', string='EmployeeID')
    Priority = fields.Char('Priority')
    BankAccountNumber = fields.Char('BankAccountNumber')
    BankAccountType = fields.Char('BankAccountType')
    BankClearanceNumber = fields.Char('BankClearanceNumber')
    PaymentMethodID = fields.Char('PaymentMethodID')
    BankAccountHolderName = fields.Char('BankAccountHolderName')
    BankAccountRelationship = fields.Char('BankAccountRelationship')
    BankName = fields.Char('BankName')
    BankBranchName = fields.Char('BankBranchName')
    SwiftCode = fields.Char('SwiftCode')
    AdditionalPayInfo1 = fields.Char('AdditionalPayInfo1')
    AdditionalPayInfo2 = fields.Char('AdditionalPayInfo2')
    Amount = fields.Char('Amount')
    PercentageSplit = fields.Char('PercentageSplit')
    AmountEnc = fields.Char('AmountEnc')
    LastChanged = fields.Datetime('LastChanged')

class EmployeevsFamilyLink(models.Model):
    """ EmployeevsFamilyLink """
    _name = 'employee_family_link'
    _description = 'EmployeevsFamilyLink'

    ReminderType = fields.Char('ReminderType')
    EmployeeID = fields.Many2one('employee_codes', string='EmployeeID')
    FirstName = fields.Char('FirstName')
    LastName = fields.Char('LastName')
    RelationshipCode = fields.Char('RelationshipCode')
    ContactPersonCode = fields.Char('ContactPersonCode')
    IDNumber = fields.Char('IDNumber')
    BirthDate = fields.Char('BirthDate')
    TelephoneNumber = fields.Char('TelephoneNumber')
    CellphoneNumber = fields.Char('CellphoneNumber')
    WorkphoneNumber = fields.Char('WorkphoneNumber')
    EmailAddress = fields.Char('EmailAddress')
    PostalAddress01 = fields.Char('PostalAddress01')
    PostalAddress02 = fields.Char('PostalAddress02')
    PostalAddress03 = fields.Char('PostalAddress03')
    PostalCode = fields.Char('PostalCode')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class EmployeevsPositionLink(models.Model):
    """ EmployeevsPositionLink """
    _name = 'employee_position_link'
    _description = 'EmployeevsPositionLink'
        
    EmployeeID = fields.Many2one('employee_codes', string='EmployeeID')
    PositionID = fields.Many2one('position_codes', string='PositionID')
    Company = fields.Char('Company')
    PositionNumber = fields.Char('PositionNumber')
    PositionStartDate = fields.Char('PositionStartDate')
    PositionEndDate = fields.Char('PositionEndDate')
    NewPositionID = fields.Char('NewPositionID')
    NewPositionStartDate = fields.Char('NewPositionStartDate')
    LastChanged = fields.Char('LastChanged')
    EmployeevsPositionLinkType = fields.Char('EmployeevsPositionLinkType')
    ReasonCode = fields.Char('ReasonCode')
    UserID = fields.Char('UserID')
    RecruitProjectManagerID = fields.Char('RecruitProjectManagerID')

class EmploymentStatus(models.Model):
    """ EmploymentStatus """
    _name = 'employment_status'
    _description = 'EmploymentStatus'
    
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    Code = fields.Char('Code')
    EquityEmploymentStatusCode = fields.Char('EquityEmploymentStatusCode')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class EquityAnalysisCodeLink(models.Model):
    """ EquityAnalysisCodeLink """
    _name = 'equity_analysis_code_link'
    _description = 'EquityAnalysisCodeLink'

    CompanyID = fields.Char('CompanyID')    
    
    DepartmentCode = fields.Char('DepartmentCode')
    BranchCode = fields.Char('BranchCode')
    BusinessUnitCode = fields.Char('BusinessUnitCode')
   
    JobTitlesCode = fields.Many2one('job_titles', string='JobTitlesCode')
    JobGradesCode = fields.Many2one('job_grades', string='JobGradesCode')
    JobGeneralCode = fields.Many2one('job_general', string='JobGeneralCode')
    JobFunctionsCode = fields.Many2one('job_functions', string='JobFunctionsCode')
    JobCode = fields.Many2one('job_codes', string='JobCode')
        
    OccupationalLevelCode = fields.Char('OccupationalLevelCode')
    OccupationalCategoryCode = fields.Char('OccupationalCategoryCode')
    WorkplaceCode = fields.Char('WorkplaceCode')
    ProvinceCode = fields.Char('ProvinceCode')
    EquityJobFunctionCode = fields.Char('EquityJobFunctionCode')
    LastChanged = fields.Datetime('LastChanged')

class EquityDisciplinaryGrievance(models.Model):
    """ EquityDisciplinaryGrievance """
    _name = 'equity_disciplinary_grievance'
    _description = 'EquityDisciplinaryGrievance'

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    Code = fields.Char('Code')
    EquityEmploymentStatusCode = fields.Char('EquityEmploymentStatusCode')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class EquityEmploymentStatus(models.Model):
    """ EquityEmploymentStatus """
    _name = 'equity_employment_status'
    _description = 'EquityEmploymentStatus'

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    EquityEmploymentStatusCode = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class EquityRemunerationHistory(models.Model):
    """ EquityRemunerationHistory """
    _name = 'equity_remuneration_history'
    _description = 'EquityRemunerationHistory'

    name = fields.Char(related="EquityRemuneration", string='Name', readonly=True)
    EmployeeID = fields.Many2one('employee_codes', string='EmployeeID')
    PositionID = fields.Many2one('position_codes', string='PositionID')
    RemunerationTrnDate = fields.Char('RemunerationTrnDate')
    OccupationalLevelCode = fields.Char('OccupationalLevelCode')
    OccupationalCategoryCode = fields.Char('OccupationalCategoryCode')
    EquityJobFunctionCode = fields.Char('EquityJobFunctionCode')
    CitizenshipCode = fields.Char('CitizenshipCode')
    TypeOfEmploymentCode = fields.Char('TypeOfEmploymentCode')
    DisciplinaryCount = fields.Char('DisciplinaryCount')
    SkillsTrainingCount = fields.Char('SkillsTrainingCount')
    EquityRemunerationEnc = fields.Char('EquityRemunerationEnc')
    LastChanged = fields.Datetime('LastChanged')
    EquityRemuneration = fields.Char('EquityRemuneration')
    FixedAmountAnnualValue = fields.Char('FixedAmountAnnualValue')
    FixedAmountAnnualValueEnc = fields.Char('FixedAmountAnnualValueEnc')
    VariableAmountToBeAnnualised = fields.Char('VariableAmountToBeAnnualised')
    VariableAmountToBeAnnualisedEnc = fields.Char('VariableAmountToBeAnnualisedEnc')
    VariableAmountAnnualValue = fields.Char('VariableAmountAnnualValue')
    VariableAmountAnnualValueEnc = fields.Char('VariableAmountAnnualValueEnc')

class KPARating(models.Model):
    """ KPARating """
    _name = 'kpa_rating'
    _description = 'KPARating'
    
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    KPARatingID = fields.Char('KPARatingID')
    KPARatingTypeCode = fields.Char('KPARatingTypeCode')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Rating = fields.Char('Rating')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class MedicalAid(models.Model):
    """ MedicalAid """
    _name = 'medical_aid'
    _description = 'MedicalAid'    

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')

class PensionFund(models.Model):
    """ PensionFund """
    _name = 'pension_fund'
    _description = 'PensionFund'    

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    LastChanged = fields.Datetime('LastChanged')
 
class PositionCodes(models.Model):
    """ PositionCodes """
    _name = 'position_codes'
    _description = 'PositionCodes'    
    
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    Code = fields.Char('Code')
    Company = fields.Char('Company')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')

    JobTitlesCode = fields.Many2one('job_titles', string='JobTitlesCode')
    JobGradesCode = fields.Many2one('job_grades', string='JobGradesCode')
    JobFunctionsCode = fields.Many2one('job_functions', string='JobFunctionsCode')
    JobGeneralCode = fields.Many2one('job_general', string='JobGeneralCode')
    JobCode = fields.Many2one('job_codes', string='JobCode')
    SalarySurveyPattersonGradeCode = fields.Many2one('salary_survey_patterson_grade', string='SalarySurveyPattersonGradeCode')
    
    Status = fields.Char('Status')
    VacancyDate = fields.Char('VacancyDate')
    ReserveDate = fields.Char('ReserveDate')
    BranchCode = fields.Char('BranchCode')
    DepartmentCode = fields.Char('DepartmentCode')
    BusinessUnitCode = fields.Char('BusinessUnitCode')
    ZoneCode = fields.Char('ZoneCode')
    KPARatingTypeCode = fields.Char('KPARatingTypeCode')
    CompetenceRatingTypeCode = fields.Char('CompetenceRatingTypeCode')
    LastChanged = fields.Datetime('LastChanged')
    RecruitProcessTemplateID = fields.Char('RecruitProcessTemplateID')
    RecruitAdminCheckTemplateID = fields.Char('RecruitAdminCheckTemplateID')
    RecruitAssessmentTemplateID = fields.Char('RecruitAssessmentTemplateID')
    OldVacancyDate = fields.Char('OldVacancyDate')
    OldReserveDate = fields.Char('OldReserveDate')
    OldStatus = fields.Char('OldStatus')
    SalarySurveyJobFamilyCode = fields.Char('SalarySurveyJobFamilyCode')
    SalarySurveyJobCode = fields.Char('SalarySurveyJobCode')
    UseKPIWeight = fields.Char('UseKPIWeight')
    HoldStatus = fields.Char('HoldStatus')

class RecruitPositionAppliedForStatusCode(models.Model):
    """ RecruitPositionAppliedForStatusCode """
    _name = 'recruit_position_applied_for_status_code'
    _description = 'RecruitPositionAppliedForStatusCode'    

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')
    
class RecruitPostingStatusCode(models.Model):
    """ RecruitPostingStatusCode """
    _name = 'recruit_posting_status_code'
    _description = 'RecruitPostingStatusCode'    

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')
    
class RecruitProcessCode(models.Model):
    """ RecruitProcessCode """
    _name = 'recruit_process_code'
    _description = 'RecruitProcessCode'    

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class RecruitSourceCode(models.Model):
    """ RecruitSourceCode """
    _name = 'recruit_source_code'
    _description = 'RecruitSourceCode'    

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')
    
class RecruitStatusCode(models.Model):
    """ RecruitStatusCode """
    _name = 'recruit_status_code'
    _description = 'RecruitStatusCode'    

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')
    
class InterventionType(models.Model):
    """ InterventionType """
    _name = 'intervention_type'
    _description = 'InterventionType'    

    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class JobCodes(models.Model):
    """ JobCodes """
    _name = 'job_codes'
    _description = 'JobCodes'    
        
    Code = fields.Char('Code')
    name = fields.Char(related="LongDescription", string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    JobTitlesCode = fields.Many2one('job_titles', string='JobTitlesCode')
    JobGradesCode = fields.Many2one('job_grades', string='JobGradesCode')
    JobFunctionsCode = fields.Many2one('job_functions', string='JobFunctionsCode')
    JobGeneralCode = fields.Many2one('job_general', string='JobGeneralCode')
    LastChanged = fields.Datetime('LastChanged')

class JobFunctions(models.Model):
    """ JobFunctions """
    _name = 'job_functions'
    _description = 'JobFunctions'    

    Code = fields.Char('Code')
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class JobGeneral(models.Model):
    """ JobGeneral """
    _name = 'job_general'
    _description = 'JobGeneral'    

    Code = fields.Char('Code')
    name = fields.Char(related="ShortDescription", string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class JobGrades(models.Model):
    """ JobGrades """
    _name = 'job_grades'
    _description = 'JobGrades'    

    Code = fields.Char('Code')
    name = fields.Char(related='ShortDescription', string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')

class JobTitles(models.Model):
    """ JobTitles """
    _name = 'job_titles'
    _description = 'JobTitles'    

    Code = fields.Char('Code')
    name = fields.Char(related='ShortDescription', string='Name', readonly=True)
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    
class JobvsKeyPerformanceLink(models.Model):
    """ JobvsKeyPerformanceLink """
    _name = 'jobvs_key_performance_link'
    _description = 'JobvsKeyPerformanceLink'    
    
    JobCode = fields.Many2one('job_codes', string='JobCode')
    KeyPerformanceAreaCode = fields.Many2one('key_performance_area', string='KeyPerformanceAreaCode')
    Weight = fields.Char('Weight')
    LastChanged = fields.Datetime('LastChanged')

class KeyPerformanceArea(models.Model):
    """ KeyPerformanceArea """
    _name = 'key_performance_area'
    _description = 'KeyPerformanceArea'  
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class KeyPerformanceIndicator(models.Model):
    """ KeyPerformanceIndicator """
    _name = 'key_performance_indicator'
    _description = 'KeyPerformanceIndicator'  
    Code = fields.Char('Code')
    KeyPerformanceAreaCode = fields.Many2one('key_performance_area', string='KeyPerformanceAreaCode')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')
    
class Learnership(models.Model):
    """ Learnership """
    _name = 'learnership'
    _description = 'Learnership'  
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')

class NQFBand(models.Model):
    """ NQFBand """
    _name = 'nqf_band'
    _description = 'NQFBand'
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class NQFLevel(models.Model):
    """ NQFLevel """
    _name = 'nqf_level'
    _description = 'NQFLevel'
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')
    SortOrder = fields.Char('SortOrder')
    QueryType = fields.Char('QueryType')
    NQFBandCode = fields.Many2one('nqf_band', string='NQFBandCode')
    LevelValue = fields.Char('LevelValue')

class OccupationalCategory(models.Model):
    """ OccupationalCategory """
    _name = 'occupational_category'
    _description = 'OccupationalCategory'
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class OccupationalLevel(models.Model):
    """ OccupationalLevel """
    _name = 'occupational_level'
    _description = 'OccupationalLevel'
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class OFOCategory(models.Model):
    """ OFOCategory """
    _name = 'ofo_category'
    _description = 'OFOCategory'
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class SalarySurveyPattersonGrade(models.Model):
    """ SalarySurveyPattersonGrade """
    _name = 'salary_survey_patterson_grade'
    _description = 'SalarySurveyPattersonGrade'
    Code = fields.Char('Code')
    Band = fields.Char('Band')
    SubBand = fields.Char('SubBand')
    Description = fields.Char('Description')
    DecisionType = fields.Char('DecisionType')
    TypicalTitles = fields.Char('TypicalTitles')
    CorrelateEquate = fields.Char('CorrelateEquate')
    CorrelatePeromnes = fields.Char('CorrelatePeromnes')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class SETA(models.Model):
    """ SETA """
    _name = 'seta'
    _description = 'SETA'
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

class TypeOfLearning(models.Model):
    """ TypeOfLearning """
    _name = 'type_of_learning'
    _description = 'TypeOfLearning'
    Code = fields.Char('Code')
    LongDescription = fields.Char('LongDescription')
    ShortDescription = fields.Char('ShortDescription')
    Comments = fields.Char('Comments')
    LastChanged = fields.Datetime('LastChanged')

    
    