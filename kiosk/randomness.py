from django.dispatch import receiver
import time
try:
  from kiosk.signal_handler import signal_notifier
except:
  from signal_handler import signal_notifier

@receiver(signal_notifier)
def control_state(sender, **kwargs):
  for key, value in kwargs.items():
    print ("%s = %s" %(key,value))
  print ("signal received in randomness")

if __name__ == "__main__":
  i=0
  while True:
    print ('i is ',i)
    i+=1
    time.sleep(5)
