# -*- coding: utf-8 -*-
from odoo import http

# class NydaAssetManagement(http.Controller):
#     @http.route('/nyda_asset_management/nyda_asset_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nyda_asset_management/nyda_asset_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nyda_asset_management.listing', {
#             'root': '/nyda_asset_management/nyda_asset_management',
#             'objects': http.request.env['nyda_asset_management.nyda_asset_management'].search([]),
#         })

#     @http.route('/nyda_asset_management/nyda_asset_management/objects/<model("nyda_asset_management.nyda_asset_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nyda_asset_management.object', {
#             'object': obj
#         })