# -*- coding: utf-8 -*-
from odoo import http

# class NydaCommunications(http.Controller):
#     @http.route('/nyda_communications/nyda_communications/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nyda_communications/nyda_communications/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nyda_communications.listing', {
#             'root': '/nyda_communications/nyda_communications',
#             'objects': http.request.env['nyda_communications.nyda_communications'].search([]),
#         })

#     @http.route('/nyda_communications/nyda_communications/objects/<model("nyda_communications.nyda_communications"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nyda_communications.object', {
#             'object': obj
#         })