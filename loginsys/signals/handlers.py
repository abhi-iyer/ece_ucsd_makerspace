from loginsys.signals import turn_off_sensor
from loginsys.signals import disable_entrance_timer
from loginsys.sensors import main_handler
from django.dispatch import receiver
from django.shortcuts import redirect
from loginsys import settings
'''
Usage:
1) Receive a notification from server and communicate it to sensor
functionality to sleep/freeze alarm system for certain time
'''
@receiver(turn_off_sensor)
def control_state(sender, **kwargs):
  for key, value in kwargs.items():
    if key == "switch_time":
      switch_time = int(value)
  print ("signal received in loginsys signal handler")
  main_handler.sleep_alarm(switch_time)

@receiver(disable_entrance_timer)
def get_homepage(sender, **kwargs):
  print ("received signal in get_homepage")
  settings.kiosk_entry_status = 1
