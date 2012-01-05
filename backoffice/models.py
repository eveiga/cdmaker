# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine


Base = declarative_base()

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    address = Column(String)
    budget_carrierA = Column(Integer)
    budget_carrierB = Column(Integer)
    budget_carrierC = Column(Integer)
    budget_manufacturerA = Column(Integer)
    budget_manufacturerB = Column(Integer)
    budget_manufacturerC = Column(Integer)
    distance_manufacturerA = Column(Integer)
    distance_manufacturerB = Column(Integer)
    distance_manufacturerC = Column(Integer)


engine = create_engine('sqlite:///backoffice/orders.db', echo=True)

create_table = lambda engine: Base.metadata.create_all(engine)
