from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'accounts_index'),
    url(r'^signin$', views.signin, name = 'accounts_signin'),
    url(r'^register$', views.register, name = 'accounts_register'),
    url(r'^logout$', views.logout, name = 'accounts_logout'),
    url(r'^travels/(?P<id>\d+)$', views.travels, name = 'accounts_travels'),
    url(r'^addTripPage/(?P<id>\d+)$', views.addTripPage, name = 'accounts_addTripPage'),
    url(r'^addTrip$', views.addTrip, name = 'accounts_addTrip'),
    url(r'^travels/destinationPage/(?P<destination>\d+)$', views.destinationPage, name = 'accounts_destinationPage'),
]