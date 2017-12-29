/*!
 * Start Bootstrap - Grayscale Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */
 // Newsletter popop on click

 function deselect(e) {
   $('.pop').slideFadeToggle(function() {
     e.removeClass('selected');
   });
 }

 $(function() {
   $('#newsletter').on('click', function() {
     if($(this).hasClass('selected')) {
       deselect($(this));
     } else {
       $(this).addClass('selected');
       $('.pop').slideFadeToggle();
     }
     return false;
   });

   $('.close').on('click', function() {
     deselect($('#newsletter'));
     return false;
   });
 });

 $.fn.slideFadeToggle = function(easing, callback) {
   return this.animate({ opacity: 'toggle', height: 'toggle' }, 'fast', easing, callback);
 };



// jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
});

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});
