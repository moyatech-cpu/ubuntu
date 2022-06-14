/*
* ----------------------------------------------------------------------------------------
Author       : Onepageboss
Template Name: GETX Onepage Business Template
Version      : 1.0

   ____                   _____                             ____     ____     _____    _____ 
  / __ \                 |  __ \                           |  _ \   / __ \   / ____|  / ____|
 | |  | |  _ __     ___  | |__) |   __ _    __ _    ___    | |_) | | |  | | | (___   | (___  
 | |  | | | '_ \   / _ \ |  ___/   / _` |  / _` |  / _ \   |  _ <  | |  | |  \___ \   \___ \ 
 | |__| | | | | | |  __/ | |      | (_| | | (_| | |  __/   | |_) | | |__| |  ____) |  ____) |
  \____/  |_| |_|  \___| |_|       \__,_|  \__, |  \___|   |____/   \____/  |_____/  |_____/ 
                                            __/ |                                            
                                           |___/                                             
* ----------------------------------------------------------------------------------------
*/

(function ($) {
    'use strict';

    jQuery(document).ready(function () {

        /*
         * ----------------------------------------------------------------------------------------
         *  PRELOADER JS
         * ----------------------------------------------------------------------------------------
         */
        $(window).on('load',function () {
            $('.preloader').fadeOut();
            $('.preloader-area').delay(350).fadeOut('slow');

            $('.work .work-posts').isotope({
                itemSelector: '.col-md-4'
            });

            // init Isotope
            var $container = $('.work-posts').isotope({
                itemSelector: '.item'
            });
            // filter functions
            var filterFns = {
                // show if number is greater than 50
                numberGreaterThan50: function () {
                    var number = $(this).find('.number').text();
                    return parseInt(number, 10) > 50;
                },
                // show if name ends with -ium
                ium: function () {
                    var name = $(this).find('.name').text();
                    return name.match(/ium$/);
                }
            };
        });

        /*
         * ----------------------------------------------------------------------------------------
         *  STICKY JS
         * ----------------------------------------------------------------------------------------
         */
        // $(".header-top-area").sticky({
        //     topSpacing: 0,
        // });


        /*
         * ----------------------------------------------------------------------------------------
         *  SMOTH SCROOL JS
         * ----------------------------------------------------------------------------------------
         */

        // $('a.smoth-scroll').on("click", function (e) {
        //     var anchor = $(this);
        //     $('html, body').stop().animate({
        //         scrollTop: $(anchor.attr('href')).offset().top - 50
        //     }, 1000);
        //     e.preventDefault();
        // });


        /*
         * ----------------------------------------------------------------------------------------
         *  WORK JS
         * ----------------------------------------------------------------------------------------
         */




        /*
         * ----------------------------------------------------------------------------------------
         *  MAGNIFIC POPUP JS
         * ----------------------------------------------------------------------------------------
         */

        // $('.video-play').magnificPopup({
        //     type: 'inline'
        // });

        // $('.work-popup').magnificPopup({
        //     type: 'image',
        //     gallery: {
        //         enabled: true
        //     }

        // });

        // $('.video-play').magnificPopup({
        //   items: {
        //       src: '<div class="white-popup"><iframe width="100%" height="100%" src="//www.youtube.com/embed/XAmZeH-VNL0" frameborder="0" allowfullscreen></iframe></div>',
        //       type: 'inline'
        //   },
        //   closeBtnInside: true
        // });

        /*
         * ----------------------------------------------------------------------------------------
         *  PARALLAX JS
         * ----------------------------------------------------------------------------------------
         */

        $(window).stellar({
            responsive: true,
            positionProperty: 'position',
            horizontalScrolling: false
        });

        /*
         * ----------------------------------------------------------------------------------------
         *  COUNTER UP JS
         * ----------------------------------------------------------------------------------------
         */

        $('.counter-num').counterUp();


        /*
         * ----------------------------------------------------------------------------------------
         *  TESTIMONIAL JS
         * ----------------------------------------------------------------------------------------
         */

        $(".testimonial-list").owlCarousel({
            items: 1,
            autoPlay: true,
            navigation: false,
            itemsDesktop: [1199, 1],
            itemsDesktopSmall: [980, 1],
            itemsTablet: [768, 1],
            itemsTabletSmall: false,
            itemsMobile: [479, 1],
            pagination: true,
            autoHeight: true,
        });

        $(".team-list").owlCarousel({
            items: 4,
            autoPlay: true,
            navigation: false,
            itemsDesktop: [1199, 1],
            itemsDesktopSmall: [980, 2],
            itemsTablet: [768, 2],
            itemsTabletSmall: false,
            itemsMobile: [479, 1],
            autoHeight: true,
            pagination: true,
        });

        /*
         * ----------------------------------------------------------------------------------------
         *  GOOGLE MAP JS
         * ----------------------------------------------------------------------------------------
         */
        var contact = {
            "lat": "-37.7622470161679",
            "lon": "145.06004333496094"
        }; //Change a map coordinate here!
        try {
            $('.map').gmap3({
                action: 'addMarker',
                latLng: [contact.lat, contact.lon],
                map: {
                    center: [contact.lat, contact.lon],
                    zoom: 5
                },
            }, {
                action: 'setOptions',
                args: [{
                    scrollwheel: false
						}]
            });
        } catch (err) {

        }

        /*
         * ----------------------------------------------------------------------------------------
         *  EXTRA JS
         * ----------------------------------------------------------------------------------------
         */
        // $(document).on('click', '.navbar-collapse.in', function (e) {
        //     if ($(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle') {
        //         $(this).collapse('hide');
        //     }
        // });
        // $('body').scrollspy({
        //     target: '.navbar-collapse',
        //     offset: 195
        // });

        
        new WOW().init();
    });

})(jQuery);