from django.urls import path
from . import views

app_name = "maps"
urlpatterns = [
    path("mapView/", views.map, name="mapView"),
]

