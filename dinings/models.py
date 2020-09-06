from django.db import models
from django.urls import reverse
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)  # 어떤 name일까?

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class DiningCategory(AbstractItem):
    """ Dining Category Object Definition """

    class Meta:
        verbose_name_plural = "Dining Category"


class Photo(core_models.TimeStampedModel):
    caption = models.CharField(max_length=80)
    # image field는 image만을 위한것
    # image 뿐만 아니라 video도 올릴수 있음
    # upload폴더내 food_photos폴더가 생성하여 Image를 저장한다.
    file = models.ImageField(upload_to="dining_photos")
    dining = models.ForeignKey(
        "Dining", related_name="photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.caption


class Dining(core_models.TimeStampedModel):

    """Food Table Defintion"""

    name = models.CharField(max_length=30)
    address = models.CharField(max_length=40, blank=True)  # 주소
    description = models.CharField(max_length=140, blank=True)
    menu = models.CharField(max_length=30, blank=True)
    price = models.IntegerField(default=0)
    host = models.ForeignKey(
        "users.User", related_name="dinings", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        "DiningCategory", related_name="dinings", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name

    def food_photo(self):
        try:
            (photo,) = self.photos.all()[:1]  # 전체 방에서 첫번쨰 사진들
            return photo.file.url
        except ValueError:
            return None

    def total_rating(self):
        # 전체 평점
        # self에서는 많은 review를 가지고 있다.
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                # 전체 평점/총 리뷰 개수
                all_ratings += review.food_rating()
            return all_ratings / len(all_reviews)
        return
