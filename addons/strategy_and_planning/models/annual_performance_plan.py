from odoo import api, fields, models
from datetime import datetime


class AnnualPerformancePlan(models.Model):
    _name = 'annual.performance.plan'
    _rec_name = 'seq_name'

    app_annual_target_seq = fields.Char(string="APP Annual Target Seq")
    exe_annual_target_seq = fields.Char(string="Exe Annual Target Seq")

    seq_name = fields.Char(string='Seq Name')

    state = fields.Selection([('new', 'New'), ('team_approved', 'Team Approved'), ('ceo_approved', 'CEO Approved'),
                              ('reject', 'Rejected')], default='new', string="State")
    employee_id = fields.Many2one('hr.employee', string='Responsible Person')
    strategic_plan_id = fields.Many2one('strategic.plan', string='Strategic Plan')
    name = fields.Char(string='Title')
    strategic_goal_ids = fields.One2many('strategic.goals', 'annual_performance_plan_id',
                                         related='strategic_plan_id.strategic_goal_ids', string='Strategic Goal')
    strategic_plan_objectives_ids = fields.One2many('strategic.plan.objectives', 'annual_performance_plan_id',
                                                    string='Strategic Objectives')
    from_year = fields.Date(string='From Year', related='strategic_plan_id.from_year')
    to_year = fields.Date(string='To Year', related='strategic_plan_id.to_year')
    objective_statement = fields.Char(string='Objective Statement')
    justification = fields.Char(string='Justification')
    strategic_objective_short_name = fields.Char(string='Strategic Objective (Short Name)')
    budget = fields.Char(string='Budget')
    financial_year = fields.Datetime(string='Financial Year')
    year = fields.Selection([(y, str(y)) for y in range(1995, (datetime.now().year + 100) + 1)],
                            stirng='Financial Year')
    delegation = fields.Many2one('hr.department', string='Division Responsible')
    performance_indicator = fields.Text(string='Performance Indicator')
    ceo_id = fields.Many2one('res.users', string="CEO")
    type_bool = fields.Selection([('app', 'APP'), ('exe', 'execution')], string='Type')
    strategic_objectives_id = fields.Many2one('strategic.plan.objectives', string='Strategic Objectives')
    annual_target = fields.Text(string='Annual Target', related='strategic_objectives_id.strategic_objective')
    readonly_bool = fields.Boolean(string='Readonly boolean')

    @api.model
    def create(self, vals):
        res = super(AnnualPerformancePlan, self).create(vals)
        if res.type_bool == 'app':
            # if not res.app_annual_target_seq:
            print('in if cond--------->>>>>>')
            app_seq = self.env['ir.sequence'].next_by_code('app.annual.performance.plan') or _('New')
            res.app_annual_target_seq = app_seq
            res.seq_name = app_seq

        elif res.type_bool == 'exe':
            # if not res.exe_annual_target_seq:
            print('in else------->>>>')
            exe_seq = self.env['ir.sequence'].next_by_code('exe.annual.performance.plan') or _('New')
            res.exe_annual_target_seq = exe_seq
            res.seq_name = exe_seq

        return res


    @api.onchange('strategic_plan_id')
    def onchange_strategic_plan_id(self):
        if self.strategic_plan_id:
            strategic_goals = self.env['strategic.goals'].search(
                [('strategic_plan_id', '=', self.strategic_plan_id.id)]).ids

            strategic_objects = self.env['strategic.plan.objectives'].search(
                [('strategic_goal_id', '=', strategic_goals)]).ids
            self.readonly_bool = True
            return {'domain': {'strategic_objectives_id': [('id', 'in', strategic_objects)]}, }
        # if self.strategic_goal_ids:
        #     strategic_plan_objectives = self.env['strategic.plan.objectives'].search(
        #         [('id', 'in', self.strategic_goal_ids.ids)]).ids
        #     self.strategic_plan_objectives_ids = [(6, 0, strategic_plan_objectives)]

    # @api.multi
    # def get_years(self):
    #     year_list = []
    #     for i in range(2016, 2036):
    #         year_list.append((i, str(i)))
    #     return year_list

    @api.multi
    def create_quarterly_smart_button(self):
        print("create_quarterly_smart_button call thyu", self.id)
        return {'name': 'Quarterly Form',
                'view_type': 'form',
                'view_mode': 'tree',
                'views': [(self.env.ref('strategy_and_planning.view_annual_performance_plan_target_form').id, 'form')],
                'res_model': 'annual.performance.plan.target',
                'view_id': self.env.ref('strategy_and_planning.view_annual_performance_plan_target_form').id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_strategic_plan_id': self.strategic_plan_id.id, 'default_from_year': self.from_year,
                            'default_to_year': self.to_year, 'default_annual_performance_plan_id': self.id,
                            'default_budget': self.budget}
                }

    @api.multi
    def view_quartely_app_target_smart_button(self):
        quartely_app = self.env['annual.performance.plan.target'].search([('annual_performance_plan_id', '=', self.id)])
        quartely_app_action = self.env.ref('strategy_and_planning.action_annual_performance_plan_target').read()[0]
        if len(quartely_app) >= 1:
            quartely_app_action['domain'] = [('id', 'in', quartely_app.ids)]
            return quartely_app_action
        else:
            return None

    @api.multi
    def view_quartely_exe_target_smart_button(self):
        quartely_exe = self.env['annual.performance.plan.target'].search([('annual_performance_plan_id', '=', self.id)])
        quartely_exe_action = self.env.ref('strategy_and_planning.action_execution_plan_target').read()[0]
        if len(quartely_exe) >= 1:
            quartely_exe_action['domain'] = [('id', 'in', quartely_exe.ids)]
            return quartely_exe_action
        else:
            return None

    # @api.model
    # def create(self, vals):
    #     if self.type_bool == 'app':
    #         print('------', self.type_bool)
    #         planning_email_template = self.env.ref(
    #             'strategy_and_planning.planning_ed_email_template')
    #         planning_email_template.send_mail(self.id, force_send=True)
    #         print('----planning_email_template----', planning_email_template)
    #     # return super(AnnualPerformancePlan, self).create(vals)

    @api.multi
    def action_team_approve(self):
        return self.write({
            'state': 'team_approved'
        })

    @api.multi
    def action_ceo_approve(self):
        self.write({
            'ceo_id': self.env.user.id,
            'state': 'ceo_approved'
        })
        if self.state == "ceo_approved":
            eds = self.env['res.users'].search(
                [("groups_id", "=", self.env.ref("strategy_and_planning.group_executive_director").id)])
            for ed in eds:
                email_template = self.env.ref('strategy_and_planning.execution_plan_email_template')
                if email_template:
                    self.env['mail.template'].browse(email_template.id).send_mail(self.id, force_send=True,
                                                                                  email_values={
                                                                                      'email_to': ed.login
                                                                                  })
        return True

    @api.multi
    def action_reject(self):
        return self.write({
            'state': 'reject'
        })

    @api.multi
    def get_rb_data(self):
        print('----se;lfffff---', self)
        reportback_data = self.env['report.back'].search([('annual_id', '=', int(self.id))])
        if reportback_data:
            return reportback_data.ids
        else:
            return False
