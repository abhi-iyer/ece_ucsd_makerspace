#settings.py for initializing global variables

def init():
  global HOLD_TIME
  global kiosk_entry_status
  global supervisor_check
  HOLD_TIME = 15 #maximum sensor turn off time on authorization
  kiosk_entry_status = 0 # 0 means no entry detected; 1 means entry observed
  supervisor_check = None # Supervisor checking
