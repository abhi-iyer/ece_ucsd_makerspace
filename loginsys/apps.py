from django.apps import AppConfig
from loginsys import settings

class LoginsysConfig(AppConfig):
  name = 'loginsys'

  def ready(self):
    '''
    Import signal handler, sensor handler, set global variables
    Usage:
    1) signal receiver is activated
    2) sensor-alarm system activates in the backend
    '''
    settings.init()
    import loginsys.signals.handlers
    import loginsys.sensors.handlers
