#!/usr/bin/env python
# _*_ coding: utf-8 _*_

# Author: liulonghui(liulonghui@gochinatv.com)
# Copyright 2017 GoChinaTV

from api.config import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True


class LocalConfig(BaseConfig):
    DEBUG = True
