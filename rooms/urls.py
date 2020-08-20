from django.urls import path
from . import views

app_name = "rooms"
# views.py의 room_detail함수에서 return값 pk가 넘어옴<변수type:변수명>
urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]
