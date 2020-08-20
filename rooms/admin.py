from . import models
from django.contrib import admin
from django.utils.html import mark_safe


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):
    # 장고가 자동으로 room의 foreign key를 가지고 있는 이미지를 집어넣는다.
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,)
    # fields셋 정리 => admin패널과 admin패널에 보이는 항목들,
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                    "room_type",
                )
            },
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "More About Space",
            {
                "classes": ("collapse",),  # 내용을 숨기거나 보이거나 할 수 있다. default는 hide
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Spaces", {"fields": ("beds", "bedrooms", "baths", "guests")}),
        ("Last Details", {"fields": ("host",)}),
    )
    # 항목 display에 내용을 보여줌
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    ordering = (
        "name",
        "price",
        "bedrooms",
    )

    #  filter bar를 생성
    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )
    # filter_horizontal은 Many to Many Relation에서 작동한다.
    # raw
    raw_id_fields = ("host",)
    # Customize-> search_fields :: search box ..이며 default로 icontains를 가짐: insensitive를 가지고 소,대문자를 구별하지 않는다.
    # Prefix	Lookup
    # ^	startswith
    # =	iexact
    # @	search
    # None	icontains
    search_fields = ("=city", "^host__username")

    # Many to Many relation에서 사용하는 horizontal filter
    filter_horizontal = ("amenities", "facilities", "house_rules")

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "Amenity Count"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"


##
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # 가끔 장고에서 obj 안에 있는 내용을 볼려고 할때 보여지는 결과가 전부가 아닐 수도 있다.
        # return obj.file.url
        return mark_safe(f'<img src="{obj.file.url}" width="50px" />')

    get_thumbnail.short_description = "Thumbnail"
