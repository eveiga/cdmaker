# -*- coding: utf-8 -*-
import logging
import sys
import os

from base64 import standard_b64encode
from hashlib import sha1
from datetime import datetime

from suds.client import Client

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

class BackofficeClient(object):
    def __init__(self):
        self.client = Client('http://localhost:7891/?wsdl')

    def get_auth(self, user_id):
        auth = self.client.factory.create("ns0:Auth")
        now = datetime.now()

        auth.user_id = user_id
        auth.timestamp = from_dt_to_ts(now)
        auth.hmac = generate_hmac(user_id, from_dt_to_ts(now), "password")

        return auth

    def get_budget_callback(self, order, price, user_id):
        logger.info("%s Sending %d€ for as getBudgetResponse"%(user_id, price,))
        self.client.service.getBudgetResponse(
            order,
            price,
            self.get_auth(user_id),
        )

    def set_status_order(self, order, status, user_id):
        logger.info("%s Sending %s as status for order number %d"%(
            user_id,
            status,
            order,)
        )

        self.client.service.setStatusOrder(
            order,
            status,
            self.get_auth(user_id),
        )
