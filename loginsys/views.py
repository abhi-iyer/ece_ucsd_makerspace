from django.shortcuts import render
from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
from .helper_functions import *
import json
import time

def index(request):
    context = {'title': 'Main Login'}
    return render(request, 'loginsys/index.html', context)

def student_info(request):
    if (request.method == "POST"):
        pid = card_parse(request.POST['pid'])
        print ('pid caught is ', pid);
        time.sleep(3)
        if (pid != 0):
            student = get_student(pid)
            if student != 'NE' :
              data = {'status':'OK', 'data':student}

              num_people = request.session.get('num_people', 0)
              request.session['num_people'] = num_people+1

              return HttpResponse(json.dumps(data))
            else:
              data = {'status':'NE', 'data':''}
              return HttpResponse(json.dumps(data))
        else:
            data = {'status':'ERROR', 'data': 'Invalid card. Please use an official Student ID card issued by UC San Diego.'}
            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Please enter your PID in the appropriate field, not in the URL.')
