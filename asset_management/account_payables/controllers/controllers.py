# -*- coding: utf-8 -*-
from odoo import http

# class BcsVsp(http.Controller):
#     @http.route('/bcs_vsp/bcs_vsp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bcs_vsp/bcs_vsp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bcs_vsp.listing', {
#             'root': '/bcs_vsp/bcs_vsp',
#             'objects': http.request.env['bcs_vsp.bcs_vsp'].search([]),
#         })

#     @http.route('/bcs_vsp/bcs_vsp/objects/<model("bcs_vsp.bcs_vsp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bcs_vsp.object', {
#             'object': obj
#         })