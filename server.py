#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'tigerstudent'

import json
import re
import datetime
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
import mailsending
import config
from tornado.options import define, options, parse_command_line

define("port", default=8000, help="run on the given port", type=int)


def check_email(email):
    """
    检查email参数是否符合一般邮箱格式
    :param email:
    :return:
    """
    reg = r'''^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+'''
    if re.match(reg, email) is None:
        return False
    return True


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/rest", MainHandler),
        ]
        settings = {}
        tornado.web.Application.__init__(self, handlers, debug=True, **settings)


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        response = {}
        request_body = json.loads(self.request.body)    # 解析接收到的json字符串
        email = request_body.get("email")
        first_name = request_body.get("first_name")
        last_name = request_body.get("last_name")
        contact_number = request_body.get("contact_number")
        title = request_body.get("title")
        content = request_body.get("content")
        link = request_body.get("link")

        #检验是否所有元素都非空
        if email is None or first_name is None or last_name is None or contact_number is None or title is None \
                or content is None or link is None:
            response["error"] = "bad parameter"
            self.write(json.dumps(response))
            return

        logging.info("receive request from %s" % email)     # 接收到有效请求

        #检查email地址是否格式正确
        if check_email(email) is False:
            logging.info("invalid email:%s" % email)
            response["error"] = "invalid email"
            self.write(json.dumps(response))
            return

        #发送通知邮件给请求发送者
        if send_to_sender(request_body):
            logging.info("send notification succeed.To %s" % email)
        else:
            logging.info("send notification failed.To %s" % email)

        #发送通知邮件给专用邮箱
        if send_to_dedicated_email(request_body):
            logging.info("send notification succeed.To %s" % email)
        else:
            logging.info("send notification failed.To %s" % email)


def send_to_sender(request_body):
    mail_content = """From: %s\nTo: %s\nSubject: Thanks for your application

    Dear %s,
    We have received your application. Please do NOT reply this email.
    Thanks, Tech Team
    """ % (config.notification_email, request_body["email"], request_body["last_name"])

    return mailsending.send_mail(config.notification_email, request_body["email"], mail_content)


def send_to_dedicated_email(request_body):
    mail_content = """From: %s\nTo: %s\nSubject: Application Received from %s

    Received an application from %s %s at %s
    """ % (config.notification_email, config.dedicated_email, request_body["email"], \
           request_body["last_name"], request_body["first_name"], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    return mailsending.send_mail(config.notification_email, config.dedicated_email, mail_content)


def main():
    parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
