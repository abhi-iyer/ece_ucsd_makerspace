"""
WSGI config for ece_ucsd_makerspace project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os,sys,subprocess

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ece_ucsd_makerspace.settings")
print ("Starting sensor code from project wsgi")
subprocess.Popen(["python", "randomness.py"], cwd="kiosk/")
application = get_wsgi_application()
