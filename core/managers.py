from django.db import models


class CustomModelManager(models.Manager):

    """ Custom Model Manager Definition"""

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
