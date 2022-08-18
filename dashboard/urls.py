from django.urls import path
from .views import *

urlpatterns = [
    path("base", base),
	path("geolocations", myFirstMap, name="map"),
	path("categoryMap", draw_treeMap, name="treemap"),
	path("questions", get_all_question, name="questions")
]
