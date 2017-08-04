$(document).ready(function() {
  $('#check_user').on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $('.input_check').addClass('active');
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var input = $('input[name=pid]').val();
    $(this).closest('form').find("input[name=pid], textarea").val("");
    console.log(input);
    $.ajax( {
      type: 'POST',
      url : '/loginsys/student_info',
      data : {
        'pid' : input,
        'csrfmiddlewaretoken':csrftoken,
      },
      success : function(content) {
        console.log(content);
        console.log('success');
        resp = JSON.parse(content);
        console.log(resp);
        console.log(resp['status']);
        if(resp['status'] == 'OK') {
          //data = {status: "OK", data: "First Last"}
          $('#username').text(resp['data']);
          $('.input_check').removeClass('active');
          $('#welcome_page').fadeOut('fast');
          $('#authorized_page').fadeIn('slow');
          setInterval(function() {
            $('#authorized_page').fadeOut('slow');
            $('#welcome_page').fadeIn('slow');
          }, 5000);
        } else {
          if(resp['status'] == 'ERROR') {
            //data = {status: "ERROR", data: "Invalid CARD"}
            $('.alert').text(resp['data']);
          } else { 
            //data = {status: "NE", data: "Unauthorized"}
            $('.alert').text('YOU ARE UNAUTHROIZED, KINDLY GET AUTHORIZATION FIRST');
          }
          $('.input_check').removeClass('active');
          $('.input_err').addClass('active');
          setInterval(function() {
            //$('.alert').fadeOut('slow');
            $('.input_err').removeClass('active');
          }, 5000);
        }
      },
      error: function(content) {
        console.log('failure');
        console.log(content);
      },
      complete: function() {
      }
    });

// another Option
//    var url = '/loginsys/student_info';
//    $.post (url, {'pid': input, 'csrfmiddlewaretoken': csrftoken , }, function (data) {
//      console.log(data); 
//      if (data == 'succeess') {
//        console.log(data);
//        console.log('success');
//        $(document).fadeOut('slow');
//       //$(location).attr('href','kiosk/authorize');
//      } else {
//        console.log(data);
//        console.log('failure');
//        $(document).fadeOut('slow');
//        //$(location).attr('href','kiosk/unauthorize');
//      }
//    });
//
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
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


//    $.ajaxSetup({
//    beforeSend: function(xhr, settings) {
//      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//        xhr.setRequestHeader("X-CSRFToken", csrf_token);
//      }
//    }
//    });
