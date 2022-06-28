# -*- coding: utf-8 -*-
from odoo import http

# class CsdIntergration(http.Controller):
#     @http.route('/csd_intergration/csd_intergration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/csd_intergration/csd_intergration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('csd_intergration.listing', {
#             'root': '/csd_intergration/csd_intergration',
#             'objects': http.request.env['csd_intergration.csd_intergration'].search([]),
#         })

#     @http.route('/csd_intergration/csd_intergration/objects/<model("csd_intergration.csd_intergration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('csd_intergration.object', {
#             'object': obj
#         })