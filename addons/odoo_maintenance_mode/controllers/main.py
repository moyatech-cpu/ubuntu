# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
from odoo.addons.web.controllers.main import WebClient, Binary, Home
import werkzeug.utils
import logging
import odoo
_logger = logging.getLogger(__name__)


class Home(Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        
        res = super(Home, self).web_client()
        maintainance_mode = request.env['website'].odoo_maintainance_mode()
        if maintainance_mode['wk_display_page']:
            return werkzeug.utils.redirect('/')
        return res

    @http.route('/web/login', type='http', auth="none", sitemap=False)
    def web_login(self, redirect=None, **kw):
        response = super(Home, self).web_login(redirect=redirect, **kw)
        if not redirect and request.params['login_success']:
        # # #     _logger.info('----------eee-----22-----%r',request.params['login_success'])
            maintainance_mode = request.env['website'].odoo_maintainance_mode()
            if maintainance_mode['is_sigin_clicked']:
                context = dict(request.session.context)
                context.update({'login_clicked': True})
                request.session.context = context
                return http.redirect_with_hash(redirect)
        return response

    @http.route('/subscriber/email', type='json', auth="public", website=True)
    def subscriber_email(self, email=False, **kw):
        if email:
            email = email.strip()
            subscriber_obj = request.env['wk.subscriber.emails']
            maintenance_mode_id = False
            obj = request.env['website'].get_config_id()
            if obj:
                maintenance_mode_id = obj.id
            exists = subscriber_obj.sudo().search([('email', '=', email)])
            if exists:
                if exists.state == 'pending':
                    return 'already_exists'
                else:
                    exists.write({'state': 'pending'})
            else:
                subscriber_obj.sudo().create(
                    {'email': email, 'state': 'pending', 'maintenance_mode_id': maintenance_mode_id})
            return 'new_customer'
        return False
