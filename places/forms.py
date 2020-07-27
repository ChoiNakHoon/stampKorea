from django import forms
from . import models


class SearchForm(forms.Form):

    """ Search Form Definition """

    search = forms.CharField()

