# coding=utf-8

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class TechnicalTrainingApprenticeship(models.Model):
    """ Technical Training Apprenticeship model """
    _name = 'technical.training.apprenticeship'
    _description = "Technical Training Apprenticeship model"

    name = fields.Char("Batch")
    branch_id = fields.Many2one('res.branch', string="Branch")
    programme_type = fields.Selection([('apprenticeship_programme', 'Apprenticeship Programme')],
                                      string="Programme Type")
    state = fields.Selection([('draft', 'New'),
                              ('start_training', 'Technical Skills Intake'), ('placed_at_company', 'Work Placement'),
                              ('mentorship_log_book', 'Mentorship logbook'),
                              ('service_provider_submit', 'Service Provider Submit'),
                              ('service_provider_submitted_report', 'Service Provider Submitted Report'),
                              ('nyda_specialist_reviews', 'NYDA Specialist Reviews'),
                              ('upload_site_visit', 'Upload Site Visit Report'),
                              ('submitted_report', 'Submitted Report'),
                              ('approve_site_visit', 'Approve Site Visit Report'),
                              ('rej_site_visit', 'Reject Site Visit Report'),
                              ('pass', 'Trade Test Pass'), ('fail', 'Trade Test Fail'),
                              ('me_evaluation','M&E Evaluation'), ('complete_me_evaluation','Complete M&E Evaluation')],
                             string="State", default='draft')
    trainer_id = fields.Many2one('res.users', string="Service Provider", domain=lambda self: [
        ("groups_id", "=", self.env.ref("bmt_training.group_trainer").id)])
    company_id = fields.Char(string="Company")
    mentorship_report_log_book = fields.Binary(string="Mentorship report/Log book")
    log_book_file_name = fields.Char(string="Mentorship report/Log book File name")
    site_visit_report = fields.Binary(string="Site Visit Report")
    site_visit_file_name = fields.Char(string="Site Visit File name")
    site_visit_file_ids = fields.Many2many('ir.attachment', string="Site Visit Reports")
    project_closeout_report = fields.Binary(string="Project Closeout Report")
    project_closeout_file_name = fields.Char(string="Project Closeout File name")
    trade_test = fields.Binary(string="Trade Test Regi", help="Trade Test Registration")
    trade_test_name = fields.Char(string="Trade File Name")
    certi_file = fields.Binary(string="Certification")
    certi_file_name = fields.Char(string="Certification File name")
    enrolled_users_apprenticeship_ids = fields.One2many('enrolled.users', 'technical_training_apprenticeship_id',
                                                        string="Enrolled Users")
    course_duration = fields.Selection([('three_years', '3 years(4 months training and 8 months at workplace')],
                                       string="Course Duration", default="three_years")
    current_year = fields.Selection(
        [('first_year', 'First year'), ('second_year', 'Second Year'), ('third_year', 'Third Year')],
        string="Current Year", default='first_year')
    head_office_user_id = fields.Many2one('res.users', string="Head Office User")
    site_visit_user_id = fields.Many2one('res.users', string="Site Visit User")
    pcr_user_id = fields.Many2one('res.users', string="PCR User")
    evaluation_user_id = fields.Many2one('res.users', string="Evaluation User")
    nyda_user_id = fields.Many2one('res.users', string="NYDA Specialist User")
    manager_id = fields.Many2one('res.users', string="Manager")
    reject_reason = fields.Text(string="Rejection Reason")
    fy_id = fields.Many2one('technical.training.apprenticeship', string="First Year")
    sy_id = fields.Many2one('technical.training.apprenticeship', string="Second Year")
    ty_id = fields.Many2one('technical.training.apprenticeship', string="Third Year")
    start_date = fields.Date(string="Start Date", help="Training Start Date")


    def approve_sv_report(self):
        self.state = 'approve_site_visit'
        self.manager_id = self.env.user.id

    def rej_sv_report(self):
        self.state = 'rej_site_visit'
        self.manager_id = self.env.user.id

    @api.model
    def create(self, vals):
        res = super(TechnicalTrainingApprenticeship, self).create(vals)
        ref_number = self.env['ir.sequence'].next_by_code('att') or _('New')
        res.name = ref_number
        return res

    def start_training(self):
        if not len(self.enrolled_users_apprenticeship_ids) == 0:
            self.write({
                'start_date': datetime.now().date(),
                'state': 'start_training'
            })
        else:
            raise UserError(_("Please add the Users !!"))

    def assign_company(self):
        self.state = 'placed_at_company'

    def submit_to_ho(self):
        uploaded_log = 0
        total_ben = len(self.enrolled_users_apprenticeship_ids)
        for benificiary in self.enrolled_users_apprenticeship_ids:
            if benificiary.mentorship_report_log_book:
                uploaded_log += 1
        if uploaded_log == total_ben:
            self.state = 'mentorship_log_book'
        else:
            raise UserError(_("Please attach the Mentorship Log Book report for all the benificiary !!"))

    def approve_ho(self):
        uploaded_log = 0
        total_ben = len(self.enrolled_users_apprenticeship_ids)
        for benificiary in self.enrolled_users_apprenticeship_ids:
            if benificiary.mentorship_report_log_book:
                uploaded_log += 1
        if uploaded_log == total_ben:
            self.write({
                'state': 'service_provider_submit',
                'head_office_user_id': self.env.user.id or False
            })
        else:
            raise UserError(_("Please attach the Mentorship Log Book report for all the benificiary !!"))

    def service_provider_submit_report(self):
        self.state = 'service_provider_submitted_report'

    def nyda_specialist_review(self):
        self.state = 'nyda_specialist_reviews'

    def nyda_specialist_approve(self):
        self.state = 'upload_site_visit'
        self.nyda_user_id = self.env.user.id or False

    def submit_sv_report(self):
        if len(self.site_visit_file_ids) != 0:
            self.write({
                'state': 'submitted_report',
                'site_visit_user_id': self.env.user.id or False
            })
            if self.current_year != 'third_year':
                vals = {'name': self.name or '',
                        'branch_id': self.branch_id.id or False,
                        'programme_type': self.programme_type,
                        'trainer_id': self.trainer_id.id or False,
                        'company_id': self.company_id or False,
                        'state': 'placed_at_company',}
                if self.current_year == 'first_year':
                    vals.update({'current_year': 'second_year'})
                elif self.current_year == 'second_year':
                    vals.update({'current_year': 'third_year'})
                new_year = self.sudo().create(vals)
                for usr in self.enrolled_users_apprenticeship_ids:
                    self.env['enrolled.users'].create({
                        'technical_training_apprenticeship_id': new_year.id or False,
                        'certificate_name': usr.certificate_name or '',
                        'technical_training_id': usr.technical_training_id.id or False,
                        'geographic_location': usr.geographic_location or '',
                        'gender': usr.gender,
                        'population_group': usr.population_group or '',
                        'e_mail': usr.e_mail or '',
                        'contact_number': usr.contact_number or '',
                        'benificiary_id': usr.benificiary_id.id or False,
                        'surname': usr.surname,
                        'year': new_year.current_year
                    })
        else:
            raise UserError(_("Please attach the Site Visit report !!"))

    def button_trade_test_pass(self):
        self.write({
            'state': 'pass',
        })

    def button_trade_test_fail(self):
        self.write({
            'state': 'fail',
        })

    def me_evaluate(self):
        self.state = 'me_evaluation'

    def complete_me_eval(self):
        self.state = 'complete_me_evaluation'
        self.evaluation_user_id = self.env.user.id or False


