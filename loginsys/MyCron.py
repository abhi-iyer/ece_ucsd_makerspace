fom django_cron import CronJobBase, Schedule
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from .models import AdminLog
from datetime import datetime

class MyCronJob(CronJobBase):
    # RUN_AT_TIMES = [ '23:00' ]

    # schedule = Schedule(run_at_times=RUN_AT_TIMES)
    
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    code = 'loginsys.new_session'  # a unique code

    def do(self):
        session = SessionStore()
        num_people = Session.objects.get('num_people')
        log = Log(datetime.now(), num_people)
        log.save()
        
        session["num_people"] = 0

