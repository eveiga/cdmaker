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
from soap_client import BackofficeClient

logger.setLevel(logging.INFO)

def calculate_budget_price(order, address):
    sleep(2)

    #Get random price
    random_price = random.randint(1,10)
    logger.info("Calculated %d€ price"%(random_price,))

    #Send budget to backoffice callback endpoint
    BackofficeClient().get_budget_callback(order, random_price)

class BudgetService(DefinitionBase):
    @soap(Integer, String, _returns=String)
    def getBudget(self, order, address):
        thread.start_new_thread(calculate_budget_price, (order, address,))
        logger.info("Returning async request")
        return "OK"

if __name__=="__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    soap_application = Application([BudgetService], 'tns')
    wsgi_application = wsgi.Application(soap_application)
    server = make_server(host, port, wsgi_application)
    logger.info("Manufacturer serving on %s:%s"%(host,port,))
    server.serve_forever()
