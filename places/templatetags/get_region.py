from django import template
from django.db.models import Q
from places import models as places_models

register = template.Library()


@register.simple_tag
def get_region():

    search = []
    search += places_models.Region.objects.all()
    for i in range(31, 39):
        search += places_models.Sub_Region.objects.filter(region__code=f"{i}")

    return search
