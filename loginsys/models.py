from __future__ import unicode_literals
from django.db import models
from datetime import datetime

class Student(models.Model):
        last_name = models.CharField(max_length=20, null=True)
        first_name = models.CharField(max_length=20, null=True)
        pid = models.CharField(max_length=9, null=True)
        employee_num = models.CharField(max_length=20, null=True)
        class_org = models.CharField(max_length=20, null=True)
        dept = models.CharField(max_length=20, null=True)
        class_year = models.CharField(max_length=15, null=True)
        suspended = models.BooleanField(default=False)

        def __str__(self):
            return '%s, %s' % (self.last_name, self.first_name)

class AdminInfo(models.Model):
        student = models.ForeignKey(Student)
        printer_train = models.DateTimeField('3D-Printer')
        laser_train = models.DateTimeField('Laser Cutter')

class Log(models.Model):
        # student = models.ForeignKey(Student)
        date = models.DateTimeField('Date')
        users = models.IntegerField('Num of users')

        def create(cls, d, u):
            log = cls(date = d, users=u)    
            return log
        # login = models.DateTimeField('Log Into Lab')
        # logout = models.DateTimeField('Log Out of Lab')

