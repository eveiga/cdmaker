# -*- coding: utf-8 -*-
from base64 import standard_b64encode
from hashlib import sha1
from datetime import datetime

from suds.client import Client

def generate_hmac(self, *args):
    return standard_b64encode(
        sha1(u"-".join(args).encode("utf-8")).digest()
    )

from_dt_to_ts = lambda dt: dt.strftime("%Y%m%d%H%M%S")

class BackofficeClient(object):
    def __init__(self):
        self.client = Client('http://localhost:7891/?wsdl')

    def get_budget_callback(self, order, price, user_id):
        auth = self.client.factory.create("ns0:Auth")
        now = datetime.now()

        auth.user_id = user_id
        auth.timestamp = from_dt_to_ts(now)
        auth.hmac = generate_hmac(user_id, from_dt_to_ts(now), "password")

        self.client.service.getBudgetResponse(order, price, auth)
