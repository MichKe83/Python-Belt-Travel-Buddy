from django.conf.urls import url
from . import views          
urlpatterns = [
url(r'^$', views.index),
url(r'^register$', views.register),
url(r'^login$', views.login),
url(r'^travels$', views.travels),
url(r'^addTrip$', views.addTrip),
url(r'^destination/(?P<id>\d+)$', views.destination),
# url(r'^joinTrip/(?P<id>\d+)$', views.joinTrip),
url(r'^submitTrip$', views.submitTrip),
url(r'^delete/(?P<id>\d+)$', views.delete),
url(r'^logout$', views.logout), 
]