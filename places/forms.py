from django import forms
from . import models


class SearchForm(forms.Form):

    """ Search Form Definition """

    search = forms.CharField()
    # region = forms.ModelChoiceField(
    #     required=False, queryset=models.Region.objects.all()
    # )
    # city = forms.ModelChoiceField(
    #     required=False, queryset=models.Sub_Region.objects.all(),
    # )
    # cat_type = forms.ModelChoiceField(
    #     required=False, empty_label="Any Kind", queryset=models.Cat_Type.objects.all()
    # )

