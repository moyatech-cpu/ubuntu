from odoo import api, fields, models


class ProjectPlanLinkage(models.Model):
    _name = 'project.plan.linkage'

    app_target = fields.Many2one('annual.performance.plan.target', string='APP Target')
    delegation = fields.Char(stirng='Delegation')
    budget = fields.Char(stirng='Budget')
    project_name_linkage = fields.Char(stirng='Project Name/Linkage')
