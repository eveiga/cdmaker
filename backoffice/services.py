# -*- coding: utf-8 -*-
import ujson
from base64 import standard_b64encode
from hashlib import sha1

from sqlalchemy.orm import sessionmaker

from models import Order, engine, create_table
from soap_client import ManufacturerClient, CarrierClient
from soap_definitions import manufacturers, carriers
from rest_client import GoogleMapsApiClient

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
