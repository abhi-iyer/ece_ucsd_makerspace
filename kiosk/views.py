from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    context = {'title':'Main Login'}
    return render(request,'kiosk/index.html',context)

def thanks(request):
    return HttpResponse('Thank You')
