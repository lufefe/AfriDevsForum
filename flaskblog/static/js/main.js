
$(document).ready(function(){
    $('.toggle').click(function(){
//        alert("Clicked");
        $('ul').toggleClass('pull-right');
        $('ul').toggleClass('active');
    })

    $('.ui.accordion').accordion();
    $('#founder')
  .transition('pulse')
;
})
