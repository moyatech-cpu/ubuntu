# -*- coding: utf-8 -*-
from odoo import http

# class NydaRegionalReportsUpdate(http.Controller):
#     @http.route('/nyda_regional_reports_update/nyda_regional_reports_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nyda_regional_reports_update/nyda_regional_reports_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nyda_regional_reports_update.listing', {
#             'root': '/nyda_regional_reports_update/nyda_regional_reports_update',
#             'objects': http.request.env['nyda_regional_reports_update.nyda_regional_reports_update'].search([]),
#         })

#     @http.route('/nyda_regional_reports_update/nyda_regional_reports_update/objects/<model("nyda_regional_reports_update.nyda_regional_reports_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nyda_regional_reports_update.object', {
#             'object': obj
#         })