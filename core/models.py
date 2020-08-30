from django.db import models
from . import managers

# 공통된 common 요소들을 적용시키기 위한 core apps이며 db에 등록되지 않음
class TimeStampedModel(models.Model):
    """ Time stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    # 공통적으로 들어가는 요소들을 DB에 저장하지 않고 기능만 사용하기 위해서 abstarct = true
    class Meta:
        abstract = True  # AbstractModel은 model이지만 DB에 나타나지 않은 model

