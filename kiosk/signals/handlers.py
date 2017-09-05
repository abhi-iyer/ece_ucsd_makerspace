from kiosk.signals import turn_off_sensor
from kiosk.signals import disable_entrance_sensor
from kiosk.sensors import main_handler
from django.dispatch import receiver
from django.shortcuts import redirect
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
  #print ("signal received in kiosk signal handler")
  main_handler.sleep_alarm(switch_time)

@receiver(disable_entrance_sensor)
def get_homepage(sender):
  print "received signal in get_homepage"
  return redirect('http://127.0.0.1:8000/')
