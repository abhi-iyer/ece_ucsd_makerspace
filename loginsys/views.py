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
        #this could be yes or no to the question asked when supervisor swipe in
        print ('option received is ',option)
        #In this method we are checking admin has logged in as student or supervisor
        user = settings.supervisor_check.user
        data = {'data':user.first_name + " " + user.last_name}
        
        if (option == 'YES'):
          data['status'] = 'ADMIN_IN' 
          #Supervisor entering
          #Abhi: set supervisor_active in User as True
          #log supervisor entry in Supervisor_Duty table
          log = AdminLog(user=user, administrator = True, date=timezone.now(), login_status=AdminLog.SUCCESS)
          #Abhi: create a new function (eg. get_active_supervisor) (see sample below) this function will be called bcoz active TA's just changed
          #data = get_active_supervisor()
        else:
          data['status'] = 'STUDENT_IN' 
          #supervisor entering as student
          #Nothign to add here
          log = AdminLog(user=user, administrator = False, date=timezone.now(), login_status=AdminLog.SUCCESS)
          
        log.save()
        settings.kiosk_entry_status = 0 #expecting to be 1 as soon as user enter
        #sending notification to RPi
        print ("Notifying to switch off sensor for %d seconds"% settings.HOLD_TIME)
        turn_off_sensor.send(sender=None,switch_time=settings.HOLD_TIME)

        settings.supervisor_check = None
        return HttpResponse(json.dumps(data))
          
            
def user_info(request):
    if (request.method == "POST"):
        pid = card_parse(request.POST['pid'])
        print ('pid caught is ', pid);
        if (pid != 0):
            the_user = get_user(pid)
            if the_user != None: # the_user found in database
              if (the_user.currently_suspended != True): # the_user is not suspended
                #supervisor log in/log out system management here
                if (the_user.currently_administrator == True):
                  supervisor_info = get_supervisor_status(the_user)
                  if (the_user.supervisor_active == False):
                    #supervisor entering(might be as a student)
                    settings.supervisor_check = supervisor_info
                    data = {'status':'ADMIN', 'data':'Do you want to Sign in as a Supervisor ???'} 
                    return HttpResponse(json.dumps(data))
                  else :
                    #Supervisor exiting 
                    the_user.supervisor_active = False
                    #also log supervisor exit in Supervisor_Duty table
                    data = {'status':'HOME'}
                    #Abhi: create a new function (eg. get_active_supervisor) (see sample below) this function will be called bcoz active TA's just changed
                    #data = get_active_supervisor()
                    return HttpResponse(json.dumps(data))

                data = {'status':'STUDENT', 'data':the_user.first_name + " " + the_user.last_name}
                log = AdminLog(user=the_user, administrator = the_user.currently_administrator, date=timezone.now(), login_status=AdminLog.SUCCESS)
                log.save()
                settings.kiosk_entry_status = 0 #expecting to be 1 as soon as user enter
                #sending notification to RPi
                print ("Notifying to switch off sensor for %d seconds"% settings.HOLD_TIME)
                turn_off_sensor.send(sender=None,switch_time=settings.HOLD_TIME)

                return HttpResponse(json.dumps(data))
              else:  # the_user is suspended
                data = {'status':'INV', 'data':the_user.first_name + " " + the_user.last_name + " is suspended"}

                log = AdminLog(user=the_user, suspended=the_user.currently_suspended, administrator = the_user.currently_administrator, date=timezone.now(), login_status=AdminLog.SUSPENDED)
                log.save()

                return HttpResponse(json.dumps(data))

            else: # the_user not found in data base
              data = {'status':'INV', 'data':"You're UNAUTHORIZED. Please fulfill the online requirements to get access."}

              log = AdminLog(user = None, error=True, date=timezone.now(), login_status=AdminLog.FAILURE)
              log.save()

              return HttpResponse(json.dumps(data))
        else:
            data = {'status':'INV', 'data': 'INVALID CARD. Please use an official UC San Diego card.'}

            log = AdminLog(user = None, error=True, date=timezone.now(), login_status=AdminLog.INVALID)
            log.save()

            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Please enter your PID in the appropriate field, not in the URL.')

def kiosk_entry_status(request):
  data = {'status':settings.kiosk_entry_status}
  return HttpResponse(json.dumps(data))

def get_active_supervisor():
  #Abhi return a dictionary containing ta active names;
  #You will get data by quering User database and checking for supervisor_active as True
  #sample_data = {ta_active:'first_name,last_name;first_name,last_name'}
  #return sample_data
  pass
