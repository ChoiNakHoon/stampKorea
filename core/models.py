from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stamp Model Definition """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # 데이터베이스에 추가 되지 않기 위해서 추상클래스
    class Meta:
        abstract = True
