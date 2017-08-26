from django.apps import AppConfig

class KioskConfig(AppConfig):
  name = 'kiosk'

  def ready(self):
    #import kiosk.sro4_fast_sampling
    import kiosk.signals.handlers
