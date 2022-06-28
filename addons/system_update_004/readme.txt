=======================================================================================================================
pddd/nyda_grant_and_voucher/static/src/xml/thresholds_grant.xml
=======================================================================================================================
<?xml version="1.0" encoding="UTF-8" ?>
<templates>
    <t t-name="threshold_one">
        <div class="demo_header" style="text-align:center;">
            <h4>
                <b>Supporting Documents for Application</b>
            </h4>
        </div>
        <div class="req sfield4" id="sfield4">
            <div class="row">
                <div class="col-md-6">
                    <h4>Certified ID copy of the applicant (not older than 3 months)
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Certified ID copy of the applicant (not older than 3 months), if Cooperative – Certified ID copies of all members">
                            <input name="certified_identity_document_applicant" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- UPDATE 1 START Ammended changes -->
		<div class="req sfield16" id="sfield16">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of residence
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Proof of residence">
                            <input name="proof_of_residence" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield17" id="sfield17">
            <div class="row">
                <div class="col-md-6">
                    <h4>Curriculum Vitae
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Curriculum Vitae">
                            <input name="curriculum_vitae" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield61" id="sfield61">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of Bank Account</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="Proof Of Bank Account">
                            <input name="business_bank_account" type="file" class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!--  <div class="req sfield19" id="sfield19">
            <div class="row">
                <div class="col-md-6">
                    <h4>Supplier Quotations with contact details
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Supplier Quotations with contact details">
                            <input name="supplier_quotations" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>-->
        <div class="req sfield91" id="sfield91">
            <div class="row">
                <div class="col-md-6">
                    <h4>Supplier Quotations with contact details
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Supplier Quotations with contact details">
                            <input name="x_supplier_quotations_ids" type="file"
                                   class="file-upload-field identity" multiple="true" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield20" id="sfield20">
            <div class="row">
                <div class="col-md-6">
                    <h4>Supplier bank details (not older than 3 months)
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Supplier bank details (not older than 3 months)">
                            <input name="supplier_bank_details" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- UPDATE 1 END Ammended below with <b style="color:red"><a href="nyda_grant_and_voucher/static/EmployeeFormList.docx">Download</a></b>  -->
        <div class="sfield1" id="sfield1">
            <div class="row">
                <div class="col-md-6">
                    <h4>NYDA business plan template <b style="color:red"><a href="nyda_grant_and_voucher/static/GrantBusinessPlanTemplate.doc">Download</a></b> </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="NYDA Business plan template">
                            <input name="nyda_business_plan_template_document" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
		<!-- <div class="req sfield21" id="sfield21">
            <div class="row">
                <div class="col-md-6">
                    <h4>Usage of working capital – maximum R7 000,00
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Usage of working capital – maximum R7 000.00">
                            <input name="usage_of_working_capital_7" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div> -->
        
    </t>

    <t t-name="threshold_two">
        <div class="demo_header" style="text-align:center;">
            <h4>
                <b>Supporting Documents for Application</b>
            </h4>
        </div>
        <div class="req sfield4" id="sfield4">
            <div class="row">
                <div class="col-md-6">
                    <h4>Certified ID copy of the applicant (not older than 3 months)
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Certified ID copy of the applicant (not older than 3 months), if Cooperative – Certified ID copies of all members">
                            <input name="certified_identity_document_applicant" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- UPDATE 3 START Ammended changes -->
		<div class="req sfield16" id="sfield16">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of residence
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Proof of residence">
                            <input name="proof_of_residence" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield17" id="sfield17">
            <div class="row">
                <div class="col-md-6">
                    <h4>Curriculum Vitae
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Curriculum Vitae">
                            <input name="curriculum_vitae" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield23" id="sfield23">
            <div class="row">
                <div class="col-md-6">
                    <h4>6 Months personal bank statement
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="6 Months personal bank statement">
                            <input name="six_month_personal_bs" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield24" id="sfield24">
            <div class="row">
                <div class="col-md-6">
                    <h4>6 Months business bank statement
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="6 Months business bank statement">
                            <input name="six_month_business_bs" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield25" id="sfield25">
            <div class="row">
                <div class="col-md-6">
                    <h4>BMT Certificate or any Qualification (Diploma or Degree Business Management, Entrepreneurship)
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="BMT Certificate or any Qualification (Diploma or Degree Business Management, Entrepreneurship)">
                            <input name="certificate_qualification" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield91" id="sfield91">
            <div class="row">
                <div class="col-md-6">
                    <h4>Supplier Quotations with contact details
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Supplier Quotations with contact details">
                            <input name="x_supplier_quotations_ids" type="file"
                                   class="file-upload-field identity" multiple="true" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield20" id="sfield20">
            <div class="row">
                <div class="col-md-6">
                    <h4>Supplier bank details (not older than 3 months)
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Supplier bank details (not older than 3 months)">
                            <input name="supplier_bank_details" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- UPDATE 3 END Ammended changes -->
        <div class="sfield5" id="sfield5">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of Business Registration</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="Proof of Business Registration ">
                            <input name="proof_of_business_registration" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
		
        

        <div class="sfield1" id="sfield1">
            <!-- UPDATE 2 END Ammended below with <b style="color:red"><a href="nyda_grant_and_voucher/static/EmployeeFormList.docx">Download</a></b>  -->
        	<div class="row">
                <div class="col-md-6">
                    <h4>NYDA business plan template <b style="color:red"><a href="nyda_grant_and_voucher/static/GrantBusinessPlanTemplate.doc">Download</a></b></h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="NYDA Business plan template">
                            <input name="nyda_business_plan_template_document" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="req sfield61" id="sfield61">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of Bank Account</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="Proof Of Bank Account">
                            <input name="business_bank_account" type="file" class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
		<!-- UPDATE 4 START  Ammended changes 
        <div class="req sfield26" id="sfield26">
            <div class="row">
                <div class="col-md-6">
                    <h4>Usage of working capital – maximum R5 000,00
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Usage of working capital – maximum R5 000,00">
                            <input name="usage_of_working_capital_5" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
                        <div class="col-md-12" style="color:rebeccapurple">
                            <label class="checkbox_style" style="font-size: 16px">
                                <span>I have the required skill(s) to operate the business</span>
                                <input type="checkbox" name="check_skills_requried" id="x_no_loan_funding_debt"/>
                                <span class="checkmark"/>
                            </label>                       
                        </div>                     
        </div>-->
        <!-- UPDATE 4 END  Ammended changes -->
    </t>

    <t t-name="threshold_three">
        <div class="demo_header" style="text-align:center;">
            <h4>
                <b>Supporting Documents for Application</b>
            </h4>
        </div>
		<div class="req sfield4" id="sfield4">
            <div class="row">
                <div class="col-md-6">
                    <h4>Certified ID copy of the applicant (not older than 3 months), if Cooperative – Certified ID
                        copies of all members
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Certified ID copy of the applicant (not older than 3 months), if Cooperative – Certified ID copies of all members">
                            <input name="certified_identity_document_applicant" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- UPDATE 5 START Ammended changes -->
		<div class="req sfield16" id="sfield16">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of residence
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Proof of residence">
                            <input name="proof_of_residence" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield17" id="sfield17">
            <div class="row">
                <div class="col-md-6">
                    <h4>Curriculum Vitae
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Curriculum Vitae">
                            <input name="curriculum_vitae" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield27" id="sfield27">
            <div class="row">
                <div class="col-md-6">
                    <h4>Original bank statements for the past six to twenty-four months
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Original bank statements for the past six to twenty-four months">
                            <input name="six_twentyfour_bs" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield3" id="sfield3">
            <div class="row">
                <div class="col-md-6">
                    <h4>Formal Business Plan</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="Formal Business Plan ">
                            <input name="formal_business_plan" type="file" class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
		
        

        <div class="req sfield5" id="sfield5">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of Business Registration</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="Proof of Business Registration ">
                            <input name="proof_of_business_registration" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
		<div class="req sfield28" id="sfield28">
            <div class="row">
                <div class="col-md-6">
                    <h4>Provide Management Accounts
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Provide Management Accounts">
                            <input name="management_accounts" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="sfield10" id="sfield10">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of market/Letters of intent or off-take contracts (where applicable).</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Proof of market/Letters of intent or off-take contracts.">
                            <input name="market_letters_off_take_contracts" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
       <!-- <div class="req sfield30" id="sfield30">
            <div class="row">
                <div class="col-md-6">
                    <h4>Business operational for a minimum of one year
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Business operational for a minimum of one year">
                            <input name="business_operational_attachment" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div> --> 
        <div class="req sfield31" id="sfield31">
            <div class="row">
                <div class="col-md-6">
                    <h4>Business Asset Registry
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Business Asset Registry">
                            <input name="buisness_asset_reg" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield32" id="sfield32">
            <div class="row">
                <div class="col-md-6">
                    <h4>Valid Tax Clearance Certificate
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Valid Tax Clearance Certificate">
                            <input name="tax_certificate" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
       <!-- <div class="req sfield33" id="sfield33">
            <div class="row">
                <div class="col-md-6">
                    <h4>Breakdown of the use of funds
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Breakdown of the use of funds">
                            <input name="funds_breakdown" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
          <div class="req sfield34" id="sfield34">
            <div class="row">
                <div class="col-md-6">
                    <h4>Usage of working capital – maximum R10 000,00 
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Usage of working capital – maximum R10 000,00 ">
                            <input name="usage_of_working_capital_10" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>-->
        <div class="req sfield6" id="sfield6">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of Business Bank Confirmation Letter</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="Proof of Business Bank Confirmation Letter">
                            <input name="business_bank_account" type="file" class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </t>

    <t t-name="threshold_four">
        <div class="demo_header" style="text-align:center;">
            <h4>
                <b>Supporting Documents for Application</b>
            </h4>
        </div>
        <div class="req sfield4" id="sfield4">
            <div class="row">
                <div class="col-md-6">
                    <h4>Certified ID copy of the applicant (not older than 3 months), if Cooperative – Certified ID
                        copies of all members
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Certified ID copy of the applicant (not older than 3 months), if Cooperative – Certified ID copies of all members">
                            <input name="certified_identity_document_applicant" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- UPDATE 6 START Ammended changes -->
		<div class="req sfield16" id="sfield16">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of residence
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Proof of residence">
                            <input name="proof_of_residence" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield17" id="sfield17">
            <div class="row">
                <div class="col-md-6">
                    <h4>Curriculum Vitae
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Curriculum Vitae">
                            <input name="curriculum_vitae" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield27" id="sfield27">
            <div class="row">
                <div class="col-md-6">
                    <h4>Original bank statements for the past six to twenty-four months
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Original bank statements for the past six to twenty-four months">
                            <input name="six_twentyfour_bs" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield3" id="sfield3">
            <div class="row">
                <div class="col-md-6">
                    <h4>Formal Business Plan</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="Formal Business Plan ">
                            <input name="formal_business_plan" type="file" class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        

        <div class="req sfield5" id="sfield5">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of Business Registration</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="Proof of Business Registration ">
                            <input name="proof_of_business_registration" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="req sfield6" id="sfield6">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of Business Bank Confirmation Letter</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper" data-text="Proof of Business Bank Confirmation Letter">
                            <input name="business_bank_account" type="file" class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="req sfield7" id="sfield7">
            <div class="row">
                <div class="col-md-6">
                    <h4>Financial Statements (Prepared and signed by an Accountants)</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Latest Audited Financial Statement">
                            <input name="financial_statement_signed_accountant" type="file"
                                   class="file-upload-field identity"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
		
        <div class="sfield100" id="sfield100">
            <div class="row">
                <div class="col-md-6">
                    <h4>One Year Management Accounts</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="One Year Management Accounts">
                            <input name="one_year_management_account" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="sfield10" id="sfield10">
            <div class="row">
                <div class="col-md-6">
                    <h4>Proof of market/Letters of intent or off-take contracts (where applicable).</h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Proof of market/Letters of intent or off-take contracts.">
                            <input name="market_letters_off_take_contracts" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!--<div class="req sfield30" id="sfield30">
            <div class="row">
                <div class="col-md-6">
                    <h4>Business operational for a minimum of three years
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Business operational for a minimum of one year">
                            <input name="business_operational_attachment" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>-->
        <div class="req sfield31" id="sfield31">
            <div class="row">
                <div class="col-md-6">
                    <h4>Business Asset Registry
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Business Asset Registry">
                            <input name="buisness_asset_reg" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="req sfield32" id="sfield32">
            <div class="row">
                <div class="col-md-6">
                    <h4>Valid Tax Clearance Certificate
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Valid Tax Clearance Certificate">
                            <input name="tax_certificate" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!--<div class="req sfield33" id="sfield33">
            <div class="row">
                <div class="col-md-6">
                    <h4>Breakdown of the use of funds
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Breakdown of the use of funds">
                            <input name="funds_breakdown" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
         <div class="req sfield34" id="sfield34">
            <div class="row">
                <div class="col-md-6">
                    <h4>Usage of working capital – maximum R20 000,00 
                    </h4>
                    <div class="form_upload" style="padding-top:10px;padding-bottom:10px">
                        <div class="file-upload-wrapper"
                             data-text="Usage of working capital – maximum R10 000,00 ">
                            <input name="usage_of_working_capital_20" type="file"
                                   class="file-upload-field identity" required="required"/>
                        </div>
                    </div>
                </div>
            </div>
        </div> -->
    </t>


