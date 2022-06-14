# -*- coding: utf-8 -*-

from odoo import models, fields, api

class primnet_integration(models.Model):
    _name = 'monitoring'

    @api.multi
    def default_dashboard(self):
        #url = '<iframe src="http://cs.transcendmx.com/login.inc.php?user=admin&pass=cogta2013" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        url = '<iframe src="http://cs.transcendmx.com/dashboard.php?user={self.env.user.id}" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url

    @api.multi
    def default_control_center(self):
        url = '<iframe src="http://cs.transcendmx.com/controlcentre.php?user={self.env.user.id}" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url

    @api.multi
    def default_org_plans(self):
        url = '<iframe src="http://cs.transcendmx.com/stratplan.php?user={self.env.user.id}" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
        
    @api.multi
    def default_window_period(self):
        url = '<iframe src="http://cs.transcendmx.com/windowperiod.php?user={self.env.user.id}" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_quarterly_report(self):
        url = '<iframe src="http://cs.transcendmx.com/report.php?user={self.env.user.id}" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_org_report(self):
        url = '<iframe src="http://cs.transcendmx.com/reviewreport.php?user={self.env.user.id}" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
                         
    overall_dashboard   = fields.Html(string="Primnet URL", default=lambda self: self.default_dashboard())
    control_center      = fields.Html(string="Primnet URL", default=lambda self: self.default_control_center())
    org_plans           = fields.Html(string="Primnet URL", default=lambda self: self.default_org_plans())
    window_period       = fields.Html(string="Primnet URL", default=lambda self: self.default_window_period())
    quarterly_report    = fields.Html(string="Primnet URL", default=lambda self: self.default_quarterly_report())
    org_report          = fields.Html(string="Primnet URL", default=lambda self: self.default_org_report())