from __future__ import unicode_literals
from django.db import models
from datetime import datetime

class Student(models.Model):
        last_name = models.CharField(max_length=20, null=True)
        first_name = models.CharField(max_length=20, null=True)
        pid = models.CharField(max_length=9, null=True)
        employee_num = models.CharField(max_length=20, null=True)
        dept = models.CharField(max_length=20, null=True)
        class_year = models.CharField(max_length=15, null=True)
        suspended = models.BooleanField(default=False)

        def __str__(self):
            return '%s, %s' % (self.last_name, self.first_name)

class AdminInfo(models.Model):
        student = models.ForeignKey(Student)
        printer_train = models.DateTimeField('3D-Printer')
        laser_train = models.DateTimeField('Laser Cutter')

class AdminLog(models.Model):
        # student = models.ForeignKey(Student)
        last_name = models.CharField(max_length=20, null=True)
        first_name = models.CharField(max_length=20, null=True)
        pid = models.CharField(max_length=9, null=True)
        error = models.BooleanField(default=False)        
 
        date = models.DateTimeField()
        
        SUCCESS="SUCC"
        FAILURE="FAIL"
        SUSPENDED="SUSP"
        INVALID="INVA"
        
        
        SUCCESS_CHOICES = (
            (SUCCESS, "Success"),
            (FAILURE, "Student Not Found in Database"),
            (SUSPENDED, "Access Revoked"),
            (INVALID, "Invalid ID Card"),
        )        

        login_status = models.CharField(
            max_length=4,
            choices=SUCCESS_CHOICES,
            default=SUCCESS,        
        )
        
        def __str__(self):
            if (self.error != True):
                return "Success for %s, %s" % (self.last_name, self.first_name)
            elif (self.login_status == "FAIL"):
                return "Student Not Found in Database"
            elif (self.login_status == "SUSP"):
                return "Access Revoked for %s, %s" % (self.last_name, self.first_name)
            elif (self.login_status == "INVA"):
                return "Invalid ID Card"
       # def create(cls, student, date, success):
        #    log = cls(student_id=student, date=date, success=success)    
         #   return log
