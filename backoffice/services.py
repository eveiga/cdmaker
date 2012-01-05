# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker

from models import Order, engine, create_table


class OrderProcessor(object):
    def __init__(self):
        #Lets just assure table order is created
        create_table(engine)

        #Create sqlalchemy session
        self.session = sessionmaker(bind=engine)()

    def create_order(self, name, address):
        new_order = Order(username=name, address=address)
        self.session.add(new_order)
        self.session.commit()

        return new_order.id

    def process_order(self, tracks):
        pass
