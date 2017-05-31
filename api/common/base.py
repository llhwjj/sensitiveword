#!/usr/bin/env python
# _*_ coding: utf-8 _*_

# Author: liulonghui(liulonghui@gochinatv.com)
# Copyright 2017 GoChinaTV

from uuid import UUID
from datetime import datetime, date
import time

from flask import make_response
from flask import jsonify

from api import app
from urllib.parse import urlparse

# URL_CONFIG = urlparse(app.config['SQLALCHEMY_DATABASE_URI'])


def extended_encoder(x):
    if isinstance(x, datetime):
        return int(x.timestamp())
    if isinstance(x, UUID):
        return str(x)
    if isinstance(x, date):
        return x.isoformat()
    return x


class BaseResponse():
    data = {}
    status = 200
    message = ""
    version = 0

    def __init__(self, data={}, status=200, message=""):
        self.data = data
        self.status = status
        self.message = message,
        self.version = int(time.time())

    def to_dict(self, rel=None, backref=None):
        item = self.__dict__
        item['message'] = item['message'][0]
        return item

    @classmethod
    def return_response(cls, data={}, status=200, message="", headers={}):
        res = cls(
            data=data,
            status=status,
            message=message
        ).to_dict()
        return make_response(jsonify(res), status, headers)

    @classmethod
    def return_success(cls, data={}):
        return cls.return_response(data)

    @classmethod
    def return_error(cls, status, message):
        return cls.return_response(status=status, message=message)

    @classmethod
    def return_internal_server_error(cls, message='Internal Server Error'):
        return cls.return_response(status=500, message=message)

    @classmethod
    def return_unauthorized(cls, message='Unauthorized'):
        return cls.return_response(status=401, message=message)

    @classmethod
    def return_not_found(cls, message='Not Found'):
        return cls.return_response(status=404, message=message)

    @classmethod
    def return_forbidden(cls, message='Forbidden'):
        return cls.return_response(status=403, message=message)


class BaseRequest(object):
    @classmethod
    def get_param_int(cls, params, key, default=0):
        res = params.get(key, default)
        return int(res)
