from django.db import models

# Create your models here.

class Student(models.Model):
    pid = models.CharField(max_length=10, null=True)
    employee_id = models.CharField(max_length=10, null=True)
    user_role = models.CharField(max_length=10, null=True)
    dept = models.CharField(max_length=10, null=True)
    class_lvl = models.CharField(max_length=10, null=True)
    suspended = models.BooleanField(default = False)
    newsletter = models.BooleanField(default = False)

class Training_dates(models.Model):
    student = models.ForeignKey(Student,unique=True)
    tr_1 = models.DateTimeField('laser_cut')
    tr_2 = models.DateTimeField('3d-print')
    tr_3 = models.DateTimeField('solder')
