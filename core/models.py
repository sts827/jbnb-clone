from django.db import models

# 공통된 common 요소들을 적용시키기 위한 core apps이며 db에 등록되지 않음
class TimeStampedModel(models.Model):
    """ Time stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

