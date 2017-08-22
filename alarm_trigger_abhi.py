from subprocess import call
from threading import Timer
mode = 1

def call_alarm():
  global mode
  print ("call_alarm mode value ", mode)
  #if mode == 1:
    #call(["omxplayer","--vol","-1200","-o","local","justwhat.mp3"])

def sleep_alarm():
  global mode
  print("sleep_alarm alarm mode is ", mode)
  mode = 0
  t = Timer(10, set_alarm)
  t.start()
  print("sleep_Alarm alarm mode is ", mode)

def set_alarm():
  global mode
  print("set_alaem alarm mode is ", mode)
  mode = 1
  print("set_alarm alarm mode is ", mode)

#if __name__ == "__main__" :
#  while True:
#    pass
