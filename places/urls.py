from django.urls import path
from . import views

app_name = "places"

urlpatterns = [
    path("<int:pk>", views.PlaceFastivalDetail.as_view(), name="festival-detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]
