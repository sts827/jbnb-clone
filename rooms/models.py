from django.utils import timezone
from django.db import models
from django.urls import reverse
from core import models as core_models
from django_countries.fields import CountryField
from cal import Calendar

# from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Model"""

    name = models.CharField(max_length=80)  # 어떤 name일까?

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType object Definition """

    class Meta:
        # class이름 Custom
        verbose_name = "Room Type"
        # ordering = ["created"] # room type생성시 오래된 항목은 밑으로 정렬


class Amenity(AbstractItem):
    """ Amenity Model Definit """

    class Meta:
        # class이름 Custom
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """ Facility Model Item """

    class Meta:
        # class이름 Custom
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ Mouse Model Definition"""

    class Meta:
        # class이름 Custom
        verbose_name = "House Rule"


# python은 상,하 순서가 있기 때문에 Room 클래스 밑에 photo를 선언해줘야함.
# django는 "str"만 알려주면 알아서 찾아주기 때문에 해당되는 클래스명(user,..)을 ""로 Foreign key를 설정 할수도 있다.
class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    # image field는 image만을 위한것
    # image 뿐만 아니라 video도 올릴수 있음
    # upload폴더내 room_photos폴더가 생성하여 Image를 저장한다.
    file = models.ImageField(upload_to="room_photos")
    # room과 Photo를 연결해주고 room을 지우면 photo도 같이 삭제?
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    # db에 파일확장자 에러?
    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    # 서로 다른 model을 연결시켜주는 ForeignKey('','')

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    # address -> 지도로 띠워주기
    address = models.CharField(max_length=140)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    # bath
    baths = models.IntegerField()
    guests = models.IntegerField(help_text="How many people will be staying?")
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # 여기 아래서부터는 이해가 필요함
    # host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    # related_name은 장고가 대상을 찾을 때 사용되는 이름
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    # foreign key를 쓰지 않는 이유는 일대다 관계가 아니라 다대다 관계이기 때문
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    # house_rule
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)
    # category => models.ManyToManyField("category",related_name="")

    def __str__(self):
        return self.name

    def save(self, *args, **kargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kargs)

    # 이 메소드는 사용자가 원하는 model을 찾을 수 있는 url을 찾게 해줌
    # from django.urls import reverse 는 url name을 필요로 하는 function, 그 url을 return한다.
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        # 전체 평점
        # self에서는 많은 review를 가지고 있다.
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                # 전체 평점/총 리뷰 개수
                all_ratings += review.rating_average()
            return all_ratings / len(all_reviews)
        return

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]  # 전체 방에서 첫번쨰 사진들
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]  # 각방에서 첫번째부터 네번째 사진들 출력
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]

