# -*- coding: utf-8 -*-
from odoo import http

# class SystemUpdate008(http.Controller):
#     @http.route('/system_update_008/system_update_008/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/system_update_008/system_update_008/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('system_update_008.listing', {
#             'root': '/system_update_008/system_update_008',
#             'objects': http.request.env['system_update_008.system_update_008'].search([]),
#         })

#     @http.route('/system_update_008/system_update_008/objects/<model("system_update_008.system_update_008"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('system_update_008.object', {
#             'object': obj
#         })