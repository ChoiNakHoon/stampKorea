import random
import json
from django.views.generic import ListView, View
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from places import models as places_models
from reviews import forms as reviews_forms
from lists import forms as lists_forms
from . import forms


class HomeView(ListView):

    """ Home View Definition """

    # 최대 보여지는 페이지를 n번으로 제한하고
    # 최대 보여지는 max_index에 도달하고 next하게 되면
    # n번으로 제한된 만큼 페이지가 보여진다.
    def get(self, request):

        queryset = places_models.Place.objects.filter(
            Q(content_type="85") & Q(photos__isnull=False)
        ).order_by("-created")

        bList = list(queryset)
        fastival_list = random.sample(bList, 5)

        paginator = Paginator(queryset, 12, orphans=1)

        page = request.GET.get("page", 1)

        places = paginator.get_page(page)

        page_numbers_range = 10

        max_index = len(paginator.page_range)

        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]

        return render(
            request,
            "places/places_list.html",
            context={
                "places": places,
                "page_range": page_range,
                "fastival_list": fastival_list,
            },
        )


class PlaceDetailView(View):

    """ Detail View Definition """

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        place = places_models.Place.objects.get(pk=pk)
        form = reviews_forms.CreateReviewForm()
        list_form = lists_forms.CreateListForm()
        if place.content_type == "85":
            return render(
                self.request,
                "places/place_detail.html",
                context={"place": place, "form": form, "list_form": list_form},
            )
        elif place.content_type == "76":
            return render(
                self.request,
                "places/place_nature_detail.html",
                context={"place": place, "form": form, "list_form": list_form},
            )
        elif place.content_type == "78":
            return render(
                self.request,
                "places/place_culture_detail.html",
                context={"place": place, "form": form, "list_form": list_form},
            )
        elif place.content_type == "75":
            return render(
                self.request,
                "places/place_sports_detail.html",
                context={"place": place, "form": form, "list_form": list_form},
            )
        elif place.content_type == "80":
            return render(
                self.request,
                "places/place_accommodation_detail.html",
                context={"place": place, "form": form, "list_form": list_form},
            )
        elif place.content_type == "82":
            return render(
                self.request,
                "places/place_cuisine_detail.html",
                context={"place": place, "form": form, "list_form": list_form},
            )
        elif place.content_type == "79":
            return render(
                self.request,
                "places/place_shopping_detail.html",
                context={"place": place, "form": form, "list_form": list_form},
            )
        elif place.content_type == "77":
            return render(
                self.request,
                "places/place_transportation_detail.html",
                context={"place": place, "form": form, "list_form": list_form},
            )
        else:
            return render(
                self.request, "places/places_list.html", context={"place": place,},
            )


class SearchView(ListView):

    """ Search View Definition """

    def get(self, request):
        form = forms.SearchForm(request.GET)
        word = "%s" % self.request.GET["search"]  # 검색어
        result_word = word.capitalize()

        if form.is_valid():

            cat_type = form.cleaned_data.get("cat_type")

            queryset = places_models.Place.objects.filter(
                Q(
                    Q(region__name__contains=result_word)
                    | Q(region_sub__name__contains=result_word)
                    | Q(cat_type__name__contains=result_word)
                )
                & Q(photos__isnull=False)
            ).distinct()

            if cat_type is not None:
                queryset = queryset.filter(cat_type=cat_type)
            queryset.values()

            paginator = Paginator(queryset, 12, orphans=1)

            page = request.GET.get("page", 1)

            places = paginator.get_page(page)

            page_numbers_range = 7

            max_index = len(paginator.page_range)

            current_page = int(page) if page else 1

            start_index = (
                int((current_page - 1) / page_numbers_range) * page_numbers_range
            )
            end_index = start_index + page_numbers_range
            if end_index >= max_index:
                end_index = max_index

            page_range = paginator.page_range[start_index:end_index]

            locations = [
                [l.title, l.address, l.cat_type.name, l.mapx, l.mapy, i]
                for i, l in enumerate(places)
            ]
            return render(
                request,
                "places/search.html",
                context={
                    "form": form,
                    "places": places,
                    "page_range": page_range,
                    "word": word,
                    "cat_type": cat_type,
                    "locations": locations,
                },
            )

        else:
            form = forms.SearchForm()

        return render(
            request, "places/search.html", context={"form": form, "word": word,},
        )

