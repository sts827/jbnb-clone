from . import models
from django.contrib import admin
from django.utils.html import mark_safe


@admin.register(models.FoodType)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name",)


class FoodPhotoInline(admin.TabularInline):
    # 장고가 자동으로 room의 foreign key를 가지고 있는 이미지를 집어넣는다.
    model = models.FoodPhoto


# Register your models here.
@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):

    # admin-> blue패널에 나타내는 항목
    fieldsets = (
        (
            "Food Info",
            {
                "fields": (
                    "category",
                    "name",
                    "store",
                    "description",
                    "price",
                    "address",
                )
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )
    # 항목 display에 내용을 보여줌
    list_display = (
        "category",
        "store",
        "name",
        "price",
        "address",
    )

    ordering = ("-created",)


@admin.register(models.FoodPhoto)
class FoodPhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    # 가끔 장고에서 obj 안에 있는 내용을 볼려고 할때 보여지는 결과가 전부가 아닐 수도 있다.
    # return obj.file.url
    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
