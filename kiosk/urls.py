from django.conf.urls import url

from . import views
'''
Default route: localhost:8000/ (or localhost:8000/kiosk/) calls views.main_kiosk;
Everything else is dormant
'''

urlpatterns = [
    url(r'^$', views.main_kiosk, name='index'),
    url(r'^landing$', views.landing, name='landing'),
    url(r'^authorize$', views.auth, name='auth'),
    url(r'^ta-call$', views.tacall, name='tacall'),
]
