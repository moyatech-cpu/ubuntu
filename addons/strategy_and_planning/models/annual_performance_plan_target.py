from odoo import api, fields, models


class AnnualPerformancePlanTarget(models.Model):
    _name = 'annual.performance.plan.target'
    _rec_name = 'seq_name'

    seq_name = fields.Char(string='Seq Name')
    app_quarter_target_seq = fields.Char(string="APP Quarter Target Seq")
    exe_quarter_target_seq = fields.Char(string="Exe Quarter Target Seq")

    state = fields.Selection([('new', 'New'), ('team_approved', 'Team Approved'), ('ceo_approved', 'CEO Approved'),
                              ('reject', 'Rejected')], default='new', string="State")
    employee_id = fields.Many2one(related='annual_performance_plan_id.employee_id', string='Responsible Person')
    strategic_plan_id = fields.Many2one('strategic.plan', string='Strategic Plan')
    name = fields.Char(string='Title')
    annual_performance_plan_id = fields.Many2one('annual.performance.plan', string='Annual Target')
    strategic_goal_ids = fields.One2many('strategic.goals', 'annual_performance_plan_id', string='Strategic Goal',
                                         related='strategic_plan_id.strategic_goal_ids')
    strategic_plan_objectives_ids = fields.One2many('strategic.plan.objectives', 'annual_performance_plan_target_id',
                                                    string='Strategic Objectives')
    from_year = fields.Date(string='From Year', related='strategic_plan_id.from_year')
    to_year = fields.Date(string='To Year', related='strategic_plan_id.to_year')
    objective_statement = fields.Char(string='Objective Statement',
                                      related='annual_performance_plan_id.objective_statement')
    justification = fields.Char(string='Justification', related='annual_performance_plan_id.justification')
    budget = fields.Char(string='Budget', related='annual_performance_plan_id.budget')
    target = fields.Text(string='Target')
    baseline = fields.Text(string='Baseline')
    related_type_bool = fields.Selection(related='annual_performance_plan_id.type_bool', string='Related Type Bool')
    programme = fields.Many2one('business.units', string="Business Unit Responsible")
    indicator = fields.Text(string='Indicator')
    risk = fields.Text(string='Risk')
    evidence = fields.Text(string='Evidence')
    dependent_branch_1 = fields.Selection(
        [('B_r_u_d',
          'Branch: Regional and Urban Devlopment and Legislative Support. Previously Known As: Provincial and '
          'Municipal Government and Support'),
         ('B_c_w_p', 'Branch: Community Works Programme'),
         ('B_c_f_s', 'Branch: Corporate and Financial Services'),
         ('B_i_d_a', 'Branch: Institutional Devlopment AKA GIR'),
         ('B_n_d_m', 'Branch: National Disaster Management Center'),
         ('B_l_g_s',
          'Branch: Local Government Support and Intervention Management Prevously Known As: Policy, Research '
          'and Knowledge Management'),
         ('B_m_i_s', 'Branch: MISA'),
         ('B_i_d', 'Branch: Institutinal Devlopment'),
         ('C_i_a', 'Chief Directorate: Internal Audit'),
         ('B_c_l', 'Chief Directorate: Communications and Liason'),
         ('o_d_g', 'Office of the Director General'),
         ('c_o_o', 'Chief Operating Officer')], string="Dependent Branch 1")
    target_1 = fields.Char(string='Target 1')
    dependent_branch_2 = fields.Selection(
        [('B_r_u_d',
          'Branch: Regional and Urban Devlopment and Legislative Support. Previously Known As: '
          'Provincial and Municipal Government and Support'),
         ('B_c_w_p', 'Branch: Community Works Programme'),
         ('B_c_f_s', 'Branch: Corporate and Financial Services'),
         ('B_i_d_a', 'Branch: Institutional Devlopment AKA GIR'),
         ('B_n_d_m', 'Branch: National Disaster Management Center'),
         ('B_l_g_s',
          'Branch: Local Government Support and Intervention Management Prevously Known As:'
          ' Policy, Research and Knowledge Management'),
         ('B_m_i_s', 'Branch: MISA'),
         ('B_i_d', 'Branch: Institutinal Devlopment'),
         ('C_i_a', 'Chief Directorate: Internal Audit'),
         ('B_c_l', 'Chief Directorate: Communications and Liason'),
         ('o_d_g', 'Office of the Director General'),
         ('c_o_o', 'Chief Operating Officer')], string="Dependent Branch 2")
    target_2 = fields.Char(string='Target 2')
    dependent_branch_3 = fields.Selection(
        [('B_r_u_d',
          'Branch: Regional and Urban Devlopment and Legislative Support. Previously Known As: '
          'Provincial and Municipal Government and Support'),
         ('B_c_w_p', 'Branch: Community Works Programme'),
         ('B_c_f_s', 'Branch: Corporate and Financial Services'),
         ('B_i_d_a', 'Branch: Institutional Devlopment AKA GIR'),
         ('B_n_d_m', 'Branch: National Disaster Management Center'),
         ('B_l_g_s',
          'Branch: Local Government Support and Intervention Management Prevously Known As: '
          'Policy, Research and Knowledge Management'),
         ('B_m_i_s', 'Branch: MISA'),
         ('B_i_d', 'Branch: Institutinal Devlopment'),
         ('C_i_a', 'Chief Directorate: Internal Audit'),
         ('B_c_l', 'Chief Directorate: Communications and Liason'),
         ('o_d_g', 'Office of the Director General'),
         ('c_o_o', 'Chief Operating Officer')], string="Dependent Branch 3")
    target_3 = fields.Char(string='Target 3')
    dependent_branch_4 = fields.Selection(
        [('B_r_u_d',
          'Branch: Regional and Urban Devlopment and Legislative Support. Previously Known As: '
          'Provincial and Municipal Government and Support'),
         ('B_c_w_p', 'Branch: Community Works Programme'),
         ('B_c_f_s', 'Branch: Corporate and Financial Services'),
         ('B_i_d_a', 'Branch: Institutional Devlopment AKA GIR'),
         ('B_n_d_m', 'Branch: National Disaster Management Center'),
         ('B_l_g_s',
          'Branch: Local Government Support and Intervention Management Prevously Known As: '
          'Policy, Research and Knowledge Management'),
         ('B_m_i_s', 'Branch: MISA'),
         ('B_i_d', 'Branch: Institutinal Devlopment'),
         ('C_i_a', 'Chief Directorate: Internal Audit'),
         ('B_c_l', 'Chief Directorate: Communications and Liason'),
         ('o_d_g', 'Office of the Director General'),
         ('c_o_o', 'Chief Operating Officer')], string="Dependent Branch 4")
    target_4 = fields.Char(string='Target 4')
    dependent_branch_5 = fields.Selection(
        [('B_r_u_d',
          'Branch: Regional and Urban Devlopment and Legislative Support. Previously Known As: '
          'Provincial and Municipal Government and Support'),
         ('B_c_w_p', 'Branch: Community Works Programme'),
         ('B_c_f_s', 'Branch: Corporate and Financial Services'),
         ('B_i_d_a', 'Branch: Institutional Devlopment AKA GIR'),
         ('B_n_d_m', 'Branch: National Disaster Management Center'),
         ('B_l_g_s',
          'Branch: Local Government Support and Intervention Management Prevously Known As: '
          'Policy, Research and Knowledge Management'),
         ('B_m_i_s', 'Branch: MISA'),
         ('B_i_d', 'Branch: Institutinal Devlopment'),
         ('C_i_a', 'Chief Directorate: Internal Audit'),
         ('B_c_l', 'Chief Directorate: Communications and Liason'),
         ('o_d_g', 'Office of the Director General'),
         ('c_o_o', 'Chief Operating Officer')], string="Dependent Branch 5")
    target_5 = fields.Char(string='Target 5')
    external_dependencies = fields.Text(string='External Dependencies')
    quarterly_target_ids = fields.One2many('quarterly.target', 'annual_performance_plan_quarterly_target_id',
                                           string='Quarter Target')

    @api.model
    def create(self, vals):
        res = super(AnnualPerformancePlanTarget, self).create(vals)
        if res.related_type_bool == 'app':
            app_seq = self.env['ir.sequence'].next_by_code('app.quarter.target') or _('New')
            res.app_quarter_target_seq = app_seq
            res.seq_name = app_seq
        elif res.related_type_bool == 'exe':
            exe_seq = self.env['ir.sequence'].next_by_code('exe.quarter.target') or _('New')
            res.exe_quarter_target_seq = exe_seq
            res.seq_name = exe_seq

        return res

    @api.onchange('strategic_plan_id')
    def onchange_strategic_plan_id(self):
        if self.strategic_goal_ids:
            strategic_plan_objectives = self.env['strategic.plan.objectives'].search(

                [('id', 'in', self.strategic_goal_ids.ids)]).ids
            self.strategic_plan_objectives_ids = [(6, 0, strategic_plan_objectives)]

    @api.multi
    def create_monthly_smart_button(self):
        return {'name': 'Monthly Form',
                'view_type': 'form',
                'view_mode': 'tree',
                'views': [(self.env.ref('strategy_and_planning.view_app_monthly_target_main_form').id, 'form')],
                'res_model': 'monthly.target.main',
                'view_id': self.env.ref('strategy_and_planning.view_app_monthly_target_main_form').id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_strategic_goal_id': self.id,
                            'default_annual_target': self.annual_performance_plan_id.id, 'default_target_name': self.id,
                            'default_quarterly_target': self.id, 'default_responsible_employee_id': self.employee_id.id,
                            'default_type_bool': self.related_type_bool}
                }

    @api.multi
    def view_monthly_exe_target_smart_button(self):
        monthly_exe = self.env['monthly.target.main'].search([('quarterly_target', '=', self.id)])
        monthly_exe_action = self.env.ref('strategy_and_planning.action_execution_plan_monthly_target').read()[0]
        if len(monthly_exe) >= 1:
            monthly_exe_action['domain'] = [('id', 'in', monthly_exe.ids)]
            return monthly_exe_action
        else:
            return None

    @api.multi
    def view_monthly_app_target_smart_button(self):
        monthly_app = self.env['monthly.target.main'].search([('quarterly_target', '=', self.id)])
        print('----monthly_app------>>>--', monthly_app)
        monthly_app_action = self.env.ref('strategy_and_planning.action_monthly_target_main_target').read()[0]
        if len(monthly_app) >= 1:
            monthly_app_action['domain'] = [('id', 'in', monthly_app.ids)]
            return monthly_app_action
        else:
            return None

    @api.multi
    def action_team_approve(self):
        return self.write({
            'state': 'team_approved'
        })

    @api.multi
    def action_ceo_approved(self):
        return self.write({
            'state': 'ceo_approved'
        })

    @api.multi
    def action_reject(self):
        return self.write({
            'state': 'reject'
        })

    @api.multi
    def get_rb_data(self):
        print('----se;lfffff---', self)
        reportback_data = self.env['report.back'].search([('quarter_id', '=', int(self.id))])
        if reportback_data:
            return reportback_data.ids
        else:
            return False


