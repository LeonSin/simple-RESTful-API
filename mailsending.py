#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'tigerstudent'

import smtplib
import config


def send_mail(sender, receiver, mail):
    smtp = smtplib.SMTP()
    smtp.connect(config.host, config.port)
    login_response = smtp.login(config.notification_email, config.notification_email_pwd)
    #判断是否登录成功
    if login_response[0] != 235:
        return False

    smtp.sendmail(sender, receiver, mail)
    return True