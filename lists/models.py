from django.db import models
from core import models as core_models

# Create your models here.
class List(core_models.TimeStampedModel):

    """ Lists model Definition """

    name = models.CharField(max_length=80)
    user = models.ForeignKey(
        "users.User", related_name="lists", on_delete=models.CASCADE
    )
    # list하나는 많은 room을 가질 수 있다.
    rooms = models.ManyToManyField("rooms.Room", related_name="lists", blank=True)

    def __str__(self):

        return self.name

    def count_rooms(self):
        return self.rooms.count()

    # short_description은 admin 패널에서 커스텀 이름
    count_rooms.short_description = "Number of Rooms"

