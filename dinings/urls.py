from django.urls import path
from . import views

app_name = "foods"

urlpatterns = [path("dining_list/", views.DiningListView.as_view(), name="dining_list")]
