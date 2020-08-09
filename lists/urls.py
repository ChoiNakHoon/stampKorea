from django.urls import path
from lists import views

app_name = "lists"

urlpatterns = [
    path("create-list/<int:place>/", views.create_list, name="create-list"),
    path("add-list/<int:place>/<str:title>", views.add_list, name="add-list"),
    path("trip-list/", views.TripListView.as_view(), name="trip-list"),
]
