import RPi.GPIO as GPIO
import time
import numpy as np
from datetime import datetime
from subprocess import call
from threading import Timer
from collections import deque
print ("Function calling check")
from django.dispatch import receiver
try:
  from kiosk.signal_handler import signal_notifier
except:
  from signal_handler import signal_notifier

@receiver(signal_notifier)
def control_state(sender, **kwargs):
  for key, value in kwargs.items():
    print ("%s = %s" % (key, value))
    if key == "switch_time":
      switch_time = int(value)
  print ("signal received in sound_sensor function")
  sensor_modifier = SensorHandler()
  print('idle is ', sensor_modifier.instance.idle_distance_first,sep='')
  sensor_modifier.sleep_alarm(switch_time)

class SensorHandler:
  class __MyOnlySensorHandler:
    def __init__(self):
      self.alarm_state = 1
      self.threshold_ratio = 0.85
      self.sample_rate = 0.05
      self.trig_first = 12
      self.echo_first = 16
      self.trig_second = 23
      self.echo_second = 24
      self.idle_distance_first = None
      self.idle_distance_second = None

  instance = None
  def __init__(self):
    if not SensorHandler.instance:
      SensorHandler.instance = SensorHandler.__MyOnlySensorHandler()

  def sleep_alarm(self,halt_time):
    print("Previous value " + str(self.instance.alarm_state))
    self.instance.alarm_state = 0
    print("Value after call " + str(self.instance.alarm_state))
    print ("switch_time is ",halt_time,sep='')
    t = Timer(halt_time, self.set_alarm)
    t.start()

  def set_alarm(self):
    print('alarm_state is ', self.instance.alarm_state,sep='')
    self.instance.alarm_state = 1

  def call_alarm(self):
    print('alarm_state is ', self.instance.alarm_state,sep='')
    if self.instance.alarm_state == 1:
      print ("called the alarm function; yipeee")
      #call(["omxplayer", "--vol", "-1200", "-o", "local", "justwhat.mp3"])
    else :
      print ("Speaker turned off")

  def uh_control(self, TRIG, ECHO, idle_distance):
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
    if (distance < self.instance.threshold_ratio*idle_distance):
      print ("Pin: ",ECHO, ":",round(distance/idle_distance,2),sep="")
      return 1

    return 0

  def entrance_clear(self):
    while True:
      GPIO.output(self.instance.trig_first, True)
      time.sleep(0.00001)
      GPIO.output(self.instance.trig_first, False)

      while GPIO.input(self.instance.echo_first)==0:
        pulse_start = time.time()

      while GPIO.input(self.instance.echo_first)==1:
        pulse_end = time.time()

      pulse_duration = pulse_end - pulse_start
      distance = pulse_duration * 17150
      distance = round(distance, 2)
      if (distance < self.instance.threshold_ratio*self.instance.idle_distance_first):
        print (">>>>>>>>PLEASE GET OUT<<<<<<<<<<<<",sep="")
        time.sleep(1)
        continue
      else:
        print ("entrance_clear Pin: ",self.instance.echo_first, ":",round(distance/self.instance.idle_distance_first,2),sep="")

      GPIO.output(self.instance.trig_second, True)
      time.sleep(0.00001)
      GPIO.output(self.instance.trig_second, False)

      while GPIO.input(self.instance.echo_second)==0:
        pulse_start = time.time()

      while GPIO.input(self.instance.echo_second)==1:
        pulse_end = time.time()

      pulse_duration = pulse_end - pulse_start
      distance = pulse_duration * 17150
      distance = round(distance, 2)
      if (distance < self.instance.threshold_ratio*self.instance.idle_distance_second):
        print (">>>>>>>>PLEASE GET OUT<<<<<<<<<<<<",sep="")
        time.sleep(1)
        continue
      else:
        print ("entrance_clear Pin: ",self.instance.echo_second, ":",round(distance/self.instance.idle_distance_second,2),sep="")

      break

    return

  def reject_outliers(self,data):
    m = 2
    u = np.mean(data)
    s = np.std(data)
    filtered = [e for e  in data if (u - 3*s < e < u + 3*s)]
    return filtered

  def uh_setup(self,TRIG, ECHO):
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

    x_mod = self.reject_outliers(x) #remove junk data from reading
    average_dist = np.mean(x_mod)
    print ("\nPin: ",ECHO," idle_distance is set as ",average_dist,sep="")
    print ("\nPin: ",ECHO," threshold_distance is set as ", self.instance.threshold_ratio*average_dist,sep="")
    return average_dist

  def alarm_sound(self):
    call(["omxplayer",'--vol','-1200',"-o","local","justwhat.mp3"])

  def start(self):
    print ("SETUP BEGIN from start function")
    sensor_control = SensorHandler()
    print ('echo ', sensor_control.instance.trig_first, sep='')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor_control.instance.trig_first, GPIO.OUT)
    GPIO.setup(sensor_control.instance.echo_first, GPIO.IN)
    GPIO.setup(sensor_control.instance.trig_second, GPIO.OUT)
    GPIO.setup(sensor_control.instance.echo_second, GPIO.IN)

    GPIO.output(sensor_control.instance.trig_first, False)
    GPIO.output(sensor_control.instance.trig_second, False)
    print ("Waiting For Sensor To Settle")
    time.sleep(2)
    print ("Distance Measurement In Progress")

    sensor_first_past = [0]*10
    sensor_second_past = [0]*10
    sensor_last_active = 0
    print ("setting up sensor 1\n")
    sensor_control.instance.idle_distance_first = sensor_control.uh_setup(sensor_control.instance.trig_first, sensor_control.instance.echo_first)
    print ("setting up sensor 2\n")
    sensor_control.instance.idle_distance_second = sensor_control.uh_setup(sensor_control.instance.trig_second, sensor_control.instance.echo_second)
    print ('setup done')
    print ('idle_distnce_first ', sensor_control.instance.idle_distance_first, sep='')
    while (True):
      #print "----------------------------------------------------------------------"
      status_first = sensor_control.uh_control(sensor_control.instance.trig_first, sensor_control.instance.echo_first, sensor_control.instance.idle_distance_first)
      sensor_first_past = np.roll(sensor_first_past,1)
      sensor_first_past[0] = status_first
      time.sleep(sensor_control.instance.sample_rate)
      status_second = sensor_control.uh_control(sensor_control.instance.trig_second, sensor_control.instance.echo_second, sensor_control.instance.idle_distance_second)
      sensor_second_past = np.roll(sensor_second_past,1)
      sensor_second_past[0] = status_second
      #print ("\t\tfirst:second::", status_first,":",status_second,sep="")

      if(status_first and (sensor_last_active!=1)) :
        sensor_last_active = 1
        sensor_second_sum = sum(sensor_second_past)
        if (sensor_second_sum >= 2) :
          print (">>>>>>>>>>>>>>>>>>>>>Student ExiteD<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
          sensor_first_past = [0]*10
          sensor_second_past = [0]*10
          sensor_last_active = 0
          time.sleep(3)
          sensor_control.entrance_clear()
      elif(status_second and (sensor_last_active!=2)):
        sensor_last_active = 2
        sensor_first_sum = sum(sensor_first_past)
        if (sensor_first_sum >= 2) :
          print (">>>>>>>>>>>>>>>>>>>>>INTRUDER DETECTED<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
          sensor_control.call_alarm()
          sensor_first_past = [0]*10
          sensor_second_past = [0]*10
          sensor_last_active = 0
          time.sleep(3)
          sensor_control.entrance_clear()
      else:
        pass

      time.sleep(sensor_control.instance.sample_rate)

if __name__ == "__main__" :
  try:
    print ("SETUP BEGIN")
    sensor_control = SensorHandler()
    print ('echo ', sensor_control.instance.trig_first, sep='')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor_control.instance.trig_first, GPIO.OUT)
    GPIO.setup(sensor_control.instance.echo_first, GPIO.IN)
    GPIO.setup(sensor_control.instance.trig_second, GPIO.OUT)
    GPIO.setup(sensor_control.instance.echo_second, GPIO.IN)

    GPIO.output(sensor_control.instance.trig_first, False)
    GPIO.output(sensor_control.instance.trig_second, False)
    print ("Waiting For Sensor To Settle")
    time.sleep(2)
    print ("Distance Measurement In Progress")

    sensor_first_past = [0]*10
    sensor_second_past = [0]*10
    sensor_last_active = 0
    print ("setting up sensor 1\n")
    sensor_control.instance.idle_distance_first = sensor_control.uh_setup(sensor_control.instance.trig_first, sensor_control.instance.echo_first)
    print ("setting up sensor 2\n")
    sensor_control.instance.idle_distance_second = sensor_control.uh_setup(sensor_control.instance.trig_second, sensor_control.instance.echo_second)
    print ('setup done')
    print ('dile_diatnce_first ', sensor_control.instance.idle_distance_first, sep='')
    while (True):
      #print "----------------------------------------------------------------------"
      status_first = sensor_control.uh_control(sensor_control.instance.trig_first, sensor_control.instance.echo_first, sensor_control.instance.idle_distance_first)
      sensor_first_past = np.roll(sensor_first_past,1)
      sensor_first_past[0] = status_first
      time.sleep(sensor_control.instance.sample_rate)
      status_second = sensor_control.uh_control(sensor_control.instance.trig_second, sensor_control.instance.echo_second, sensor_control.instance.idle_distance_second)
      sensor_second_past = np.roll(sensor_second_past,1)
      sensor_second_past[0] = status_second
      #print ("\t\tfirst:second::", status_first,":",status_second,sep="")

      if(status_first and (sensor_last_active!=1)) :
        sensor_last_active = 1
        sensor_second_sum = sum(sensor_second_past)
        if (sensor_second_sum >= 2) :
          print (">>>>>>>>>>>>>>>>>>>>>Student ExiteD<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
          sensor_first_past = [0]*10
          sensor_second_past = [0]*10
          sensor_last_active = 0
          time.sleep(3)
          sensor_control.entrance_clear()
      elif(status_second and (sensor_last_active!=2)):
        sensor_last_active = 2
        sensor_first_sum = sum(sensor_first_past)
        if (sensor_first_sum >= 2) :
          print (">>>>>>>>>>>>>>>>>>>>>INTRUDER DETECTED<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
          sensor_control.call_alarm()
          sensor_first_past = [0]*10
          sensor_second_past = [0]*10
          sensor_last_active = 0
          time.sleep(3)
          sensor_control.entrance_clear()
      else:
        pass

      time.sleep(sensor_control.instance.sample_rate)

  except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
