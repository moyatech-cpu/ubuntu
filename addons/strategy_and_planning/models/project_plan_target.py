from odoo import api, fields, models


class ProjectPlanTarget(models.Model):
    _name = 'project.plan.target'

    app_target = fields.Many2one('annual.performance.plan.target', string='APP Target')
    app_target_budget = fields.Char(string='APP Target Budget')
    project_plan_linkage = fields.Many2one('project.plan.linkage', string='Project Plan Linkage')
    project_plan_linkage_budget = fields.Char(string='Project Plan Linkage Budget')
