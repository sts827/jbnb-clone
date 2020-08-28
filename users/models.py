import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.shortcuts import reverse


class User(AbstractUser):

    """ User Model """

    # >>>>>  table의  변수선언 <<<<< #
    # --------------------------- #

    # 성별 선택
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    # Gender select을 위한 choices
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    # 언어 선택
    LANGUAGE_ENGLISH = "English"
    LANGUAGE_KOREAN = "Korean"
    # Language select을 위한 choices
    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    # 지역 선택 => 프로젝트에 맞게 설정
    # 특별시: special city, 광역시: Metroplitan City, 도: Province,
    # 시: City, 군:Coutry, 구:District, 읍:Town, 면: TownShip, 동: Neighborhood, 리: Village
    CITY_SEOUL = "서울"
    CITY_TONGYEONG = "통영"
    CITY_BUSAN = "부산"

    # City select을 위한 choices
    CITY_CHOICES = (
        (CITY_SEOUL, "서울"),
        (CITY_TONGYEONG, "통영"),
        (CITY_BUSAN, "부산"),
    )

    # Login
    LOGIN_EMAIL = "Email"
    LOGIN_GITHUB = "Github"
    LOGIN_KAKAO = "Kakao"

    # Login select을 위한 choices
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    # 화폐 선택
    CURRENCY_KRW = "원화"
    CURRENCY_LOCAL = "상품권"

    # Currency select을 위한 choices
    CURRENCY_CHOICES = (
        (CURRENCY_KRW, "원화"),
        (CURRENCY_LOCAL, "상품권"),
    )

    # >>>>> Field 선언 <<<<< #
    # --------------------------- #

    # table 변수 선언과 field선언 후 python manage.py makemigrations => python manage.py migrate #
    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=10, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    city = models.CharField(choices=CITY_CHOICES, max_length=15, blank=True)
    superhost = models.BooleanField(default=False)
    # email confirm fields
    # email과 pw를 이용해서 새 계정을 만들면 email_secret에 아무숫자나 집어넣어서 Email을 Sending하기 위한 필드
    # :: views.py참고
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    # verify_email함수는 자주 사용하는 곳에 위치시키자.
    # MailGun사이트의 Authorized Recipients user 확인
    def verify_email(self):
        # email verify가 안되면 아무것도 안함
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )

            send_mail(
                "Verify Jbnb Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()  # verify가 완료된후 save()하면 admin에서 보여지게 된다.
        return

    # Admin패널에서 객체(object)를 볼때 get_absolute_url을 자주 사용한다.
    def get_absolute_url(self):
        # Detail 안에 있는 모델을 보기위해선 URL을 반환해야한다.
        return reverse("users:profile", kwargs={"pk": self.pk})


## push 알림 email
