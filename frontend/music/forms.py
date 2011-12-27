# -*- coding: utf-8 -*-
from django import forms

class GetArtistForm(forms.Form):
    artist_name = forms.CharField(label="Artist Name", max_length=50)
