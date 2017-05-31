#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from flask import g
# from flask import request
# import time
# import thread
from api import app
# from api import sensitive_words
from api.config import BaseConfig
from api.service import sensitive_word_bp
from api.service import sensitive_word_reload_bp


# # 创建定期更新敏感词线程函数
# def update_sensitive_word():
#     try:
#         while True:
    #         readliens = open(BaseConfig.WORD_PATH, 'r').readliens()
    #         for line in readliens:
    #             line = line.strip()
    #             if not line:
    #                 continue
    #             sensitive_words.add_word(line, line)
    #         sensitive_words.make_automaton()
    #         time.sleep(int(BaseConfig.WORD_UPDATE_FREQUENCY))
    #     return True
    # except Exception as e:
    #     app.logger.error("update_sensitive_word exception:{}".format(e))
    #     return False

# thread.start_new_thread(update_sensitive_word)

URL_PREFIX = BaseConfig.APPLICATION_ROOT
app.register_blueprint(sensitive_word_bp, url_prefix=URL_PREFIX)
app.register_blueprint(sensitive_word_reload_bp, url_prefix=URL_PREFIX)
