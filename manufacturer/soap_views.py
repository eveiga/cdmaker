# -*- coding: utf-8 -*-
import thread
import random
import logging
import sys
import os
from time import sleep

from soaplib.core.service import soap, DefinitionBase
from soaplib.core.server import wsgi
from soaplib.core.model.primitive import String, Integer
from soaplib.core.model.clazz import Array
from soaplib.core import Application
from wsgiref.simple_server import make_server

pardir = os.path.abspath(os.path.pardir)
sys.path.append(pardir)
cdmaker = pardir.rsplit(os.path.sep)[-1]
from cdmaker.log import logger
from soap_client import BackofficeClient, generate_hmac
from soap_definitions import Auth

logger.setLevel(logging.INFO)


def is_valid_request(auth):
    expected_hmac=generate_hmac(
        auth.user_id,
        auth.timestamp,
        "password",
    )

    return expected_hmac==auth.hmac

def calculate_budget_price(order, tracks, user_id):
    sleep(5)

    #Get random price
    random_price = random.randint(1,10)

    #Send budget to backoffice callback endpoint
    BackofficeClient().get_budget_callback(order, random_price, user_id,)

def set_status_order(order, user_id):
    sleep(5)

    BackofficeClient().set_status_order(order, "Processed", user_id,)

class BudgetService(DefinitionBase):
    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super(BudgetService, self).__init__(*args, **kwargs)

    @soap(Integer, Array(String), Auth, _returns=String)
    def getBudget(self, order, tracks, auth):
        if is_valid_request(auth):
            thread.start_new_thread(
                calculate_budget_price,
                (order, tracks, self.user_id,)
            )
            logger.info("%s Returning async request for getBudget"%(self.user_id,))
            return "OK"

    @soap(Integer, Auth, _returns=String)
    def confirmBudget(self, order, auth):
        if is_valid_request(auth):
            thread.start_new_thread(
                set_status_order,
                (order, self.user_id,)
            )
            logger.info("%s Returning async request for confirmBudget"%(self.user_id,))
            return "OK"


if __name__=="__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    user_id_dict={
        '7888':'manufacturerA',
        '7889':'manufacturerB',
        '7890':'manufacturerC',
    }

    class BudgetApplication(Application):
        def get_service(self, service, *args, **kwargs):
            return service(user_id_dict.get(str(port)))

    soap_application = BudgetApplication([BudgetService], 'tns')
    wsgi_application = wsgi.Application(soap_application)
    server = make_server(host, port, wsgi_application)
    logger.info("Manufacturer serving on %s:%s"%(host,port,))
    server.serve_forever()
