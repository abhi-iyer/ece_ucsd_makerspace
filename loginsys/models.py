from __future__ import unicode_literals

from django.db import models

class Student(models.Model):
	pid = models.CharField(max_length=9, null=True)
	employee_num = models.CharField(max_length=20, null=True)
	class_org = models.CharField(max_length=20, null=True)
	dept = models.CharField(max_length=20, null=True)
	class_year = models.CharField(max_length=15, null=True)
	suspended = model.BooleanField(default=False)

class AdminInfo(models.Model):
	student = model.ForeignKey(Student)
	printer_train = models.DateTimeField('3D-Printer')
	laser_train = models.DateTimeField('Laser Cutter')

class Log(models.Model):
	student = model.ForeignKey(Student)
	login = models.DateTimeField('Log Into Lab')
	logout = models.DateTimeField('Log Out of Lab')

