#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
"""api初始化信息"""

# Author: liulonghui(liulonghui@gochinatv.com)
# Copyright 2017 GoChinaTV

from api.run import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8800)
