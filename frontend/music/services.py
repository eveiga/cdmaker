# -*- coding: utf-8 -*-
from urllib import quote

import ujson

from suds.client import Client

class BackofficeClient(object):
    def __init__(self):
        self.client = Client('http://localhost:7891/?wsdl')


class MusicBackofficeClient(BackofficeClient):
    def search_artist(self, artist_name):
        return ujson.decode(
            self.client.service.searchArtist(quote(artist_name))
        )

    def get_artist_tracks(self, artist_name):
        return ujson.decode(
            self.client.service.getTracks(quote(artist_name))
        )


class OrderBackofficeClient(BackofficeClient):
    def submit_order(self, tracks, user_name, address):
        user_data = self.client.factory.create('User')
        user_data.name = user_name
        user_data.address = address
