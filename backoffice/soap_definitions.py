# -*- coding: utf-8 -*-
from soaplib.core.model.clazz import ClassModel
from soaplib.core.model.primitive import String
from soaplib.core.model.clazz import Array

manufacturers = {
    'manufacturerA':{
        'endpoint':'http://localhost:7888/?wsdl',
        'address':'Rua de Camões, 99, Porto, Portugal'
    },
    'manufacturerB':{
        'endpoint':'http://localhost:7889/?wsdl',
        'address':'Avenida Dom Nuno Alvares Pereira, Almada, Portugal',
    },
    'manufacturerC':{
        'endpoint':'http://localhost:7890/?wsdl',
        'address':'Avenida da Republica, Faro, Portugal',
    },
}

carriers = {
    'carrierA':'http://localhost:7885/?wsdl',
    'carrierB':'http://localhost:7886/?wsdl',
    'carrierC':'http://localhost:7887/?wsdl',
}

class Order(ClassModel):
    __namespace__ = "order"
    name = String
    address = String
    tracks = Array(String)


class Auth(ClassModel):
    __namespace__ = "auth"
    user_id = String
    timestamp = String
    hmac = String
