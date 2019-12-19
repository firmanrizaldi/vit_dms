# -*- coding: utf-8 -*-

###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
#
#    Odoo Proprietary License v1.0
#    
#    This software and associated files (the "Software") may only be used 
#    (executed, modified, executed after modifications) if you have
#    purchased a valid license from the authors, typically via Odoo Apps,
#    or if you have received a written agreement from the authors of the
#    Software (see the COPYRIGHT file).
#    
#    You may develop Odoo modules that use the Software as a library 
#    (typically by depending on it, importing it and using its resources),
#    but without copying any source code or material from the Software.
#    You may distribute those modules under the license of your choice,
#    provided that this license is compatible with the terms of the Odoo
#    Proprietary License (For example: LGPL, MIT, or proprietary licenses
#    similar to this one).
#    
#    It is forbidden to publish, distribute, sublicense, or sell copies of
#    the Software or modified copies of the Software.
#    
#    The above copyright notice and this permission notice must be included
#    in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###################################################################################

import os
import json
import base64
import logging
import unittest
import requests

import odoo
from odoo import _
from odoo.tests import common

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

HOST = '127.0.0.1'
PORT = odoo.tools.config['xmlrpc_port']

class RESTTestCase(common.TransactionCase):
    
    at_install = False
    post_install = True
    
    def setUp(self):
        super(RESTTestCase, self).setUp()
        
    def tearDown(self):
        super(RESTTestCase, self).tearDown()
    
    def url(self, url):
        if url.startswith('/'):
            url = "http://%s:%s%s" % (HOST, PORT, url)
        return url
    
    def authentication(self):
        response = requests.post(
            self.url('/api/authenticate'),
            data = {
                'db': "openerp_test",
                'login': "admin",
                'password': "admin"})
        self.assertTrue(response)
        return response.json()['token']
        
    def test_verison(self):
        response = requests.get(self.url('/api'))
        self.assertTrue(response)
    
    def test_authentication(self):
        response = requests.post(
            self.url('/api/authenticate'),
            data = {
                'db': "openerp_test",
                'login': "admin",
                'password': "admin"})
        self.assertTrue(response)
        token = response.json()['token']
        response = requests.get(
            self.url('/api/life'),
            data = {'token': token})
        self.assertTrue(response)
        response = requests.post(
            self.url('/api/refresh'),
            data = {'token': token})
        self.assertTrue(response)
        response = requests.post(
            self.url('/api/close'),
            data = {'token': token})
        self.assertTrue(response)
        response = requests.get(
            self.url('/api/life'),
            data = {'token': token})
        self.assertFalse(response)
        
    def test_search(self):
        token = self.authentication()
        response = requests.get(
            self.url('/api/search'),
            data = {'token': token,
                    'model': 'res.partner'})
        self.assertTrue(response)
        response = requests.get(
            self.url('/api/search'),
            data = {'token': token,
                    'model': 'res.partner',
                    'id': 1})
        self.assertTrue(response)
        response = requests.get(
            self.url('/api/search'),
            data = {'token': token,
                    'model': 'res.partner',
                    'domain': '[["id", "=", 1]]'})
        self.assertTrue(response)
        
    def test_read(self):
        token = self.authentication()
        response = requests.get(
            self.url('/api/read'),
            data = {'token': token,
                    'model': 'res.users',
                    'fields': '["login", "name"]'})
        self.assertTrue(response)
        
    def test_create(self):
        token = self.authentication()
        response = requests.post(
            self.url('/api/create'),
            data = {'token': token,
                    'values': '{"name": "MuK IT"}'})
        self.assertTrue(response)
        
    def test_write(self):
        token = self.authentication()
        response = requests.put(
            self.url('/api/write'),
            data = {'token': token,
                    'ids': '[1]',
                    'values': '{"name": "MuK IT"}'})
        self.assertTrue(response)
        
    def test_unlink(self):
        token = self.authentication()
        response = requests.delete(
            self.url('/api/unlink'),
            data = {'token': token,
                    'model': 'res.users',
                    'ids': '[2]'})
        self.assertTrue(response)

    def test_method(self):
        token = self.authentication()
        response = requests.post(
            self.url('/api/call'),
            data = {'token': token,
                    'method': 'copy',
                    'ids': '[1]'})
        self.assertTrue(response)
        