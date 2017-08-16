from subprocess import call
import threading
mode = 1
def call_alarm():
  global mode
  if mode == 1:
    call(["omxplayer","","",""])

def sleep_alarm():
  global mode
  mode = 0

def set_alarm()
  global mode
  mode = 1

