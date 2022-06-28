odoo.define('nyda_grant_and_voucher.grant-voucher', function (require) {
'use strict';
var core = require('web.core');
var qweb = core.qweb;
var ajax = require('web.ajax');
ajax.loadXML('/nyda_grant_and_voucher/static/src/xml/thresholds_grant.xml', qweb);

    console.log('---->>>--->>>>')
//only number allow in input field dynamic
function number_validation(){
    console.log("number_validation==========================call thayyu")
    $(".numericOnly").bind('keypress',function (e) {
        if (String.fromCharCode(e.keyCode).match(/[^0-9]/g)) return false;
    });
    console.log("FLOAT_validation======DECIMAL====================call thayyu")
    $(".floatOnly").bind('keypress',function (e) {
        if (String.fromCharCode(e.keyCode).match(/^[0-9]*.?[0-9]*$/g)) return false;
    });

//    $("#grant_amount_threshold").bind('keypress',function (e) {
//        if (String.fromCharCode(e.keyCode).match(/^[0-9]*[.]?[0-9]*$/g)) return false;
//    });
}




//only FLOAT number allow in input field dynamic
//function float_validation(){
//    console.log("FLOAT_validation======DECIMAL====================call thayyu")
//    $(".floatOnly").bind('keypress',function (e) {
//        if (String.fromCharCode(e.keyCode).match(/^[0-9]*[.]?[0-9]*$/g)) return false;
//    });
//}



$(document).ready(function() {
	/*******************************************************************************************
	*UPDATE{start}: [25/08/2021 - Add threshold supporting docs for default 'threshold_one' LM.Mahasha]
	********************************************************************************************/
	//$('#new_threshold_grant').empty();
	//$('#new_threshold_grant').append(qweb.render('threshold_one', {}));
        /*******************************************************************************************
	*UPDATE{end}: [25/08/2021 - Add threshold supporting docs for default 'threshold_one' LM.Mahasha]
	********************************************************************************************/

        $('#btnStatus').click(function(){
            var isChecked = $('#rdSelect').prop('checked');
            alert(isChecked);
        });

        $(".ownership_table").bind("keyup", function() {

            var sum = 0;
            $(this).find('.ownership_value_cal').each(function () {
                var ownership_value_cal = $(this).val();
                console.log("MID WAY=------>>>>", ownership_value_cal)

                sum += parseFloat(ownership_value_cal);
                console.log("SUM   -------CURRENT-------", sum)
                if(sum==100){
                    $("#ownership_value_error").css('color', 'green');
                    $("#total_business_ownership_percent").val(sum);
                    $("#ownership_value_error").html("Ownership % is 100.")
                }
                else{
                     $("#ownership_value_error").css('color','red');
                     $("#ownership_value_error").html("Ownership % should be 100 in order for it to be valid.");
                     $("#total_business_ownership_percent").val(sum);
                }
            });
        });

        $(".ownership_status_table").bind("keyup", function() {

            var sum = 0;
            $(this).find('.ownership_status_value_cal').each(function () {
                var ownership_status_value_cal = $(this).val();
                console.log("MID WAY=------>>>>", ownership_status_value_cal)

                sum += parseFloat(ownership_status_value_cal);
                console.log("SUM   -------CURRENT-------", sum)
                if(sum==100){
                    $("#ownership_status_value_error").css('color', 'green');
                    $("#total_status_ownership_percent").val(sum);
                    $("#ownership_status_value_error").html("Ownership % is 100.")
                }
                else{
                     $("#ownership_status_value_error").css('color','red');
                     $("#ownership_status_value_error").html("Ownership % should be 100 in order for it to be valid.");
                     $("#total_status_ownership_percent").val(sum);
                }
            });
        });

        //Count the number of jobs at company
        $(".job_creation_table").bind("keyup", function() {

            var sum = 0;
            $(this).find('.job_creation_value_cal').each(function () {
                var job_creation_value_cal = $(this).val();
                console.log("MID WAY=------>>>>", job_creation_value_cal)

                sum += parseFloat(job_creation_value_cal);
                console.log("SUM   -------CURRENT-------", sum)
                
                $("#total_count_employees").val(sum);
                
            });
        });        

        //only number allow in input field
        $(".numericOnly").bind('keypress',function (e) {
            if (String.fromCharCode(e.keyCode).match(/[^0-9]/g)) return false;
        });

        $(".floatOnly").bind('keyup',function (e) {
        if (String.fromCharCode(e.keyCode).match(/^\d*\.?\d*$/g)) return false;
        });

        $("#grant_amount_threshold").bind('keyup',function () {
        var val = $("#grant_amount_threshold").val();
            console.log('----------->>>val ', val);
            if (val > 250000){
                console.log('---->>>Maximum amount exceeded')
                $("#grant_error_display").html("Please enter amount less than 250000");
                return false
            }
            else{
                $("#grant_error_display").html("");
            }

        });

        $("#est_turn_over").on('click', function(){
            var val = $("#est_turn_over_field").val();
            var expected_turn_over_range=0;
            console.log("-------->>>>>>>>>>>>", val)
            if(val == 'lttthousand' || val == 'ttfthousand' || val == 'ftnthousand' || val == 'othhthousand' || val == 'htththousand'
            || val == 'ttththousand' || val=='ttfhthousand' || val=='ftnhthousand'){
                console.log("valll =====>>>>>>>>>>>>", val);
                expected_turn_over_range = 1;
                $("#exp_turn_over_hidden_field").val(expected_turn_over_range)
            }
            else if(val=='ottmillion' || val=='tttmillion' || val=='ttfmillion'){
                console.log("val==============>>>>>>>>>>>.", val);
                expected_turn_over_range = 2;
                $("#exp_turn_over_hidden_field").val(expected_turn_over_range)
            }

            else if(val=='mtfmillion'){
                console.log("val=======>>>>>>>>>>>>>>", val);
                expected_turn_over_range = 3;
                $("#exp_turn_over_hidden_field").val(expected_turn_over_range)
            }
            else{
                console.log("NO value to get")
            }
        });

        $(".bus_dev_ass").on('click', function(){
            var chkArray = [];
            var selected;
            $(".bus_dev_ass:checked").each(function(){
                chkArray.push($(this).val());
            });
            console.log(chkArray);
            selected = chkArray.join(',');
            console.log(selected)

            $("#check_box_hidden_field").val(selected)
        });


        $("#selection_threshold").on('change', function(){
            var val = $("#selection_threshold").val();
            console.log('----------->>>val ', $('#new_threshold_grant'))
            console.log('----------->>>val ', qweb)
            if (val == 'threshold_1'){
//                $modelContainer.append(qweb.render('nyda_grant_and_voucher.DocumentsInspector.resModel', options));
                $('#new_threshold_grant').empty();
                $('#new_threshold_grant').append(qweb.render('threshold_one', {}));

                }

            if (val == 'threshold_2'){
                 $('#new_threshold_grant').empty();
                $('#new_threshold_grant').append(qweb.render('threshold_two', {}));
            }

            if (val == 'threshold_3'){
                 $('#new_threshold_grant').empty();
                $('#new_threshold_grant').append(qweb.render('threshold_three', {}));
            }
            if (val == 'threshold_4'){
                 $('#new_threshold_grant').empty();
                $('#new_threshold_grant').append(qweb.render('threshold_four', {}));
            }
            if (val == 'threshold_5'){
                console.log('---->>>threshold5');
                $(".display_additional_jobs").html("Must create at least three permanent additional jobs(Must sustain at least 5 permanent jobs for cooperatives).");
                $(".display_working_capital").html("Usage of working capital – R20000,00.");
                $(".display_business_operational").html("The business must be operational for a minimum of three years.");
                $("#sfield3").removeClass('hidden');
                $("#sfield4").removeClass('hidden');
                $("#sfield5").removeClass('hidden');
                $("#sfield6").removeClass('hidden');
                $("#sfield7").removeClass('hidden');
                $("#sfield8").removeClass('hidden');
                $("#sfield9").removeClass('hidden');
                $("#sfield10").removeClass('hidden');
                $("#sfield11").removeClass('hidden');
                $("#sfield12").removeClass('hidden');
                $("#sfield13").removeClass('hidden');
                $("#sfield14").removeClass('hidden');
                $("#sfield15").removeClass('hidden');
            }

        });
	
	/*******************************************************************************************
	*UPDATE{start}: [25/08/2021 - Add threshold supporting docs for default 'threshold_one' LM.Mahasha]
	********************************************************************************************/
	try{
		//$("#selection_threshold").trigger("change");
		$('#selection_threshold').val('threshold_1').change();
	} catch (err){
		console.log(err);
	}
        /*******************************************************************************************
	*UPDATE{end}: [25/08/2021 - Add threshold supporting docs for default 'threshold_one' LM.Mahasha]
	********************************************************************************************/
	
        //dynamic table for job creation
        var counter = 0;
        if($('#job_creation')){
            $("#addJobRow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td style="border-bottom: 3px solid black; border-right: 3px solid black; border-left: 3px solid black;"><select name="population_group" class="select_style" id="select_geo">  <option value="african">African</option> <option value="white">White</option><option value="indian">Indian</option>   <option value="coloured">Colored</option></select></td>';
                cols += '<td style="border-bottom: 3px solid black;"><input type="number" class="form-control numericOnly job_creation_value_cal" name="before_funding_male"/></td>';
                cols += '<td style="border-bottom: 3px solid black; border-right: 1px solid black;"><input type="number" class="form-control numericOnly job_creation_value_cal" name="before_funding_female"/></td>';
                cols += '<td style="border-bottom: 3px solid black;"><input type="number" class="form-control numericOnly" name="before_funding_disabled_male"/></td>';
                cols += '<td style="border-bottom: 3px solid black; border-right: 1px solid black;"><input type="number" class="form-control numericOnly" name="before_funding_disabled_female"/></td>';
                cols += '<td style="border-bottom: 3px solid black;"><input type="number" class="form-control numericOnly" name="before_funding_age_male"/></td>';
                cols += '<td style="border-right: 3px solid black; border-bottom: 3px solid black;"><input type="number" class="form-control numericOnly" name="before_funding_age_female"/></td>';
                cols += '<td style="border-bottom: 3px solid black;"><input type="number" class="form-control numericOnly" name="after_funding_male"/></td>';
                cols += '<td style="border-bottom: 3px solid black; border-right: 1px solid black;"><input type="number" class="form-control numericOnly" name="after_funding_female"/></td>';
                cols += '<td style="border-bottom: 3px solid black;"><input type="number" class="form-control numericOnly" name="after_funding_disabled_male"/></td>';
                cols += '<td style="border-bottom: 3px solid black; border-right: 1px solid black;"><input type="number" class="form-control numericOnly" name="after_funding_disabled_female"/></td>';
                cols += '<td style="border-bottom: 3px solid black;"><input type="number" class="form-control numericOnly" name="after_funding_age_male"/></td>';
                cols += '<td style="border-bottom: 3px solid black; border-right: 3px solid black;"><input type="number" class="form-control numericOnly" name="after_funding_age_female"/></td>';

                cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#job_creation.order-list").append(newRow);
                counter++;
                number_validation();
            });

        }
        $("table.order-list").on("click", ".ibtnDel", function (event) {
            $(this).closest("tr").remove();
            counter -= 1
        });

        //dynamic table for utilize fund
        var utilize_counter = 0;
        if($('#utilization_fund')){
            $("#addUtilizeRow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><input type="text" class="form-control" name="name"/></td>';
                cols += '<td><input type="number" class="form-control numericOnly" name="amount"/></td>';

                cols += '<td><input type="button" class="ibtnUtilizeDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#utilization_fund.order-list").append(newRow);
                utilize_counter++;
                console.log("utilize_counter===================",)
                number_validation();
            });
        }
        $("table.order-list").on("click", ".ibtnUtilizeDel", function (event) {
            $(this).closest("tr").remove();
            utilize_counter -= 1
        });

        //dynamic table for grant business income
        var grant_business_income_counter = 0;
        if($('#grant_business_income')){
            $("#addGrantBusinessIncomeRow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><select name="name" class="select_style">'+
                  '<option value="sales">Sales</option><option value="debtors">Debtors</option></select></td>';
                cols += '<td><input type="number" class="form-control numericOnly" name="rupees"/></td>';

                cols += '<td><input type="button" class="ibtnGBIDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#grant_business_income.order-list").append(newRow);
                grant_business_income_counter++;
                number_validation();
            });
        }
        $("table.order-list").on("click", ".ibtnGBIDel", function (event) {
            $(this).closest("tr").remove();
            grant_business_income_counter -= 1
        });

        //dynamic table for grant business income
        var grant_personal_income_counter = 0;
        if($('#grant_personal_income')){
            $("#addGrantPersonalIncomeRow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><select name="name" class="select_style">'+
                  '<option value="applicant_salary">Applicant Salary</option><option value="spouse_salary">Spouse Salary</option>'+
                  '</select></td>';
                cols += '<td><input type="number" class="form-control numericOnly" name="rupees"/></td>';

                cols += '<td><input type="button" class="ibtnGPIDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#grant_personal_income.order-list").append(newRow);
                grant_personal_income_counter++;
                number_validation();
            });
        }
        $("table.order-list").on("click", ".ibtnGPIDel", function (event) {
            $(this).closest("tr").remove();
            grant_personal_income_counter -= 1
        });

        //dynamic table for grant business expenses
        var grant_business_expenses_counter = 0;
        if($('#grant_business_expenses')){
            $("#addGrantBusinessExpensesRow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><select name="name" class="select_style">'+
                  '<option value="rent">Rent</option><option value="equipment">Equipment</option>'+
                  '<option value="stock_material">Purchases: Stock/Material</option><option value="water_electricity">Water/Electricity</option>'+
                  '<option value="insurance">Insurance</option><option value="security">Security</option>'+
                  '<option value="accounting_fees">Accounting fees</option><option value="petrol_transport">Petrol/Transport</option>'+
                  '<option value="maintenance">Maintenance</option><option value="salaries_wages">Salaries/Wages</option>'+
                  '<option value="owner_drawings">Owner’s Drawings</option><option value="rsc_levies">RSC Levies</option>'+
                  '<option value="uif_contributions">UIF Contributions</option><option value="tel_fax_postage">Tel/Fax/Postage</option>'+
                  '<option value="stationery">Stationery</option><option value="loan_1_repayment">Loan 1 Repayment</option>'+
                  '<option value="loan_2_repayment">Loan 2 Repayment</option><option value="consumables">Consumables</option>'+
                  ' <option value="sundry_expenses">Sundry Expenses</option></select></td>';
                cols += '<td><input type="number" class="form-control numericOnly" name="rupees"/></td>';

                cols += '<td><input type="button" class="ibtnGBEDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#grant_business_expenses.order-list").append(newRow);
                grant_business_expenses_counter++;
                number_validation();
            });
        }
        $("table.order-list").on("click", ".ibtnGBEDel", function (event) {
            $(this).closest("tr").remove();
            grant_business_expenses_counter -= 1
        });

        //dynamic table for grant personal expenses
        var grant_personal_expenses_counter = 0;
        if($('#grant_personal_expenses')){
            $("#addGrantPersonalExpensesRow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><select name="name" class="select_style">'+
                  '<option value="rent_bond">Rent/Bond</option><option value="car_instalment">Car Instalment</option>'+
                  '<option value="water_electricity">Water Electricity</option><option value="groceries">Groceries</option>'+
                  '<option value="clothing">Clothing</option><option value="travel_transport">Travel/Transport</option>'+
                  '<option value="entertainment">Entertainment</option><option value="medical_expenses">Medical Expenses</option>'+
                  '<option value="donations_church">Donations/Church</option><option value="school_fees">School Fees</option>'+
                  '<option value="family_commitments">Family Commitments</option><option value="insurance_fees">Insurance Fees</option>'+
                  '<option value="life">Life</option><option value="endowment">Endowment</option>'+
                  '<option value="investments">Investments</option><option value="funeral">Funeral</option>'+
                  '<option value="store_cards">Store Cards</option><option value="telephone">Telephone</option>'+
                  '<option value="hp_instalments">HP Instalments</option><option value="nlr_exposure">NLR Exposure</option>'+
                  ' <option value="cca_exposure">CCA Exposure</option></select></td>';
                cols += '<td><input type="number" class="form-control numericOnly" name="rupees"/></td>';

                cols += '<td><input type="button" class="ibtnGPEDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#grant_personal_expenses.order-list").append(newRow);
                grant_personal_expenses_counter++;
                number_validation();
            });
        }
        $("table.order-list").on("click", ".ibtnGPEDel", function (event) {
            $(this).closest("tr").remove();
            grant_personal_expenses_counter -= 1
        });

        //dynamic table for grant other expenses
        var grant_other_expenses_counter = 0;
        if($('#grant_other_expenses')){
            $("#addGrantOtherExpensesRow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><select name="name" class="select_style">'+
                  '<option value="land_buildings">Land/Buildings</option><option value="furniture_fittings">Furniture/Fittings</option>'+
                  ' <option value="equipment">Equipment</option><option value="vehicles">Vehicles</option>'+
                  '</select></td>';
                cols += '<td><input type="number" class="form-control numericOnly" name="rupees"/></td>';

                cols += '<td><input type="button" class="ibtnGOEIDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#grant_other_expenses.order-list").append(newRow);
                grant_other_expenses_counter++;
                number_validation();
            });
        }
        $("table.order-list").on("click", ".ibtnGOEIDel", function (event) {
            $(this).closest("tr").remove();
            grant_other_expenses_counter -= 1
        });

        //dynamic table for ownership status
        var ownership_status_counter = 0;
        if($('#ownership_status')){
            $("#addOwnerStatusRow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><input type="text" class="form-control" name="name"/></td>';
                cols += '<td><input type="text" class="form-control" name="position"/></td>';
                cols += '<td><input type="text" class="form-control" name="mobile"/></td>';
                cols += '<td><select name="disability" class="select_style">'+
                  ' <option value="yes">Yes</option><option value="no">No</option>'+
                  '</select></td>';
                 cols += '<td><select name="gender" class="select_style" style="width:90px">'+
                  ' <option value="female">Female</option><option value="male">Male</option>'+
                  '</select></td>';
                  cols += '<td><select name="geographical_type" class="select_style" style="width:82px">'+
                  '<option value="urban">Urban</option><option value="rural">Rural</option>'+
                  '</select></td>';
                 cols += '<td><select name="population_group" class="select_style" style="width:104px">'+
                  '<option value="african">African</option> <option value="white">White</option>'+
                  ' <option value="indian">Indian</option>  <option value="coloured">Coloured</option>'+
                  '</select></td>';
                cols += '<td><input type="number" class="form-control ownership_status_value_cal" name="ownership"/></td>';

                cols += '<td><input type="button" class="ibtnOSDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#ownership_status.order-list").append(newRow);
                ownership_status_counter++;
                number_validation();
            });
        }
        $("table.order-list").on("click", ".ibtnOSDel", function (event) {
            $(this).closest("tr").remove();
            ownership_status_counter -= 1
        });

         //dynamic table for ownership status
        var business_ownership_status_counter = 0;
        if($('#business_ownership_status')){
            $("#addBusinessOwnerStatusRow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><input type="text" class="form-control" name="name"/></td>';
                cols += '<td><input type="text" class="form-control" name="x_id_number"/></td>';
                
                cols += '<td><select name="position" class="select_style"><option value="">- Select Position -</option><option value="Director">Director</option><option value="Owner/Manager">Owner/Manager</option><option value="Manager">Manager</option><option value="Employee">Employee</option></select></td>';
                
                cols += '<td><input type="text" class="form-control" name="mobile"/></td>';
                
                cols += '<td><select name="disability" class="select_style">'+
                  ' <option value="yes">Yes</option><option value="no">No</option>'+
                  '</select></td>';
                
                 cols += '<td><select name="gender" class="select_style" style="width:90px">'+
                  ' <option value="female">Female</option><option value="male">Male</option>'+
                  '</select></td>';
                  cols += '<td><select name="geographical_type" class="select_style" style="width:82px">>'+
                  '<option value="urban">Urban</option><option value="rural">Rural</option>'+
                  '</select></td>';
                 cols += '<td><select name="population_group" class="select_style" style="width:104px">>'+
                  '<option value="african">African</option> <option value="white">White</option>'+
                  ' <option value="indian">Indian</option>  <option value="coloured">Coloured</option>'+
                  '</select></td>';
                cols += '<td><input type="number" class="form-control ownership_value_cal" name="ownership"/></td>';

                cols += '<td><input type="button" class="ibtnBOSDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#business_ownership_status.order-list").append(newRow);
                business_ownership_status_counter++;
                number_validation();
            });
        }
        $("table.order-list").on("click", ".ibtnBOSDel", function (event) {
            $(this).closest("tr").remove();
            business_ownership_status_counter -= 1
        });

        //validation for business_start_reason_ids field
        $('.business_start_reason_ids').change(function() {
             if($(this).parent().text().trim().toLowerCase() == 'other'){
                if($(this).is(':checked')){
                    $('#business_start_reason_char').addClass('req');
                    $('#business_start_reason_char').addClass('invalid');
                }
                else{
                    $('#business_start_reason_char').removeClass('req');
                    $('#business_start_reason_char').removeClass('invalid');
                }
              }
        });

        //validation for business_start_reason_ids field
        $('.startup_business_start_reason_ids').change(function() {
             if($(this).parent().text().trim().toLowerCase() == 'other'){
                if($(this).is(':checked')){
                    $('#startup_business_start_reason_char').addClass('req');
                    $('#startup_business_start_reason_char').addClass('invalid');
                }
                else{
                    $('#startup_business_start_reason_char').removeClass('req');
                    $('#startup_business_start_reason_char').removeClass('invalid');
                }
              }
        });

        //validation for existing_business_start_reason_ids field
        $('.existing_business_start_reason_ids').change(function() {
             if($(this).parent().text().trim().toLowerCase() == 'other'){
                if($(this).is(':checked')){
                    $('#existing_business_start_reason_char').addClass('req');
                    $('#existing_business_start_reason_char').addClass('invalid');
                }
                else{
                    $('#existing_business_start_reason_char').removeClass('req');
                    $('#existing_business_start_reason_char').removeClass('invalid');
                }
              }
        });

        //validation for business_start_reason_ids field
        $('.business_start_reason_ids').change(function() {
             if($(this).parent().text().trim().toLowerCase() == 'other'){
                if($(this).is(':checked')){
                    $('#business_start_reason_char').addClass('req');
                    $('#business_start_reason_char').addClass('invalid');
                }
                else{
                    $('#business_start_reason_char').removeClass('req');
                    $('#business_start_reason_char').removeClass('invalid');
                }
              }
        });

    var currentTab = 0; // Current tab is set to be the first tab (0)
    showTab(currentTab); // Display the current tab

    function showTab(n) {
      console.log('---nnnnn-',n)
      var x = document.getElementsByClassName("tab");
	console.log("----XXXXXXXXX---",x)
      if(x){
      x[n].style.display = "block";}
      if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
      } else {
        document.getElementById("prevBtn").style.display = "inline";
      }
      if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Submit";
      } else {
        document.getElementById("nextBtn").innerHTML = "Next";
      }
      fixStepIndicator(n)
    }

    //Display Next Tab
     $('#nextBtn').click(function() {
        var n=1;
        var x = document.getElementsByClassName("tab");
        if (n == 1 && !validateForm()) return false;
        /*******************************************************************************************
	*UPDATE{start}: [25/08/2021 - Add threshold supporting docs for default 'threshold_one' LM.Mahasha]
	This statement will be exec when the user presses the next button, when this statement is placed
	within the $(document).ready(function() it doesn't find threshold_one since element is not yet populated
	********************************************************************************************/
        if (currentTab == 0){
	    try{
		//$("#selection_threshold").trigger("change");
		$('#selection_threshold').val('threshold_1').change();
	    } catch (err){
		console.log(err);
	    }
        }
       
	if (currentTab == 1 && !validate2ndPage()) return false;
	
	if (currentTab == 3 && !validate4thPage()) return false;
	
        /*******************************************************************************************
	*UPDATE{end}: [25/08/2021 - function call for 2nd Tab validation of business support services LM.Mahasha]
	********************************************************************************************/
        
        x[currentTab].style.display = "none";
        currentTab = currentTab + n;
        if (currentTab >= x.length) {
         var element = document.getElementById("div_loading");
            document.getElementById("regForm").submit();
            element.classList.add("loading");
            return false;
        }
        showTab(currentTab);
        //put data in hide field form_data
        if($('#job_creation')){
                event.preventDefault();
                var values = {};
                var job_creation_ids = [];
                var grant_amount_utilization = [];
                var grant_business_income_ids = [];
                var grant_personal_income_ids = [];
                var grant_business_expenses_ids = [];
                var grant_personal_expenses_ids = [];
                var other_expenses_ids = [];
                var ownership_status_ids = [];
                var business_ownership_status_ids = [];
                var business_start_reason_ids = [];
                var startup_business_sector_ids = [];
                var existing_business_sector_ids = [];
                var startup_business_start_reason_ids = [];
                var existing_business_start_reason_ids = [];
                var startup_legal_entity_ids = [];
                var grant_business_sector_ids = [];
                var grant_legal_entity_ids = [];
                var existing_legal_entity_ids = [];
                var business_development_assistance_ids = [];
                $('#job_creation tbody tr').each(function(){
                        var r_val = {}
                        r_val['before_funding_male'] = $(this).find('td input[name="before_funding_male"]').val();
                        r_val['before_funding_female'] = $(this).find('td input[name="before_funding_female"]').val();
                        r_val['before_funding_disabled_male'] = $(this).find('td input[name="before_funding_disabled_male"]').val();
                        r_val['before_funding_disabled_female'] = $(this).find('td input[name="before_funding_disabled_female"]').val();
                        r_val['before_funding_age_male'] = $(this).find('td input[name="before_funding_age_male"]').val();
                        r_val['before_funding_age_female'] = $(this).find('td input[name="before_funding_age_female"]').val();
                        r_val['after_funding_male'] = $(this).find('td input[name="after_funding_male"]').val();
                        r_val['after_funding_female'] = $(this).find('td input[name="after_funding_female"]').val();
                        r_val['after_funding_disabled_male'] = $(this).find('td input[name="after_funding_disabled_male"]').val();
                        r_val['after_funding_disabled_female'] = $(this).find('td input[name="after_funding_disabled_female"]').val();
                        r_val['after_funding_age_male'] = $(this).find('td input[name="after_funding_age_male"]').val();
                        r_val['after_funding_age_female'] = $(this).find('td input[name="after_funding_age_female"]').val();
                        r_val['population_group'] = $(this).find('td select[name="population_group"]').val();
                        job_creation_ids.push(r_val);

                    });

                    $('#utilization_fund tbody tr').each(function(){
                        var r_val_utilize = {}
                        r_val_utilize['name'] = $(this).find('td input[name="name"]').val();
                        r_val_utilize['amount'] = $(this).find('td input[name="amount"]').val();
                        grant_amount_utilization.push(r_val_utilize);

                    });

                    $('#grant_business_income tbody tr').each(function(){
                        var grant_business_income = {}
                        grant_business_income['name'] = $(this).find('td select[name="name"]').val();
                        grant_business_income['rupees'] = $(this).find('td input[name="rupees"]').val();
                        grant_business_income_ids.push(grant_business_income);

                    });

                    $('#grant_personal_income tbody tr').each(function(){
                        var grant_personal_income = {}
                        grant_personal_income['name'] = $(this).find('td select[name="name"]').val();
                        grant_personal_income['rupees'] = $(this).find('td input[name="rupees"]').val();
                        grant_personal_income_ids.push(grant_personal_income);

                    });

                    $('#grant_business_expenses tbody tr').each(function(){
                        var grant_business_expenses = {}
                        grant_business_expenses['name'] = $(this).find('td select[name="name"]').val();
                        grant_business_expenses['rupees'] = $(this).find('td input[name="rupees"]').val();
                        grant_business_expenses_ids.push(grant_business_expenses);

                    });

                    $('#grant_personal_expenses tbody tr').each(function(){
                        var grant_personal_expenses = {}
                        grant_personal_expenses['name'] = $(this).find('td select[name="name"]').val();
                        grant_personal_expenses['rupees'] = $(this).find('td input[name="rupees"]').val();
                        grant_personal_expenses_ids.push(grant_personal_expenses);

                    });

                    $('#grant_other_expenses tbody tr').each(function(){
                        var grant_other_expenses = {}
                        grant_other_expenses['name'] = $(this).find('td select[name="name"]').val();
                        grant_other_expenses['rupees'] = $(this).find('td input[name="rupees"]').val();
                        other_expenses_ids.push(grant_other_expenses);

                    });

                    $('#ownership_status tbody tr').each(function(){
                        var ownership_status = {}
                        ownership_status['name'] = $(this).find('td input[name="name"]').val();
                        ownership_status['position'] = $(this).find('td input[name="position"]').val();
                        ownership_status['mobile'] = $(this).find('td input[name="mobile"]').val();
                        ownership_status['disability'] = $(this).find('td select[name="disability"]').val();
                        ownership_status['gender'] = $(this).find('td select[name="gender"]').val();
                        ownership_status['geographical_type'] = $(this).find('td select[name="geographical_type"]').val();
                        ownership_status['population_group'] = $(this).find('td select[name="population_group"]').val();
                        ownership_status['ownership'] = $(this).find('td input[name="ownership"]').val();
                        if(ownership_status['name']){
                            ownership_status_ids.push(ownership_status);
                        }

                    });

                    $('#business_ownership_status tbody tr').each(function(){
                        var business_ownership_status = {}
                        business_ownership_status['name'] = $(this).find('td input[name="name"]').val();
                        business_ownership_status['x_id_number'] = $(this).find('td input[name="x_id_number"]').val();
                        business_ownership_status['position'] = $(this).find('td select[name="position"]').val();
                        business_ownership_status['mobile'] = $(this).find('td input[name="mobile"]').val();
                        business_ownership_status['disability'] = $(this).find('td select[name="disability"]').val();
                        business_ownership_status['gender'] = $(this).find('td select[name="gender"]').val();
                        business_ownership_status['geographical_type'] = $(this).find('td select[name="geographical_type"]').val();
                        business_ownership_status['population_group'] = $(this).find('td select[name="population_group"]').val();
                        business_ownership_status['ownership'] = $(this).find('td input[name="ownership"]').val();
                        if(business_ownership_status['name'] ){
                            business_ownership_status_ids.push(business_ownership_status);
                        }

                    });



                    $.each($("input[name='business_start_reason_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            business_start_reason_ids.push(parseInt($(this).val()));
                        }

                    });

                    $.each($("input[name='startup_business_start_reason_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            startup_business_start_reason_ids.push(parseInt($(this).val()));
                        }
                    });

                    $.each($("input[name='existing_business_start_reason_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            existing_business_start_reason_ids.push(parseInt($(this).val()));
                        }
                    });

                    $.each($("input[name='startup_business_sector_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            startup_business_sector_ids.push(parseInt($(this).val()));
                        }
                    });

                    $.each($("input[name='existing_business_sector_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            existing_business_sector_ids.push(parseInt($(this).val()));
                        }
                    });

                    $.each($("input[name='grant_business_sector_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            grant_business_sector_ids.push(parseInt($(this).val()));
                        }
                    });

                    $.each($("input[name='startup_legal_entity_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            startup_legal_entity_ids.push(parseInt($(this).val()));
                        }
                    });

                    $.each($("input[name='grant_legal_entity_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            grant_legal_entity_ids.push(parseInt($(this).val()));
                        }
                    });

                     $.each($("input[name='existing_legal_entity_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            existing_legal_entity_ids.push(parseInt($(this).val()));
                        }
                    });

                     $.each($("input[name='business_development_assistance_ids']:checked"), function(){
                        if($(this).val() != 'other'){
                            business_development_assistance_ids.push(parseInt($(this).val()));
                        }
                    });

                    values['job_creation_ids'] = job_creation_ids;
                    values['grant_amount_utilization'] = grant_amount_utilization;
                    values['grant_business_income_ids'] = grant_business_income_ids;
                    values['grant_personal_income_ids'] = grant_personal_income_ids;
                    values['grant_business_expenses_ids'] = grant_business_expenses_ids;
                    values['grant_personal_expenses_ids'] = grant_personal_expenses_ids;
                    values['other_expenses_ids'] = other_expenses_ids;
                    values['ownership_status_ids'] = ownership_status_ids;
                    values['business_ownership_status_ids'] = business_ownership_status_ids;
                    values['business_start_reason_ids'] = business_start_reason_ids;
                    values['startup_business_start_reason_ids'] = startup_business_start_reason_ids;
                    values['existing_business_start_reason_ids'] = existing_business_start_reason_ids;
                    values['startup_business_sector_ids'] = startup_business_sector_ids;
                    values['existing_business_sector_ids'] = existing_business_sector_ids;
                    values['grant_business_sector_ids'] = grant_business_sector_ids;
                    values['startup_legal_entity_ids'] = startup_legal_entity_ids;
                    values['grant_legal_entity_ids'] = grant_legal_entity_ids;
                    values['existing_legal_entity_ids'] = existing_legal_entity_ids;
                    values['business_development_assistance_ids'] = business_development_assistance_ids;
                    $('input[name="form_data"]').val(JSON.stringify(values));
        }


     })

    //Display Prevous Tab
    $('#prevBtn').click(function() {
         var n=-1;
             var x = document.getElementsByClassName("tab");
          // Exit the function if any field in the current tab is invalid:
          if (n == 1 && !validateForm()) return false;
          // Hide the current tab:
          x[currentTab].style.display = "none";
          // Increase or decrease the current tab by 1:
          currentTab = currentTab + n;
          // if you have reached the end of the form...
          if (currentTab >= x.length) {
            document.getElementById("regForm").submit();
            return false;
          }
          showTab(currentTab);
    })
	/*******************************************************************************************
	*UPDATE{start}: [24/11/2021 - function definition 2nd Tab validation of business support services LM.Mahasha]
	********************************************************************************************/
	function validate2ndPage() {
		var x, y, z, p, i,bds,x_bds_count, valid = true;
  		x = document.getElementsByClassName("tab");
		bds = document.getElementsByClassName("bus_dev_ass");
		x_bds_count = 0;
		for (var i = 0; i < bds.length; ++i) {
    		if(bds[i].checked)
				x_bds_count++;
		}
		//var business_ids = x[currentTab].getElementsByClassName("bus_dev_ass");
		//evade other forms except voucher application form
		//$('#regForm').attr('action') == "/voucher-application-submit"){
		//$(this).closest("form").attr('action') == "/voucher-application-submit"
		if ($("#regForm").attr("action").indexOf("voucher") != -1){
			try{
				if ($("#check_box_hidden_field").val().length < 1){
					valid = false;
					alert("Please select atleast one Business support services");
  				} 
  				else if (x_bds_count >= 5){
					valid = false;
					alert("Only a maximum of 4 business support services can be selected");
  				}
			} catch (err){
				console.log(err);
			}
		}
		return valid; // return the valid status
	}

	function validate4thPage() {
		var valid = true;
		if ($("#regForm").attr("action").indexOf("grant") != -1){
     			var no_loan_funding_debt	= document.getElementById("x_no_loan_funding_debt");
     			var no_sme_loan_funding		= document.getElementById("x_no_sme_loan_funding");
     			var loan_not_written_off	= document.getElementById("x_loan_not_written_off");
	
      			//Check if declarations have been selected before submitting the form
      			if (no_loan_funding_debt.checked == false || no_sme_loan_funding.checked == false || loan_not_written_off.checked == false) {
	        		valid	= false;
	        		alert("Please confirm all loan funding programme declarations.");
	        		throw new Error("Please confirm all loan funding programme declarations.");
      			}
      		}
		return valid; // return the valid status
	}
		
	/*******************************************************************************************
	 *UPDATE{end}: [24/11/2021 - function definition for 2nd Tab validation of business support services LM.Mahasha]
	 ********************************************************************************************/

	
    function validateForm() {
  // This function deals with validation of the form fields
  var x, y, z, p, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByClassName("req");
  z = x[currentTab].getElementsByClassName("identity");
  var phone_val = x[currentTab].getElementsByClassName("phone_val");
  //var threshold_val = document.getElementsById("selection_threshold");
  
  for (i = 0; i < y.length; i++) {
    if (y[i].value == "") {
      y[i].className += " invalid";
      valid = false;
    }
  }

  for (i = 0; i < z.length; i++) {
       if (z[i].value == "") {
            valid = false;
             alert("All Supporting Documents are Mandatory Please Submit All Your Documents");
             break;
      }

      if (z[i].id == "certified_copy_age") {
    	  
    	  if (!z[i].checked) {
    		  valid = false;
    		  alert("Please confirm if your ID Copy is not older than 3 Months.");
    		  break;
    	  }
     }
  }

  if(phone_val[0]){
    if (phone_val[0].value.length != 10) {
            valid = false;
             alert("Please enter valid phone number");
      }
  }

  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

    function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active","");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}

    $("form").on("change", ".file-upload-field", function(){
        $(this).parent(".file-upload-wrapper").attr("data-text",$(this).val().replace(/.*(\/|\\)/, '') );
    });

    $(".existing_business").on('click', function(){
    var val = $(".existing_business:checked").val();
    if (val == 'True'){
            $('.existing_business_div').removeClass('hidden');
            $('.que_two_voucher').addClass('hidden');
            $('.que_three_voucher').addClass('hidden');
        }else{
            $('.existing_business_div').addClass('hidden');
            $('.que_two_voucher').removeClass('hidden');
            $('.que_two_voucher').removeClass('hidden');
        }
    });

    $(".business_idea").on('click', function(){
    var val = $(".business_idea:checked").val();
    if (val == 'True'){
            $('.business_idea_div').removeClass('hidden');
            $('.que_three_voucher').addClass('hidden');
        }else{
            $('.business_idea_div').addClass('hidden');
            $('.que_three_voucher').removeClass('hidden');

        }
    });

    $(".no_business").on('click', function(){
    var val = $(".no_business:checked").val();
    if (val == 'True'){
            $('.no_business_div').removeClass('hidden');
        }else{
            $('.no_business_div').addClass('hidden');
        }
    });

    $(".existing_business_button_hide").on('click', function(){
    var val = $(".existing_business_button_hide:checked").val();
    if (val == 'True'){
            $('.exiting_business_grant_hide').removeClass('hidden');
        }else{
            $('.exiting_business_grant_hide').addClass('hidden');
        }
    });

//    $(".existing_business").on('click', function(){
//    console.log('--que one ---')
//    var val = $(".existing_business:checked").val();
//    console.log('---------', val)
//    if (val == 'False'){
//            $('.que_two_voucher').removeClass('hidden');
//        }else{
//            $('.que_two_voucher').addClass('hidden');
//        }
//    });
//
//    $(".business_idea").on('click', function(){
//    var val = $(".business_idea:checked").val();
//    if (val == 'False'){
//            $('.que_three_voucher').removeClass('hidden');
//        }else{
//            $('.que_three_voucher').addClass('hidden');
//        }
//    });


});

});

