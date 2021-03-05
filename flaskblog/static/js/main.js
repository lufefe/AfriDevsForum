$(document).ready(function(){
    $('.toggle').click(function(){
//        alert("Clicked");
        $('ul').toggleClass('pull-right');
        $('ul').toggleClass('active');
    })

    $('.ui.accordion').accordion();
    $('#founder').transition('pulse');
    $('.ui.basic.modal').modal('show');

    $("#submail").keyup(function(){

     var email = $("#submail").val();
     var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

     if (!filter.test(email)) {
       //alert('Please provide a valid email address');
       $("#error_email").text(email+" is not a valid email");
       email.focus;
       //return false;
    } else {
        $("#error_email").text("");
    }
    });

     $("#subscribe").click(function(){
        var email = $("#submail").val();
        var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        if (!filter.test(email)) {
           alert('The email address you provide is not valid');
           $("#submail").focus();
           return false;
        } else {

        }
    });


});
/* DARK MODE */
//$(function () {
//  $(document).scroll(function () {
//    var $nav = $(".fixed-top");
//    $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
//
//    if ($nav.hasClass('scrolled')){
//        $('#brand-logo').attr("src",'/static/site_pics/site_logo_1_trans_orange_512.png');
//        $(".media").css("background-color", "blanchedalmond");
//        $("html").css("background-color", "#201f1f");
//        $("body").css("background-color", "#201f1f");
//    }
//    else{
//        $('#brand-logo').attr("src",'/static/site_pics/site_logo_1_trans.png');
//        $(".media").css("background-color", "white");
//         $("html").css("background-color", "#fffafa");
//        $("body").css("background-color", "#fffafa");
//    }
//    //document.getElementById('brand-logo').src='/static/site_pics/site_logo_1_trans_orange_512.png';
//    });
//  });


