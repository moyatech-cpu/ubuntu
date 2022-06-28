# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CancelBMTTrainingUpdate(models.Model):
    
    _inherit="bmt.training.application"
    
    reinstate_bmt_reason = fields.Text(string='Reason To Reinstate')
    cancel_bmt_reason = fields.Text(string='Reason To Cancel')
    status = fields.Selection([('new','New'),('allocated','Allocated'),('cancelled','Cancelled')],string="state", default="new")
    current_state = fields.Char('Current State')
       
    @api.multi
    def btn_cancel_application(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel BMT Application',
            'res_model': 'cancel.bmt.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.cancel_reason_bmt_form').id),
            'target': 'new',
        }
    
    @api.multi
    def btn_reinstate_application(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reinstate BMT Application',
            'res_model': 'cancel.bmt.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.reinstate_bmt_form').id),
            'target': 'new',
        }
        
        
class CancelBusinessMGMTTrainingUpdate(models.Model):

    _inherit="business.mgmt.training"
    
    reinstate_b_mgmt_reason = fields.Text(string='Reason To Reinstate')
    cancel_b_mgmt_reason = fields.Text(string='Reason To Cancel')
    status = fields.Selection([('new','New'),('cancelled','Cancelled')],string="state", default="new")
    current_state = fields.Char('Current State')

    @api.multi
    def btn_cancel_b_mgmt_training(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Training',
            'res_model': 'cancel.business.mgmt.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.cancel_reason_business_mgmt_form').id),
            'target': 'new',
        }
    
    @api.multi
    def btn_reinstate_b_mgmt_training(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reinstate Training',
            'res_model': 'cancel.business.mgmt.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.reinstate_reason_business_mgmt_form').id),
            'target': 'new',
        }
        
class CancelPitchingTrainingUpdate(models.Model):

    _inherit="business.mgmt.training.pitching"
    
    reinstate_pitching_reason = fields.Text(string='Reason To Reinstate')
    cancel_pitching_reason = fields.Text(string='Reason To Cancel')
    status = fields.Selection([('new','New'),('cancelled','Cancelled')],string="state", default="new")
    current_state = fields.Char('Current State')

       
    @api.multi
    def btn_cancel_pitch_training(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Training',
            'res_model': 'cancel.pitching.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.cancel_reason_pitch_training_form').id),
            'target': 'new',
        }
    
    @api.multi
    def btn_reinstate_pitch_training(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reinstate Training',
            'res_model': 'cancel.pitching.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.reinstate_reason_pitch_training_form').id),
            'target': 'new',
        }
        
class CancelSalesPitchTrainingUpdate(models.Model):

    _inherit="sales.pitch.training"
    
    reinstate_sales_pitch_reason = fields.Text(string='Reason To Reinstate')
    cancel_sales_pitch_reason = fields.Text(string='Reason To Cancel')
    state = fields.Selection([('new', 'New'), ('start_training', 'Start Training'), ('end_training', 'End Training'),
                              ('coordinator_review', 'Coordinator Review'), ('bm_review', 'Branch Manager Review'),
                              ('ho_admin_review', 'HO Admin Review'), ('ho_manager_review', 'HO Manager Review'),
                              ('completed', 'Completed'),('cancelled','Cancelled'),('me_approved', 'M&E Approved'),('me_rejected', 'M&E Rejected')], string="State", default='new')
    current_state = fields.Char('Current State', default='new')

    def me_approve(self):
        self.state = 'me_approved'

    @api.multi
    def btn_cancel_sales_pitch(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Training',
            'res_model': 'cancel.sales.pitch.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.cancel_sales_pitch_training_form').id),
            'target': 'new',
        }
    
    @api.multi
    def btn_reinstate_sales_pitch(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reinstate Training',
            'res_model': 'cancel.sales.pitch.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.reinstate_reason_sales_pitch_training_form').id),
            'target': 'new',
        }
    
class CancelCoopGovTrainingUpdate(models.Model):

    _inherit="cooperative.governance.training"
    
    reinstate_gov_training_reason = fields.Text(string='Reason To Reinstate')
    cancel_gov_training_reason = fields.Text(string='Reason To Cancel')
    state = fields.Selection([('new', 'New'), ('start_training', 'Start Training'), ('end_training', 'End Training'),
                              ('coordinator_review', 'Coordinator Review'), ('bm_review', 'Branch Manager Review'),
                              ('ho_admin_review', 'HO Admin Review'), ('ho_manager_review', 'HO Manager Review'),
                              ('completed', 'Completed'),('cancelled','Cancelled'),('me_approved', 'M&E Approved'),('me_rejected', 'M&E Rejected')], string="State", default='new')
    current_state = fields.Char('Current State', default='new')

    def me_approve(self):
        self.state = 'me_approved'

    @api.multi
    def btn_cancel_coop_traning(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Training',
            'res_model': 'cancel.coop.governance.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.cancel_reason_coop_gov_form').id),
            'target': 'new',
        }
    
    @api.multi
    def btn_reinstate_coop_training(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reinstate Training',
            'res_model': 'cancel.coop.governance.training.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_007.reinstate_reason_coop_gov_form').id),
            'target': 'new',
        }