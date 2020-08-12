from django import forms
from . import models


class SearchForm(forms.Form):

    """ Search Form Definition """

    search = forms.CharField(required=False, initial="Seoul")
    cat_type = forms.ModelChoiceField(
        required=False, queryset=models.Cat_Type.objects.all()
    )

