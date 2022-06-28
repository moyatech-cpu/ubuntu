# -*- coding: utf-8 -*-
from odoo import http

# class PdddSettings(http.Controller):
#     @http.route('/pddd_settings/pddd_settings/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pddd_settings/pddd_settings/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pddd_settings.listing', {
#             'root': '/pddd_settings/pddd_settings',
#             'objects': http.request.env['pddd_settings.pddd_settings'].search([]),
#         })

#     @http.route('/pddd_settings/pddd_settings/objects/<model("pddd_settings.pddd_settings"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pddd_settings.object', {
#             'object': obj
#         })