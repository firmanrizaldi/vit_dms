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

import json
import inspect
import logging
import traceback

import werkzeug
from werkzeug import urls
from werkzeug import utils
from werkzeug import exceptions
from werkzeug.urls import iri_to_uri

import odoo
from odoo import _
from odoo import api
from odoo import tools
from odoo import http
from odoo import models
from odoo import release
from odoo.http import request
from odoo.http import Response
from werkzeug._internal import _log

_logger = logging.getLogger(__name__)

REST_VERSION = {
    'server_version': release.version,
    'server_version_info': release.version_info,
    'server_serie': release.serie,
    'api_version': 1,
}

NOT_FOUND = {
    'error': 'unknown_command',
}

DB_INVALID = {
    'error': 'invalid_db',
}

FORBIDDEN = {
    'error': 'token_invalid',
}

NO_API = {
    'error': 'rest_api_not_supported',
}

LOGIN_INVALID = {
    'error': 'invalid_login',
}

def abort(message, rollback=False, status=403):
    response = Response(json.dumps(message,
                        sort_keys=True, indent=4, cls=ObjectEncoder),
                        content_type='application/json;charset=utf-8', status=status) 
    if rollback:
        request._cr.rollback()
    exceptions.abort(response)
    
def check_token():
    token = request.params.get('token') and request.params.get('token').strip()
    if not token:
        abort(FORBIDDEN)
    env = api.Environment(request.cr, odoo.SUPERUSER_ID, {})
    uid = env['muk_rest.token'].check_token(token)
    if not uid:
        abort(FORBIDDEN)
    request._uid = uid
    request._env = api.Environment(request.cr, uid, request.session.context or {})
    
def ensure_db():
    db = request.params.get('db') and request.params.get('db').strip()
    if db and db not in http.db_filter([db]):
        db = None
    if not db and request.session.db and http.db_filter([request.session.db]):
        db = request.session.db
    if not db:
        db = db_monodb(request.httprequest)
    if not db:
        abort(DB_INVALID, status=404)
    if db != request.session.db:
        request.session.logout()
    request.session.db = db
    try:
        env = api.Environment(request.cr, odoo.SUPERUSER_ID, {})
        module = env['ir.module.module'].search([['name', '=', "muk_rest"]], limit=1)
        if module.state != 'installed':
            abort(NO_API, status=500)
    except Exception as error:
        _logger.error(error)
        abort(DB_INVALID, status=404)

def check_params(params):
    missing = []
    for key, value in params.items():
        if not value:
            missing.append(key)
    if missing:
        abort({'error': "arguments_missing %s" % str(missing)}, status=400)

class ObjectEncoder(json.JSONEncoder):
        def default(self, obj):
            def encode(item):
                if isinstance(item, models.BaseModel):
                    vals = {}
                    for name, field in item._fields.items():
                        if name in item:
                            if isinstance(item[name], models.BaseModel):
                                records = item[name]
                                if len(records) == 1:
                                    vals[name] = (records.id, records.sudo().display_name)
                                else:
                                    val = []
                                    for record in records:
                                        val.append((record.id, record.sudo().display_name))
                                    vals[name] = val
                            else:
                                try:
                                    vals[name] = item[name].decode()
                                except AttributeError:
                                    vals[name] = item[name]
                        else:
                            vals[name] = None
                    return vals
                if inspect.isclass(item):
                    return item.__dict__
                try:
                    return json.JSONEncoder.default(self, item)
                except TypeError:
                    return "error"
            try:
                try:
                    result = {}
                    for key, value in obj.items():
                        result[key] = encode(item)
                    return result
                except AttributeError:
                    result = []
                    for item in obj:
                        result.append(encode(item))
                    return result
            except TypeError:
                return encode(item)

