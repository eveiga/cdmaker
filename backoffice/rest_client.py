# -*- coding: utf-8 -*-
from urllib import urlencode

import httplib2


class RestClient(object):
    def __init__(self):
        self.http = httplib2.Http()

    def make_request(self, url, **params):
        return self.http.request(
            url+'?'+urlencode(params)
        )

class LastFMClient(RestClient):
    base_url =  "http://ws.audioscrobbler.com/2.0/"

    api_key = "113fcbb3c49001c4be4d8a4ab0ab215e"
    api_secret = "e5f7958361f9adde7c8919bf261e72aa"

    def getArtists(self, artist_name):
        response, content = self.make_request(
            url=self.base_url,
            api_key=self.api_key,
            artist=artist_name,
            format="json",
            method="artist.search",
        )

        return content

    def getArtistTracks(self, artist_name):
        response, content = self.make_request(
            url = self.base_url,
            api_key=self.api_key,
            format="json",
            artist=artist_name,
            method="artist.gettoptracks",
        )

        return content


class GoogleMapsApiClient(RestClient):
    base_url = "http://maps.googleapis.com/maps/api/distancematrix/json"

    def get_distance(self, origin, destiny):
        response, content = self.make_request(
            url=self.base_url,
            language='pt-PT',
            sensor='false',
            origins=origin,
            destinations=destiny,
        )

        return content
