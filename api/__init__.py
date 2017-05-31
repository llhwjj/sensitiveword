#!/usr/bin/env python
# _*_ coding: utf-8 _*_

# Author: liulonghui(liulonghui@gochinatv.com)
# Copyright 2017 GoChinaTV

import os
import time
import logging

import ahocorasick
from flask import g
from flask import Flask
from flask import request
from werkzeug.contrib.fixers import ProxyFix
from api.config import BaseConfig


CONFIG_NAME_MAPPER = {
    'local': 'api.local_config.LocalConfig',
    'product': 'api.local_config.ProductionConfig',
    'dev': 'api.local_config.DevelopmentConfig',
    'test': 'api.local_config.TestingConfig'
}


def create_app(flask_config_name=None):
    """
    创建配置
    :return:
    """
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    env_flask_config_name = os.getenv('FLASK_CONFIG')
    config_mapper_name = flask_config_name or env_flask_config_name or 'dev'
    config_name = CONFIG_NAME_MAPPER[config_mapper_name]
    app.config.from_object(config_name)
    print('-------------------------init app-------------------------')
    logging.basicConfig(
        filename=app.config['METRICS_LOG_FILE'], level=logging.ERROR)
    return app


app = create_app()


# metrics only begin by zebin
@app.before_request
def before_request():
    g.request_start_time = time.time()
    if app.config['DEBUG']:
        content_type = request.content_type or ''
        if 'application/x-www-form-urlencoded' in content_type:
            _args = request.form
        elif 'application/json' in content_type:
            _args = request.json
        else:
            _args = request.args
        app.logger.debug(
            '{} {}\nargs:{}\nheaders:{}'.format(
                request.method, request.url, _args, request.headers
            )
        )


@app.after_request
def after_request(response):
    if not hasattr(g, 'request_start_time'):
        return response
    elapsed = time.time() - g.request_start_time
    req_info = str(g.request_start_time) + ": " + request.method + "_" + request.url
    app.logger.debug(req_info + ":" + ' time_used:' + str(elapsed))
    return response


# metrics only end
# update sensitive
sensitive_words = ahocorasick.Automaton()
def load_sensitive_word():
    try:
        lines = open(BaseConfig.WORD_PATH, 'r').readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            sensitive_words.add_word(line, line)
        sensitive_words.make_automaton()
        return True
    except Exception as e:
        app.logger.error("load_sensitive_word exception:{}".format(e))
        return False
load_sensitive_word()

# db = SQLAlchemy(app)
