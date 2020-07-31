from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, place):
    user = context.request.user
    _list = context.get("lists")
    the_list = list_models.List.objects.get(user=user, title=_list)
    if the_list is not None:
        return place in the_list.place.all()
    else:
        return False
