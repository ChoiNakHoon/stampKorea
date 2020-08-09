from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Q
from places import models as place_models
from lists import models as lists_models
from . import forms


def create_list(request, place):
    title = request.POST.get("title", None)
    """ Create lists Definition """
    if request.method == "POST":
        form = forms.CreateListForm(request.POST)
        place = place_models.Place.objects.get(pk=place)
        print(f"create_list : {title}")
        if not place:
            return redirect(reverse("core:home"))
        if form.is_valid():
            # _lists = lists_models.List.objects.filter(user=request.user, title=title)
            # if _lists is None:
            lists = form.save()
            lists.user = request.user
            lists.save()
            lists.place.add(place)
            place.likes.add(request.user)
            messages.success(request, "Success List Saved")
            # else:
            #     messages.warning(request, "Lists Exisits")
            #     print("존재합니다.")
            return redirect(reverse("places:detail", kwargs={"pk": place.pk}))


def add_list(request, place, title):
    action = request.GET.get("action", None)
    place = place_models.Place.objects.get(pk=place)
    if place is not None and action is not None:
        the_list, _ = lists_models.List.objects.get_or_create(
            user=request.user, title=title
        )
        if action == "add":
            the_list.place.add(place)
            place.likes.add(request.user)
        elif action == "remove":
            the_list.place.remove(place)
            place.likes.remove(request.user)

    return redirect(reverse("places:detail", kwargs={"pk": place.pk}))


class TripListView(TemplateView):
    """ SeeFav View Definition """

    template_name = "lists/list.html"
