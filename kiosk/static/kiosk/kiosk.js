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
      return false;
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
        if(resp['status'] == 'STUDENT') {
          
          handle_user_entrance(resp);

        } else if (resp['status'] == 'ADMIN') {
          console.log('Caught in else if');
          $('.text.loader').addClass('disabled');
          $('#welcome_page').css('opacity','0.2');
          $('.alert').text(resp['data']);
          $('#user_option').removeClass('page_hide');
        } else if (resp['status'] == 'HOME') {
          console.log('Caught in else if Home condition');
          $('#welcome_page').css('opacity','1');
          $('#welcome_page').fadeOut('fast');
          $('.alert').empty();
          $('#user_option').addClass('page_hide');
          $('.text.loader').removeClass('disabled');
          $('.page.dimmer').removeClass('active');
          $('#welcome_page').fadeIn('fast');
          $('#pid_field').focus();
          update_supervisor(resp['ta_active']);
        } else {
          console.log('Caught in else');
          $('.text.loader').addClass('disabled');
          $('#welcome_page').css('opacity','0.2');
          $('.alert').text(resp['data']);

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
  $('#opt_yes').on('click',function(event) {
    event.preventDefault();
    event.stopPropagation();
    send_server_supervisor_response('YES');  
    return false;
  });
  $('#opt_no').on('click',function(event) {
    event.preventDefault();
    event.stopPropagation();
    send_server_supervisor_response('NO');  
    return false;
  });
});
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function send_server_supervisor_response(user_opt) {
  console.log(user_opt);
  console.log('at least here');
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  $.ajax( {
    type: 'POST',
    url : '/loginsys/supervisor_info',
    data : { 
      'option' : user_opt,
      'csrfmiddlewaretoken':csrftoken,
    }, 
    success : function (content) {
      console.log('success');
      resp = JSON.parse(content);
      console.log(resp);
      if(resp['status'] == 'STUDENT_IN') {
        handle_user_entrance(resp);
      } else {
        console.log(resp['status']);
        update_supervisor(resp['ta_active']);
        handle_user_entrance(resp);
      }
    },
    error: function(content) {
      console.log('failure');
      console.log(content);
    },
    complete: function() {
    }
  });
}
function update_supervisor(supervisor_name_list) {
  console.log('updating html to show new supervisor');
  $('.supervisor_display').empty();
  if (supervisor_name_list == '') {
    return
  }
  console.log(supervisor_name_list);
  var supervisor_name = supervisor_name_list.split(';');
  $(supervisor_name).each(function(index) {
    console.log(index + ' : ' + supervisor_name[index]);
    var name = supervisor_name[index].split(',');
    name_underscore = name[0] + "_" + name[1];
    name_space = name[0] + " " + name[1];
    $('.supervisor_display').append(
    "<div class='column'><p class='ui ta_font text_midblue' id=''>" +  name_space + "</p><img class='ui centered small image' src =" + dummy_image_url + name_underscore+".jpg /></div>"
    );  
  }); 
}
function handle_user_entrance(resp) {
  console.log(resp['data'])
  var max_time = 15;
  $("#countdown_ctrl").text(max_time);
  $('.page.dimmer').removeClass('active');
  $('#username').text(resp['data']);
  $('#welcome_page').fadeOut('fast');
  $('#authorized_page').removeClass('page_hide');
  var timeleft = max_time;
  var downloadTimer = setInterval(function(){
    $.ajax({
      type: 'GET',
      url : '/loginsys/kiosk_entry_status',
      success : function(content) {
        entry_stts = JSON.parse(content);
        console.log(entry_stts);
        if(entry_stts['status'] == '1') {
          clearInterval(downloadTimer);
          console.log('timer cleared')
          $('#authorized_page').addClass('page_hide');
          $('#welcome_page').fadeIn('slow',function() {
            $('#pid_field').focus();
          });
          $('#username').empty();
        }
      },
      error : function(content) {
      },
      complete : function() {
      }
    });
    timeleft--;
    $("#countdown_ctrl").text(timeleft);
    if(timeleft <= 0) {
      clearInterval(downloadTimer);
      $('#authorized_page').addClass('page_hide');
      $('#welcome_page').css('opacity','1');
      $('#welcome_page').fadeIn('fast',function() {
        $('#pid_field').focus();
      });
      $('#username').empty();
    }
  },1000);
}
