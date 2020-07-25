from django import template
from places import models as places_models

register = template.Library()


@register.simple_tag
def get_region():

    search = []
    search += places_models.Region.objects.all()

    return search
