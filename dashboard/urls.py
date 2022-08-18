from django.urls import path
from .views import *

urlpatterns = [
	path("geolocations", myFirstMap, name="map"),
]
