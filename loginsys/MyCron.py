from django_cron import CronJobBase, Schedule
from django.http import HttpResponse
from .models import Log
from datetime import datetime

def CronJob(CronJobBase):
    RUN_AT_TIMES = [ '23:00' ]

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'loginsys.new_session'  # a unique code

    def do(self):
        num_people = request.session.get('num_people')
	log = Log(datetime.now(), num_people)
	log.save()
	
	del request.session['num_people']

