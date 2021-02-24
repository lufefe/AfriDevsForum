$(document).ready(function(){
    $('.toggle').click(function(){
//        alert("Clicked");
        $('ul').toggleClass('pull-right');
        $('ul').toggleClass('active');
    })

    $('.ui.accordion').accordion();
    $('#founder').transition('pulse');
})

$(function () {
  $(document).scroll(function () {
    var $nav = $(".fixed-top");
    $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());

    if ($nav.hasClass('scrolled')){
        document.getElementById('brand-logo').src='/static/site_pics/site_logo_1_trans_orange_512.png';
        $(".media").css("background-color", "blanchedalmond");
        $("html").css("background-color", "#201f1f");
        $("body").css("background-color", "#201f1f");
    }
    else{
        document.getElementById('brand-logo').src='/static/site_pics/site_logo_1_trans.png';
        $(".media").css("background-color", "white");
         $("html").css("background-color", "#fffafa");
        $("body").css("background-color", "#fffafa");
    }
    //document.getElementById('brand-logo').src='/static/site_pics/site_logo_1_trans_orange_512.png';
    });
  });


