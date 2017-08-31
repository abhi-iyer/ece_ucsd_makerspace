from kiosk.signals import turn_off_sensor
from kiosk.sensors import main_handler
from django.dispatch import receiver
#from kiosk.ultrasound_sensor_control import SensorHandler

#main_handler = SensorHandler()
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

#main_handler.sensor_benchmark_setup()
#main_handler.start_reading()
