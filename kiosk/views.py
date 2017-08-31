from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

'''
Function in use: 
1) main_kiosk - main entrance kiosk route handler

Function dormant:
1) landing
2) auth
3) tacall
'''

def main_kiosk(request):
  context = {'title':'MainLogin'}
  return render(request,'kiosk/index_semantic.html',context)

def landing(request):
  return render(request,'kiosk/landing.html')

def auth(request):
  return render(request,'kiosk/authorize.html')

def tacall(request):
  return render(request,'kiosk/assistance.html')
