from .models import *
from datetime import datetime
from django.utils import timezone
import string

def get_user(pid):
    try:
        user = User.objects.get(pid=pid)
        return user
    except:
        return None #No entry

def card_parse(input):
    if input:
        if ( input[0] == ';' ):
            # magnetic-strip card swiper's rules
            user_pid = input[2:11]
            return user_pid
        elif (input[0] == 'A' or input[0] == 'a'):
            l = list(input)
            l[0] = '9'
            user_pid = "".join(l)             
            return user_pid
        else:
            return 0
    else:
        return 0

def get_logs(date):
    try:
        log = AdminLog.objects.get(date=date)
        return log
    except:
        return None # no logs for specified day
        

