from django.db import models
from django.urls import reverse
from core import models as core_models


class AbstractFoodItem(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)  # 어떤 name일까?

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class FoodType(AbstractFoodItem):

    """ Food Type object Definition """

    class Meta:
        # class이름 Customize
        verbose_name = "Food Type"


class FoodMenu(AbstractFoodItem):

    """ Food Menu object Definition"""

    class Meta:
        verbose_name = "Food Menu"


class FoodPhoto(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    # image field는 image만을 위한것
    # image 뿐만 아니라 video도 올릴수 있음
    # upload폴더내 food_photos폴더가 생성하여 Image를 저장한다.
    file = models.ImageField(upload_to="food_photos")
    food = models.ForeignKey("Food", related_name="photos", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created",)

    # db에 파일확장자 에러?
    def __str__(self):
        return self.caption


class Food(core_models.TimeStampedModel):

    """Food Table Defintion"""

    # Food Category Select을 위한 entity

    FOOD_KOREA = "한식"
    FOOD_JAP = "일식"
    FOOD_USA = "양식"
    FOOD_CHN = "중식"

    FOOD_CHOICES = (
        (FOOD_KOREA, "한식"),
        (FOOD_JAP, "일식"),
        (FOOD_USA, "양식"),
        (FOOD_CHN, "중식"),
    )

    # Category Select("한식","일식","양식","중식")
    category = models.CharField(choices=FOOD_CHOICES, max_length=20, blank=True)
    name = models.CharField(max_length=20, blank=True)  # 음식 이름
    store = models.CharField(max_length=20, blank=True)  # 가게 이름
    price = models.IntegerField(default=0)  # 가격
    address = models.CharField(max_length=40)  # 주소
    description = models.CharField(max_length=140)
    host = models.ForeignKey(
        "users.User", related_name="foods", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
