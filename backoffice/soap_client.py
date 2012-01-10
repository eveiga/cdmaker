# -*- coding: utf-8 -*-
from suds.client import Client


class BaseSoapClient(object):
    def __init__(self, endpoint):
        self.endpoint=endpoint

    @property
    def client(self):
        return Client(self.endpoint)

class ManufacturerClient(BaseSoapClient):
    def getBudget(self, order, tracks):
        self.client.service.getBudget(order, tracks)

    def confirmBudget(self, order_id):
        pass


class CarrierClient(BaseSoapClient):
    def getBudget(self, order, name, address):
        self.client.service.getBudget(order, name, address)

    def confirmBudget(self, order_id):
        pass
