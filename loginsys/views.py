from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

def index(request):
	context = {'title': 'Main Login'}
	return render(request, 'loginsys/index.html', context)

def thanks(request):
	return HttpResponse('Thank You!')

def queryDB(request):
	return HttpResponse('Thank You!')
#def queryDB(pid=Student.objects.get(pid)):
#	with connection.cursor() as cursor:
#		cursor.execute("SELECT * FROM students WHERE pid = '%s'" %pid)
#		row = cursor.fetchone()
#		while row is not None:
#			print(row)	# typically only one row should be printed, as only one person has this unique PID
#			row = cursor.fetchone()
