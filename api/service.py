#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: liulonghui(liulonghui@gochinatv.com)
# Copyright 2017 GoChinaTV
from flask import request
from flask import Blueprint
from api import app
from api import sensitive_words
from api.common.base import BaseResponse
from api.config import BaseConfig
from api.common.decorator import args_required

sensitive_word_bp = Blueprint('sensitive_word', __name__)
sensitive_word_reload_bp = Blueprint('sensitive_word_reload', __name__)


def sensitive_word_replace(body):
    result = body
    result_list = []
    check_status = False
    start_dict = {}
    end_dict = {}
    try:
        for end_index, original_value in sensitive_words.iter(body):
            start_index = end_index - len(original_value) + 1
            result_list.append((start_index, end_index, original_value))

        for line in result_list:
            if line[0] in start_dict:
                if line[1] < start_dict[line[0]][1]:
                    continue
                start_dict[line[0]] = line
                continue
            start_dict[line[0]] = line

        for k, v in start_dict.items():
            if v[1] in end_dict:
                if v[0] > end_dict[v[1]][0]:
                    continue
                end_dict[v[1]] = v
                continue
            end_dict[v[1]] = v
        app.logger.info("sensitive_word_replace end_dict:{}".format(end_dict))
        for v in end_dict.values():
            result = result.replace(
                result[v[0]:v[1]+1],
                BaseConfig.REPLACE_CHAR*len(v[2]))
        app.logger.info("sensitive_word_replace reuslt:{}".format(result))
        if len(result_list):
            check_status = True
        return result, check_status
    except Exception as e:
        app.logger.error("sensitive_word_check exception:{}".format(e))
        return result, check_status


def sensitive_word_check(body):
    try:
        result_list = []
        for end_index, original_value in sensitive_words.iter(body):
            start_index = end_index - len(original_value) + 1
            result_list.append((start_index, end_index, original_value))
        return len(result_list)
    except Exception as e:
        app.logger.error("sensitive_word_check exception:{}".format(e))
        return False


def sensitive_word_keywords(body):
    result_list = []
    try:
        for end_index, original_value in sensitive_words.iter(body):
            start_index = end_index - len(original_value) + 1
            tmp = {}
            tmp['start_index'] = start_index
            tmp['end_index'] = end_index
            tmp['word'] = original_value
            result_list.append(tmp)
            # result_list.append((start_index, end_index, original_value))
        return result_list
    except Exception as e:
        app.logger.error("sensitive_word_keywords exception:{}".format(e))
        return result_list


def sensitive_word_replace_and_keywords(body):
    result = body
    result_list = []
    keywords_list = []
    check_status = False
    start_dict = {}
    end_dict = {}
    try:
        for end_index, original_value in sensitive_words.iter(body):
            start_index = end_index - len(original_value) + 1
            result_list.append((start_index, end_index, original_value))
            tmp = {}
            tmp['start_index'] = start_index
            tmp['end_index'] = end_index
            tmp['word'] = original_value
            keywords_list.append(tmp)

        for line in result_list:
            if line[0] in start_dict:
                if line[1] < start_dict[line[0]][1]:
                    continue
                start_dict[line[0]] = line
                continue
            start_dict[line[0]] = line

        for k, v in start_dict.items():
            if v[1] in end_dict:
                if v[0] > end_dict[v[1]][0]:
                    continue
                end_dict[v[1]] = v
                continue
            end_dict[v[1]] = v
        app.logger.info("sensitive_word_replace end_dict:{}".format(end_dict))
        for v in end_dict.values():
            result = result.replace(
                result[v[0]:v[1]+1],
                BaseConfig.REPLACE_CHAR*len(v[2]))
        app.logger.info("sensitive_word_replace reuslt:{}".format(result))
        if len(keywords_list):
            check_status = True
        return result, check_status, keywords_list
    except Exception as e:
        app.logger.error("sensitive_word_check exception:{}".format(e))
        return result, check_status, keywords_list


@sensitive_word_bp.route('/sensitive_word', methods=['POST'])
@args_required('body', 'method')
def check_sensitive_word():
    """
    body: 需要检查的内容
    method: 需要检查的方法，replace 、 check 、keywords, replace_keywords
            keywords (start, end, word)
    return: data = {
        'replace': '',
        'check': True| False,
        'keywords': []
    }
    """
    args = request.json

    replace_body = ''
    check_status = False
    keywords = []
    data = {
        "replace_body": replace_body,
        "check_status": check_status,
        "keywords": keywords
    }
    try:
        if args['method'] == 'replace':
            replace_body, check_status = sensitive_word_replace(args['body'])
        elif args['method'] == 'check':
            check_status = sensitive_word_check(args['body'])
        elif args['method'] == 'keywords':
            keywords = sensitive_word_keywords(args["body"])
            if len(keywords):
                check_status = True
        elif args['method'] == 'replace_keywords':
            replace_body, check_status, keywords = sensitive_word_replace_and_keywords(args['body'])
        else:
            pass
        data['replace_body'] = replace_body
        data['check_status'] = check_status
        data['keywords'] = keywords
        app.logger.debug("check_sensitive_word body:{}, result:{}".format(
            args['body'], data))
        return BaseResponse.return_response(data)
    except Exception as e:
        app.logger.error("check_sensitive_word excption:{}".format(e))
        return BaseResponse.return_internal_server_error()


@sensitive_word_reload_bp.route('/sensitive_word_reload', methods=['GET'])
def sensitive_words_reload():
    try:
        app.logger.info("sensitive_word_reload file:{}".format(
            BaseConfig.WORD_PATH))
        lines = open(BaseConfig.WORD_PATH, 'r').readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            sensitive_words.add_word(line, line)
        sensitive_words.make_automaton()
        return BaseResponse.return_response()
    except Exception as e:
        app.logger.error("sensitive_words_reload excption:{}".format(e))
        return BaseResponse.return_internal_server_error()
