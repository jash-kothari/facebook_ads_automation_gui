from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'/get_data/$', views.get_data, name='get_data'),
]