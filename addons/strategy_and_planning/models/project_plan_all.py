from odoo import api, fields, models


class ProjectPlanAll(models.Model):
    _name = 'project.plan.all'

    strategic_plan_id = fields.Many2one('strategic.plan', string='Strategic Plan')
    from_year = fields.Date(string='From Year')
    to_year = fields.Date(string='To Year')
    # goal_statement_id = fields.Many2one('', string='Goal Statement')
    # strategic_objective = fields.Many2one('', string='Strategic Objective')
    # app_strategic_objective = fields.Many2one('', string='APP Strategic Objective')
    # app_target = fields.Many2one('', string='APP Target')
    # action_project_linkage = fields.Many2one('', string='Action Project Name/Linkage')
    delegation = fields.Char(String='Delegation')
    target = fields.Char(String='Target')
    dependencies = fields.Char(String='Dependencies')
