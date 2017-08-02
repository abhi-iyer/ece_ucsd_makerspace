from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^authorize$', views.auth, name='auth'),
    url(r'^unauthorize$', views.unauth, name='unauth'),
    url(r'^ta-call$', views.tacall, name='tacall'),
]
