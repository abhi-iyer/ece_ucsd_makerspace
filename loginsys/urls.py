from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^user_info$', views.user_info, name='user_info')
]
