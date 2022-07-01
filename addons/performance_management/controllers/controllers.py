# -*- coding: utf-8 -*-
from odoo import http

# class PerformanceManagement(http.Controller):
#     @http.route('/performance_management/performance_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/performance_management/performance_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('performance_management.listing', {
#             'root': '/performance_management/performance_management',
#             'objects': http.request.env['performance_management.performance_management'].search([]),
#         })

#     @http.route('/performance_management/performance_management/objects/<model("performance_management.performance_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('performance_management.object', {
#             'object': obj
#         })