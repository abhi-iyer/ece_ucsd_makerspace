from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^user_info$', views.user_info, name='user_info'),
    url(r'^supervisor_info$', views.supervisor_info, name='supervisor_info'),
    url(r'^kiosk_entry_status$', views.kiosk_entry_status, name='entry_status')
]
