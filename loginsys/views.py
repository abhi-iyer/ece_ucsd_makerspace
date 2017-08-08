from django.shortcuts import render
from django.http import HttpResponse
from .helper_functions import *
import json
import time
from datetime import datetime
from .models import *
from django.utils import timezone

def index(request):
    context = {'title': 'Main Login'}
    return render(request, 'loginsys/index.html', context)

def user_info(request):
    if (request.method == "POST"):
        pid = card_parse(request.POST['pid'])
        print ('pid caught is ', pid);
        time.sleep(3)
        if (pid != 0):
            user = get_user(pid)
            if user != None: # user found in database
              
              if (user.suspended == False): # user is not suspended
                data = {'status':'OK', 'data':user.first_name + " " + user.last_name}                
 
                log = AdminLog(administrator = user.administrator, last_name=user.last_name, first_name=user.first_name, pid=user.pid, date=timezone.now(), login_status=AdminLog.SUCCESS)
                log.save()     
  
                return HttpResponse(json.dumps(data))
              else:  # user is suspended
                data = {'status':'NOK', 'data':user.first_name + " " + user.last_name + " is suspended"}
                
                log = AdminLog(error=True, administrator = user.administrator, last_name=user.last_name, first_name=user.first_name, pid=user.pid, date=timezone.now(), login_status=AdminLog.SUSPENDED)
                log.save()
                
                return HttpResponse(json.dumps(data))                

            else: # user not found in data base
              data = {'status':'NE', 'data':''}
              
              log = AdminLog(error=True, date=timezone.now(), login_status=AdminLog.FAILURE)
              log.save()
            
              return HttpResponse(json.dumps(data))
        else:
            data = {'status':'ERROR', 'data': 'Invalid card. Please use an official Student ID card issued by UC San Diego.'}
            
            log = AdminLog(error=True, date=timezone.now(), login_status=AdminLog.INVALID)
            log.save()
            
            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Please enter your PID in the appropriate field, not in the URL.')
