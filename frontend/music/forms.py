# -*- coding: utf-8 -*-
from django import forms

class GetArtistForm(forms.Form):
    artist_name = forms.CharField(label="Artist Name", max_length=50)

class GetUserInfoForm(forms.Form):
    name = forms.CharField(label="Name", max_length = 50)
    address = forms.CharField(label="Address", max_length=175)
