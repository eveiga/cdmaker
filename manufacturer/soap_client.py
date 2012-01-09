# -*- coding: utf-8 -*-
from suds.client import Client

class BackofficeClient(object):
    def __init__(self):
        self.client = Client('http://localhost:7891/?wsdl')

    def get_budget_callback(self, order, price):
        self.client.service.getBudgetResponse(order, price)
