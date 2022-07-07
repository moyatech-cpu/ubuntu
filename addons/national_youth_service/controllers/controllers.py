# -*- coding: utf-8 -*-
from odoo import http

# class NationalYouthService(http.Controller):
#     @http.route('/national_youth_service/national_youth_service/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/national_youth_service/national_youth_service/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('national_youth_service.listing', {
#             'root': '/national_youth_service/national_youth_service',
#             'objects': http.request.env['national_youth_service.national_youth_service'].search([]),
#         })

#     @http.route('/national_youth_service/national_youth_service/objects/<model("national_youth_service.national_youth_service"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('national_youth_service.object', {
#             'object': obj
#         })