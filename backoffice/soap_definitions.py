# -*- coding: utf-8 -*-
from soaplib.core.model.clazz import ClassModel
from soaplib.core.model.primitive import String
from soaplib.core.model.clazz import Array

class Order(ClassModel):
    __namespace__ = "order"
    name = String
    address = String
    tracks = Array(String)
