# -*- coding: utf-8 -*-
from urllib import quote
from base64 import standard_b64encode
from hashlib import sha1
from datetime import datetime

import ujson
from django.conf import settings

from suds.client import Client

def generate_hmac(self, *args):
    return standard_b64encode(
        sha1(u"-".join(args).encode("utf-8")).digest()
    )

from_dt_to_ts = lambda dt: dt.strftime("%Y%m%d%H%M%S")

class BackofficeClient(object):
    def __init__(self):
        self.client = Client('http://localhost:7891/?wsdl')

    def get_auth_instance(self):
        now = datetime.now()

        auth = self.client.factory.create("ns0:Auth")
        auth.user_id = settings.USER_ID
        auth.timestamp = from_dt_to_ts(now)
        auth.hmac = generate_hmac(
            settings.USER_ID,
            from_dt_to_ts(now),
            "password",
        )

        return auth


class MusicBackofficeClient(BackofficeClient):
    def search_artist(self, artist_name):
        return ujson.decode(
            self.client.service.searchArtist(
                quote(artist_name),
                self.get_auth_instance(),
            )
        )

    def get_artist_tracks(self, artist_name):
        return ujson.decode(
            self.client.service.getTracks(
                quote(
                    artist_name
                ),
                self.get_auth_instance(),
            )
        )


class OrderBackofficeClient(BackofficeClient):
    def submit_order(self, selected_tracks, user_name, address):
        order = self.client.factory.create("ns1:Order")

        order.name = user_name
        order.address = address
        tracks = self.client.factory.create("stringArray")
        tracks.string = selected_tracks
        order.tracks = tracks

        return self.client.service.submitOrder(
            order,
            self.get_auth_instance(),
        )
