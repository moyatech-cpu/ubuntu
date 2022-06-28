odoo.define('nyda_grant_and_voucher.pre-assessment', function (require) {
'use strict';

    $(document).ready(function(){
        $(".radio-button").on('click', function(){
            var val = $(".radio-button:checked").val();
            if (val == 'yes'){
                $('.board_member_hide').removeClass('hidden');
            }else{
                $('.board_member_hide').addClass('hidden');
            }
        });
    });

    $(document).ready(function(){
    $(".radio-button1").on('click', function() {
        var val = $(".radio-button1:checked").val();
        if (val == "yes") {
        $('.board_member_hide1').removeClass('hidden');
        $('.board_member_hide1_12').addClass('hidden');
        }
        else {
        $('.board_member_hide1').addClass('hidden');
        $('.board_member_hide1_12').removeClass('hidden');
    }
    });
    });

    $(document).ready(function(){
    $(".radio-button2").on('click', function() {
        var val = $(".radio-button2:checked").val();
        if (val == "yes") {
        $('.board_member_hide2').removeClass('hidden');
        }
        else {
        $('.board_member_hide2').addClass('hidden');
    }
    });
    });

    $(document).ready(function(){
    $(".radio-button3").on('click', function() {
        var val = $(".radio-button3:checked").val();
        if (val == "no") {
        $('.board_member_hide3').removeClass('hidden');
        }
        else {
        $('.board_member_hide3').addClass('hidden');
    }
    });
    });

    $(document).ready(function(){
    $(".radio-button4").on('click', function() {
        var val = $(".radio-button4:checked").val();
        if (val == "yes") {
        $('.board_member_hide4').removeClass('hidden');
        }
        else {
        $('.board_member_hide4').addClass('hidden');
    }
    });
    });

    $(document).ready(function(){
    $(".radio-button5").on('click', function() {
        var val = $(".radio-button5:checked").val();
        if (val == "yes") {
        $('.board_member_hide5').removeClass('hidden');
        }
        else {
        $('.board_member_hide5').addClass('hidden');
    }
    });
    });

    $(document).ready(function(){
    $(".radio-button6").on('click', function() {
        var val = $(".radio-button6:checked").val();
        if (val == "yes") {
        $('.board_member_hide6').removeClass('hidden');
        }
        else {
        $('.board_member_hide6').addClass('hidden');
    }
    });

    $(".radio-button9").on('click', function() {
        var val = $(".radio-button9:checked").val();
        if (val == "yes") {
        $('.reg_num_div').removeClass('hidden');
        }
        else {
        $('.reg_num_div').addClass('hidden');
    }
    });


    $("input[name='business_plan']").on('change', function(ev) {
        var val = $(ev.currentTarget).val();
        if (val == "yes") {
            $('.business_plan_doc').removeClass('hidden');
        }
        else {
            $('.business_plan_doc').addClass('hidden');
        }
    });

    $("input[name='Entrepreneurship_training']").on('change', function(ev) {
        var val = $(ev.currentTarget).val();
        if (val == "yes") {
            $('.supporting_docs_info').removeClass('hidden');
			$('#nextBtn').removeClass('hidden');
        }
        else {
            $('.supporting_docs_info').addClass('hidden');
        }
        if (val == "no"){
            $('.received_entrepreneurship').removeClass('hidden');
			$('#nextBtn').addClass('hidden');
        }
        else {
            $('.received_entrepreneurship').addClass('hidden');
        }
    });
    var counter = 0;
    if($('#assessment_supporting_docs')){
            $("#adddocrow").on("click", function () {
                var newRow = $("<tr>");
                var cols = "";

                cols += '<td><input type="file" class="form-control" required="required" name="supportingdoc'+ counter + '"/></td>';

                cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
                newRow.append(cols);
                $("table#assessment_supporting_docs.order-list").append(newRow);
                counter++;
            });
        }
    });

    $(document).ready(function(){
    $(".radio-button7").on('click', function() {
        var val = $(".radio-button7:checked").val();
        var val1 = $(".radio-button8:checked").val();
        if (val == "yes") {
        $('.board_member_hide7').removeClass('hidden');
        document.getElementById("radio11").disabled = true;
        $('.board_member_hide8').addClass('hidden');
        }
        else {
        $('.board_member_hide7').addClass('hidden');
        document.getElementById("radio11").disabled = false;
    }
    });

    $(".radio-button8").on('click', function() {
        var val2 = $(".radio-button7:checked").val();
        var val3 = $(".radio-button8:checked").val();
        if (val3 == "yes") {
            $('.board_member_hide8').removeClass('hidden');
            }
        else {
           $('.board_member_hide8').addClass('hidden');
        }
        if (val3 == "no"){
        $('.board_member_hide7').removeClass('hidden');
            }
        else {
           $('.board_member_hide7').addClass('hidden');
        }
    });

    $("#only_number").keypress(function (e) {
     //if the letter is not digit then display error and don't type anything
         if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            //display error message
            $("#errmsg").html("Digits Only").show().fadeOut("slow");
                   return false;
        }
   });

   $("#child_number").keypress(function (e) {
     //if the letter is not digit then display error and don't type anything
         if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            //display error message
            $("#errmsg").html("Digits Only").show().fadeOut("slow");
                   return false;
        }
   });

   $("#child_supporting").keypress(function (e) {
     //if the letter is not digit then display error and don't type anything
         if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            //display error message
            $("#errmsg").html("Digits Only").show().fadeOut("slow");
                   return false;
        }
   });

   $("#turnover_business").keypress(function (e) {
     //if the letter is not digit then display error and don't type anything
         if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            //display error message
            $("#errmsg").html("Digits Only").show().fadeOut("slow");
                   return false;
        }
   });

   $( "input[name*='stock']").keypress(function (e) {
     //if the letter is not digit then display error and don't type anything
         if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
            //display error message
            $("#errmsg").html("Digits Only").show().fadeOut("slow");
                   return false;
        }
   });

    });




});