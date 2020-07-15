from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.core.paginator import Paginator
from places import models as places_models
from . import forms


class HomeView(ListView):

    """ Home View Definition """

    # 최대 보여지는 페이지를 n번으로 제한하고
    # 최대 보여지는 max_index에 도달하고 next하게 되면
    # n번으로 제한된 만큼 페이지가 보여진다.
    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     paginator = context["paginator"]
    #     # 보여지는 페이지 숫자
    #     page_numbers_range = 10
    #     max_index = len(paginator.page_range)

    #     page = self.request.GET.get("page")
    #     current_page = int(page) if page else 1

    #     start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    #     end_index = start_index + page_numbers_range
    #     if end_index >= max_index:
    #         end_index = max_index

    #     page_range = paginator.page_range[start_index:end_index]
    #     context["page_range"] = page_range
    #     return context
    def get(self, request):
        queryset = places_models.Place.objects.filter(content_type="85").order_by(
            "-created"
        )
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
            context={"places": places, "page_range": page_range},
        )


class PlaceDetailView(DetailView):

    """ Detail View Definition """

    model = places_models.Place


class SearchView(ListView):

    """ Search View Definition """

    def get(self, request):
        form = forms.SearchForm(request.GET)
        form.fields["city"].queryset = places_models.Sub_Region.objects.filter(
            region=request.GET.get("region")
        )
        if form.is_valid():

            region = form.cleaned_data.get("region")
            city = form.cleaned_data.get("city")
            cat_type = form.cleaned_data.get("cat_type")
            # filter
            filter_args = {}

            if region is not None:
                # filter_args에 filter할 key와 옵션을 기입
                filter_args["region__name__istartswith"] = region

            if city is not None:
                filter_args["region_sub__name__istartswith"] = city

            if cat_type is not None:
                filter_args["cat_type"] = cat_type

            queryset = places_models.Place.objects.filter(**filter_args).order_by(
                "-created"
            )

            paginator = Paginator(queryset, 12, orphans=1)

            page = request.GET.get("page", 1)

            places = paginator.get_page(page)

            page_numbers_range = 10

            max_index = len(paginator.page_range)

            current_page = int(page) if page else 1

            start_index = (
                int((current_page - 1) / page_numbers_range) * page_numbers_range
            )
            end_index = start_index + page_numbers_range
            if end_index >= max_index:
                end_index = max_index

            page_range = paginator.page_range[start_index:end_index]

            return render(
                request,
                "places/search.html",
                context={"form": form, "places": places, "page_range": page_range},
            )

        else:
            form = forms.SearchForm()

        return render(request, "places/search.html", context={"form": form})

