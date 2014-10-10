#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'tigerstudent'

import unittest
import server


class TestMailSending(unittest.TestCase):
    def setUp(self):
        self.request_body = {
            "email": "tigerstudent007@gmail.com",
            "first_name": "Peter",
            "last_name": "Pan",
            "contact_number": "86-13227892789",
            "title": "Request Title",
            "content": "Request Content",
            "link": "https://github.com"
        }

    def test_send_to_sender(self):
        server.send_to_sender(self.request_body)
        print "done"

    def test_send_to_dedicated_email(self):
        server.send_to_dedicated_email(self.request_body)
        print "done"

    def test_check_email(self):
        email = "tigerstudent007@gmail.com"
        assert server.check_email(email)
        print server.check_email(email)