class RESTController(http.Controller):

    @http.route('/api/<path:path>', auth="none", type='http')
    def catch(self, **kw):    
        return Response(json.dumps(NOT_FOUND,
                        sort_keys=True, indent=4, cls=ObjectEncoder),
                        content_type='application/json;charset=utf-8', status=404) 
    
    @http.route('/api', auth="none", type='http')
    def version(self, **kw):    
       return Response(json.dumps(REST_VERSION,
                        sort_keys=True, indent=4, cls=ObjectEncoder),
                        content_type='application/json;charset=utf-8', status=200) 
    
    @http.route('/api/authenticate', auth="none", type='http', methods=['POST'], csrf=False)
    def authenticate(self, db=None, login=None, password=None, **kw):    
        check_params({'db': db, 'login': login, 'password': password})
        ensure_db()
        uid = request.session.authenticate(db, login, password)
        if uid:
            env = api.Environment(request.cr, odoo.SUPERUSER_ID, {})
            token = env['muk_rest.token'].generate_token(uid)
            return Response(json.dumps({'token': token.token},
                        sort_keys=True, indent=4, cls=ObjectEncoder),
                        content_type='application/json;charset=utf-8', status=200) 
        else:
            abort(LOGIN_INVALID, status=401) 

    @http.route('/api/refresh', auth="none", type='http', methods=['POST'], csrf=False)
    def refresh(self, token=None, **kw):
        check_params({'token': token})
        ensure_db()
        check_token()
        env = api.Environment(request.cr, odoo.SUPERUSER_ID, {})
        result = env['muk_rest.token'].refresh_token(token)
        return Response(json.dumps(result,
                        sort_keys=True, indent=4, cls=ObjectEncoder),
                        content_type='application/json;charset=utf-8', status=200) 
    
    @http.route([
        '/api/life',
        '/api/life/<string:token>'], auth="none", type='http', csrf=False)
    def life(self, token=None, **kw):
        check_params({'token': token})
        ensure_db()
        check_token()
        env = api.Environment(request.cr, odoo.SUPERUSER_ID, {})
        result = env['muk_rest.token'].lifetime_token(token)
        return Response(json.dumps(result,
                        sort_keys=True, indent=4, cls=ObjectEncoder),
                        content_type='application/json;charset=utf-8', status=200) 
        
    @http.route('/api/close', auth="none", type='http', methods=['POST'], csrf=False)
    def close(self, token=None, **kw):
        check_params({'token': token})
        ensure_db()
        check_token()
        env = api.Environment(request.cr, odoo.SUPERUSER_ID, {})
        result = env['muk_rest.token'].delete_token(token)
        return Response(json.dumps(result,
                        sort_keys=True, indent=4, cls=ObjectEncoder),
                        content_type='application/json;charset=utf-8', status=200) 
        
    @http.route([
        '/api/search',
        '/api/search/<string:model>',
        '/api/search/<string:model>/<int:id>',
        '/api/search/<string:model>/<int:id>/<int:limit>',
        '/api/search/<string:model>/<int:id>/<int:limit>/<int:offset>'], auth="none", type='http', csrf=False)
    def search(self, model='res.partner', id=None, domain=None, context=None, count=False,
               limit=80, offset=0, order=None, token=None, **kw):
        check_params({'token': token})
        ensure_db()
        check_token()
        try:
            args = domain and json.loads(domain) or []
            if id:
                args.append(['id', '=', id])
            context = context and json.loads(context) or {}
            default = request.session.context.copy()
            default.update(context)
            model = request.env[model].with_context(default)
            result = model.search(args, offset=offset, limit=limit, order=order, count=count)
            return Response(json.dumps(result,
                            sort_keys=True, indent=4, cls=ObjectEncoder),
                            content_type='application/json;charset=utf-8', status=200)
        except Exception as error:
            _logger.error(error)
            abort({'error': traceback.format_exc()}, rollback=True, status=400)
        
    @http.route([
        '/api/read',
        '/api/read/<string:model>',
        '/api/read/<string:model>/<int:id>',
        '/api/read/<string:model>/<int:id>/<int:limit>',
        '/api/read/<string:model>/<int:id>/<int:limit>/<int:offset>'], auth="none", type='http', csrf=False)
    def read(self, model='res.partner', id=None, fields=None, domain=None, context=None,
             limit=80, offset=0, order=None, token=None, **kw):
        check_params({'token': token})
        ensure_db()
        check_token()
        try:
            fields = fields and json.loads(fields) or None
            args = domain and json.loads(domain) or []
            if id:
                args.append(['id', '=', id])
            context = context and json.loads(context) or {}
            default = request.session.context.copy()
            default.update(context)
            model = request.env[model].with_context(default)
            result = model.search_read(domain=args, fields=fields, offset=offset, limit=limit, order=order)
            return Response(json.dumps(result,
                            sort_keys=True, indent=4, cls=ObjectEncoder),
                            content_type='application/json;charset=utf-8', status=200)
        except Exception as error:
            _logger.error(error)
            abort({'error': traceback.format_exc()}, rollback=True, status=400)
            
    @http.route('/api/create', auth="none", type='http', methods=['POST'], csrf=False)
    def create(self, model='res.partner', values=None, context=None, token=None, **kw):
        check_params({'token': token})
        ensure_db()
        check_token()
        try:
            values = values and json.loads(values) or {}
            context = context and json.loads(context) or {}
            default = request.session.context.copy()
            default.update(context)
            model = request.env[model].with_context(default)
            result = model.create(values)
            return Response(json.dumps(result,
                            sort_keys=True, indent=4, cls=ObjectEncoder),
                            content_type='application/json;charset=utf-8', status=200)
        except Exception as error:
            _logger.error(error)
            abort({'error': traceback.format_exc()}, rollback=True, status=400)
            
    @http.route('/api/write', auth="none", type='http', methods=['PUT'], csrf=False)
    def write(self, model='res.partner', ids=None, values=None, context=None, token=None, **kw):
        check_params({'ids': ids, 'token': token})
        ensure_db()
        check_token()
        try:
            ids = ids and json.loads(ids) or []
            values = values and json.loads(values) or {}
            context = context and json.loads(context) or {}
            default = request.session.context.copy()
            default.update(context)
            model = request.env[model].with_context(default)
            records = model.browse(ids)
            result = records.write(values)
            return Response(json.dumps(result,
                            sort_keys=True, indent=4, cls=ObjectEncoder),
                            content_type='application/json;charset=utf-8', status=200)
        except Exception as error:
            _logger.error(error)
            abort({'error': traceback.format_exc()}, rollback=True, status=400)

    @http.route('/api/unlink', auth="none", type='http', methods=['DELETE'], csrf=False)
    def unlink(self, model='res.partner', ids=None, context=None, token=None, **kw):
        check_params({'ids': ids, 'token': token})
        ensure_db()
        check_token()
        try:
            ids = ids and json.loads(ids) or []
            context = context and json.loads(context) or {}
            default = request.session.context.copy()
            default.update(context)
            model = request.env[model].with_context(default)
            records = model.browse(ids)
            result = records.unlink()
            return Response(json.dumps(result,
                            sort_keys=True, indent=4, cls=ObjectEncoder),
                            content_type='application/json;charset=utf-8', status=200)
        except Exception as error:
            _logger.error(error)
            abort({'error': traceback.format_exc()}, rollback=True, status=400)
            
    @http.route('/api/call', auth="none", type='http', methods=['POST'], csrf=False)
    def call(self, model='res.partner', method=None, ids=None, context=None, args=None,
               kwargs=None, token=None, **kw):
        check_params({'method': method, 'token': token})
        ensure_db()
        check_token()
        try:
            ids = ids and json.loads(ids) or []
            args = args and json.loads(args) or []
            kwargs = kwargs and json.loads(kwargs) or {}
            context = context and json.loads(context) or {}
            default = request.session.context.copy()
            default.update(context)
            model = request.env[model].with_context(default)
            records = model.browse(ids)
            result = getattr(records, method)(*args, **kwargs)
            return Response(json.dumps(result,
                            sort_keys=True, indent=4, cls=ObjectEncoder),
                            content_type='application/json;charset=utf-8', status=200)
        except Exception as error:
            _logger.error(error)
            abort({'error': traceback.format_exc()}, rollback=True, status=400)