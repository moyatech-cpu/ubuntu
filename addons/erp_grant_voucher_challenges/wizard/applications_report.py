# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError

class Applications(models.TransientModel):
    _name = 'report.applications.grant'
    _description = 'Grant Detail Application Reports'

    start_date = fields.Date(string='Start Date',required=True)
    end_date = fields.Date(string='End Date',required=True)
    status = fields.Selection(
        [('new', 'New'), ('ict_checked', 'ITC Checked'), ('inspected', 'Inspected'),
         ('deligence_done', 'Deligence Done')
            , ('investment_memo_upload', 'Investment  Upload'), ('bgarg_review', 'BGARC Review'),
         ('send_letter', 'Send Rejection Letter'), ('hogac_review', 'HOGAC Review'),
         ('approved', 'Approved'), ('sent_approval_letter', 'Send Approval Letter'),
         ('uploaded_approval_letter', 'Contracting'),
         ('bdo_review', 'BDO Review'), ('branch_manager_review', 'Branch Manager Review'),
         ('disbursement', 'Disbursement Pack'),
         ('bcs_approved', 'BCS Approved'), ('qao_approved', 'QAO Approved'), ('edm_approved', 'EDM Approved'),
         ('approval_revoked', 'Approval Revoked'), ('aftercare', 'Aftercare'), ('completed', 'Completed'),
         ('reject', 'Reject')],
        default='new',
        string="status")
    all_branches = fields.Boolean('All branches', default=False)
    branch = fields.Many2one('res.branch','Branch')

    @api.multi
    def get_detail_applications(self):
        if self.status:
            if self.start_date and self.end_date and self.all_branches:
                mentees = self.env['grant.application'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date),('status','=',self.status)])
            elif self.start_date and self.end_date and not self.all_branches:
                mentees = self.env['grant.application'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date),('branch_id','=',self.branch.id),('status','=',self.status)])
        else:
            if self.start_date and self.end_date and self.all_branches:
                mentees = self.env['grant.application'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date)])
            elif self.start_date and self.end_date and not self.all_branches:
                mentees = self.env['grant.application'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date),('branch_id','=',self.branch.id)])

        return mentees
    
    def get_detail_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('erp_grant_voucher_challenges.action_print_grant_app_report').report_action(self)