
$(document).ready(function() {

  $('#submit-login').on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();

    $('.page.dimmer').dimmer('show');

    setTimeout(function() {
      $('#my_div').load('/kiosk/authorize');
      $('.page.dimmer').dimmer('hide');
    }, 2000);

    return false;
  });

});