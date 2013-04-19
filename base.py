#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random

import urllib
import tornado.options
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    User = None

    def initialize(self):
        pass

    def db(self):
        return self.application.db

    def page(self, sql, num=20, isHtml=True):
        """
        分页方法
        """
        self.PAGE = ""
        count = self.db().execute_rowcount(sql)
        page = int(self.get_argument("page", 1))
        page = max(page, 1)
        pageCount = count / num + 1
        page = min(pageCount, page)

        start = (page - 1) * num

        if pageCount > 1:
            sql += " LIMIT %s,%s" % (start, num)
            path = self.request.path
            arguments = self.request.arguments

            if page < 2:
                prevHtml = '<span class="prev">前页</span>'
            else:
                arguments['page'] = max(page - 1, 1)
                if arguments['page'] == 1:
                    del arguments['page']
                prevHtml = '<a href="%s?%s" class="prev">前页</a>' % (
                    path, urllib.urlencode(arguments))
            if not page < pageCount:
                nextHtml = '<span class="next">后页</span>'
            else:
                arguments['page'] = min(page + 1, pageCount)
                nextHtml = '<a href="%s?%s" class="next">后页</a>' % (
                    path, urllib.urlencode(arguments))
            pageHtml = '<div class="pageBox">%s<span class="this">%s/%s</span>%s</div>' % (
                prevHtml, page, pageCount, nextHtml)
            if isHtml:
                self.PAGE = pageHtml
            else:
                self.PAGE = dict(
                    start=start,
                    thisPage=page,
                    pageCount=pageCount,
                    prevStart=max(start - num, 0),
                    nextStart=min(start + num, count),
                    html=pageHtml
                )
        list = self.db().query(sql)
        return list


    def get_current_user(self):
        """
        检测是否登陆
        """
        user_id = self.get_argument("user_id")
        ssid = self.get_argument("ssid")
        if not user_id or not ssid:
            return None
        self.User = self.db().get("SELECT * FROM user WHERE id = %s AND ssid = %s LIMIT 1"
            , user_id, ssid)
        return self.User


    def success(self, message=u"Success!"):
        """
        成功操作提示
        """
        self.ajaxReturn(message, True)


    def error(self, message=u"Error", ):
        """
        失败操作提示
        """
        self.ajaxReturn(message, False)


    def ajaxReturn(self, message="", status=True):
        """
        返回json数据
        """

        if isinstance(message, dict):
            self.write({'status': status, 'data': message})
        else:
            self.write({'status': status, 'data': message})

