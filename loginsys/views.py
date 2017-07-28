from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
	context = {'title': 'Main Login'}
	return render(request, 'loginsys/index.html', context)

def thanks(request):
	return HttpResponse('Thank You!')
