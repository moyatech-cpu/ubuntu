# -*- coding: utf-8 -*-
from odoo import http

# class PrimnetIntegration(http.Controller):
#     @http.route('/primnet_integration/primnet_integration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/primnet_integration/primnet_integration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('primnet_integration.listing', {
#             'root': '/primnet_integration/primnet_integration',
#             'objects': http.request.env['primnet_integration.primnet_integration'].search([]),
#         })

#     @http.route('/primnet_integration/primnet_integration/objects/<model("primnet_integration.primnet_integration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('primnet_integration.object', {
#             'object': obj
#         })