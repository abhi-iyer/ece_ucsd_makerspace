from __future__ import unicode_literals
from django.db import models
from datetime import datetime

class User(models.Model):
        last_name = models.CharField(max_length=20, null=True)
        first_name = models.CharField(max_length=20, null=True)
        pid = models.CharField(max_length=9, null=True)
        employee_num = models.CharField(max_length=20, null=True)
        dept = models.CharField(max_length=20, null=True)
        class_year = models.CharField(max_length=15, null=True)
        administrator = models.BooleanField(default=False)     
        suspended = models.BooleanField(default=False)
        
        def __str__(self):
            return '%s %s' % (self.first_name, self.last_name)

class AdminLog(models.Model):
        last_name = models.CharField(max_length=20, null=True)
        first_name = models.CharField(max_length=20, null=True)
        pid = models.CharField(max_length=9, null=True)
        error = models.BooleanField(default=False)        
        administrator = models.BooleanField(default=False)
        suspended = models.BooleanField(default=False)
        date = models.DateTimeField()
        
        SUCCESS="SUCC"
        FAILURE="FAIL"
        SUSPENDED="SUSP"
        INVALID="INVA"
        
        
        SUCCESS_CHOICES = (
            (SUCCESS, "Success"),
            (FAILURE, "User Not Found in Database"),
            (SUSPENDED, "Access Revoked"),
            (INVALID, "Invalid ID Card"),
        )        

        login_status = models.CharField(
            max_length=4,
            choices=SUCCESS_CHOICES,
            default=SUCCESS,        
        )
        
        def __str__(self):
            if (self.error == False and self.suspended == False):
                if (self.administrator == True):
                    return 'TA %s %s logged in successfully' % (self.first_name, self.last_name)
                else:
                    return 'Student %s %s logged in successfully' % (self.first_name, self.last_name)
            elif (self.suspended == True):
                if (self.administrator == True):
                    return 'Access revoked for TA %s %s' % (self.first_name, self.last_name)
                else:
                    return 'Access revoked for Student %s %s' % (self.first_name, self.last_name)
            elif (self.login_status == "FAIL"):
                return 'User not found in database'
            elif (self.login_status == "INVA"):
                return 'Invalid ID card'
