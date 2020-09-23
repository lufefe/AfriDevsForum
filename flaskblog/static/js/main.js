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
    }
    else{
        document.getElementById('brand-logo').src='/static/site_pics/site_logo_1_trans.png';
    }
    //document.getElementById('brand-logo').src='/static/site_pics/site_logo_1_trans_orange_512.png';
    });
  });


