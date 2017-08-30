$(document).ready(function() {
  console.log( "ready!" );
  $('#pid_field').focus(function() {
    console.log(".focus called")
  });
  $('#check_user').on('click', function(event) {
    console.log('caught check_user')
    event.preventDefault();
    event.stopPropagation();
    $('#input_null').empty();
    var input = $('input[name=pid]').val();
    $(this).closest('form').find("input[name=pid], textarea").val("");
    console.log(input);
    if(!input) {
      $('#input_null').text("Fill out this field");
      return false;
    } else {
      $('#input_null').empty();
    }
    $('.page.dimmer').addClass('active');
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax( {
      type: 'POST',
      url : '/loginsys/user_info',
      data : {
        'pid' : input,
        'csrfmiddlewaretoken':csrftoken,
      },
      success : function(content) {
        console.log('success');
        resp = JSON.parse(content);
        console.log(resp);
        if(resp['status'] == 'OK') {
          //data = {status: "OK", data: "First Last"}
          $('.page.dimmer').removeClass('active');
          $('#username').text(resp['data']);
          $('#welcome_page').fadeOut('fast');
          $('#authorized_page').removeClass('page_hide');
          setTimeout(function() {
            $('#authorized_page').addClass('page_hide');
            $('#welcome_page').fadeIn('slow',function() {
              $('#pid_field').focus();
            });
            $('#username').empty();
          },5000);
        } else {
          $('.text.loader').addClass('disabled');
          if(resp['status'] == 'ERROR') {
            //data = {status: "ERROR", data: "Invalid CARD"}
            $('.alert').text(resp['data']);
          } else if (resp['status'] == 'NOK') {
            $('.alert').text(resp['data']);
          } else { 
            //data = {status: "NE", data: "Unauthorized"}
            $('.alert').text('YOU ARE UNAUTHORIZED. PLEASE COMPLETE THE ONLINE TUTORIALS TO GET ACCESS.');
          }
          setTimeout(function() {
            $('.alert').empty();
            $('.text.loader').removeClass('disabled');
            $('.page.dimmer').removeClass('active');
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

    return false;
  });
  
  $('#ta_call').on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $('#welcome_page').fadeOut('fast');
    $('#ta_page').removeClass('page_hide');
    setTimeout(function() {
      $('#ta_page').addClass('page_hide');
      //$.when($('#ta_page').fadeOut('fast')).done(function() {
      $('#welcome_page').fadeIn('slow',function() {
        $('#pid_field').focus();
      });
      //});
    }, 5000);
    return false;
  });
});
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
// another Option
//    var url = '/loginsys/user_info';
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



//    $.ajaxSetup({
//    beforeSend: function(xhr, settings) {
//      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//        xhr.setRequestHeader("X-CSRFToken", csrf_token);
//      }
//    }
//    });
