$(document).ready(function() {
  console.log( "ready!" );
  $('#pid_field').focus();
  $('#check_user').on('click', function(event) {
    console.log('caught check_user')
    event.preventDefault();
    event.stopPropagation();
    //$('#input_null').empty();
    var input = $('input[name=pid]').val();
    $(this).closest('form').find("input[name=pid], textarea").val("");
    console.log(input);
    if(!input) {
      $('#pid_field').focus();
      //$('#input_null').text("Fill out this field");
      return false;
    } else {
      //$('#input_null').empty();
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
          $('#username').text(resp['data']);
          $('#welcome_page').fadeOut('fast');
          $('.page.dimmer').removeClass('active');
          $('#authorized_page').removeClass('page_hide');
          var timeleft = 10;
          var downloadTimer = setInterval(function(){
            timeleft--;
            $("#countdowntimer").text(timeleft);
            if(timeleft <= 0) {
              clearInterval(downloadTimer);
              $("#countdowntimer").text('10');
            }
          },1000);
          setTimeout(function() {
            $('#authorized_page').addClass('page_hide');
            $('#welcome_page').fadeIn('slow',function() {
              $('#pid_field').focus();
            });
            $('#username').empty();
          },10000);
        } else {
          $('.text.loader').addClass('disabled');
          $('#welcome_page').css('opacity','0.2');
          if(resp['status'] == 'ERROR') {
            $('.alert').text(resp['data']);
          } else if (resp['status'] == 'NOK') {
            $('.alert').text(resp['data']);
          } else { 
            $('.alert').text("You're UNAUTHORIZED. Please fulfill the online requirements to get access.");
          }
          setTimeout(function() {
            $('#welcome_page').css('opacity','1');
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
      $('#welcome_page').fadeIn('slow',function() {
        $('#pid_field').focus();
      });
    }, 5000);
    return false;
  });
});
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
