import RPi.GPIO as GPIO
import time
import numpy as np
from datetime import datetime
from subprocess import call
from threading import Timer
from collections import deque

GPIO.setmode(GPIO.BCM)
RATIO = 0.90
SAMPLE_RATE = 0.05
TRIG_first = 12
ECHO_first = 16

TRIG_second = 23
ECHO_second = 24


alarm_state = 1

GPIO.setup(TRIG_first,GPIO.OUT)
GPIO.setup(ECHO_first,GPIO.IN)
GPIO.setup(TRIG_second,GPIO.OUT)
GPIO.setup(ECHO_second,GPIO.IN)

GPIO.output(TRIG_first, False)
GPIO.output(TRIG_second, False)
print ("Waiting For Sensor To Settle")
time.sleep(2)

print ("Distance Measurement In Progress")

def sleep_alarm():
  global alarm_state
  print("Previous value " + str(alarm_state))
  alarm_state = 0
  print("Value after call " + str(alarm_state))
  #t = Timer(10, set_alarm)
  #t.start()
  time.sleep(10)
  set_alarm()

def set_alarm():
  global alarm_state
  alarm_state = 1

def call_alarm():
  global alarm_state
  if alarm_state == 1:
    call(["omxplayer", "--vol", "-1200", "-o", "local", "justwhat.mp3"])

def uh_control(control, TRIG, ECHO, idle_distance):
  if control == 0:
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    try:
      pulse_duration = pulse_end - pulse_start
    except:
      print ("ERROR: Either pulse_end or pulse_end is not defined")
      return 0
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    #print "pin: ", ECHO, " distance: ",distance
    #print (ECHO,":", distance,":",round(distance/idle_distance,2),sep="")
    if (distance < RATIO*idle_distance):
      print ("Pin: ",ECHO, ":",round(distance/idle_distance,2),sep="")
      return 1

    return 0
  if control == 1:
    GPIO.output(TRIG, False)

def entrance_clear(TRIG_1,ECHO_1,idle_distance_1, TRIG_2,ECHO_2, idle_distance_2):
  while True:
    GPIO.output(TRIG_1, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_1, False)

    while GPIO.input(ECHO_1)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO_1)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    if (distance < RATIO*idle_distance_1):
      print (">>>>>>>>PLEASE GET OUT<<<<<<<<<<<<",sep="")
      time.sleep(1)
      continue
    else:
      print ("entrance_clear Pin: ",ECHO_1, ":",round(distance/idle_distance_1,2),sep="")

    GPIO.output(TRIG_2, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_2, False)

    while GPIO.input(ECHO_2)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO_2)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    if (distance < RATIO*idle_distance_2):
      print (">>>>>>>>PLEASE GET OUT<<<<<<<<<<<<",sep="")
      time.sleep(1)
      continue
    else:
      print ("entrance_clear Pin: ",ECHO_2, ":",round(distance/idle_distance_2,2),sep="")

    break
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
    #print counter, "for pin ",ECHO
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
    #print idle_distance
    if idle_distance > 2000:
        continue
    x.append(idle_distance)
    counter += 1

  x_mod = reject_outliers(x) #remove junk data from reading
  #print "x-size : ",len(x), "x_mod-size : ",len(x_mod)
  #if (len(x) != len(x_mod)):
    #for data in x:
      #print data,
    #print "\n"
    #for data in x_mod:
      #print data,
  average_dist = np.mean(x_mod)
  print ("\nPin: ",ECHO," idle_distance is set as ",average_dist,sep="")
  print ("\nPin: ",ECHO," threshold_distance is set as ", RATIO*average_dist,sep="")
  return average_dist

  if control == 1:
    GPIO.output(TRIG, False)

def alarm_sound():
  call(["omxplayer",'--vol','-1200',"-o","local","justwhat.mp3"])

if __name__ == "__main__" :
    sensor_first_past = [0,0,0,0,0,0,0,0,0,0]
    sensor_second_past = [0,0,0,0,0,0,0,0,0,0]
    sensor_last_active = 0
    try:
        print ("setting up sensor 1\n")
        idle_distance_first = uh_setup(TRIG_first, ECHO_first)
        print ("setting up sensor 2\n")
        idle_distance_second = uh_setup(TRIG_second, ECHO_second)
        print ('setup done')
        while (True):
            #print "----------------------------------------------------------------------"
            status_first = uh_control(0, TRIG_first, ECHO_first, idle_distance_first)
            sensor_first_past = np.roll(sensor_first_past,1)
            sensor_first_past[0] = status_first
            time.sleep(SAMPLE_RATE)
            status_second = uh_control(0, TRIG_second, ECHO_second, idle_distance_second)
            sensor_second_past = np.roll(sensor_second_past,1)
            sensor_second_past[0] = status_second
            print ("\t\tfirst:second::", status_first,":",status_second,sep="")

            if(status_first and (sensor_last_active!=1)) :
              sensor_last_active = 1
              sensor_second_sum = sum(sensor_second_past)
              #sensor_first_sum = sum(sensor_first_past)
              if (sensor_second_sum >= 2) :
                print (">>>>>>>>>>>>>>>>>>>>>Student ExiteD<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                sensor_first_past = [0,0,0,0,0,0,0,0,0,0]
                sensor_second_past = [0,0,0,0,0,0,0,0,0,0]
                sensor_last_active = 0
                time.sleep(3)
                entrance_clear(TRIG_first,ECHO_first,idle_distance_first, TRIG_second,ECHO_second,idle_distance_second)
            elif(status_second and (sensor_last_active!=2)):
              sensor_last_active = 2
              sensor_first_sum = sum(sensor_first_past)
              if (sensor_first_sum >= 2) :
                print (">>>>>>>>>>>>>>>>>>>>>INTRUDER DETECTED<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                #call_alarm()
                sensor_first_past = [0,0,0,0,0,0,0,0,0,0]
                sensor_second_past = [0,0,0,0,0,0,0,0,0,0]
                sensor_last_active = 0
                time.sleep(3)
                entrance_clear(TRIG_first,ECHO_first,idle_distance_first, TRIG_second,ECHO_second,idle_distance_second)
            else:
              pass

            time.sleep(SAMPLE_RATE)
            #time.sleep(0.3) #works (~2-3 signals caught while intruding; some erroneous reading)
            #time.sleep(0.1) #kinda work(~5-7 signals caught; but false readings as well like standing close but not in the direct line)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
