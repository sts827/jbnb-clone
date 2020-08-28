from django.contrib import admin
from . import models

# register에 등록했으면 config -> settings.py에서 project App이 있는지 확인하기 !! 잊지말기
@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )
    list_filter = ("status",)


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):

    list_display = ("day", "reservation")
