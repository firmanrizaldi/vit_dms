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
import time
import logging
        
from odoo import _
from odoo import models, api, fields

_logger = logging.getLogger(__name__)

try:
    import secrets
    def token_urlsafe():
        return secrets.token_urlsafe(64)
except ImportError:
    import re
    import uuid
    import base64
    def token_urlsafe():
        rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
        return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)

class RESTToken(models.Model):
    _name = 'muk_rest.token'
    
    token = fields.Char(
        string="Token",
        required=True)
    
    lifetime = fields.Integer(
        string="Lifetime",
        required=True)
    
    user = fields.Many2one(
        'res.users',
        string="User",
        required=True)

    @api.model
    def lifetime_token(self, token):
        token = self.search([['token', '=', token]], limit=1)
        if token:
            return int(token.lifetime - time.time())
        return False

    @api.model
    def delete_token(self, token):
        token = self.search([['token', '=', token]], limit=1)
        if token:
            return token.unlink()
        return False

    @api.model
    def refresh_token(self, token, lifetime=3600):
        token = self.search([['token', '=', token]], limit=1)
        if token:
            timestamp = int(time.time() + lifetime)
            return token.write({'lifetime': timestamp})
        return False

    @api.model
    def check_token(self, token):
        token = self.search([['token', '=', token]], limit=1)
        return token.user.id if token and int(time.time()) < token.lifetime else False
    
    @api.model
    def generate_token(self, uid, lifetime=3600):
        token = token_urlsafe()
        timestamp = int(time.time() + lifetime)
        return self.create({'token': token, 'lifetime': timestamp, 'user': uid})
    
    @api.model
    def _garbage_collect(self):
        token = self.search([['lifetime', '>', int(time.time())]], limit=1)
        token.unlink()