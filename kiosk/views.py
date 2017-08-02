from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    context = {'title':'Main Login'}
    return render(request,'kiosk/index_semantic.html',context)

def auth(request):
    return HttpResponse('Thank You, Please Enter')

def unauth(request):
    return HttpResponse('Error, DO NOT ENTER')

def tacall(request):
    return HttpResponse('TA on way')
