from django.apps import AppConfig

class KioskConfig(AppConfig):
  name = 'kiosk'

  def ready(self):
    import kiosk.randomness
