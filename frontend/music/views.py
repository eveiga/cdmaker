# -*- coding: utf-8 -*-
from django.views.generic import FormView, ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from music.forms import GetArtistForm
from music.services import MusicBackofficeClient

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

class ListArtistTracksView(ListView):
    template_name = 'list_artist_tracks.html'
    context_object_name = 'tracks'

    def _helper_track_info_dict(self, track):
        return {
            'name':track.get('name')
        }

    def get_queryset(self):
        tracks = MusicBackofficeClient().get_artist_tracks(self.args[0])

        return [
            self._helper_track_info_dict(track)
            for track
            in tracks['toptracks']['track']
        ]
