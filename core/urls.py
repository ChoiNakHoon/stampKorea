from django.urls import path
from places import views as places_views

app_name = "core"

urlpatterns = [
    path("", places_views.HomeView.as_view(), name="home"),
]
