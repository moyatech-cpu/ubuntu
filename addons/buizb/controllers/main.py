# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteConatctUsCreate(http.Controller):

    @http.route('/contact_us_lead', type='json', auth='public', website=True)
    def create_subscribe(self, **data):
        data = data and data['datas']
        res = dict()
        for d in eval(data):
            res[d.get('name')] = d.get('value')
        subscribe = request.env['crm.lead'].sudo().create({
            'name': res.get('name'),
            'phone': res.get('phone'),
            'email_from': res.get('email'),
            'description': res.get('message'),
        })
        if not subscribe:
            return False
