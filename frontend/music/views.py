# -*- coding: utf-8 -*-
from soaplib.core.service import soap, DefinitionBase
from soaplib.core.model.primitive import String, Integer
from soaplib.core import Application
from django.views.generic import FormView, ListView, TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from music.forms import GetArtistForm, GetUserInfoForm
from music.services import MusicBackofficeClient, OrderBackofficeClient
from soap_handler import DjangoSOAPAdaptor

class GetArtistsView(FormView):
    template_name = 'get_artists.html'
    form_class = GetArtistForm

    def form_valid(self, form):
        artist_name = form.cleaned_data['artist_name']

        return HttpResponseRedirect(
            reverse('list_artists', args=[artist_name])
        )


class ListArtistsView(ListView):
    template_name = 'list_artists.html'
    context_object_name = 'artists'

    def _helper_artist_info_dict(self, artist):
        return {
            'name':artist.get('name'),
            'image':artist.get('image')[1].get('#text'),
            'url':reverse('list_artist_tracks', args=[artist.get('name')]),
        }

    def get_queryset(self):
        artists = MusicBackofficeClient().search_artist(self.args[0])

        return [
            self._helper_artist_info_dict(artist)
            for artist
            in artists['results']['artistmatches']['artist']
        ]


class ListArtistTracksView(FormView):
    template_name = 'list_artist_tracks.html'
    context_object_name = 'tracks'
    form_class = GetUserInfoForm

    def form_valid(self, form):
        user_name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        blacklist = ['name','address','csrfmiddlewaretoken']
        tracks = [f for f in form.data.keys() if f not in blacklist]

        msg = OrderBackofficeClient().submit_order(tracks, user_name, address)

        return HttpResponseRedirect(
            reverse('checkout', args=[msg])
        )

    def _helper_track_info_dict(self, track):
        return {
            'name':track.get('name')
        }

    def get_context_data(self, **kwargs):
        tracks = MusicBackofficeClient().get_artist_tracks(self.args[0])

        new_tracks = [
            self._helper_track_info_dict(track)
            for track
            in tracks['toptracks']['track']
        ]

        kwargs['tracks'] = new_tracks

        return kwargs


class CheckoutView(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        kwargs['uri_index'] = reverse('index')
        kwargs['order_id'] = self.args[0]
        return kwargs


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs['uri_artists'] = reverse('get_artists')
        return kwargs


class OrderStatusService(DefinitionBase):
    @soap(Integer, String, _returns=String)
    def changeStatusOrder(self, order, status):
        return "OK"


orderstatus_service = DjangoSOAPAdaptor(
    Application(
        [OrderStatusService], 'tns'
    )
)
