# -*- coding: utf-8 -*-
from base64 import standard_b64encode
from hashlib import sha1
from datetime import datetime

from suds.client import Client

from soap_definitions import user_id

def generate_hmac(self, *args):
    return standard_b64encode(
        sha1(u"-".join(args).encode("utf-8")).digest()
    )

from_dt_to_ts = lambda dt: dt.strftime("%Y%m%d%H%M%S")

class BaseSoapClient(object):
    def __init__(self, endpoint):
        self.client = Client(endpoint)

    def get_auth_instance(self):
        now = datetime.now()

        auth = self.client.factory.create("ns0:Auth")
        auth.user_id = user_id
        auth.timestamp = from_dt_to_ts(now)
        auth.hmac = generate_hmac(
            user_id,
            from_dt_to_ts(now),
            "password",
        )

        return auth


class ManufacturerClient(BaseSoapClient):
    def getBudget(self, order, tracks):
        self.client.service.getBudget(order, tracks, self.get_auth_instance())

    def confirmBudget(self, order_id):
        self.client.service.confirmBudget(order_id, self.get_auth_instance())


class CarrierClient(BaseSoapClient):
    def getBudget(self, order, name, address):
        self.client.service.getBudget(order, name, address, self.get_auth_instance())

    def confirmBudget(self, order_id):
        self.client.service.confirmBudget(order_id, self.get_auth_instance())


class FrontEndClient(BaseSoapClient):
    def changeStatusOrder(self, order_id):
        self.client.service.changeStatusOrder(order_id, "Processed")
