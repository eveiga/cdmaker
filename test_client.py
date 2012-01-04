# -*- coding: utf-8 -*-
from suds.client import Client

if __name__=='__main__':
    client = Client('http://localhost:7891/?wsdl')
    order = client.factory.create("ns0:Order")
    order.name = "Teste"
    order.address = "Morada 123"
    tracks = client.factory.create("stringArray")
    tracks.string=["abc","efg"]
    order.tracks = tracks

    result = client.service.submitOrder(order)

    print result
