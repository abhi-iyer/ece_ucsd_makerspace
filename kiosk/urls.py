from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^landing$', views.landing, name='landing'),
    url(r'^authorize$', views.auth, name='auth'),
    url(r'^ta-call$', views.tacall, name='tacall'),
]
