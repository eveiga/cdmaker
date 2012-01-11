# -*- coding: utf-8 -*-
from soaplib.core.model.clazz import ClassModel
from soaplib.core.model.primitive import String


class Auth(ClassModel):
    __namespace__ = "auth"
    user_id = String
    timestamp = String
    hmac = String
