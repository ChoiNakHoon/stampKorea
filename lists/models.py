from django.db import models
from core import models as core_models
from places import models as place_models


class List(core_models.TimeStampedModel):
    """ List Model Definition """

    title = models.CharField(max_length=120)
    user = models.ForeignKey(
        "users.User", related_name="lists", on_delete=models.CASCADE
    )
    place = models.ManyToManyField("places.Place", related_name="lists", blank=True)

    def __str__(self):
        return self.title

    def count_place(self):
        return self.place.count()

    count_place.short_description = "Number of Trips"

    def get_first_thumbnail(self):
        for place in self.place.all():
            _place = place_models.Place.objects.get(pk=place.pk)
        try:
            (photo,) = _place.photos.all()[:1]
            return photo.url
        except ValueError:
            return None
