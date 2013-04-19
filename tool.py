#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import hashlib


def check_email(email=None):
    """
    检查Email格式
    """
    re_pattern = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
    check_result = re_pattern.search(email)
    if check_result:
        if len(email) >= 60:
            return False
    else:
        return False
    return True


def md5(str):
    """
    md5字符串
    :param str:
    :return:
    """
    h = hashlib.md5()
    h.update(str)
    return h.hexdigest()
