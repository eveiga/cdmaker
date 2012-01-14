# -*- coding: utf-8 -*-
from base64 import standard_b64encode
from hashlib import sha1
import logging
import os
import sys

from sqlalchemy.orm import sessionmaker
import ujson

from models import Order, engine, create_table
from soap_client import ManufacturerClient, CarrierClient, FrontEndClient
from soap_definitions import manufacturers, carriers, frontend
from rest_client import GoogleMapsApiClient

pardir = os.path.abspath(os.path.pardir)
sys.path.append(pardir)
cdmaker = pardir.rsplit(os.path.sep)[-1]
from cdmaker.log import logger

logger.setLevel(logging.INFO)


def generate_hmac(self, *args):
    return standard_b64encode(
        sha1(u"-".join(args).encode("utf-8")).digest()
    )

def is_valid_request(auth):
    expected_hmac=generate_hmac(
        auth.user_id,
        auth.timestamp,
        "password",
    )

    return expected_hmac==auth.hmac

def create_budget(user_id, order_id, price):
    session = sessionmaker(bind=engine)()

    session.query(Order).filter_by(id=order_id).update(
        {"budget_%s"%(user_id,):price}
    )
    session.commit()

def verify_and_finalize_order(order_id):
    session = sessionmaker(bind=engine)()
    order = session.query(Order).filter_by(id=order_id).one()
    if order.has_all_data():
        # We have all the info we need to choose the best pair
        best_sum = 999999999

        for manufacturer in manufacturers.iterkeys():
            for carrier in carriers.iterkeys():
                budget_man = getattr(order, "budget_%s"%(manufacturer,))
                budget_car = getattr(order, "budget_%s"%(carrier,))

                distance = getattr(order, "distance_%s"%(manufacturer,))
                distance_footprint = ((distance*0.001)*0.26)/1000

                actual = sum([budget_man, budget_car, distance_footprint])
                if actual < best_sum:
                    best_sum = actual
                    best_manufacturer = manufacturer
                    best_carrier = carrier

        logger.info("Backoffice decided best pair: %s and %s. Lets notify both."%(
            best_manufacturer, best_carrier,
        ))
        Notificator(order_id).notificate_all(best_manufacturer, best_carrier)


class Notificator(object):
    def __init__(self, order_id):
        self.order_id = order_id

    def notificate_carrier(self, carrier):
        CarrierClient(
            carriers[carrier]
        ).confirmBudget(self.order_id)

    def notificate_manufacturer(self, manufacturer):
        ManufacturerClient(
            manufacturers[manufacturer]['endpoint']
        ).confirmBudget(self.order_id)

    def notificate_frontend(self, status):
        FrontEndClient(frontend).changeStatusOrder(self.order_id, status)

    def notificate_all(self, manufacturer, carrier):
        self.notificate_manufacturer(manufacturer)
        self.notificate_carrier(carrier)
        self.notificate_frontend(status="In Progress")


class OrderProcessor(object):
    def __init__(self):
        #Lets just assure table order is created
        create_table(engine)

    def create_order(self, name, address):
        new_order = Order(username=name, address=address)

        session = sessionmaker(bind=engine)()
        session.add(new_order)
        session.commit()

        self.order = new_order

        return new_order

    def process_order(self, tracks):
        def get_distance_from_json(distance_json):
            return ujson.decode(
                distance_json
            )['rows'][0]['elements'][0]['distance']['value']

        #Request manufacturers budget
        for value in manufacturers.itervalues():
            ManufacturerClient(value['endpoint']).getBudget(
                self.order.id,
                tracks,
            )

        #Request carriers budget
        for endpoint in carriers.itervalues():
            CarrierClient(endpoint).getBudget(
                self.order.id,
                self.order.username,
                self.order.address,
            )

        session = sessionmaker(bind=engine)()
        #Calculate distances between manufacturers and client address
        for manufacturer, values in manufacturers.iteritems():
            distance=get_distance_from_json(
                GoogleMapsApiClient().get_distance(
                    values['address'],
                    self.order.address,
                )
            )

            session.query(Order).filter_by(id=self.order.id).update(
                {"distance_%s"%(manufacturer,):distance}
            )

        session.commit()
