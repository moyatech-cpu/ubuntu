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

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class Website(models.Model):
	_inherit = "website"

	@api.model
	def odoo_maintainance_mode(self):
		IrConfigParam = self.env['ir.config_parameter'].sudo()
		maintenance_mode = IrConfigParam.get_param('odoo_maintenance_mode.maintenance_mode')
		allowed_ips = IrConfigParam.get_param('odoo_maintenance_mode.allowed_ips')
		wk_display_page = False
		is_sigin_clicked = False
		accessible_user = False
		context = dict(request.session.context)
		context.update({'login_clicked': False})
		request.session.context = context
		if maintenance_mode:
			if allowed_ips:
				ip_list = []
				for ip in allowed_ips.split(","):
					ip_list.append(ip)
				user_ip = request.httprequest.environ['REMOTE_ADDR']
				if SUPERUSER_ID != self._uid:
					
					if user_ip not in ip_list:
						if request.httprequest.path != '/web/login':
							wk_display_page = True
						else:
							is_sigin_clicked = True
							context.update({'login_clicked': False})
					else:
						accessible_user = True
				else:
					accessible_user = True
		context.update({'accessible_user': accessible_user})
		return {'wk_display_page': wk_display_page, 'is_sigin_clicked': is_sigin_clicked, 'accessible_user': accessible_user}

	@api.model
	def get_config_id(self):
		IrConfigParam = self.env['ir.config_parameter']
		maintenance_mode_id = IrConfigParam.sudo().get_param('maintenance_mode_id')
		if maintenance_mode_id:
			maintenance_mode_obj = self.env[
				'maintenance.mode'].sudo().browse(int(maintenance_mode_id))
			return maintenance_mode_obj

	@api.model
	def get_page_header_message(self):
		obj = self.get_config_id()
		if obj:
			header = obj.page_header
			return header
		return False

	@api.model
	def get_page_descriptitive_message(self):
		obj = self.get_config_id()
		if obj:
			page_message = obj.page_message
			return page_message
		return False

	@api.model
	def get_login_page_message(self):
		obj = self.sudo().get_config_id()
		if obj:
			login_message = obj.login_message
			return login_message
		return False

	@api.model
	def get_admin_message(self):
		obj = self.sudo().get_config_id()
		if obj:
			admin_message = obj.admin_message
			return admin_message
		return False

	@api.model
	def get_image(self):
		obj = self.sudo().get_config_id()
		if obj:
			image = obj.image
			return obj
		return False

	@api.model
	def display_email_in_page(self):
		obj = self.sudo().get_config_id()
		if obj:
			display_email_field = obj.display_email_field
			return display_email_field
		return False

	@api.model
	def display_admin_message(self):
		obj = self.get_config_id()
		if obj:
			display_admin_mesage = obj.display_admin_mesage
			return display_admin_mesage
		return False

	@api.model
	def display_invalid_email_msg(self):
		obj = self.get_config_id()
		if obj:
			email_error_msg = obj.email_error_msg
			return email_error_msg
		return False

	@api.model
	def display_valid_email_msg(self):
		obj = self.get_config_id()
		if obj:
			email_valid_msg = obj.email_valid_msg
			return email_valid_msg
		return False
	@api.model
	def get_notification_header(self):
		obj = self.get_config_id()
		if obj:
			email_notif_title = obj.email_notif_title
			return email_notif_title
		return False
	@api.model
	def display_exists_email_msg(self):
		obj = self.get_config_id()
		if obj:
			email_exists = obj.email_exists
			return email_exists
		return False
