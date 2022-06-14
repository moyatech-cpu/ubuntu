odoo.define('client_management.form-validate', function (require) {
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
        "You are not on our age group"
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
        $('select[name="district"]').addClass('hidden');
        $('select[name="municipality"]').addClass('hidden');        
        $('label[for="district"]').addClass('hidden');
        $('label[for="municipality"]').addClass('hidden');
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
        $('select[name="metro_municipality"]').removeAttr('required');
        $('label[for="metro_municipality"]').find('span').addClass('hidden');        
//        selectMunicipality.append("<option>", { value: '', selected: true, text: '' });
        _.each(data.municipalities, function(x) {
            var opt = $('<option>').text(x[1])
            .attr('value', x[0]);
        selectMunicipality.append(opt);
        });
    })
});

$("#select_info_type").on('change', function() {
  if ($(this).val() == "training") {
    $('#traning_div').show();
  } else {
    $('#traning_div').val('').hide();
  }
}).change();

$("#enquiry").on('change', function() {
  if ($(this).val() == "other") {
    $('#enquire_div').show();
  } else {
    $('#enquire_div').val('').hide();
  }
}).change();

$.validator.addMethod("alpha", function(value, element) {
    return this.optional(element) || value == value.match(/^[a-zA-Z\s]+$/);
}, "Letters only please");
    $("#youthRegister").validate({
        rules : {
            id_number : {
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

     $("#partnerRegister").validate({
            rules : {
            name1 : {
                alpha : true,

            },
            job_title : {
                alpha : true,

            },
            cellphone : {
                digits : true,

            },
            alterphone : {
                digits : true,

            },
            landline : {
                digits : true,

            }
        }

    });
    });

//    $("#select_info_type").trigger("change");

});
