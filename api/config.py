#!/usr/bin/env python
# _*_ coding: utf-8 _*_

# Author: liulonghui(liulonghui@gochinatv.com)
# Copyright 2017 GoChinaTV


class BaseConfig(object):
    DEBUG = False

    # 地址前缀
    APPLICATION_ROOT = '/api/v1'
    METRICS_LOG_FILE = './sensitive_work.flask.log'

    # 词库路径
    WORD_PATH = "/Users/vego/project/sensitiveword/keywords/keywords.txt"
    # WORD_UPDATE_FREQUENCY = 30
    REPLACE_CHAR = '*'
