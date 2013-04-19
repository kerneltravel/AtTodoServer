#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import tornado.database
import tornado.options
import tornado.web
import action

import tornado.wsgi

from bae.core import const

from tornado.options import define, options

define("mysql_host", default=const.MYSQL_HOST+":"+const.MYSQL_PORT, help="数据库地址")
define("mysql_database", default=r"xxxxxxxxxxxxx", help="数据库名字")
define("mysql_user", default=const.MYSQL_USER, help="用户名")
define("mysql_password", default=const.MYSQL_PASS, help="密码")


class Application(tornado.wsgi.WSGIApplication):
    def __init__(self):
        handlers = [
            (r"/", action.HomeHandler),
            (r"/login", action.LoginHandler),
            (r"/load", action.LoadHandler),
            (r"/add", action.AddHandler),
            (r"/modify", action.ModifyHandler),
            (r"/unFinish", action.UnFinishHandler),
            (r"/finish", action.FinishHandler),
            (r"/remove", action.RemoveHandler),
            (r"/logout", action.LogoutHandler),
            (r"/count", action.CountHandler),
            (r"/tenM", action.TenMHandler),
            (r"/sort", action.SortHandler),
            (r"/msg", action.MsgHandler),
        ]

        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="This_is_a_website",
            login_url="/login",
        )
        tornado.wsgi.WSGIApplication.__init__(self, handlers, **settings)

        # 全局使用的数据库句柄
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password,max_idle_time=30)



from bae.core.wsgi import WSGIApplication
application = WSGIApplication(Application())