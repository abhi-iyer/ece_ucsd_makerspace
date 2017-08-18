import django.dispatch.Signal

sender = django.dispatch.Signal(providing_args=["alarm_state"])

class AlarmSender(object):

    def send_signal(self, alarm_state):
        sender.send(sender=self.__class__, alarm_state=alarm_state)

    def __init__(self):


