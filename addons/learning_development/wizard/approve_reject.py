# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class ApproveReject(models.TransientModel):
    _name = "approve.reject"
    _description = "Approve Reject Bursary Request"

    lm_support_emp_app = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                       string="I am fully in support of the employee's application")
    lm_not_support_emp_app = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                           string="I do not support the employee’s applications and have communicate the outcome to the employee in writing (copy to HRD)")
    hod_exe_man_cluster = fields.Selection([('yes', 'Yes'), ('no','No')],
                                           string="As the Executive Manager of the Cluster, I have reviewed the application and I AGREE with the recommendation made by the Line Manager")
    hod_not_exe_man_cluster = fields.Selection([('yes','Yes'), ('no','No')],
        string="As the Executive Manager of the Cluster, I have reviewed the application and I DO NOT AGREE with the recommendation made by the Line Manager")
    
    adjudication_confirm_busary_app     = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                             string="Do you confirm that the bursary application is recommended by the bursary adjudication committee?")
    
    adjudication_not_confirm_busary_app = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                             string="Do you confirm that the bursary application is NOT recommended by the bursary adjudication Committee?")

    ld_confirm_busary_app = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                             string="Do you confirm the Bursary Application is in line with the recommendations made by the Bursary Committee?")
    
    ld_not_confirm_busary_app = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                             string="Do you confirm the Bursary Application is NOT in line with the recommendations made by the Bursary Committee?")

    ceo_confirm_bursary = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                           string="Do you confirm the Bursary Application is in line with the Learning and Development Policy?")
    
    ceo_not_confirm_bursary = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                               string="Do you confirm the Bursary Application is NOT in line with the Learning and Development Policy?")
    
    type = fields.Selection([('approve', 'Approve'), ('reject', 'Reject')], string="Type")
    learn_dev_id = fields.Many2one('learning.development', string="Learning Development")
    state = fields.Selection([('line_manager', 'Line Manager'), ('hod', 'Head of Division'), ('adjudication', 'Adjudication'), ('ld_manager', 'L&D Review'), ('ceo', 'CEO')],
        state="State", related="learn_dev_id.state")
    
    line_comments = fields.Text(string="Line Manager Comments")
    hod_comments = fields.Text(string="HOD Comments")
    adjudication_comments = fields.Text(string="Adjudication Comments")
    ld_comments = fields.Text(string="Learning and Development Comments")
    ceo_comments = fields.Text(string="CEO Comments")    

    def submit_request(self):
        if self.type == 'approve' and self.state == 'line_manager':
            if self.lm_support_emp_app == 'yes':
                self.learn_dev_id.state = 'hod'
                self.learn_dev_id.line_comments = self.line_comments
        elif self.type == 'reject' and self.state == 'line_manager':
            if self.lm_not_support_emp_app == 'yes':
                self.learn_dev_id.state = 'bursary_reject'
                self.learn_dev_id.line_comments = self.line_comments
        
        elif self.type == 'approve' and self.state == 'hod':
            if self.hod_exe_man_cluster == 'yes':
                self.learn_dev_id.state = 'adjudication'
                self.learn_dev_id.line_comments = self.hod_comments
        elif self.type == 'reject' and self.state == 'hod':
            if self.hod_not_exe_man_cluster == 'yes':
                self.learn_dev_id.state = 'bursary_reject'
                self.learn_dev_id.line_comments = self.hod_comments

        elif self.type == 'approve' and self.state == 'adjudication':
            if self.adjudication_confirm_busary_app == 'yes':
                self.learn_dev_id.state = 'ld_manager'
                self.learn_dev_id.adjudication_comments = self.adjudication_comments
        elif self.type == 'reject' and self.state == 'adjudication':
            if self.ld_not_confirm_busary_app == 'yes':
                self.learn_dev_id.state = 'bursary_reject'
                self.learn_dev_id.adjudication_comments = self.adjudication_comments
        
        elif self.type == 'approve' and self.state == 'ld_manager':
            if self.ld_confirm_busary_app == 'yes':
                self.learn_dev_id.state = 'ceo'
                self.learn_dev_id.line_comments = self.ld_comments
        elif self.type == 'reject' and self.state == 'ld_manager':
            if self.ld_not_confirm_busary_app == 'yes':
                self.learn_dev_id.state = 'bursary_reject'
                self.learn_dev_id.line_comments = self.ld_comments
        
        elif self.type == 'approve' and self.state == 'ceo':
            if self.ceo_confirm_bursary == 'yes':
                self.learn_dev_id.state = 'bursary_app'
                self.learn_dev_id.line_comments = self.ceo_comments
        elif self.type == 'reject' and self.state == 'ceo':
            if self.ceo_not_confirm_bursary == 'yes':
                self.learn_dev_id.state = 'bursary_reject'
                self.learn_dev_id.line_comments = self.ceo_comments
