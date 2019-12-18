# -*- coding: utf-8 -*-
from odoo import http

# class VitMukDms(http.Controller):
#     @http.route('/vit_muk_dms/vit_muk_dms/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_muk_dms/vit_muk_dms/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_muk_dms.listing', {
#             'root': '/vit_muk_dms/vit_muk_dms',
#             'objects': http.request.env['vit_muk_dms.vit_muk_dms'].search([]),
#         })

#     @http.route('/vit_muk_dms/vit_muk_dms/objects/<model("vit_muk_dms.vit_muk_dms"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_muk_dms.object', {
#             'object': obj
#         })