
$(document).ready(function() {

  $('#submit-login').on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();

    $('.page.dimmer').dimmer('show');

// ONE OPTION...
    // $('#my_div').load('/kiosk/authorize', function(response, status) {
    //   setTimeout(function() {
    //    $('.page.dimmer').dimmer('hide');
    //   }, 2000);
    // });

// ANOTHER OPTION...
    // $.get('/kiosk/authorize', function(result) {
    //   $('#my_div').html(result);
    //   // $('#my_div').text(result);
    //   $('.page.dimmer').dimmer('hide');
    // }).fail(function() {
    //   // handle error
    // }).done(function() {
    //   // execute some more code
    // }).always(function() {
    //   // log that get was executed
    // });

    return false;
  });

});