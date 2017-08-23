import django.dispatch
signal_notifier = django.dispatch.Signal(providing_args=["switch_time"])
