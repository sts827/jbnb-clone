from . import models
from django.contrib import admin
from django.utils.html import mark_safe


@admin.register(models.DiningCategory)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.dinings.count()


class PhotoInline(admin.TabularInline):
    # 장고가 자동으로 dining의 foreign key를 가지고 있는 이미지를 집어넣는다.
    model = models.Photo


# Register your models here.
@admin.register(models.Dining)
class DinigngAdmin(admin.ModelAdmin):

    # admin-> blue패널에 나타내는 항목
    inlines = (PhotoInline,)
    fieldsets = (
        (
            "Dining Info",
            {
                "fields": (
                    "name",
                    "address",
                    "description",
                    "menu",
                    "price",
                    "category",
                )
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )
    # 항목 display에 내용을 보여줌
    list_display = (
        "category",
        "name",
        "address",
        "menu",
        "price",
    )
    list_filter = (
        "category",
        "address",
    )
    ordering = ("-created",)

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    # 가끔 장고에서 obj 안에 있는 내용을 볼려고 할때 보여지는 결과가 전부가 아닐 수도 있다.
    # return obj.file.url
    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
