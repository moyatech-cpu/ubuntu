# -*- coding: utf-8 -*-
from odoo import http

# class CancelTrainingUpdate(http.Controller):
#     @http.route('/cancel_training_update/cancel_training_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cancel_training_update/cancel_training_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cancel_training_update.listing', {
#             'root': '/cancel_training_update/cancel_training_update',
#             'objects': http.request.env['cancel_training_update.cancel_training_update'].search([]),
#         })

#     @http.route('/cancel_training_update/cancel_training_update/objects/<model("cancel_training_update.cancel_training_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cancel_training_update.object', {
#             'object': obj
#         })