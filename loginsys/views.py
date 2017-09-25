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
def supervisor_info(request):
    if(request.method == "POST"):
        option = request.POST['option']
        data = {'supervisor_update':False}
        if (supervisor_check['checking'] == 'IN'):
          user = supervisor_check['supervisor'].user
          data['status'] = 'OK' 
          data['data'] = user.first_name + " " + user.last_name
          
          if (option == 'YES'):
            log = AdminLog(user=supervisor_check['supervisor'].user, administrator = True, date=timezone.now(), login_status=AdminLog.SUCCESS)
            supervisor_update = 1
            #Add supervisor entry log in supervisor_info database 
          else:
            log = AdminLog(user=supervisor_check['supervisor'].user, administrator = False, date=timezone.now(), login_status=AdminLog.SUCCESS)
          
          settings.kiosk_entry_status = 0 #expecting to be 1 as soon as user enter
          #sending notification to RPi
          print ("Notifying to switch off sensor for %d seconds"% settings.HOLD_TIME)
          turn_off_sensor.send(sender=None,switch_time=settings.HOLD_TIME)
          log.save()

        else :
          user = supervisor_check['supervisor'].user
          data['status'] = 'Exit'
          supervisor_update = 1
          #add supervisor exit log in supervisor_info database
        
        if (supervisor_update == 1):
          #Query supervisor_info database to get last two on duty supervisor(First and last name(to be used in HTML tags))
          #add their names to data'
          data['supervisor_update'] = True
          supervisor_update = 0
          supervisor_check = {'supervisor': None, 'checking': None}
        
        return HttpResponse(json.dumps(data))
          
            
def user_info(request):
    if (request.method == "POST"):
        pid = card_parse(request.POST['pid'])
        print ('pid caught is ', pid);
        if (pid != 0):
            the_user = get_user(pid)
            if the_user != None: # the_user found in database
              if (the_user.currently_suspended != True): # the_user is not suspended
                #Do supervisor log in/log out system management here
                if (the_user.currently_administrator == True):
                  supervisor_info = get_supervisor_status(the_user)
                  if (the_user.supervisor_active == False):
                    supervisor_check['supervisor'] = supervisor_info
                    supervisor_check['checking'] = 'IN'
                    data = {'status':'Admin', 'data':'Do you want to Sign in as a Supervisor ???'} 
                    return HttpResponse(json.dumps(data))
                  else : 
                    supervisor_check['supervisor'] = supervisor_info
                    supervisor_check['checking'] = 'OUT'
                    data = {'status':'Admin', 'data':'Are you exiting (else magically re-entering) ???'} 
                    return HttpResponse(json.dumps(data))
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
              data = {'status':'NOK', 'data':"You're UNAUTHORIZED. Please fulfill the online requirements to get access."}

              log = AdminLog(user = None, error=True, date=timezone.now(), login_status=AdminLog.FAILURE)
              log.save()

              return HttpResponse(json.dumps(data))
        else:
            data = {'status':'NOK', 'data': 'INVALID CARD. Please use an official UC San Diego card.'}

            log = AdminLog(user = None, error=True, date=timezone.now(), login_status=AdminLog.INVALID)
            log.save()

            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Please enter your PID in the appropriate field, not in the URL.')

def kiosk_entry_status(request):
  data = {'status':settings.kiosk_entry_status}
  return HttpResponse(json.dumps(data))
