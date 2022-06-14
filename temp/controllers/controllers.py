# -*- coding: utf-8 -*-
from odoo import http

# class GrantAndVoucherUpdate(http.Controller):
#     @http.route('/grant_and_voucher_update/grant_and_voucher_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/grant_and_voucher_update/grant_and_voucher_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('grant_and_voucher_update.listing', {
#             'root': '/grant_and_voucher_update/grant_and_voucher_update',
#             'objects': http.request.env['grant_and_voucher_update.grant_and_voucher_update'].search([]),
#         })

#     @http.route('/grant_and_voucher_update/grant_and_voucher_update/objects/<model("grant_and_voucher_update.grant_and_voucher_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('grant_and_voucher_update.object', {
#             'object': obj
#         })