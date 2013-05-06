#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import action

from tornado.options import define, options

define("port", default=8080, help=u"监听端口", type=int)
define("mysql_host", default="127.0.0.1:3306", help=u"数据库地址")
define("mysql_database", default="todo", help=u"数据库名字")
define("mysql_user", default="root", help=u"用户名")
define("mysql_password", default="123456", help=u"密码")


class Application(tornado.web.Application):
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
            cookie_secret="Todo_is_an_tai_du",
            login_url="/login",
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # 全局使用的数据库句柄
        self.db = database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
