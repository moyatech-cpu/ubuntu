odoo.define('market_linkage.products-services', function (require) {
'use strict';

$(document).ready(function() {
    $(".numericOnly").keypress(function (e) {
        if (String.fromCharCode(e.keyCode).match(/[^0-9]/g)) return false;
    });




//    $(".submit_btn").click(function(e){
//      var target = e.target;
//      var $el = $(target);
//      $el.parent().parent().find('.custom-column-content').find('.alert-success').show()
//      console.log("el",$el)
//      console.log("el-p",$el.parent())
//      console.log("el-p-p",$el.parent().parent())
//    });
});

});

