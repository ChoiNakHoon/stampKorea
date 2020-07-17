from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("create/<int:place>/", views.create_review, name="create"),
]
