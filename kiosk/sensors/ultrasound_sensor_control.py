import RPi.GPIO as GPIO
import time
import numpy as np
from datetime import datetime
from subprocess import call
from threading import Timer
from collections import deque
import signal
import sys
from kiosk.signals import disable_entrance_timer
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
      self.sensor_first_past = [0]*10
      self.sensor_second_past = [0]*10
      self.sensor_last_active = 0
      self.idle_distance_first = None
      self.idle_distance_second = None
      self.threshold_distance_first = None
      self.threshold_distance_second = None
      self.read_sensor_timer = None
      self.alarm_state_timer = None

  instance = None
  def __init__(self):
    if not SensorHandler.instance:
      SensorHandler.instance = SensorHandler.__MyOnlySensorHandler()

  def interrupt_signal_handler(self,signal,frame):
    print("Measurement stopped by User")
    GPIO.cleanup()
    if self.instance.read_sensor_timer:
      self.instance.read_sensor_timer.cancel()
      self.instance.read_sensor_timer = None
    sys.exit(0)

  def sleep_alarm(self,halt_time):
    '''
    Description: Halts the alarm for given halt_time
    by setting alarm_state to 0(instead of 1)
    '''
    #print("Previous value " + str(self.instance.alarm_state))
    self.instance.alarm_state = 0
    #if self.instance.read_sensor_timer:
    #  self.instance.read_sensor_timer.cancel()
    #  self.instance.read_sensor_timer = None
    print("sleep_alarm: alarm state set to " + str(self.instance.alarm_state))
    #print ("switch_time is ",halt_time,sep='')
    self.instance.alarm_state_timer = Timer(halt_time, self.set_alarm)
    self.instance.alarm_state_timer.start()

  def set_alarm(self):
    '''
    Description: Sets the alarm back ON
    by setting alarm_state to 0(instead of 1)
    '''
    #print('set_alarm alarm_state is ', self.instance.alarm_state,sep='')
    self.instance.alarm_state = 1
    print('set_alarm alarm_state set to ', self.instance.alarm_state,sep='')
    #self.instance.read_sensor_timer = Timer(self.instance.sample_rate, self.start_reading())
    #self.instance.read_sensor_timer.start()

  def call_alarm(self):
    '''
    Description: Trigger the omxplayer to sound alarm
    by checking the alarm_state
    '''
    if self.instance.alarm_state == 1:
      print ("called the alarm function; yipeee")
      call(["omxplayer", "--vol", "-2400", "-o", "local", "justwhat.mp3"])
    else :
      print ("Speaker turned OFF")
      disable_entrance_timer.send(sender=None)
      self.instance.alarm_state = 1
      if self.instance.alarm_state_timer:
        self.instance.alarm_state_timer.cancel()
        self.instance.alarm_state_timer = None
        print ("disabled alarm_state_timer")
      print ("Speaker turning back ON")

  def read_sensor_distance(self,TRIG,ECHO):
    '''
    Description: Returns ultrasound sensor reading for given GPIO pin pairs
    '''
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    try:
      pulse_duration = pulse_end - pulse_start
      distance = pulse_duration * 17150
      distance = round(distance, 2)
      return distance
    except:
      print ("ERROR: Either pulse_end or pulse_end is not defined; Ignore instead of triggering flase alarm")
      return 0

  def check_intrusion(self, TRIG, ECHO, threshold_distance):
    '''
    Description: Sets the alarm back ON
    by setting alarm_state to 0(instead of 1)
    '''
    distance = self.read_sensor_distance(TRIG,ECHO)

    if ((distance > 0) and (distance < threshold_distance)):
      print ("Pin: ",ECHO, ":",round((distance*self.instance.threshold_ratio)/threshold_distance,2),' time: ',datetime.now(),sep="")
      return 1

    return 0

  def entrance_clear(self):
    '''
    Description: Check if someone is halted in grey area after intruding/exiting
    The method will not return unless it detects clear zone
    '''
    self.instance.read_sensor_timer = None
    while True:
      distance = self.read_sensor_distance(self.instance.trig_first,self.instance.echo_first)
      if ((distance > 0) and (distance < self.instance.threshold_distance_first)):
        print (">>>>>>>>PLEASE GET OUT<<<<<<<<<<<<",sep="")
        time.sleep(1)
        continue
      else:
        print ("entrance_clear Pin: ",self.instance.echo_first, ":",round(distance/self.instance.idle_distance_first,2),sep="")

      distance = self.read_sensor_distance(self.instance.trig_second,self.instance.echo_second)
      if ((distance > 0) and (distance < self.instance.threshold_distance_second)):
        print (">>>>>>>>PLEASE GET OUT<<<<<<<<<<<<",sep="")
        time.sleep(1)
        continue
      else:
        print ("entrance_clear Pin: ",self.instance.echo_second, ":",round(distance/self.instance.idle_distance_second,2),sep="")

      break
    self.instance.read_sensor_timer = Timer(self.instance.sample_rate, self.start_reading)
    self.instance.read_sensor_timer.start()

  def reject_outliers(self,data):
    '''
    Description: Sensor readings can often be erroneous. We reject such readings
    which are m*std_dev away from mean readings and then take average over the
    remaining data set.
    '''
    m = 3
    u = np.mean(data)
    s = np.std(data)
    filtered = [e for e  in data if (u - m*s < e < u + m*s)]
    return filtered

  def sensor_distance_setup(self,TRIG, ECHO):
    '''
    Description: For a given set of GPIO ultrasounic pins, continuously read few samples;
    reject false readings and returns the idle distance for that sensor.
    '''
    x = []
    counter = 0
    while counter<30 :
      time.sleep(self.instance.sample_rate)
      idle_distance = self.read_sensor_distance(TRIG,ECHO)
      if (idle_distance > 0):
        x.append(idle_distance)
        counter += 1

    x_mod = self.reject_outliers(x) #remove junk data from reading
    average_dist = np.mean(x_mod)
    print ("Pin: ",ECHO," Samples accepted in setting up benchmark: %d/%d "% (len(x_mod), len(x)),sep="")
    print ("Pin: ",ECHO," Set idle_distance:%d threshold_distance:%d " %(average_dist,self.instance.threshold_ratio*average_dist),sep="")
    return average_dist

  def sensor_benchmark_setup(self):
    '''
    Description: Called one time during setup; Set GPIO pins state to In/Out;
    Sets idle_distance to be used until it is called again
    '''
    print ("Ultrasonic sensor Setup BEGIN")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.instance.trig_first, GPIO.OUT)
    GPIO.setup(self.instance.echo_first, GPIO.IN)
    GPIO.setup(self.instance.trig_second, GPIO.OUT)
    GPIO.setup(self.instance.echo_second, GPIO.IN)

    GPIO.output(self.instance.trig_first, False)
    GPIO.output(self.instance.trig_second, False)
    #print ("Waiting For Sensor To Settle")
    time.sleep(1)
    #print ("Distance Measurement In Progress")

    print ("Setting up sensor 1\n")
    self.instance.idle_distance_first = self.sensor_distance_setup(self.instance.trig_first, self.instance.echo_first)
    self.instance.threshold_distance_first = self.instance.idle_distance_first*self.instance.threshold_ratio

    print ("Setting up sensor 2\n")
    self.instance.idle_distance_second = self.sensor_distance_setup(self.instance.trig_second, self.instance.echo_second)
    self.instance.threshold_distance_second = self.instance.idle_distance_second*self.instance.threshold_ratio
    print ('Setup COMPLETE')

  def start_reading(self):
    '''
    Description: Method is called every self.instance.sample_rate(default:0.05) seconds;
    It checks for sensor being triggered and based on past readings; decipher if
    there has been an intrusion or not; If yes, take necessary steps.
    '''
    #print "----------------------------------------------------------------------"
    self.instance.read_sensor_timer = None

    status_first = self.check_intrusion(self.instance.trig_first, self.instance.echo_first, self.instance.threshold_distance_first)
    self.instance.sensor_first_past = np.roll(self.instance.sensor_first_past,1)
    self.instance.sensor_first_past[0] = status_first

    time.sleep(self.instance.sample_rate)

    status_second = self.check_intrusion(self.instance.trig_second, self.instance.echo_second, self.instance.threshold_distance_second)
    self.instance.sensor_second_past = np.roll(self.instance.sensor_second_past,1)
    self.instance.sensor_second_past[0] = status_second
    #print ("\t\tfirst:second::", status_first,":",status_second,sep="")

    '''Logic to decipher if a student exited or entered'''
    if(status_first and (self.instance.sensor_last_active!=1)) :
      self.instance.sensor_last_active = 1
      sensor_second_sum = sum(self.instance.sensor_second_past)
      if (sensor_second_sum >= 2) :
        print (">>>>>>>>>>>>>>>>>>>>>Student ExiteD<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.instance.sensor_first_past = [0]*10
        self.instance.sensor_second_past = [0]*10
        self.instance.sensor_last_active = 0
        self.instance.read_sensor_timer = Timer(3,self.entrance_clear)
        self.instance.read_sensor_timer.start()

    elif(status_second and (self.instance.sensor_last_active!=2)):
      self.instance.sensor_last_active = 2
      sensor_first_sum = sum(self.instance.sensor_first_past)
      if (sensor_first_sum >= 2) :
        print (">>>>>>>>>>>>>>>>>>>>>INTRUDER DETECTED<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.call_alarm()
        self.instance.sensor_first_past = [0]*10
        self.instance.sensor_second_past = [0]*10
        self.instance.sensor_last_active = 0
        self.instance.read_sensor_timer = Timer(3,self.entrance_clear)
        self.instance.read_sensor_timer.start()

    else:
      pass

    if self.instance.read_sensor_timer == None:
      self.instance.read_sensor_timer = Timer(self.instance.sample_rate, self.start_reading)
      self.instance.read_sensor_timer.start()

if __name__ == "__main__" :

  try:
    main_handler = SensorHandler()
    signal.signal(signal.SIGINT, main_handler.interrupt_signal_handler)
    main_handler.sensor_benchmark_setup()
    main_handler.start_reading()

  except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