class TechnicalTraining(models.Model):
    """ Technical Training model """
    _name = 'technical.training'
    _description = "Technical Training"

    name = fields.Char("Project Name")
    branch_id = fields.Many2one('res.branch', string="Branch")
    programme_type = fields.Selection(
        [('short_skills', 'Short Skills Programme'), ('leanership', 'Leanership Programme')],
        string="Programme Type")
    site_visit_file_ids = fields.Many2many('ir.attachment', string="Site Visit")
    state = fields.Selection([('start_training', 'Benificiary Recruitment'), ('placed_at_company', 'Placed At Company'),
                              ('submit_head_office', 'Submitted Report to Head Office'),
                              ('ho_approve', 'Head Office Approve'), ('ho_reject', 'Head Office Reject'),
                              ('conducting_site_visit', 'Conducting Site Visit'),
                              ('submit_sv_to_manager', 'Submitted Site Visit Report to Manager'),
                              ('site_visit_approve', 'Site Visit Approved'), ('site_visit_reject', 'Site Visit Reject'),
                              ('pc_submit', 'Project Closeout Report Submitted'),
                              ('nyda_review', 'NYDA Specialist Review'), ('nyda_approve', 'NYDA Specialist Approve'),
                              ('nyda_reject', 'NYDA Specialist Reject'),
                              ('pc_manager_review', 'Project Closeout Manager Review'),
                              ('pc_approve', 'Project Closeout Approve'), ('pc_reject', 'Project Closeout Reject'),
                              ('certificate_uploaded', 'Certificate Uploaded'),
                              ('me_evaluation','M&E Evaluation'), ('complete_me_evaluation','Complete M&E Evaluation')],
                             string="State")
    trainer_id = fields.Many2one('res.users', string="Service Provider", domain=lambda self: [
        ("groups_id", "in", [self.env.ref("bmt_training.group_trainer").id,
                             self.env.ref("client_management.group_partner_service_provider").id])],
                                 default=lambda self: self.get_trainer())
    company_id = fields.Char(string="Company")
    mentorship_report_log_book = fields.Binary(string="Mentorship report/Log book")
    log_book_file_name = fields.Char(string="Mentorship report/Log book File name")
    site_visit_report = fields.Binary(string="Site Visit Report")
    site_visit_file_name = fields.Char(string="Site Visit File name")
    project_closeout_report = fields.Binary(string="Project Closeout Report")
    project_closeout_file_name = fields.Char(string="Project Closeout File name")
    enrolled_users_ids = fields.One2many('enrolled.users', 'technical_training_id', string="Enrolled Users")
    course_duration = fields.Selection([('twelve_months', '12 months(6 months at workplace)'), ('six_months', '6 months(3 months at workplace)')],
                                       string="Course Duration", compute="compute_course_duration")
    site_visit_reject = fields.Text(string="Site Visit Reject")
    ho_rejected = fields.Text(string="Head Office Reject")
    prc_reject = fields.Text(string="Project Closeout Reject")
    nyda_reject = fields.Text(string="NYDA Specialist Reject")
    nyda_specialist_id = fields.Many2one('res.users', string="NYDA Specialist",
                                         domain=lambda self: [("groups_id", "=",self.env.ref("bmt_training.group_nyda_specialist").id)])
    ho_admin_id = fields.Many2one('res.users', string="Head Office Manager",
                                         domain=lambda self: [("groups_id", "=",self.env.ref("bmt_training.group_ho_manager").id)])

    @api.model
    def get_trainer(self):
        service_provider = self.env.ref("client_management.group_partner_service_provider").users.ids
        trainer = self.env.ref("bmt_training.group_trainer").users.ids
        groups = []
        for spid in service_provider:
            groups.append(spid)
        for tid in trainer:
            groups.append(tid)
        if self.env.user.id in groups:
            return self.env.user.id
        else:
            return False

    @api.onchange('trainer_id')
    def get_branch(self):
        if self.trainer_id:
            self.branch_id = self.trainer_id.branch_id.id
            trainer = self.env['link.service.provider'].search([('service_provider_id', '=', self.trainer_id.id)])
            if len(trainer) == 1:
                self.nyda_specialist_id = trainer.nyda_specialist_id.id
            else:
                self.nyda_specialist_id = False

    @api.model
    def create(self, vals):
        res = super(TechnicalTraining, self).create(vals)
        if res.programme_type == 'short_skills':
            ref_number = self.env['ir.sequence'].next_by_code('sstt') or _('New')
            res.name = ref_number
        elif res.programme_type == 'leanership':
            ref_number = self.env['ir.sequence'].next_by_code('ltt') or _('New')
            res.name = ref_number
        return res

    @api.depends('programme_type')
    def compute_course_duration(self):
        if self.programme_type == 'short_skills':
            self.course_duration = 'six_months'
        elif self.programme_type == 'leanership':
            self.course_duration = 'twelve_months'

    def nyda_review(self):
        self.state = 'nyda_review'

    def nyda_reject_reason(self):
        self.state = 'site_visit_approve'

    def nyda_approve(self):
        self.state = 'nyda_approve'

    def start_training(self):
        if not len(self.enrolled_users_ids) == 0:
            self.state = 'start_training'
        else:
            raise UserError(_("Please add the Users !!"))

    def assign_company(self):
        for benificiary in self.enrolled_users_ids:
            benificiary.work_placement_id = self.company_id
        self.state = 'placed_at_company'

    def submit_to_ho(self):
        uploaded_log = 0
        total_ben = len(self.enrolled_users_ids)
        for benificiary in self.enrolled_users_ids:
            if benificiary.mentorship_report_log_book:
                uploaded_log += 1
        if uploaded_log == total_ben:
            self.state = 'submit_head_office'
        else:
            raise UserError(_("Please attach the Mentorship Log Book report for all the benificiary !!"))

    def approve_ho(self):
        uploaded_log = 0
        total_ben = len(self.enrolled_users_ids)
        for benificiary in self.enrolled_users_ids:
            if benificiary.mentorship_report_log_book:
                uploaded_log += 1
        if uploaded_log == total_ben:
            self.state = 'ho_approve'
        else:
            raise UserError(_("Please attach the Mentorship Log Book report for all the benificiary !!"))

    def reject_ho(self):
        uploaded_log = 0
        total_ben = len(self.enrolled_users_ids)
        for benificiary in self.enrolled_users_ids:
            if benificiary.mentorship_report_log_book:
                uploaded_log += 1
        if uploaded_log == total_ben:
            self.state = 'ho_reject'
        else:
            raise UserError(_("Please attach the Mentorship Log Book report for all the benificiary !!"))

    def conduct_site_visit(self):
        self.state = 'conducting_site_visit'

    def submit_sv_report(self):
        if self.site_visit_report:
            self.state = 'submit_sv_to_manager'
        else:
            raise UserError(_("Please attach the Site Visit report !!"))

    def site_visit_app(self):
        if len(self.site_visit_file_ids) != 0:
            self.state = 'site_visit_approve'
        else:
            raise UserError(_("Please attach the Site Visit report !!"))

    def site_visit_rej(self):
        if self.site_visit_report:
            self.state = 'site_visit_reject'
        else:
            raise UserError(_("Please attach the Site Visit report !!"))

    def submit_pc_report(self):
        if self.project_closeout_report:
            self.state = 'pc_submit'
        else:
            raise UserError(_("Please attach the Project Closeout report !!"))

    def pc_approve(self):
        if self.project_closeout_report:
            self.state = 'pc_approve'
        else:
            raise UserError(_("Please attach the Project Closeout report !!"))

    def pc_reject(self):
        if self.project_closeout_report:
            self.state = 'pc_reject'
        else:
            raise UserError(_("Please attach the Project Closeout report !!"))

    def upload_certi(self):
        uploaded_certi = 0
        total_ben = len(self.enrolled_users_ids)
        for benificiary in self.enrolled_users_ids:
            if benificiary.certificate:
                uploaded_certi += 1
        if uploaded_certi == total_ben:
            self.state = 'certificate_uploaded'
        else:
            raise UserError(_("Please upload all the certificates !!"))

    # def me_evaluate(self):084 299 5925
    #     self.state = 'me_evaluation'

    # def complete_me_eval(self):
    #     self.state = 'complete_me_evaluation'
