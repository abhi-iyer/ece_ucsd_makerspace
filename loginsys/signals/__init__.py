from django.dispatch import Signal
turn_off_sensor = Signal(providing_args=["switch_time"])
disable_entrance_timer = Signal()
