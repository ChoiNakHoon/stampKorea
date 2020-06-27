from collections import defaultdict
from django.db import models
from core import models as core_models


class Region(core_models.TimeStampedModel):
    """ Region Item """

    # 지역 코드
    code = models.CharField(max_length=4, null=True, blank=True)
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = "Region"

    def __str__(self):
        return self.name


class Sub_Region(core_models.TimeStampedModel):
    """ Sub_Region Item """

    # 지역 세부 코드
    region = models.ForeignKey(
        "Region", related_name="region", on_delete=models.CASCADE
    )
    code = models.CharField(max_length=4, null=True, blank=True)
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = "Town/City"

    def __str__(self):
        return f"{self.region.name} - {self.name}"


class Cat_Type(core_models.TimeStampedModel):
    """ Cat Type Item """

    code = models.CharField(max_length=4, null=True, blank=True)
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Cat Type"

    def __str__(self):
        return self.name


class Sub_Info(core_models.TimeStampedModel):

    """ Sub_Infomation """

    place = models.OneToOneField("Place", related_name="info", on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    text = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Detail Infomation"

    def __str__(self):
        return self.title


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="place_photos")
    place = models.ForeignKey("Place", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Place(core_models.TimeStampedModel):

    """ Place Model Definition """

    # 공통정보
    content_id = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(max_length=120)
    address = models.CharField(max_length=255)
    overview = models.TextField()
    directions = models.TextField()
    tel = models.CharField(max_length=20)
    mapy = models.CharField(max_length=20)
    mapx = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)
    region = models.ForeignKey(
        "Region", related_name="places", on_delete=models.SET_NULL, null=True
    )
    region_sub = models.ForeignKey(
        "Sub_Region", related_name="places", on_delete=models.SET_NULL, null=True,
    )
    cat_type = models.ForeignKey(
        "Cat_Type", related_name="places", on_delete=models.SET_NULL, null=True,
    )
    created_time = models.CharField(max_length=20)
    updated_time = models.CharField(max_length=20)

    # 소개정보
    info_center = models.CharField(max_length=255)
    parking = models.CharField(max_length=15)
    rest_date = models.CharField(max_length=30)
    use_time = models.TextField()

    # 좋아요
    likes = models.ManyToManyField("users.User", related_name="posts", blank=True)

    def __str__(self):
        return f"{self.title} - {self.region} : {self.region_sub}"

    # 전체 별점 평균 구하기
    def total_rating(self):
        all_reviews = self.reviews.all()
        total_avg = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                total_avg += review.rating_avg()
            return round(total_avg / len(all_reviews), 2)
        return 0

    total_rating.short_description = ".Avg"

    # 현재 장소를 유저가 선택한 수를 구한다.
    def get_likes_count(self):
        return self.likes.count()

    get_likes_count.short_description = ".Like"

    # is_parking
    # is_use_time
    # is_... 뭐 is 다 만들어 봐..
    # 데이터 받아 온 뒤에 bool값으로 규정.
