from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    RATING_DEFAULT = 0
    RATING_ONE = 1
    RATING_TWO = 2
    RATING_THREE = 3
    RATING_FOUR = 4
    RATING_FIVE = 5

    RATING_CHOICES = (
        (RATING_DEFAULT, "I need some help!"),
        (RATING_ONE, "I'm really upset"),
        (RATING_TWO, "I've got a problem"),
        (RATING_THREE, "Things are pretty good"),
        (RATING_FOUR, "Feeling Great!"),
        (RATING_FIVE, "Fantistic"),
    )

    review = models.TextField()
    accuracy = models.IntegerField(choices=RATING_CHOICES, default=RATING_FIVE)
    safety = models.IntegerField(choices=RATING_CHOICES, default=RATING_FIVE)
    communication = models.IntegerField(choices=RATING_CHOICES, default=RATING_FIVE)
    location = models.IntegerField(choices=RATING_CHOICES, default=RATING_FIVE)
    value = models.IntegerField(choices=RATING_CHOICES, default=RATING_FIVE)
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    place = models.ForeignKey(
        "places.Place", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.place.title} :: {self.user.username}"

    # 평균 평점
    def rating_avg(self):
        avg = (
            self.accuracy
            + self.safety
            + self.communication
            + self.location
            + self.value
        ) / 5
        return round(avg, 2)

    class Meta:
        ordering = ("-created",)
