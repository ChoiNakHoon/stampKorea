from django import forms
from . import models


class CreateListForm(forms.ModelForm):

    """ Create Lists Form Definition """

    class Meta:
        model = models.List
        fields = ("title",)

    def save(self):
        lists = super().save(commit=False)
        return lists
