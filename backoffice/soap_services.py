# -*- coding: utf-8 -*-
import thread
import logging
import sys
from urllib import unquote

from soaplib.core.service import soap, DefinitionBase
from soaplib.core.server import wsgi
from soaplib.core.model.primitive import String
from soaplib.core import Application
from wsgiref.simple_server import make_server

sys.path.append("..")
from cdmaker.log import logger
from lastfm_client import LastFMClient

logger.setLevel(logging.INFO)

class MusicService(DefinitionBase):
    @soap(String, _returns=String)
    def searchArtist(self, artist_name):
        response = LastFMClient().getArtists(artist_name)
        logger.info("Backoffice: Returning request for artist search")
        return response


    @soap(String, _returns=String)
    def getTracks(self, artist_name):
        response = LastFMClient().getArtistTracks(unquote(artist_name))
        logger.info("Backoffice: Returning request for tracks search")
        return response

class OrderService(DefinitionBase):
    pass


if __name__=="__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    soap_application = Application([MusicService, OrderService], 'tns')
    wsgi_application = wsgi.Application(soap_application)
    server = make_server(host, port, wsgi_application)
    logger.info("Backoffice serving on %s:%s"%(host,port,))
    server.serve_forever()
