import RPi.GPIO as GPIO
import time
import numpy as np
from datetime import datetime
GPIO.setmode(GPIO.BCM)
RATIO = 0.8
TRIG_first = 12
ECHO_first = 16

TRIG_second = 23
ECHO_second = 24

GPIO.setup(TRIG_first,GPIO.OUT)
GPIO.setup(ECHO_first,GPIO.IN)
GPIO.setup(TRIG_second,GPIO.OUT)
GPIO.setup(ECHO_second,GPIO.IN)

GPIO.output(TRIG_first, False)
GPIO.output(TRIG_second, False)
time.sleep(2)

def uh_control(control, TRIG, ECHO, idle_distance):
  if control == 0:
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    if (distance < RATIO*idle_distance):
      return 1

    return 0
  if control == 1:
    GPIO.output(TRIG, False)

def entrance_clear(TRIG,ECHO,idle_distance):
  while True:
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    if (distance < RATIO*idle_distance):
      print(">>>>>>>>PLEASE GET OUT<<<<<<<<<<<<")
      time.sleep(0.3)
    else:
      return

def reject_outliers(data):
  m = 2
  u = np.mean(data)
  s = np.std(data)
  filtered = [e for e  in data if (u - 3*s < e < u + 3*s)]
  return filtered

def uh_setup(TRIG, ECHO):
  x = []
  counter = 0
  while counter<30 :
    print(counter, "for pin ",ECHO)
    time.sleep(0.3)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()
    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    idle_distance = pulse_duration * 17150
    idle_distance = round(idle_distance, 2)
    if idle_distance > 2000:
        continue
    x.append(idle_distance)
    counter += 1

  x_mod = reject_outliers(x) #remove junk data from reading
  average_dist = np.mean(x_mod)
  return average_dist

  if control == 1:
    GPIO.output(TRIG, False)


if __name__ == "__main__" :

    try:
        idle_distance_first = uh_setup(TRIG_first, ECHO_first)
        idle_distance_second = uh_setup(TRIG_second, ECHO_second)
        primary_last_status = 0
        secondary_last_status = 0
        while (True):
            status_first = uh_control(0, TRIG_first, ECHO_first, idle_distance_first)
            status_second = uh_control(0, TRIG_second, ECHO_second, idle_distance_second)
            if((status_first and status_second) or (status_second and primary_last_status)) :
              print("Intruder detected!")
              time.sleep(3)
              entrance_clear(TRIG_first,ECHO_first,idle_distance_first)
              primary_last_status = 0
              secondary_last_status = 0
            elif(status_first and secondary_last_status):
              print("User exited")
              time.sleep(3)
              entrance_clear(TRIG_first,ECHO_first,idle_distance_first)
              primary_last_status = 0
              secondary_last_status = 0
            else:
              primary_last_status = status_first
              secondary_last_status = status_second
            time.sleep(0.3)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
