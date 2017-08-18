from django.core.signals import request_finished
from django.dispatch import receiver
from sender import AlarmSender

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")

signal.connect(my_callback, sender = AlarmSender )
