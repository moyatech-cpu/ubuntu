# -*- coding: utf-8 -*-
from odoo import http

# class SystemUpdate009(http.Controller):
#     @http.route('/system_update_009/system_update_009/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/system_update_009/system_update_009/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('system_update_009.listing', {
#             'root': '/system_update_009/system_update_009',
#             'objects': http.request.env['system_update_009.system_update_009'].search([]),
#         })

#     @http.route('/system_update_009/system_update_009/objects/<model("system_update_009.system_update_009"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('system_update_009.object', {
#             'object': obj
#         })