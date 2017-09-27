from __future__ import unicode_literals
from django.db import models
from datetime import datetime

class User(models.Model):
        last_name = models.CharField(max_length=20, null=True)
        first_name = models.CharField(max_length=20, null=True)
        card_id = models.CharField(max_length=9, null=True)
        current_department = models.CharField(max_length=20, null=True)
        class_year = models.CharField(max_length=15, null=True)
        currently_administrator = models.BooleanField(default=False)
        currently_suspended = models.BooleanField(default=False)
        supervisor_active = models.BooleanField(default=False)
        def __str__(self):
            return '%s %s' % (self.first_name, self.last_name)

class Supervisor_Duty(models.Model):
        user = models.ForeignKey(User, default=None, null=True)
        onduty = models.BooleanField(default=False)
        time = models.DateTimeField()
        
        def __str__(self):
            return 'Supervisor: %s %s Status: %s Time: %s' % (self.user.first_name, self.user.last_name, self.onduty, self.time.strftime("%Y-%m-%d %H:%M:%S"))

class AdminLog(models.Model):
        user = models.ForeignKey(User, default=None, null=True)

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
                    return 'TA %s %s logged in successfully at %s' % (self.user.first_name, self.user.last_name, self.date.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    return 'Student %s %s logged in successfully at %s' % (self.user.first_name, self.user.last_name, self.date.strftime("%Y-%m-%d %H:%M:%S"))
            elif (self.suspended == True):
                if (self.administrator == True):
                    return 'Access revoked for TA %s %s at %s' % (self.user.first_name, self.user.last_name, self.date.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    return 'Access revoked for Student %s %s at %s' % (self.user.first_name, self.user.last_name, self.date.strftime("%Y-%m-%d %H:%M:%S"))
            elif (self.error == True and self.login_status == "FAIL"):
                return 'User not found in database'
            elif (self.error == True and self.login_status == "INVA"):
                return 'Invalid ID card'
