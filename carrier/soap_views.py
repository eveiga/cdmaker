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
from soaplib.core import Application
from wsgiref.simple_server import make_server

pardir = os.path.abspath(os.path.pardir)
sys.path.append(pardir)
cdmaker = pardir.rsplit(os.path.sep)[-1]
from cdmaker.log import logger
from soap_client import BackofficeClient

logger.setLevel(logging.INFO)

def calculate_budget_price(order, address, user_id):
    sleep(2)

    #Get random price
    random_price = random.randint(1,10)
    logger.info("Calculated %d€ price"%(random_price,))

    #Send budget to backoffice callback endpoint
    BackofficeClient().get_budget_callback(order, random_price, user_id)

class BudgetService(DefinitionBase):
    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        super(BudgetService, self).__init__(*args, **kwargs)

    @soap(Integer, String, _returns=String)
    def getBudget(self, order, address):
        thread.start_new_thread(
            calculate_budget_price,
            (order, address, self.user_id,)
        )
        logger.info("Returning async request")
        return "OK"

if __name__=="__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    user_id_dict={
        '7885':'carrierA',
        '7886':'carrierB',
        '7887':'carrierC',
    }

    class BudgetApplication(Application):
        def get_service(self, service, *args, **kwargs):
            return service(user_id_dict.get(str(port)))

    soap_application = BudgetApplication([BudgetService], 'tns')
    wsgi_application = wsgi.Application(soap_application)
    server = make_server(host, port, wsgi_application)
    logger.info("Manufacturer serving on %s:%s"%(host,port,))
    server.serve_forever()
