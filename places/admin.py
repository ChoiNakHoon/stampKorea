from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from . import models


@admin.register(models.Cat_Type, models.Sub_Region)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    pass


class CityInfoInline(admin.TabularInline):
    """ City Info Inline Definition """

    model = models.Sub_Region


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    """ Region Admin Definition """

    inlines = (CityInfoInline,)

    list_display = (
        "name",
        "code",
    )


@admin.register(models.Sub_Info)
class SubInfoAdmin(admin.ModelAdmin):
    """ Sub_Infomation Admin Definition """

    pass


class SubInfoInline(admin.TabularInline):
    """ Sub Infomation Definition """

    model = models.Sub_Info


class PhotoInline(admin.TabularInline):
    """ Photo Inline Definition """

    model = models.Photo


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    """ Place Admin Definition """

    inlines = (SubInfoInline, PhotoInline)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "title",
                    "address",
                    "overview",
                    "directions",
                    "tel",
                    "mapy",
                    "mapx",
                    "zipcode",
                    "region",
                    "region_sub",
                    "cat_type",
                    "homepage",
                )
            },
        ),
        ("Times", {"fields": ("created_time", "updated_time",)}),
        (
            "Introduction Info : Nature",
            {
                "classes": ("collapse",),
                "fields": (
                    "heritage1",
                    "expagerange",
                    "expguide",
                    "info_center",
                    "use_time",
                    "rest_date",
                    "parking",
                ),
            },
        ),
        (
            "Introduction Info : Culture/Art/History",
            {
                "classes": ("collapse",),
                "fields": (
                    "infocenterculture",
                    "usetimeculture",
                    "restdateculture",
                    "usefee",
                    "parkingculture",
                ),
            },
        ),
        (
            "Introduction Info : Festival",
            {
                "classes": ("collapse",),
                "fields": (
                    "agelimit",
                    "bookingplace",
                    "discountinfofestival",
                    "eventenddate",
                    "eventstartdate",
                    "eventhomepage",
                    "eventplace",
                    "placeinfo",
                    "playtime",
                    "program",
                    "subevent",
                    "usetimefestival",
                    "sponsor1",
                    "sponsor1tel",
                    "sponsor2",
                    "sponsor2tel",
                ),
            },
        ),
        (
            "Introduction Info : Leisure/Sports",
            {
                "classes": ("collapse",),
                "fields": (
                    "expagerangeleports",
                    "infocenterleports",
                    "reservation",
                    "usetimeleports",
                    "restdateleports",
                    "usefeeleports",
                    "parkingleports",
                ),
            },
        ),
        (
            "Introduction Info : Accommodation",
            {
                "classes": ("collapse",),
                "fields": (
                    "checkintime",
                    "checkouttime",
                    "infocenterlodging",
                    "reservationlodging",
                    "subfacility",
                    "parkinglodging",
                ),
            },
        ),
        (
            "Introduction Info : Shopping",
            {
                "classes": ("collapse",),
                "fields": (
                    "fairday",
                    "infocentershopping",
                    "opentime",
                    "restdateshopping",
                    "parkingshopping",
                ),
            },
        ),
        (
            "Introduction Info : Cuisine/Dining",
            {
                "classes": ("collapse",),
                "fields": (
                    "firstmenu",
                    "treatmenu",
                    "infocenterfood",
                    "opentimefood",
                    "restdatefood",
                    "reservationfood",
                    "parkingfood",
                ),
            },
        ),
        (
            "Introduction Info : Transportation",
            {
                "classes": ("collapse",),
                "fields": (
                    "conven",
                    "disablefacility",
                    "foreignerinfocenter",
                    "parkingtraffic",
                ),
            },
        ),
        ("Other", {"fields": ("likes", "language", "content_id", "content_type",)}),
    )

    list_display = (
        "title",
        "address",
        "tel",
        "region_title",
        "get_likes_count",
        "total_rating",
        "content_type",
    )

    list_filter = (
        "region",
        "region_sub",
        "cat_type",
    )

    search_fields = (
        "^region",
        "^region_sub",
        "^title",
        "^cat_type",
    )

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"

    def region_title(self, obj):
        print(obj)
        if obj.region_sub is not None:
            return f"{obj.region_sub.region.name} - {obj.region_sub.name}"
        else:
            return 0

    region_title.short_description = "Region"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    # mark_safe
    # html 코드를 직접 넣기 위한 방법
    # 위 기능을 사용하지 않으면 장고에서 html tag 및 script를 사용 못함
    # safety하기 때문에 (해킹 방지)
    def get_thumbnail(self, obj):
        return mark_safe('<img width="100px" src="{}"/>'.format(obj.url))

    get_thumbnail.short_description = "Thumbnail"
