from django.shortcuts import redirect, reverse
from django.contrib import messages
from places import models as place_models
from . import forms


def create_review(request, place):

    """ Create Reviews Definition """
    print("여기 리뷰입니다.")
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        place = place_models.Place.objects.get(pk=place)
        if not place:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.place = place
            review.user = request.user
            review.save()
            messages.success(request, "Success Reviewed")
            return redirect(reverse("places:detail", kwargs={"pk": place.pk}))


# Create your views here.
