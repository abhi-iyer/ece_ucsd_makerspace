from kiosk.signals import turn_off_sensor
from django.dispatch import receiver
#from kiosk.sro4_fast_sampling import SensorHandler
import time
#try:
#from kiosk.signal_handler import signal_notifier
#except:
#  from signal_handler import signal_notifier
calib_distance = 0

@receiver(turn_off_sensor)
def control_state(sender, **kwargs):
  for key, value in kwargs.items():
    print ("%s = %s" %(key,value))
  print ("signal received in vmndfkjvndjkfv")
  #sensor_modifier = SensorHandler()
  # print('idle is ', sensor_modifier.instance.idle_distance_first,sep='')
  #sensor_modifier.sleep_alarm(switch_time)

#main_handler = SensorHandler()
#main_handler.start()