</templates>

==========================================================================================================================


=======================================================================================================================
Register Grant Form view on studio
=======================================================================================================================
								<group>
                                    <field name="proof_of_residence_name" invisible="1"/>
                                    <field name="proof_of_residence" filename="proof_of_residence_name"/>
                                    
                                    <field name="curriculum_vitae_name" invisible="1"/>
                                    <field name="curriculum_vitae" filename="curriculum_vitae_name"/>
                                    
                                    <field name="business_bank_account_name" invisible="1"/>
                                    <field name="business_bank_account" filename="business_bank_account_name"/>
                                    
                                    <field name="supplier_quotations_name" invisible="1"/>
                                    <field name="x_supplier_quotations_ids" string="Supplier Quotations" widget="many2many_tags" />
                                </group>
                                <group>
                                    <field name="supplier_bank_details_name" invisible="1"/>
                                    <field name="supplier_bank_details" filename="supplier_bank_details_name"/>
                                    
                                    <field name="six_month_personal_bs_name" invisible="1"/>
                                    <field name="six_month_personal_bs" filename="six_month_personal_bs_name"/>
                                    
                                    <field name="six_month_business_bs_name" invisible="1"/>
                                    <field name="six_month_business_bs" filename="six_month_business_bs_name"/>
                                    
                                    <field name="certificate_qualification_name" invisible="1"/>
                                    <field name="certificate_qualification" filename="certificate_qualification_name"/>
                                    
                                    <field name="six_twentyfour_bs_name" invisible="1"/>
                                    <field name="six_twentyfour_bs" filename="six_twentyfour_bs_name"/>
                                </group>
                                <group>
                                    <field name="management_accounts_name" invisible="1"/>
                                    <field name="management_accounts" filename="management_accounts_name"/>
                                    
                                    <field name="buisness_asset_reg_name" invisible="1"/>
                                    <field name="buisness_asset_reg" filename="buisness_asset_reg_name"/>
                                    
                                    <field name="tax_certificate_name" invisible="1"/>
                                    <field name="tax_certificate" filename="tax_certificate_name"/>
                                    
                                    
                                </group>

==========================================================================================================================


=======================================================================================================================
main.py 333 on 35 to 407/ 649 - 677, 696 - 709
=======================================================================================================================