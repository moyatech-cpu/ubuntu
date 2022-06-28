# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TravelPurchaseOrder(models.Model):
    
    _inherit = "purchase.order"
    
    travel_order_id = fields.Many2one('project.task', string='Travel Order Reference', index=True, ondelete='cascade')
    travel_prod_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Text(string='Description', required=True)

