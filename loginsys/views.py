from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .helper_functions import *

def index(request):
	context = {'title': 'Main Login'}
	return render(request, 'loginsys/index.html', context)

def student_info(request):
    if (request.method == "POST"):
        pid = card_parse(request.POST['pid'])
        if (pid != 0):
            student = get_student(pid)
            return HttpResponse(student)
        else:
            return HttpResponse("Invalid card. Please use an official Student ID card issued by UC San Diego.")
    else:
        return HttpResponse("Please enter your PID in the appropriate field, not in the URL.")
