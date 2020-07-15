from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, place):
    user = context.request.user
    the_list = list_models.List.objects.get(user=user, name="My Favourites Houses")
    if the_list is not None:
        return place in the_list.places.all()
    else:
        return False
