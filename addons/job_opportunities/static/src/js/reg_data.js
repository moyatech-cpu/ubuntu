odoo.define("job_opportunities.reg_data", function (require){
    "use strict";

    var base = require('web_editor.base');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var qweb = core.qweb;
    var session = require('web.session');

$(document).ready(function(){

        console.log("Page Loaded !!");
        var mcounter = 1
        var thcounter = 1
        var twecounter = 1

        $("#add_matric").click(function(){
            mcounter += 1
            console.log('Add matric clicked', mcounter);
            var cols = '';

            cols += '<div class="col-md-12 col-sm-12" id="matric'+ mcounter +'"><div class="col-md-3 col-sm-3">';
            cols += '<div class="form-group "><input class="form-control" id="subject'+ mcounter +'" name="subject'+ mcounter +'" placeholder="Subject" type="text" required="required"/></div></div>';
            cols += '<div class="col-md-3 col-sm-3"><div class="form-group "><select class="select form-control" id="level'+ mcounter +'" name="level'+ mcounter +'" required="required"><option value="level_one">Level 1: 0 - 30%</option><option value="level_two">Level 2: 30 - 40%</option><option value="level_three">Level 3: 40 - 50%</option><option value="level_four">Level 4: 50 - 60%</option><option value="level_five">Level 5: 60 - 70%</option><option value="level_six">Level 6: 70 - 80%</option><option value="level_seven">Level 7: 80 - 100%</option></select></div></div>';
            cols += '<div class="col-md-3 col-sm-3"><div class="form-group "><input class="form-control" id="symbol'+ mcounter +'" name="symbol'+ mcounter +'" placeholder="Symbol"type="text" required="required"/></div></div>';
            cols += '<div class="col-md-3 col-sm-3"><div class="form-group "><input class="form-control" id="attachment_matric'+ mcounter +'" name="attachment_matric'+ mcounter +'" placeholder="Attachment" type="file"/></div></div></div>';

            $("#matric").after(cols);
            $("#total_matric").val(mcounter);
        });

        $("#add_thedu").click(function(){
            thcounter += 1
            console.log('Add counter clicked', thcounter);
            var cols = '';

            cols += '<div class="row"><div class="col-md-12 col-sm-12"><div class="col-md-6 col-sm-6"><div class="form-group "><label class="control-label requiredField" for="teritory_name">Name<span class="asteriskField">*</span></label>';
            cols += '<input class="form-control" id="teritory_name'+ thcounter +'" name="teritory_name'+ thcounter +'" placeholder="Name" type="text" required="required"/></div></div>';
            cols += '<div class="col-md-6 col-sm-6"><div class="form-group "><label class="control-label requiredField" for="major_subjects">Major Subjects<span class="asteriskField">*</span></label>';
            cols += '<input class="form-control" id="major_subjects'+ thcounter +'" name="major_subjects'+ thcounter +'" placeholder="Major Subjects" type="text" required="required"/></div></div></div></div>';
            cols += '<div class="row"><div class="col-md-12 col-sm-12"><div class="col-md-6 col-sm-6"><div class="form-group "><label class="control-label requiredField" for="year_completed_date">Teritory Year Completed<span class="asteriskField">*</span></label>';
            cols += '<input id="year_completed_date'+ thcounter +'" type="date" name="year_completed_date'+ thcounter +'" class="form-control" required="required"/></div></div>';
            cols += '<div class="col-md-6 col-sm-6"><div class="form-group "><label class="control-label requiredField" for="major_subjects">Qualification Obtained<span class="asteriskField">*</span></label>';
            cols += '<input class="form-control" id="qualification'+ thcounter +'" name="qualification'+ thcounter +'" placeholder="Qualification Obtained" type="text" required="required"/></div></div></div></div>';
            cols += '<div class="row"><div class="col-md-12 col-sm-12"><div class="col-md-6 col-sm-6"><div class="form-group "><label class="control-label requiredField" for="major_subjects">Attachment<span class="asteriskField">*</span></label>';
            cols += '<input class="form-control" id="attachment'+ thcounter +'" name="attachment'+ thcounter +'" placeholder="Attachment" type="file" required="required"/></div></div></div></div>';

            $("#th_data").after(cols);
            $("#total_thedu").val(thcounter);
        });

        $("#add_work").click(function(){
            twecounter += 1
            console.log('Add counter clicked', twecounter);
            var cols = '';

            cols += '<div class="row"><div class="col-md-6 col-sm-6"><div class="form-group "><label class="control-label" for="organisation_name">Name of organisation</label>';
            cols += '<input class="form-control" id="organisation_name'+ twecounter +'" name="organisation_name'+ twecounter +'" placeholder="Organisation Name" type="text"/></div></div>';
            cols += '<div class="col-md-6 col-sm-6"><div class="form-group"><label class="control-label" for="org_start_date">Start Date</label>';
            cols += '<input id="org_start_date'+ twecounter +'" type="date" name="org_start_date'+ twecounter +'" class="form-control"/></div></div>';
            cols += '<div class="col-md-6 col-sm-6"><div class="form-group"><label class="control-label" for="org_end_date">End Date</label>';
            cols += '<input id="org_end_date'+ twecounter +'" type="date" name="org_end_date'+ twecounter +'" class="form-control"/></div></div>';
            cols += '<div class="col-md-6 col-sm-6"><div class="form-group "><label class="control-label" for="pos_held">Position Held</label><select class="select form-control" id="pos_held'+ twecounter +'" name="pos_held'+ twecounter +'"><option value="">Please Select Position</option>';
            cols += '<t t-foreach="job" t-as="pos"><option t-att-value="pos.id'+ twecounter +'"><t t-esc="pos.name"/></option></t></select></div></div>';
            cols += '<div class="col-md-6 col-sm-6"><div class="form-group"><label class="control-label" for="reason_for_leaving">Reason for Leaving</label>';
            cols += '<textarea class="form-control" cols="40" id="reason_for_leaving'+ twecounter +'" name="reason_for_leaving'+ twecounter +'" placeholder="Please Enter Reason for Leaving" rows="4"></textarea></div></div></div>';

            $("#work_exp").after(cols);
            $("#total_work_exp").val(twecounter);
        });

        $(document).on('change', '#matric_certi', function(ev){
            ev.preventDefault();
            var is_matric = $("#matric_certi").val();
            if (is_matric == 'yes') {
               $('#matric_data').removeClass('d-none');
               return false;
            }else if (is_matric == 'no') {
               $('#matric_data').addClass('d-none');
               return false;
            }
        });

        $(document).on('change', '#ter_high_edu', function(ev){
            ev.preventDefault();
            var is_edu = $("#ter_high_edu").val();
            if (is_edu == 'yes') {
               $('#ter_high_data').removeClass('d-none');
               return false;
            }else if (is_edu == 'no') {
               $('#ter_high_data').addClass('d-none');
               return false;
            }
        });

    });
});
