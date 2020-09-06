from django.urls import path
from . import views

app_name = "rooms"
# views.py의 room_detail함수에서 return값 pk가 넘어옴<변수type:변수명>
urlpatterns = [
    path("create/", views.CreateRoomView.as_view(), name="create"),
    path("room_list/", views.HomiView.as_view(), name="room_list"),
    path("map_view/", views.map_view, name="map_view"),
    path("room_category/", views.get_find_room, name="room_category"),
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add", views.AddPhotoView.as_view(), name="add-photo"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
