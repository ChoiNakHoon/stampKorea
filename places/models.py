from datetime import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
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
        return self.name


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

    place = models.ForeignKey("Place", related_name="info", on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    text = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Detail Infomation"

    def __str__(self):
        return self.title


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    url = models.URLField(blank=True, null=True)
    place = models.ForeignKey("Place", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Place(core_models.TimeStampedModel):

    """ Place Model Definition """

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_SPANISH = "es"
    LANGUAGE_CHINESE = "zh"
    LANGUAGE_JAPNESE = "jp"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_SPANISH, "Español"),
        (LANGUAGE_CHINESE, "汉语·中文"),
        (LANGUAGE_JAPNESE, "日本語"),
    )

    # 공통정보
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_ENGLISH
    )
    content_id = models.CharField(max_length=120, blank=True, null=True)
    content_type = models.CharField(max_length=120, blank=True, null=True)
    title = models.CharField(max_length=120)
    address = models.CharField(max_length=255, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    directions = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=150, null=True, blank=True)
    mapy = models.CharField(max_length=20, null=True, blank=True)
    mapx = models.CharField(max_length=20, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    region = models.ForeignKey(
        "Region", related_name="places", on_delete=models.SET_NULL, null=True
    )
    region_sub = models.ForeignKey(
        "Sub_Region", related_name="places", on_delete=models.SET_NULL, null=True,
    )
    cat_type = models.ForeignKey(
        "Cat_Type", related_name="places", on_delete=models.SET_NULL, null=True,
    )
    created_time = models.CharField(max_length=80, blank=True, null=True)
    updated_time = models.CharField(max_length=80, blank=True, null=True)

    homepage = models.TextField(null=True, blank=True)

    # 소개 정보 - 관광지 (type = 76)
    expagerange = models.CharField(
        max_length=255, help_text="체험가능 연령", null=True, blank=True
    )
    expguide = models.TextField(help_text="체험 내용", null=True, blank=True)
    heritage1 = models.BooleanField(help_text="문화 유산 유무", default=False)
    info_center = models.TextField(help_text="문의 및 안내", null=True, blank=True)
    rest_date = models.CharField(max_length=20, help_text="쉬는 날", null=True, blank=True)
    parking = models.CharField(max_length=15, help_text="주차 시설", null=True, blank=True)
    use_time = models.TextField(help_text="이용 시간", null=True, blank=True)

    # 소개 정보 - 문화 시설 (type = 78)
    infocenterculture = models.TextField(help_text="문의 및 안내", null=True, blank=True)
    restdateculture = models.CharField(
        max_length=20, help_text="쉬는 날", null=True, blank=True
    )
    usefee = models.TextField(help_text="이용 요금", null=True, blank=True)
    usetimeculture = models.TextField(
        max_length=80, help_text="이용 시간", null=True, blank=True
    )
    parkingculture = models.CharField(
        max_length=15, help_text="주차 시설", null=True, blank=True
    )

    # 소개 정보 - 행사 Festival (type = 85)
    agelimit = models.CharField(
        max_length=120, help_text="관람 가능연령", null=True, blank=True
    )
    bookingplace = models.CharField(
        max_length=255, help_text="예매처", null=True, blank=True
    )
    discountinfofestival = models.TextField(help_text="할인 정보", null=True, blank=True)
    eventstartdate = models.CharField(max_length=80, blank=True, null=True)
    eventenddate = models.CharField(max_length=80, blank=True, null=True)
    eventhomepage = models.TextField(help_text="행사 홈페이지", null=True, blank=True)
    eventplace = models.CharField(
        max_length=255, help_text="행사 장소", null=True, blank=True
    )
    placeinfo = models.TextField(help_text="행사장 위치 안내", blank=True, null=True)
    playtime = models.CharField(max_length=100, help_text="공연시간", blank=True, null=True)
    program = models.TextField(help_text="행사 프로그램", blank=True, null=True)
    sponsor1 = models.CharField(
        max_length=255, help_text="주최자 정보", blank=True, null=True
    )
    sponsor1tel = models.CharField(
        max_length=150, help_text="주최자 연락처", blank=True, null=True
    )
    sponsor2 = models.CharField(
        max_length=255, help_text="주관사 정보", blank=True, null=True
    )
    sponsor2tel = models.CharField(
        max_length=150, help_text="주관사 연락처", blank=True, null=True
    )
    subevent = models.TextField(help_text="부대행사", blank=True, null=True)
    usetimefestival = models.TextField(help_text="이용요금", blank=True, null=True)

    # 소개 정보 - 레포츠 (type = 75)
    expagerangeleports = models.CharField(
        max_length=255, help_text="체험 가능 연령", blank=True, null=True
    )
    infocenterleports = models.TextField(help_text="문의 및 안내", blank=True, null=True)
    reservation = models.TextField(help_text="예약 안내", blank=True, null=True)
    restdateleports = models.CharField(
        max_length=80, help_text="쉬는날", blank=True, null=True
    )
    usefeeleports = models.CharField(
        max_length=255, help_text="입장료", blank=True, null=True
    )
    usetimeleports = models.CharField(
        max_length=255, help_text="이용 시간", blank=True, null=True
    )
    parkingleports = models.TextField(
        max_length=120, help_text="주차 시설", blank=True, null=True
    )

    # 소개 정보 - 숙박 (type = 80)
    checkintime = models.CharField(max_length=80, blank=True, null=True)
    checkouttime = models.CharField(max_length=80, blank=True, null=True)
    infocenterlodging = models.TextField(help_text="문의 및 안내", blank=True, null=True)
    parkinglodging = models.CharField(
        max_length=120, help_text="주차 시설", blank=True, null=True
    )
    reservationlodging = models.TextField(help_text="예약 안내", blank=True, null=True)
    subfacility = models.TextField(help_text="부대 시설", blank=True, null=True)

    # 소개 정보 - 쇼핑 (type = 79)
    fairday = models.CharField(max_length=255, help_text="장서는 날", blank=True, null=True)
    infocentershopping = models.TextField(help_text="문의 및 안내", blank=True, null=True)
    opentime = models.CharField(
        max_length=200, help_text="운영 시간", blank=True, null=True
    )
    restdateshopping = models.CharField(
        max_length=255, help_text="쉬는 날", blank=True, null=True
    )
    parkingshopping = models.CharField(
        max_length=120, help_text="주차 시설", blank=True, null=True
    )

    # 소개 정보 - 음식점 (type = 82)
    firstmenu = models.CharField(
        max_length=255, help_text="대표 메뉴", blank=True, null=True
    )
    treatmenu = models.TextField(help_text="취급 메뉴", blank=True, null=True)
    infocenterfood = models.TextField(help_text="문의 및 안내", blank=True, null=True)
    opentimefood = models.CharField(
        max_length=255, help_text="영업 시간", blank=True, null=True
    )
    restdatefood = models.CharField(
        max_length=255, help_text="쉬는 날", blank=True, null=True
    )
    reservationfood = models.TextField(help_text="예약 안내", blank=True, null=True)
    parkingfood = models.CharField(
        max_length=180, help_text="주차 시설", blank=True, null=True
    )

    # 소개 정보 - 교통 정보 (type = 77)
    conven = models.TextField(help_text="편의 시설", blank=True, null=True)
    disablefacility = models.TextField(help_text="장애인 편의시설", blank=True, null=True)
    foreignerinfocenter = models.TextField(
        help_text="외국인 문의 및 안내", blank=True, null=True
    )
    parkingtraffic = models.CharField(
        max_length=180, help_text="주차 시설", blank=True, null=True
    )
    # 좋아요
    likes = models.ManyToManyField("users.User", related_name="posts", blank=True)

    def __str__(self):
        return f"{self.title} - {self.region} : {self.region_sub}"

    def get_absolute_url(self):
        return reverse("places:detail", kwargs={"pk": self.pk})

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

    # 각 place에서 첫번째 사진을 가져 옵니다.
    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]  # unpacking list
            return photo.url
        except ValueError:
            return None

    # place에 4장의 사진을 가져 옵니다.
    def get_next_four_photo(self):
        photo = self.photos.all()[1:5]
        return photo

    # 현재 장소를 유저가 선택한 수를 구한다.
    def get_likes_count(self):
        return self.likes.count()

    get_likes_count.short_description = ".Like"

    def get_start_date(self):
        if self.eventstartdate is not None:
            return datetime.strptime(self.eventstartdate, "%Y%m%d").date()
        else:
            return timezone.now().date()

    def get_end_date(self):
        if self.eventenddate is not None:
            return datetime.strptime(self.eventenddate, "%Y%m%d").date()
        else:
            return timezone.now().date()

    # 현재 시간에서 진행이 가능 한 경우
    def is_progress(self):
        if self.eventenddate is not None:
            now = timezone.now().date()
            end_date = datetime.strptime(self.eventenddate, "%Y%m%d").date()
            return now < end_date
        else:
            return False

    is_progress.boolean = True

    # is_parking
    # is_use_time
    # is_... 뭐 is 다 만들어 봐..
    # 데이터 받아 온 뒤에 bool값으로 규정.
