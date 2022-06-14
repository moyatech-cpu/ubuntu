odoo.define('thusano_fund.form-validate', function (require) {
'use strict';

var ajax = require('web.ajax');

$(document).ready(function() {
    function calyear(dt1,dt2){
        var diff =(dt2.getTime() - dt1.getTime()) / 1000;
        diff /= (60 * 60 * 24);
        if((diff/365.25)>35){
            return 36
        }
        else{
//        return Math.abs(Math.round(diff/365.25));
            return (diff/365.25);
        }
    }
    $.validator.addMethod(
        "australianDate",
        function(value, element) {
            if(parseInt(value.substring(0, 2))<50){

                if(calyear(new Date('20'+value.substring(0, 2)+'/'+value.substring(2, 4)+'/'+(parseInt(value.substring(4, 6)))),new Date())>=14 && calyear(new Date('20'+value.substring(0, 2)+'/'+value.substring(2, 4)+'/'+value.substring(4, 6)),new Date())<36)
                {
                    return true;
                }
                else{
                    return false;
                }
            }
            else{
                if(calyear(new Date('19'+value.substring(0, 2)+'/'+value.substring(2, 4)+'/'+value.substring(4, 6)),new Date())>14 && calyear(new Date('19'+value.substring(0, 2)+'/'+value.substring(2, 4)+'/'+value.substring(4, 6)),new Date())<36)
                {
                    return true;
                }
                else{
                    return false;
                }
            }
        },
        " "
    );
//    $.validator.methods.email = function( value, element ) {
//  return this.optional( element ) || /[a-z]+@[a-z]+\.[a-z]+/.test( value );
//}

$('select[name="province"]').on('change', function() {
    ajax.jsonRpc("/get_districts/" + $("select[name='province']").val(), 'call').then(
    function(data) {

        var selectDistricts = $('select[name="district"]');
        selectDistricts.children('option:not(:first)').remove();
//        selectDistricts.append("<option>", { value: '', selected: true });
        _.each(data.districts, function(x) {
            var opt = $('<option>').text(x[1])
            .attr('value', x[0]);
        selectDistricts.append(opt);
        });
          var selectMunicipality = $('select[name="metro_municipality"]');
        selectMunicipality.children('option:not(:first)').remove();
        $('#metro_municipality_div').addClass('hidden');
        if(data.metro_municipality.length > 0){
            $('#metro_municipality_div').removeClass('hidden');


//        selectDistricts.append("<option>", { value: '', selected: true });
        _.each(data.metro_municipality, function(x) {
            var opt = $('<option>').text(x[1])
            .attr('value', x[0]);
        selectMunicipality.append(opt);
        });
        }
        var selectBranch = $('select[name="near_branch"]');
        selectBranch.children('option:not(:first)').remove();
        if(data.branches.length > 0){
            _.each(data.branches, function(x) {
                var opt = $('<option>').text(x[1])
                .attr('value', x[0]);
                selectBranch.append(opt);
            });
        }

    })
});

$('select[name="metro_municipality"]').on('change', function(event) {
    var current_value = $(event.currentTarget).val();
    if(current_value) {
        $('select[name="metro_municipality"]').attr('required','required');
        $('label[for="metro_municipality"]').find('span').removeClass('hidden');
        $('select[name="district"]').removeAttr('required');
        $('select[name="municipality"]').removeAttr('required');
        $('label[for="district"]').find('span').addClass('hidden');
        $('label[for="municipality"]').find('span').addClass('hidden');
    } else{
        $('select[name="metro_municipality"]').removeAttr('required');
        $('label[for="metro_municipality"]').find('span').addClass('hidden');
        $('select[name="district"]').prop('required',true);
        $('select[name="municipality"]').prop('required',true);
        $('label[for="district"]').find('span').removeClass('hidden');
        $('label[for="municipality"]').find('span').removeClass('hidden');
    }
});

//$('input[name="email"]').on('change', function(ev) {
//    var sEmail = $(ev.currentTarget).val();
//    var filter = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
//    if (filter.test(sEmail)) {
//        $('label[id="email-error"]').addClass("hidden");;
//    }
//    else {
//        $('label[id="email-error"]').removeClass('hidden');
//}
//});

$('select[name="district"]').on('change', function() {
    ajax.jsonRpc("/get_municipality/" + $("select[name='district']").val(), 'call').then(
    function(data) {
        var selectMunicipality = $('select[name="municipality"]');
        selectMunicipality.children('option:not(:first)').remove();
//        selectMunicipality.append("<option>", { value: '', selected: true, text: '' });
        _.each(data.municipalities, function(x) {
            var opt = $('<option>').text(x[1])
            .attr('value', x[0]);
        selectMunicipality.append(opt);
        });
    })
});


$("#gross_income").keypress(function() {
 
 return event.charCode >= 48 && event.charCode <= 57
 
});

$("#second_parent_id_number").keypress(function() {
 
 return event.charCode >= 48 && event.charCode <= 57
 
});

$("#parent_id_number").keypress(function() {
 
 return event.charCode >= 48 && event.charCode <= 57
 
});



$("#employment_status").on('change', function() {
  if ($(this).val() == "employed"|| $(this).val() =="other") {
    $('#position_div').show();
    $('#sector_div').show();
  } else {
    $('#position_div').val('').hide();
    $('#sector_div').val('').hide();
  }
}).change();

$("#emp_sect").on('change', function() {

  if($("#emp_sect").val() == "government"){
				alert("Please Note: Only non Government Employees Can Apply!");
				return false;
        	}
}).change();

$("#user_type").on('change', function() {
  if ($(this).val() == "ngo") {
    $('#ngo_div').show();
  } else {
    $('#ngo_div').val('').hide();
  }
}).change();

$("#has_sponsor").on('change', function() {
  if ($(this).val() == "True") {
    $('#sponsor_div').show();
  } else {
    $('#sponsor_div').val('').hide();
  }
}).change();

$.validator.addMethod("alpha", function(value, element) {
    return this.optional(element) || value == value.match(/^[a-zA-Z\s]+$/);
}, "Letters only please");
    $("#regForm").validate({
        rules : {
            id_number : {
            
            	digits : true,
                required: true,
                australianDate : true,
                minlength: 13,
                maxlength: 13,
            },
            
            second_parent_id_number:{
            	digits : true,
                australianDate : true,
                minlength: 13,
                maxlength: 13,
            
            },
            parent_id_number :{
            
            	digits : true,
            	required: true,
                australianDate : true,
                minlength: 13,
                maxlength: 13,
            
            },
             cellphone : {
                digits : true,

            },
            alterphone : {
                digits : true,

            },
        }
    });

     $("#regForm").validate({
            rules : {
            surname : {
                alpha : true,

            },
            cellphone : {
                digits : true,

            },
            alterphone : {
                digits : true,

            }
        }

    });
    });


});
