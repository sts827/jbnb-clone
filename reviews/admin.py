from django.contrib import admin

# 1. models 를 import
from . import models

# 2. register 생성
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ Review Admin Definition """

    list_display = ("__str__", "rating_average")


# 3. python manage.py makemigrations로 db에 모델 생성 후 migrate

