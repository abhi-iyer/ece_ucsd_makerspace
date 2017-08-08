from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    context = {'title':'MainLogin'}
    return render(request,'kiosk/index_semantic.html',context)

def landing(request):
    return render(request,'kiosk/landing.html')

def auth(request):
    return render(request,'kiosk/authorize.html')

def tacall(request):
    return render(request,'kiosk/assistance.html')
