$(document).ready(function() {
  $('#ta_call').on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();

    $('.page.dimmer').dimmer('show');
//    $.get('/kiosk/authorize', function(result) {
//      $(document).html(result);
//   });
// another option using AJAX    
//    $.ajax( {
//      type: 'GET',
//      url : '/target',
//      data : {},
//      success : function(content) {
//        $(location).attr('href','authorize');
//      }
//      error: function(content) {
//        $(location).attr('href','unauthorize');
//      }
//      complete: function() {
//        //could do something here as well  
//      }
//    });

// another Option
//    var input = $('input[name=pid]').val();
//    console.log(input)
//    var url = '';
//    $.post (url, {pid: input}, function (data) {
//      console.log(data); 
//      if (data == 'succeess') {
//        $(location).attr('href','kiosk/authorize');
//      } else {
//        $(location).attr('href','kiosk/unauthorize');
//      }
//    });

// ONE OPTION... (i don't want to have static timer)
     //$('#my_div').load('/kiosk/authorize', function(response, status) {
     //$(document).load('/kiosk/authorize', function(response, status) {
     //  setTimeout(function() {
     //   $('.page.dimmer').dimmer('hide');
     //  }, 2000);
     //});

// ANOTHER OPTION... (i am trying to load a new page instead of integrating in the already open page)
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
