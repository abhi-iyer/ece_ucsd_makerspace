from django.shortcuts import render
from django.http import HttpResponse
from .helper_functions import *
import json
import time
from datetime import datetime
from .models import *
from django.utils import timezone
from loginsys.signals import turn_off_sensor
from loginsys import settings

def index(request):
    context = {'title': 'Main Login'}
    return render(request, 'loginsys/index.html', context)

def user_info(request):
    if (request.method == "POST"):
        pid = card_parse(request.POST['pid'])
        print ('pid caught is ', pid);
        if (pid != 0):
            the_user = get_user(pid)
            if the_user != None: # the_user found in database
              if (the_user.currently_suspended != True): # the_user is not suspended
                data = {'status':'OK', 'data':the_user.first_name + " " + the_user.last_name}

                log = AdminLog(user=the_user, administrator = the_user.currently_administrator, date=timezone.now(), login_status=AdminLog.SUCCESS)
                log.save()
                settings.kiosk_entry_status = 0 #expecting to be 1 as soon as user enter
                #sending notification to RPi
                print ("Notifying to switch off sensor for %d seconds"% settings.HOLD_TIME)
                turn_off_sensor.send(sender=None,switch_time=settings.HOLD_TIME)

                return HttpResponse(json.dumps(data))
              else:  # the_user is suspended
                data = {'status':'NOK', 'data':the_user.first_name + " " + the_user.last_name + " is suspended"}

                log = AdminLog(user=the_user, suspended=the_user.currently_suspended, administrator = the_user.currently_administrator, date=timezone.now(), login_status=AdminLog.SUSPENDED)
                log.save()

                return HttpResponse(json.dumps(data))

            else: # the_user not found in data base
              data = {'status':'NE', 'data':''}

              log = AdminLog(user = None, error=True, date=timezone.now(), login_status=AdminLog.FAILURE)
              log.save()

              return HttpResponse(json.dumps(data))
        else:
            data = {'status':'ERROR', 'data': 'INVALID CARD. Please use an official UC San Diego card.'}

            log = AdminLog(user = None, error=True, date=timezone.now(), login_status=AdminLog.INVALID)
            log.save()

            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Please enter your PID in the appropriate field, not in the URL.')

def kiosk_entry_status(request):
  data = {'status':settings.kiosk_entry_status}
  return HttpResponse(json.dumps(data))
