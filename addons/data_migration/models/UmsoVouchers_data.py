from odoo import api, fields, models

class UmsoVouchers(models.Model):
    _name = 'umso.voucher'

    AdminComplianceCheckBy = fields.Char(string='Admin Compliance Check By')
    AdminComplianceCheckDT = fields.Char(string='Admin Compliance Check DT')
    AdminComplianceCheckNotes = fields.Char(String='Admin Compliance Check Note')
    AdminComplianceInvoiceRating = fields.Char(string='Admin Compliance Invoice Rating')
    AfterCareBy = fields.Char(string='After Care By')
    AfterCareDT = fields.Char(string='After Care DT')
    AfterCareDone = fields.Char(string='After Care Done')
    AfterCareDueDT = fields.Char(string='After Care Due DT')
    AfterCareJobsCreated = fields.Char(string='After Care Jobs Business')
    AfterCareNewBusiness = fields.Char(string='After Care New Business')
    AfterCareStory = fields.Char(string='After Care Story')
    ApprovedBy = fields.Char(String='Approved By')
    ApprovedDT = fields.Char(string='Approved DT')
    ApprovedNotes = fields.Char(string='Approved Notes')
    AssignedToAtCancellation = fields.Char('Assigned To At Cancellation')
    CancelledBy = fields.Char('Cancelled By')
    CancelledDT = fields.Char(string='Cancelled DT')
    CancelledNotes = fields.Char('Cancelled Notes')
    ClientAppointmentDT = fields.Char('Client Appointment DT')
    ClientInvoice = fields.Char('Client Invoice')
    ClientSignOffDT = fields.Char('Client Sign Off DT')
    ClientSignOffNotes = fields.Char('Client Sign Off Notes')
    CreatedBy = fields.Char('Created By')
    CreatedDT = fields.Char('Created DT')
    CurrentlyAssignedTo = fields.Char('Currently Assigned To')
    DeclinedBy = fields.Char('Declined By')
    DeclinedDT = fields.Char('Declined DT')
    DeclinedNotes = fields.Char('Declined Notes')
    Enabled = fields.Char('Enabled')
    EvalDT = fields.Char('Eval DT')
    EvalFacilities = fields.Char('Eval Facilities')
    EvalFriendliness = fields.Char('Eval Friendliness')
    EvalNotes = fields.Char('Eval Notes')
    EvalOverall = fields.Char('Eval Overall')
    EvalProfessionalism = fields.Char('Eval Professionalism')
    EvalWaitTime = fields.Char('Eval Wait Time')
    ExpiryDT = fields.Char('Expiry Date')
    ExpiryDoneDT = fields.Char('Expiry Done DT')
    ExpiryGPDoneDT = fields.Char('Expiry GP Done DT')
    Invoice = fields.Char('Invoice')
    InvoiceAmount = fields.Char('Invoice Amount')
    InvoiceNumber = fields.Char('Invoice Number')
    IsFromArchive = fields.Char('Is From Archive')
    IssuedBy = fields.Char('Issued By')
    IssuedDT = fields.Char('Issued DT')
    IssuedGPConfirmDT = fields.Char('Issued GP Confirm DT')
    IssuedNotes = fields.Char('Issued Notes')
    Location = fields.Char('Location')
    NextInPackage = fields.Char('Next In Package')
    PaymentAmount = fields.Char('Payment Amount')
    PaymentApprovedBy = fields.Char('Payment Approved By')
    PaymentApprovedDT = fields.Char('Payment Approved DT')
    PaymentApprovedGroupID = fields.Char('Payment Approved Group ID')
    PaymentApprovedNotes = fields.Char('Payment Approved Notes')
    PaymentDT = fields.Char('Payment DT')
    ProdComplianceCheckBy = fields.Char('Prod Compliance Check By')
    ProdComplianceCheckDT = fields.Char('Prod Compliance Check DT')
    ProdComplianceCheckNotes = fields.Char('Prod Compliance Check Notes')
    ProdComplianceProductRating = fields.Char('Prod Compliance Product Rating')
    Product = fields.Char('Product')
    ProductVerifiedBy = fields.Char('Product Verified By')
    ProductVerifiedDT = fields.Char('Product Verified DT')
    ProductVerifiedNotes = fields.Char('Product Verified Notes')
    QueriedBy = fields.Char('Queried By')
    QueriedWhat = fields.Char('Queried What')
    ReIssueAtDT = fields.Char('Re Issue At DT')
    ReIssueAtStatus = fields.Char('Re Issue At Status')
    ReIssueBy = fields.Char('Re Issue By')
    Recommendation = fields.Char('Recommendation')
    RecommendedBy = fields.Char('Recommended By')
    RecommendedDT = fields.Char('Recommended DT')
    RecommendedNotes = fields.Char('Recommended Notes')
    ReviewedDT = fields.Char('Reviewed DT')
    ReviewedNotes = fields.Char('Reviewed Notes')
    RowGUID = fields.Char('Row GUID')
    SYSTEMNotes = fields.Char('SYSTEM Notes')
    ServiceCompletedDT = fields.Char('Service Completed DT')
    ServiceType = fields.Char('Service Type')
    Status = fields.Char('Status')
    StatusAtCancellation = fields.Char('Status At Cancellation')
    StatusAtExpiry = fields.Char('Status At Expiry')
    StatusBeforeQuery = fields.Char('Status Before Query')
    SubmittedForPaymentBy = fields.Char('Submitted For Payment By')
    SubmittedForPaymentDT = fields.Char('Submitted For Payment DT')
    SubmittedForPaymentNotes = fields.Char('Submitted For Payment Notes')
    Timesheet = fields.Char('Timesheet')
    UmsoUser = fields.Char('Umso User')
    Used = fields.Char('Used')
    UsedBy = fields.Char('Used By')
    VerifiedBy = fields.Char('Verified By')
    VerifiedDT = fields.Char('Verified DT')
    VerifiedNotes = fields.Char('Verified Notes')
    VoucherExpiryExtendedBy = fields.Char('Voucher Expiry Extended By')
    VoucherExpiryExtendedDT = fields.Char('Voucher Expiry Extended DT')
    VoucherExpiryExtendedNotes = fields.Char('Voucher Expiry Extended Notes')
    VoucherNumber = fields.Char('Voucher Number')
    VoucherValue = fields.Char('Voucher Value')
    BusinessName = fields.Char('Business Name')
    BusinessStarted = fields.Char('Business Started')
    CellNo = fields.Char('Cell No')
    CreatedDT2 = fields.Char('Created DT 2')
    EmailAddress = fields.Char('Email Address')
    Enabled2 = fields.Char('Enabled 2')
    FailLoginCount = fields.Char('Fail Login Count')
    FirstName = fields.Char('First Name')
    HasExistingBusiness = fields.Char('Has Existing Business')
    HasTempUserName = fields.Char('Has TempUser Name')
    IDNumber = fields.Char('ID Number')
    Image = fields.Char('Image')
    IsDisabled = fields.Char('Is Disabled')
    IsInactiveSP = fields.Char('Is Inactive SP')
    IsMale = fields.Char('Is Male')
    IsRural = fields.Char('Is Rural')
    LastName = fields.Char('Last Name')
    Location2 = fields.Char('Location 2')
    MustChangePassword = fields.Char('Must Change Password')
    Notes = fields.Char('Notes')
    Password = fields.Char('Password')
    PasswordLastChanged = fields.Char('Password Last Changed')
    PhysicalAddress = fields.Char('Physical Address')
    PreferredComsMethod = fields.Char('Preferred Coms Method')
    Race = fields.Char('Race')
    RowGUID2 = fields.Char('Row GUID 2')
    SPName = fields.Char('SP Name')
    SPVatNumber = fields.Char('SP Vat Number')
    SPVendorID = fields.Char('SP Vendor ID')
    TelNo = fields.Char('TelNo')
    UmsoSPRatingLatest = fields.Char('Umso SP Rating Latest')
    UpdatedDT = fields.Char('Updated DT')
    UserName = fields.Char('User Name')
    UserType = fields.Char('User Type')
    BranchID = fields.Char('Branch ID')
    DistrictOffice = fields.Char('District Office')
    Enabled3 = fields.Char('Enabled 3')
    GLCode = fields.Char('GL Code')
    Name = fields.Char('Name')
    Province = fields.Char('Province')
    RowGUID3 = fields.Char('RowGUID 3')


