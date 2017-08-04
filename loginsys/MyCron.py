from django_cron import CronJobBase, Schedule
from django.http import HttpResponse

def CronJob(CronJobBase):
    RUN_AT_TIMES = [ '23:00' ]

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'loginsys.reset_system'  # a unique code

    def do(self):
        num_people = request.session.get('num_people')