class QuarterlyTarget(models.Model):
    _name = 'quarterly.target'
    _rec_name = 'quarter_target'

    annual_performance_plan_quarterly_target_id = fields.Many2one('annual.performance.plan.target',
                                                                  string='Annual Performance Plan Quarterly Target')
    annual_performance_plan_quarterly_id = fields.Many2one('annual.performance.plan',
                                                           string='Annual Performance Plan Target')
    quarter = fields.Selection([('quarter_one', 'Quarter 1'), ('quarter_two', 'Quarter 2'),
                                ('quarter_three', 'Quarter 3'), ('quarter_four', 'Quarter 4')],
                               string='Select Quarter')
    quarter_target = fields.Text(string='Quarter Target')
    quarter_budget = fields.Char(string='Budget')
    quarter_evidence = fields.Text(string='Evidence')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self._context.get('xyz'):
            quarter_targets = self.env['annual.performance.plan.target'].search([('id', '=', self._context.get('xyz'))])
            lot_ids = self.search([('id', 'in', quarter_targets.quarterly_target_ids.ids)])
        else:
            lot_ids = self.search([])
        return lot_ids.name_get()


class MonthlyTargetMain(models.Model):
    _name = 'monthly.target.main'
    _rec_name = 'seq_name'

    seq_name = fields.Char(string='Seq Name')
    app_month_target_seq = fields.Char(string="APP Month Target Seq")
    exe_month_target_seq = fields.Char(string="Exe Month Target Seq")
    state = fields.Selection([('new', 'New'), ('team_approved', 'Team Approved'), ('ceo_approved', 'CEO Approved'),
                              ('reject', 'Rejected')], default='new', string="State")
    name = fields.Char(string='Title')
    target_name = fields.Many2one('quarterly.target', string='Quarterly Target')
    description = fields.Text(string='Description')
    date = fields.Date(string='Date')
    performance_indicator = fields.Char(string='Performance Indicator')
    annual_target = fields.Many2one('annual.performance.plan', string='Annual Target')
    quarterly_target = fields.Many2one('annual.performance.plan.target', string='Quarterly Target')
    responsible_employee_id = fields.Many2one('hr.employee', string='Responsible Employee')
    monthly_target_ids = fields.One2many('monthly.target', 'monthly_target_main_id', string='Monthly Target')
    type_bool = fields.Selection([('app', 'APP'), ('exe', 'execution')], string='Type')
    reportback_id = fields.Many2one('report.back', string='Report Back')

    @api.multi
    def action_team_approve(self):
        return self.write({
            'state': 'team_approved'
        })

    @api.multi
    def action_ceo_approve(self):
        return self.write({
            'state': 'ceo_approved'
        })

    @api.multi
    def action_reject(self):
        return self.write({
            'state': 'reject'
        })

    @api.model
    def create(self, vals):
        res = super(MonthlyTargetMain, self).create(vals)
        if res.type_bool == 'app':
            app_seq = self.env['ir.sequence'].next_by_code('app.month.target') or _('New')
            res.app_month_target_seq = app_seq
            res.seq_name = app_seq
        elif res.type_bool == 'exe':
            exe_seq = self.env['ir.sequence'].next_by_code('exe.month.target') or _('New')
            res.exe_month_target_seq = exe_seq
            res.seq_name = exe_seq
        return res

    @api.multi
    def get_rb_data(self):
        print('----se;lfffff---', self)
        reportback_data = self.env['report.back'].search([('monthly_id', '=', int(self.id))])
        print('--reportback_data--', reportback_data)
        if reportback_data:
            return reportback_data.ids
        else:
            return False


