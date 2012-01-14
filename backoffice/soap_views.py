# -*- coding: utf-8 -*-
import thread
import logging
import sys
from urllib import unquote

from soaplib.core.service import soap, DefinitionBase
from soaplib.core.server import wsgi
from soaplib.core.model.primitive import String, Integer
from soaplib.core import Application
from wsgiref.simple_server import make_server

sys.path.append("..")
from cdmaker.log import logger
from rest_client import LastFMClient
from soap_definitions import Order, Auth
from services import (OrderProcessor, is_valid_request, create_budget,
    verify_and_finalize_order, Notificator)

logger.setLevel(logging.INFO)


class MusicService(DefinitionBase):
    @soap(String, Auth, _returns=String)
    def searchArtist(self, artist_name, auth):
        if is_valid_request(auth):
            response = LastFMClient().getArtists(unquote(artist_name))
            logger.info("Backoffice: Returning request for artist search")
            return response

    @soap(String, Auth, _returns=String)
    def getTracks(self, artist_name, auth):
        if is_valid_request(auth):
            response = LastFMClient().getArtistTracks(unquote(artist_name))
            logger.info("Backoffice: Returning request for tracks search")
            return response


class OrderService(DefinitionBase):
    @soap(Order,  Auth, _returns=Integer)
    def submitOrder(self, order, auth):
        if is_valid_request(auth):
            #persist the new order
            processor = OrderProcessor()
            new_order = processor.create_order(order.name, order.address)

            #create thread and process order
            thread.start_new_thread(
                processor.process_order,
                (order.tracks,),
            )

            #return the order unique id
            logger.info("Backoffice: Returning async request for submit order")
            return new_order.id

    @soap(Integer, Integer, Auth, _returns=String)
    def getBudgetResponse(self, order, price, auth):
        if is_valid_request(auth):
            create_budget(auth.user_id, order, price)
            verify_and_finalize_order(order)

    @soap(Integer, String, Auth, _returns=String)
    def setStatusOrder(self, order, status, auth):
        if is_valid_request(auth):
            Notificator(order).notificate_frontend(status)
            return "OK"

if __name__=="__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    soap_application = Application([MusicService, OrderService], 'tns')
    wsgi_application = wsgi.Application(soap_application)
    server = make_server(host, port, wsgi_application)
    logger.info("Backoffice serving on %s:%s"%(host,port,))
    server.serve_forever()
