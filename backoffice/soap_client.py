# -*- coding: utf-8 -*-
from base64 import standard_b64encode
from hashlib import sha1
from datetime import datetime
import sys
import os
import logging

from suds.client import Client

from soap_definitions import user_id
pardir = os.path.abspath(os.path.pardir)
sys.path.append(pardir)
cdmaker = pardir.rsplit(os.path.sep)[-1]
from cdmaker.log import logger

logger.setLevel(logging.INFO)

def generate_hmac(self, *args):
    return standard_b64encode(
        sha1(u"-".join(args).encode("utf-8")).digest()
    )

from_dt_to_ts = lambda dt: dt.strftime("%Y%m%d%H%M%S")

class BaseSoapClient(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint
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
        logger.info("Backoffice asking %s for a budget"%(self.endpoint,))
        self.client.service.getBudget(order, tracks, self.get_auth_instance())

    def confirmBudget(self, order_id):
        logger.info("Backoffice confirming %s budget"%(self.endpoint,))
        self.client.service.confirmBudget(order_id, self.get_auth_instance())


class CarrierClient(BaseSoapClient):
    def getBudget(self, order, name, address):
        logger.info("Backoffice confirming %s budget"%(self.endpoint,))
        self.client.service.getBudget(order, name, address, self.get_auth_instance())

    def confirmBudget(self, order_id):
        logger.info("Backoffice confirming %s budget"%(self.endpoint,))
        self.client.service.confirmBudget(order_id, self.get_auth_instance())


class FrontEndClient(BaseSoapClient):
    def changeStatusOrder(self, order_id):
        logger.info("Backoffice informing frontend of change order status")
        self.client.service.changeStatusOrder(order_id, "Processed")
