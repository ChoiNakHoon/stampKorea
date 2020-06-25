from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    """ List Admin Definition """

    list_display = (
        "title",
        "user",
        "count_place",
    )

    search_fields = ("^title",)

    filter_horizontal = ("place",)
