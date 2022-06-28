# -*- coding: utf-8 -*-

from odoo import models, fields, api

class GrantUpdate(models.Model):
    _inherit="grant.application"
    
    reinstate_grant_reason = fields.Text(string='Reason To Reinstate')
    cancel_grant_reason = fields.Text(string='Reason To Cancel')
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
         ('reject', 'Reject'),('cancelled', 'Cancelled')],
        default='new',
        string="status")
    current_state = fields.Char('Current State', default='new')


       
    @api.multi
    def btn_cancel_grant(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Grant Application',
            'res_model': 'grant.cancel.reason.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_005.cancel_reason_grant_form').id),
            'target': 'new',
        }
    
    @api.multi
    def btn_reinstate_grant(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reinstate Grant Application',
            'res_model': 'grant.cancel.reason.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_005.reinstate_grant_form').id),
            'target': 'new',
        }

class PreAssessmentUpdate(models.Model):
    
    _inherit = "client.preassessment"
    
    number_of_grants = fields.Integer("No of Grant Applications",compute='_calculate_total_grants',readonly=True,store=False)
    reinstate_assessment_reason = fields.Text(string='Reason To Reinstate')
    cancel_assessment_reason = fields.Text(string='Reason To Cancel')
    rejection_reason = fields.Text(string='Reason To Email Applicant')
    cancel_state = fields.Selection([('new', 'New'),('cancelled', 'Cancelled')])
    current_state = fields.Char('Current State', default='new')

    @api.multi
    def btn_cancel_assessment(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Application',
            'res_model': 'client.preassessment.cancel.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_005.cancel_reason_preassessment_form').id),
            'target': 'new',
        }
        
        
    @api.multi
    def btn_reinstate_assessment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reinstate Application',
            'res_model': 'client.preassessment.cancel.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_005.reinstate_preassessment_form').id),
            'target': 'new',
        }
        
    @api.multi
    def btn_set_rejected(self):
       return {
            'type': 'ir.actions.act_window',
            'name': 'Application Rejection Reason',
            'res_model': 'client.preassessment.cancel.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_005.preassessment_reject_form').id),
            'target': 'new',
            'context': {'default_assessment_id': self.id}
        }
    
    @api.depends('user_id')
    def _calculate_total_grants(self):
        for record in self:
            grant_exists_ids = self.env['grant.application'].sudo().search([('user_id', '=', record['user_id'].id)])
            record['number_of_grants'] = len(grant_exists_ids)
    
    
