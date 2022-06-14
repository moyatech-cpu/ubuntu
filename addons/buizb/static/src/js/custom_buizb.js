(function($) {
 "use strict";

   $(document).ready(function(){

       $(window).scroll(function(){
            if ($(this).scrollTop() > 100) {
                $('.scrollup').fadeIn();
            } else {
                $('.scrollup').fadeOut();
            }
        });

       $('.scrollup').on("click",function(){
            $("html, body").animate({ scrollTop: 0 }, 300);
            return false;
        });

   });
})(jQuery);

jQuery('.scroll-to-top').click(function(){
    $('html, body').animate({scrollTop : 0},500);
    return false;
});

$(window).scroll(function() {
    $edit_mode = document.getElementById('oe_main_menu_navbar');
    if ($(this).scrollTop() > 100){
        if ($edit_mode) {
            $('.navbar.navbar-default.navbar-static-top').removeClass("sticky");
        }
        else{
            $('.navbar.navbar-default.navbar-static-top').addClass("sticky");
        }
    }
    else{
        $('.navbar.navbar-default.navbar-static-top').removeClass("sticky");
  }
});

 //PORTFOLIO FILTER 
$(document).ready(function(){

    $(".filter-button").click(function(){
        var value = $(this).attr('data-filter');
        
        if(value == "all")
        {
            $('.filter').show('1000');
        }
        else
        {
            $(".filter").not('.'+value).hide('3000');
            $('.filter').filter('.'+value).show('3000');
            
        }
    });
    
    if ($(".filter-button").removeClass("active")) {
$(this).removeClass("active");
}
$(this).addClass("active");

});