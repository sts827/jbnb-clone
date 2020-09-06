from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models

# Create your models here.
class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    # 1. 처음엔 models에 모든 field를 생성한다.
    # 2. 만약 다른 model에 접근하려면 foreign key를 생성하여 접근하려고한 class아래에 생성한다.
    # 3. 그리고 마지막엔 def __str__(self): return self."name" 이나 class 안에 class Meta:를 생성한다.
    # Field가 생성되면 admin패널에서 설치한다.
    review = models.TextField()
    accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanlines = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    check_in = models.IntegerField()
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    # foreign key로 연결된 Object에서 value값을 가져 올수 있다.
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        # return self.room.host.username 로 장고는 query문없이 relation관계에 있는 모든 모델에 property에 접근 가능
        # 또한 f'{~~}'로 두가지의 내용을 나타낼수 있음.
        return f"{self.review} - {self.room}"

    # 함수를 만드는것처럼 object와 연관있는 뭔가를 model에서 만들어 전체 admin패널에 적용할 수 있다.
    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanlines
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg"

    def food_rating(self):
        avg = (self.accuracy + self.location + self.cleanlines + self.value) / 4
        return round(avg, 2)

    food_rating.short_description = "Food_Avg"

    class Meta:
        ordering = ("-created",)  # 어떤 model을 ordering할것인지 정함
