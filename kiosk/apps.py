from django.apps import AppConfig

class KioskConfig(AppConfig):
  name = 'kiosk'

  def ready(self):
    '''
    Import signal handler, sensor handler
    Usage:
    1) signal receiver is activated
    2) sensor-alarm system activates in the backend
    '''
    import kiosk.signals.handlers
    import kiosk.sensors.handlers
