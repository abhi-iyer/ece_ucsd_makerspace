from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .helper_functions import *

def index(request):
	context = {'title': 'Main Login'}
	return render(request, 'loginsys/index.html', context)

def student_info(request, pid):
    student = get_student(pid)
    return HttpResponse(student)
