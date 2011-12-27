# -*- coding: utf-8 -*-
from urllib import quote

import ujson

from suds.client import Client


class MusicBackofficeClient(object):
    def __init__(self):
        self.client = Client('http://localhost:7891/?wsdl')

    def search_artist(self, artist_name):
        return ujson.decode(
            self.client.service.searchArtist(quote(artist_name))
        )

    def get_artist_tracks(self, artist_name):
        return ujson.decode(
            self.client.service.getTracks(quote(artist_name))
        )
