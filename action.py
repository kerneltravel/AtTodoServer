#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import tornado.options
import tornado.web
import tool
from base import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        self.write("ok")


class LoginHandler(BaseHandler):
    """
    登陆
    """

    def get(self):
        self.write("欢迎来到登陆！")

    def post(self):
        email = self.get_argument('email', None)
        if not tool.check_email(email):
            self.error("格式错误!")
            return
        psw = self.get_argument('psw', None)
        userName = self.get_argument('username', None)

        user = self.db().get("SELECT * FROM user WHERE "
                             "email = %s AND psw = %s LIMIT 1", email, tool.md5(psw))
        if user:
            self.success(user)
        else:
        #            如果不能正常登陆
            user = self.db().get("SELECT * FROM user WHERE email = %s LIMIT 1", email)
            if user:
                self.error("密码错误!")
                return
                #            通过邮箱无法查找用户说明尚未注册
            if not userName:
                self.error("您还没有注册！")
                return
                #            处理无昵称的时候
            if not userName:
                emailName = email.split("@")
                userName = emailName[0]
            ssid = tool.md5(psw + str(time.time()))
            r = self.db().execute("INSERT INTO user (email,psw,username,ssid) "
                                  "VALUES (%s,%s,%s,%s)",
                email, tool.md5(psw), userName[0:10], ssid)
            if r:
                self.success({"id": r, "username": userName, "ssid": ssid, "email": email})
            else:
                self.error("注册失败！")


class LogoutHandler(BaseHandler):
    """
    退出
    """

    def get(self):
        self.success("已经退出！")


class RePswHandler(BaseHandler):
    """
    修改密码
    """

    def post(self):
        pass


class LoadHandler(BaseHandler):
    """
    初始化数据
    """

    @tornado.web.authenticated
    def post(self):
        list = self.db().query("SELECT * FROM todo WHERE user_id = %s AND remove < 1 "
                               "ORDER BY sort DESC,sort_s DESC"
            , self.User.id)
#        if not len(list):
#            self.error(list)
#            return

        self.success(list)


class AddHandler(BaseHandler):
    """
    添加todo
    """

    @tornado.web.authenticated
    def post(self):
        content = self.get_argument('content', None)
        #        处理内容
        if content:
            content = content.strip()
            #        暂时不处理提醒时间
        r = self.db().execute("INSERT INTO todo (user_id,content,create_date,sort,sort_s) VALUES "
                              "(%s,%s,%s,%s,%s)",
            self.User.id, content, int(time.time()),
            int(((time.time()) * 100) % 1000000000), 1000)
        if not r:
            self.error("添加数据失败！")
            return
            #        成功就返回id信息
        self.success(r)


class ModifyHandler(BaseHandler):
    """
    修改todo内容
    """

    @tornado.web.authenticated
    def post(self):
        content = self.get_argument('content', None)
        todoId = self.get_argument('todo_id', None)

        info = self.db().get("SELECT * FROM todo WHERE id=%s AND user_id=%s LIMIT 1",
            todoId, self.User.id)
        if not info:
            self.error("已经没有了！")
            return
        if len(content) > 100:
            pass

        r = self.db().execute("UPDATE todo SET content=%s WHERE id=%s",
            content, todoId)
        if r is False:
            self.error("编辑失败！")
            return
        self.success("编辑成功！")


class FinishHandler(BaseHandler):
    """
    完成
    """

    @tornado.web.authenticated
    def post(self):
        todoId = self.get_argument('todo_id', None)
        info = self.db().get("SELECT * FROM todo WHERE id=%s AND user_id=%s LIMIT 1",
            todoId, self.User.id)
        if not info:
            self.error("已经没有了！")
            return

        if info.finish:
            self.success("已经完成")
            return
        r = self.db().execute("UPDATE todo SET finish=%s WHERE id=%s",
            int(time.time()), todoId)
        if r is False:
            self.error("操作失败！")
        else:
            self.success("操作完成！")


class UnFinishHandler(BaseHandler):
    """
    解除完成状态
    """

    @tornado.web.authenticated
    def post(self):
        todoId = self.get_argument('todo_id', None)
        info = self.db().get("SELECT * FROM todo WHERE id=%s AND user_id=%s LIMIT 1",
            todoId, self.User.id)
        if not info:
            self.error("已经没有了！")
            return

        if not info.finish:
            self.success("已经完成")
            return
        r = self.db().execute("UPDATE todo SET finish=%s WHERE id=%s",
            0, todoId)
        if r is False:
            self.error("操作失败！")
        else:
            self.success("操作完成！")


class RemoveHandler(BaseHandler):
    """
    移除
    """

    @tornado.web.authenticated
    def post(self):
        todoId = self.get_argument('todo_id', None)
        info = self.db().get("SELECT * FROM todo WHERE id=%s AND user_id=%s LIMIT 1",
            todoId, self.User.id)
        if not info:
            self.error("已经没有了！")
            return
        if info.remove:
            self.success("已经移除了！")
            return
            #        处理finish动作失败时的remove动作
        if info.finish:
            r = self.db().execute("UPDATE todo SET remove=%s WHERE id=%s",
                int(time.time()), todoId)
        else:
            r = self.db().execute("UPDATE todo SET remove=%s finish = %s WHERE id=%s",
                int(time.time()), int(time.time()), todoId)
        if r is False:
            self.error("移除失败！")
        else:
            self.success("已移除！")


class TenMHandler(BaseHandler):
    """
    每10分钟检测下数据和提醒
    """

    @tornado.web.authenticated
    def post(self):
        timeS = int(time.time())
        count = self.db().get("SELECT COUNT(id) AS count FROM todo WHERE user_id "
                              "= %s AND finish < 1 AND remove < 1", self.User.id)
        list = self.db().query("SELECT * FROM todo WHERE user_id = %s AND "
                               "remind>%s AND remind<%s AND remove < 1",
            self.User.id, timeS, (timeS + 600))

        self.success({"count": count.count, "remind": list})


class CountHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        count = self.db().get("SELECT COUNT(id) AS count FROM todo WHERE user_id "
                              "= %s AND finish < 1 AND remove < 1", self.User.id)
        self.success({"count": count.count})


class SortHandler(BaseHandler):
    """
    排序
    """

    def post(self):
        dropId = self.get_argument("drop_id", 0)
        dropSort = self.get_argument("drop_sort", 0)
        dropSortS = self.get_argument("drop_sort_s", False)
        self.User = self.get_current_user()
        #        todo user没有自动添加上去
        info = self.db().get("SELECT * FROM todo WHERE id=%s AND user_id=%s LIMIT 1",
            dropId, self.User.id)
        if not info:
            self.error(u"已经没有了！")
            return

        if dropSortS is False or dropSortS == "false":
            sql = "UPDATE todo SET sort=%s WHERE id=%s"
            r = self.db().execute(sql, dropSort, dropId)
        else:
            sql = "UPDATE todo SET sort=%s ,sort_s=%s WHERE id=%s"
            r = self.db().execute(sql, dropSort, dropSortS, dropId)

        if r is False:
            self.error(u"排序失败！")
        else:
            self.success(u"成功！")


class MsgHandler(BaseHandler):
    """
    服务器给客户端发送消息
    """

    def post(self):
        user = self.get_current_user()
        if user:
            self.success(user.username + u"欢迎回来！")
        else:
            self.success(u"为毛不登陆？")