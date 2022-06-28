# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import ValidationError
from datetime import date
from lxml import etree

class LearningDevelopment(models.Model):
    _name = 'learning.development'
    _rec_name = 'forename'
    _description = 'Learning Development'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    @api.multi
    def default_user_name(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.name

    @api.multi
    def default_user_surname(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.surname

    @api.multi
    def default_emp_number(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.employee_number

    @api.multi
    def default_divsion(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.department_id.id

    @api.multi
    def default_position(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.job_id.id

    @api.multi
    def default_branch(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.branch_id.id

    @api.multi
    def default_province(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.x_provincial_office.id

    @api.multi
    def default_qualification(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.previous_qualification

    @api.multi
    def default_id_num(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.identification_id

    @api.multi
    def default_address(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.physical_address

    @api.multi
    def default_manager(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.parent_id

    type = fields.Selection([('bursary_request', 'Bursary Request'), ('ext_courses', 'External Courses')], string="Type")
    state = fields.Selection(
        [('bursary_req', 'New'), ('line_manager', 'Line Manager'), ('hod', 'Head of Division'), ('adjudication', 'Adjudication'), ('ld_manager', 'L&D Review'),
         ('ceo', 'CEO Review'), ('bursary_app', 'Approved'), ('bursary_reject','Rejected')], string="State", default='bursary_req', group_expand='_expand_states')

    FOLDED_STATES = ['bursary_reject','bursary_app','ceo','ld_manager']

    # Comments
    line_comments = fields.Text(string="Line Manager Comments")
    hod_comments = fields.Text(string="HOD Comments")
    adjudication_comments = fields.Text(string="Adjudication Comments")
    ld_comments = fields.Text(string="Learning and Development Comments")
    ceo_comments = fields.Text(string="CEO Comments")

    # Personal Details
    forename = fields.Char(string="Full Name", default=lambda self: self.default_user_name())
    surname = fields.Char(string="Surname", default=lambda self: self.default_user_surname())
    emp_number = fields.Char(string="Employment Number", default=lambda self: self.default_emp_number())
    division_id = fields.Many2one('hr.department', string="Division", default = lambda self: self.default_divsion())
    position_id = fields.Many2one('hr.job', string="Position", default = lambda self: self.default_position())
    branch_id = fields.Many2one('res.branch', string="Branch", default = lambda self: self.default_branch())
    province_id = fields.Many2one('res.country.state', domain=[('country_id.name', '=', 'South Africa')], string="Province", default = lambda self: self.default_province())
    obtained_qualifications = fields.Text(string="Previous Obtained Qualifications(Studies)", default = lambda self: self.default_qualification())
    app_id_num = fields.Char(string="Applicant's identity number", default = lambda self: self.default_id_num())
    physical_address = fields.Text(string="Physical Address", default = lambda self: self.default_address())
    manager_id = fields.Many2one('hr.employee', string="Manager", default = lambda self: self.default_manager())
    # Bursary request
    previous_sponsored = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                          string="Previously Sponsored Qualification Continuation")
    new_qualification = fields.Selection([('yes','Yes'),('no','No')], string="New Qualification")
    app_motivation = fields.Text(string="Application Motivation")
    proposed_qualification = fields.Text(string="Proposed Qualification")
    nqf_level = fields.Integer(string="NQF Level")
    bursary_institution_id = fields.Many2one('institution', string="Institution")
    year_of_study = fields.Selection(
        [('first_year', '1st Year'), ('second_year', '2nd  Year'), ('third_year', '3rd Year'),
         ('fourth_year', '4th Year')], string="Year Of Study")
    method_of_study = fields.Selection(
        [('part_time', 'Part-time'), ('online', 'Online'), ('study_blocks', 'Study Blocks')], string="Method Of Study")
    anticipated_year_of_completion = fields.Char(string="Anticipated Year Of Completion")
    financial_year = fields.Selection([('2021/22', '2021/22'), ('2022/23', '2022/23'), ('2023/24', '2023/24'),('2024/25', '2024/25'),
                                       ('2025/26', '2025/26'),('2026/27', '2026/27')], string="Financial Year")
    # Previous Sponsored Studies
    previous_sponsored_qualification_studies = fields.Text(string="Previous Sponsored Qualification/Studies")
    studies_institution_id = fields.Many2one('institution', string="Institution")
    student_number = fields.Text(string="Student Number")
    commenced_support_year = fields.Integer(string="Year in Which Support Commenced")
    commenced_study_year = fields.Integer(string="Year of Commencement of Sponsored Study")
    qualification_completed = fields.Boolean(string="Qaulification Completed")
    studies_completion_date = fields.Integer(string="Date of Completion of Studies")
    previous_academic_record = fields.Binary(string="Previous Academic Record")
    previous_academic_record_name = fields.Char(string="Previous Academic Record")
    # Disclaimer
    total_repay = fields.Integer(string="Total Bursary Repay Amount")
    amt_in_words = fields.Text(string="Amount In Words")
    disc_address = fields.Text(string="Physical Address")
    app_signature = fields.Binary(string="Applicant Signature")
    first_witness_name = fields.Char(string="First Witness Name")
    first_witness_surname = fields.Char(string="First Witness Surname")
    first_witness_signature = fields.Binary(string="First Witness Signature")
    second_witness_name = fields.Char(string="Second Witness Name")
    second_witness_surname = fields.Char(string="Second Witness Surname")
    second_witness_signature = fields.Binary(string="Second Witness Signature")
    # Documents
    proof_of_reg = fields.Binary(string="Proof Of Registration")
    proof_of_reg_name = fields.Char(string="Proof Of Registration Name")
    course_outline = fields.Binary(string="Course Outline")
    course_outline_name = fields.Char(string="Course Outline Name")
    quotation = fields.Binary(string="Quotation")
    quotation_name = fields.Char(string="Quotation Name")
    # Line Manager
    ind_perf = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                string="Does the individual’s performance on the job meet the expectations of the NYDA ?")
    app_per = fields.Integer(string="Applicant performance appraisal score")
    app_study = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                string="Are the studies appropriate to individual’s proposed career progression ?")
    car_dev = fields.Text(
        string="Motivate how the proposed studies support the Career Development Plan of the applicant ?")
    nyda_prop_study = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                string="Does the proposed study suit the NYDA’s resource requirements ?")
    prop_study = fields.Text(
        string="Motivate how the proposed studies will enhance the Performance Activities of the applicant? ")
    provided_support = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                        string="Was the individual provided with adequate support to achieve successful results in the previous academic year studies ?")
    motivation = fields.Text(string="Motivation")
    previous_year_motivation = fields.Text(
        string="Motivate how the previous academic year’s studies improved the performance of the applicant.")
    # Booking Info
    inst_name = fields.Char(string="Name Of Institution")
    inst_add = fields.Text(string="Address Of Institution")
    inst_number = fields.Char(string="Contact Numbers Of Institution")
    inst_course_name = fields.Char(string="Course / Conference / Workshop Title")
    duration = fields.Float(string="Duration")
    date = fields.Date(string="Date")
    qual_obtained = fields.Char(string="Qualification To Be Obtained")
    total_costs = fields.Integer(string="Total Costs")
    # Travel Arrangements
    req_travel = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Do you require travel ?")
    dept_place = fields.Char(string="Departure Place")
    dept_date = fields.Date(string="Departure date")
    return_date = fields.Date(string="Return date")
    air_travel = fields.Char(string="Air Travel (Flight)")
    inst_province_id = fields.Many2one('res.country.state', string="Province")
    #airpot_id = fields.Many2one('airpot', string="Airpot")
    voyage_number = fields.Char(string="Voyager Number: (if applicable)")
    acc_req = fields.Boolean(string="Accommodation required")
    smoking = fields.Boolean(string="Smoking")
    non_smoking = fields.Boolean(string="Non-Smoking")
    land_travel = fields.Char(string="Land Travel (transfers)")
    car_rental = fields.Char(string="Car rental")
    shuttle_service = fields.Char(string="Shuttle services")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(LearningDevelopment, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type != 'search' and self.env.uid != SUPERUSER_ID:
            has_my_group = self.env.user.has_group('learning_development.group_learn_dev_admin')
            if not has_my_group:
                if self._context.get('default_type') == 'bursary_request':
                    root = etree.fromstring(res['arch'])
                    root.set('create', 'false')
                    res['arch'] = etree.tostring(root)
        return res

    def lm_app_req(self):
        admin_group = self.env.ref('base.group_system').users.ids
        lm_group = self.env.ref('strategy_and_planning.group_line_manager').users.ids
        group_list = lm_group + admin_group
        if self.env.user.id in group_list:
            action = self.env.ref('learning_development.action_approve_wizard').read()[0]
            return action
        else:
            raise ValidationError(_("Only Line Manager or Administrator can approve it !!"))

    def lm_rej_req(self):
        admin_group = self.env.ref('base.group_system').users.ids
        lm_group = self.env.ref('strategy_and_planning.group_line_manager').users.ids
        group_list = lm_group + admin_group
        if self.env.user.id in group_list:
            action = self.env.ref('learning_development.action_reject_wizard').read()[0]
            return action
        else:
            raise ValidationError(_("Only Line Manager or Administrator can approve it !!"))

    def hod_app_req(self):
        admin_group = self.env.ref('base.group_system').users.ids
        hod_group = self.env.ref('learning_development.group_hod').users.ids
        group_list = hod_group + admin_group
        if self.env.user.id in group_list:
            action = self.env.ref('learning_development.action_approve_wizard').read()[0]
            return action
        else:
            raise ValidationError(_("Only Head Of Division or Administrator can approve it !!"))

    def hod_rej_req(self):
        admin_group = self.env.ref('base.group_system').users.ids
        hod_group = self.env.ref('learning_development.group_hod').users.ids
        group_list = hod_group + admin_group
        if self.env.user.id in group_list:
            action = self.env.ref('learning_development.action_reject_wizard').read()[0]
            return action
        else:
            raise ValidationError(_("Only Head Of Division or Administrator can approve it !!"))

    def ldm_app_req(self):
        admin_group = self.env.ref('base.group_system').users.ids
        ld_group = self.env.ref('learning_development.group_ld_manager').users.ids
        group_list = ld_group + admin_group
        if self.env.user.id in group_list:
            action = self.env.ref('learning_development.action_approve_wizard').read()[0]
            return action
        else:
            raise ValidationError(_("Only L&D Manager or Administrator can approve it !!"))

    def ldm_rej_req(self):
        admin_group = self.env.ref('base.group_system').users.ids
        ld_group = self.env.ref('learning_development.group_ld_manager').users.ids
        group_list = ld_group + admin_group
        if self.env.user.id in group_list:
            action = self.env.ref('learning_development.action_reject_wizard').read()[0]
            return action
        else:
            raise ValidationError(_("Only L&D Manager or Administrator can approve it !!"))

    def ceo_app_req(self):
        admin_group = self.env.ref('base.group_system').users.ids
        ceo_group = self.env.ref('strategy_and_planning.group_ceo').users.ids
        group_list = ceo_group + admin_group
        if self.env.user.id in group_list:
            action = self.env.ref('learning_development.action_approve_wizard').read()[0]
            return action
        else:
            raise ValidationError(_("Only CEO Manager or Administrator can approve it !!"))

    def ceo_rej_req(self):
        admin_group = self.env.ref('base.group_system').users.ids
        ceo_group = self.env.ref('strategy_and_planning.group_ceo').users.ids
        group_list = ceo_group + admin_group
        if self.env.user.id in group_list:
            action = self.env.ref('learning_development.action_approve_wizard').read()[0]
            return action
        else:
            raise ValidationError(_("Only CEO Manager or Administrator can approve it !!"))

    expand_state = fields.Selection([('bursary_req', 'New'), ('line_manager', 'Line Manager'), ('hod', 'Head Of Division'), ('adjudication', 'Adjudication')],
                                    string="State", default='bursary_req')

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).expand_state.selection]

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """ Override read_group to always display all states. """

        if groupby and groupby[0] == "state":
            # Default result structure
            states = [('bursary_req', 'New'), ('line_manager', 'Line Manager'), ('hod', 'Head Of Division'),
                      ('adjudication', 'Adjudication'), ('ld_manager', 'L&D Review'), ('ceo', 'CEO Review'),
                      ('bursary_app', 'Approved'), ('bursary_reject','Rejected')]

            read_group_all_states = [
                {'__context': {'group_by': groupby[1:]}, '__domain': domain + [('state', '=', state_value)],
                 'state': state_value, 'state_count': 0, } for state_value, state_name in states]

            # Get standard results
            read_group_res = super(LearningDevelopment, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                                  orderby=orderby)
            # Update standard results with default results
            result = []
            for state_value, state_name in states:
                res = [x for x in read_group_res if x['state'] == state_value]
                if not res:
                    res = [x for x in read_group_all_states if x['state'] == state_value]
                res[0]['state'] = state_value
                result.append(res[0])
            return result
        else:
            return super(LearningDevelopment, self).read_group \
                (domain, fields, groupby, offset=offset, limit=limit, orderby=orderby)

    @api.constrains('anticipated_year_of_completion', 'commenced_support_year', 'commenced_study_year',
                    'studies_completion_date')
    @api.one
    def _check_number(self):
        if self.type == 'bursary_request':
            number = self.anticipated_year_of_completion
            print ("\n\n\n\n\n ",number.isdigit())
            if number.isdigit() == True:
                print ("mjk")
                if number and len(number) != 4:
                    raise ValidationError(_('Anticipated Year of Completion should be 4 digits.'))
            else:
                raise ValidationError(_('Anticipated Year of Completion must be a number.'))
            s_number = self.commenced_support_year
            if s_number and len(str(abs(s_number))) > 4:
                raise ValidationError(_('Commenced Support Year must not exceed 4 digits.'))
            cs_number = self.commenced_study_year
            if cs_number and len(str(abs(cs_number))) > 4:
                raise ValidationError(_('Commenced Study Year must not exceed 4 digits.'))
            cd_number = self.studies_completion_date
            if cd_number and len(str(abs(cd_number))) > 4:
                raise ValidationError(_('Studies Completion Date must not exceed 4 digits.'))

    def bursary_request(self):
        for record in self:
            action = {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'learning.development',
                'target': 'current',
                'res_id': record.id,
                'flags': {'initial_mode': 'edit'},
                'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
            }
            return action

    def submit_request(self):
        self.state = 'line_manager'