class MonthlyTarget(models.Model):
    _name = 'monthly.target'
    _rec_name = 'monthly_target'

    monthly_target_main_id = fields.Many2one('monthly.target.main',
                                             string='Monthly Target')
    quarterly_target__id = fields.Many2one('quarterly.target',
                                           string='Quarterly Target')
    quarter_main_id = fields.Many2one(related='monthly_target_main_id.quarterly_target', string='Quarter Main ID')
    monthly = fields.Selection([('jan', 'January'), ('feb', 'February'), ('mar', 'March'), ('apr', 'April'),
                                ('may', 'May'), ('jun', 'June'), ('jul', 'July'), ('aug', 'August'),
                                ('sep', 'September'), ('oct', 'october'), ('nov', 'November'), ('dec', 'December')],
                               string='Select Month')
    monthly_target = fields.Text(string='Month Target')
    monthly_evidence = fields.Text(string='Evidence')
    monthly_bugget = fields.Char(string='Budget')
    quarter_select = fields.Selection([('quarter_one', 'Quarter 1'), ('quarter_two', 'Quarter 2'),
                                       ('quarter_three', 'Quarter 3'), ('quarter_four', 'Quarter 4')],
                                      string='Quarter')

    @api.onchange('quarterly_target__id')
    def onchange_select_quarter(self):
        if self.quarterly_target__id:
            self.quarter_select = self.quarterly_target__id.quarter
