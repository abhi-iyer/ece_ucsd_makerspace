from django.shortcuts import render
from django.http import HttpResponse
from .helper_functions import *
import json
import time
from datetime import datetime
from .models import *
from django.utils import timezone
from kiosk.signals import turn_off_sensor
#from kiosk.sro4_fast_sampling import SensorHandler
#from  kiosk import sro4_fast_sampling
def index(request):
    context = {'title': 'Main Login'}
    return render(request, 'loginsys/index.html', context)

def user_info(request):
    if (request.method == "POST"):
        pid = card_parse(request.POST['pid'])
        print ('pid caught is ', pid);
        #time.sleep(3)
        if (pid != 0):
            the_user = get_user(pid)
            if the_user != None: # the_user found in database
              if (the_user.currently_suspended != True): # the_user is not suspended
                data = {'status':'OK', 'data':the_user.first_name + " " + the_user.last_name}

                log = AdminLog(user=the_user, administrator = the_user.currently_administrator, date=timezone.now(), login_status=AdminLog.SUCCESS)
                log.save()
                #sending notification to RPi
                #test = sro4_fast_sampling.SensorHandler()
                #print ("idle_distance is ",test.instance.idle_distance_first,sep='')
                hold_time = 10 #circuit disable time in seconds
                print ("Notifying to switch off sensor for 10 seconds")
                turn_off_sensor.send(sender=None,switch_time=hold_time)

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
            data = {'status':'ERROR', 'data': 'Invalid card. Please use an official Student ID card issued by UC San Diego.'}

            log = AdminLog(user = None, error=True, date=timezone.now(), login_status=AdminLog.INVALID)
            log.save()

            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Please enter your PID in the appropriate field, not in the URL.')
