# -*- coding: utf-8 -*-

from . import wizard
from . import models

from odoo import api, SUPERUSER_ID, tools
import base64
from odoo.modules import get_module_resource

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    new_stage = env['helpdesk_lite.stage'].search(
        [('id', '=', env.ref('helpdesk_lite.stage_new').id)])
    progress_stage = env['helpdesk_lite.stage'].search(
        [('id', '=', env.ref('helpdesk_lite.stage_inprogress').id)])
    solved_stage = env['helpdesk_lite.stage'].search(
        [('id', '=', env.ref('helpdesk_lite.stage_solved').id)])
    cancelled_stage = env['helpdesk_lite.stage'].search(
        [('id', '=', env.ref('helpdesk_lite.stage_canceled').id)])
    if new_stage:
        img_path = get_module_resource('facility', 'static/description', 'new.png')
        with open(img_path, 'rb') as f:
            image = f.read()
        new_stage.write({
            'dashboard_icon': base64.b64encode(image)
        })
    if progress_stage:
        img_path = get_module_resource('facility', 'static/description', 'progress.png')
        with open(img_path, 'rb') as f:
            image = f.read()
        progress_stage.write({
            'dashboard_icon': base64.b64encode(image)
        })
    if solved_stage:
        img_path = get_module_resource('facility', 'static/description', 'solved.png')
        with open(img_path, 'rb') as f:
            image = f.read()
        solved_stage.write({
            'dashboard_icon': base64.b64encode(image)
        })
    if cancelled_stage:
        img_path = get_module_resource('facility', 'static/description', 'cancel.png')
        with open(img_path, 'rb') as f:
            image = f.read()
        cancelled_stage.write({
            'dashboard_icon': base64.b64encode(image)
        })