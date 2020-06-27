from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from . import models


@admin.register(models.Cat_Type, models.Region, models.Sub_Region)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    pass


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
                    "region_sub",
                    "cat_type",
                )
            },
        ),
        ("Times", {"fields": ("created_time", "updated_time",)}),
        (
            "Introduction Info",
            {"fields": ("info_center", "parking", "rest_date", "use_time",)},
        ),
        ("Other", {"fields": ("likes",)}),
    )

    list_display = (
        "title",
        "address",
        "tel",
        "region_title",
        "info_center",
        "parking",
        "rest_date",
        "use_time",
        "get_likes_count",
        "total_rating",
    )

    list_filter = (
        "region",
        "region_sub",
        "cat_type",
    )

    search_fields = ("^region", "^region_sub", "^title", "^cat_type")

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"

    def region_title(self, obj):
        print(obj)
        return f"{obj.region_sub.region.name} - {obj.region_sub.name}"

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
        return mark_safe('<img width="100px" src="{}"/>'.format(obj.file.url))

    get_thumbnail.short_description = "Thumbnail"
