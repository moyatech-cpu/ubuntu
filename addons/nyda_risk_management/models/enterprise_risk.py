# -*- coding: utf-8 -*-
from odoo import fields, models

class EnterpriseRisk(models.Model):
    """ Enterprise Risk Model """
    
    _name = "enterprise_risk"
    _description = "Enterprise Risk"

    @api.multi
    def default_all_risks(self):
        #url = '<iframe src="http://cs.transcendmx.com/dashboard.php?user={self.env.user.id}" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        url = '<iframe src="http://moyatech.co.za/nydarisk/management/review_risks.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url

    @api.multi
    def default_strategic_risks(self):
        url = '<iframe src="http://moyatech.co.za/nydarisk/management/strategic_risks.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url

    @api.multi
    def default_operational_risks(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/management/operational_risks.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
        
    @api.multi
    def default_risk_appetite(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/risk_appetite.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_risk_trend(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/trend.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_heat_map(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/likelihood_impact.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url

    @api.multi
    def default_risk_advice(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/riskadvice.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url  
    
    @api.multi
    def default_risk_mitigations(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/mitigations_by_date.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_risk_reviews(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/mgmt_reviews_by_date.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_performance_report(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/likelihood_impact.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_performance_dashboard(self):
        url = '<iframe src="http://www.moyatech.co.za/nydarisk/reports/likelihood_impact.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url
    
    @api.multi
    def default_risk_settings(self):
        url = '<iframe src="https://www.moyatech.co.za/nydarisk/admin/index.php" seamless="seamless" scrolling="no" allowfullscreen="true"  webkitallowfullscreen="true" mozallowfullscreen="true" frameborder="0" style="width:100%; height: 4000px;overflow:initial;" />'
        return url           
                                      
    all_risks               = fields.Html(string="Primnet URL", default=lambda self: self.default_all_risks())
    #strategic_risks         = fields.Html(string="Primnet URL", default=lambda self: self.default_strategic_risks())
    #operational_risks       = fields.Html(string="Primnet URL", default=lambda self: self.default_operational_risks())
    #risk_appetite           = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_appetite())
    #risk_trend              = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_trend())
    #heat_map                = fields.Html(string="Primnet URL", default=lambda self: self.default_heat_map())
    #risk_advice             = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_advice())
    #risk_mitigations        = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_mitigations())
    #risk_reviews            = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_reviews())
    #performance_report      = fields.Html(string="Primnet URL", default=lambda self: self.default_performance_report())
    #performance_dashboard   = fields.Html(string="Primnet URL", default=lambda self: self.default_performance_dashboard())
    #risk_settings           = fields.Html(string="Primnet URL", default=lambda self: self.default_risk_settings())