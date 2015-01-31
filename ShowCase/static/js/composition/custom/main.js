$(document).ready(function() {

  $("#pageHr,#pageHrBorder,.middle").click(function() {
        $.scrollTo($(".pagetop"), { duration: 1500});
    });

   // var flag=0;
    //$('#page #zoom').click(function() {
      //  $('#painting').off();
        //    flag=flag+1;
          //  if(flag%2 == 0)
            //  $('#painting').off();
            //else
             // $('#painting').imageLens({ lensSize: 150 });
    //});

 // $('#page #full').click(function() {
   //   $('#painting').fullScreen(true);
    //});

  $("#painting").click(function() {
        $.scrollTo($(".interpret"), { duration: 1500});
    });

  $(".about_art").sticky({topSpacing:50});
  $(".icon-bar, .ham-button").sticky({topSpacing:20});

  var active;
  active = true;
  $('.ham-button').click(function() {
    if (active === true) {
      $('#left-panel').removeClass('closed').addClass('open');
      return active = false;
      $('body').css('background','#FFFFFF');
    } else {
      $('#left-panel').removeClass('open').addClass('closed');
      return active = true;
    }
  });
});