from kiosk.signals import turn_off_sensor
from django.dispatch import receiver
from kiosk.ultrasound_sensor_control import SensorHandler
import time

main_handler = SensorHandler()

@receiver(turn_off_sensor)
def control_state(sender, **kwargs):
  for key, value in kwargs.items():
    #print ("%s = %s" %(key,value))
    if key == "switch_time":
      switch_time = int(value)
  print ("signal received in kiosk signal handler")
  #print('idle distance first is ',main_handler.instance.idle_distance_first,sep='')
  main_handler.sleep_alarm(switch_time)

main_handler.sensor_benchmark_setup()
main_handler.start_reading()
