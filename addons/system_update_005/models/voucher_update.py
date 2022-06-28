from odoo import api, fields, models

class CancelVoucherWiz(models.Model):
    _inherit="voucher.application"
    
    status = fields.Selection(
        [('new', 'New'), ('appointment_drafted', 'Appointment Drafted'), ('assessment_report', 'Assessment Reported'),
         ('recommended', 'Recommended'), ('approved', 'Approved'), ('voucher_isurance', 'Voucher Issuance'), ('work_plan', 'Work Plan'),
         ('work_plan_submitted', 'Work Plan Submitted'), ('submitted_product', 'Submitted Product'),
         ('client_review', 'Client Review'), ('nyda_review', 'NYDA Review'),
         ('bda_review', 'BDA Review'), ('bdo_review', 'BDO Review'),('pc_review', 'PC Review'),
         ('branch_manager_review', 'Branch Manager Review'), ('ho_admin_review', 'HO Admin Review'),
         ('qa_officer_review', 'QA Officer Review'),('ed_manager_review', 'ED Manager Review'),
         ('nyda_head_office', 'NYDA Head Office Review'), ('send_payment_reciept', 'Send Payment Reciept'),
         ('post_disbursement_done', 'Post Disbursement Done'),
         ('pending_payment', 'Pending Payment'), ('payment_completed', 'Payment Posted'), ('payment_released', 'Payment Released'),
         ('link_mkl_database', 'Link MKL Database'), ('decline', 'Declined'), ('cancelled', 'Cancelled'),('Legacy', 'Legacy')],
        default='new', string="status")
    cancel_voucher_reason = fields.Text(string='Reason To Cancel')
    reinstate_voucher_reason = fields.Text(string='Reason To Reinstate')
    current_state = fields.Char('Current State', default='new')
 
    
    @api.multi
    def btn_cancel_voucher(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Voucher Application',
            'res_model': 'voucher.cancel.reason.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_005.cancel_reason_voucher_form').id),
            'target': 'new',
        }
    
    @api.multi
    def btn_reinstate_voucher(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reinstate Voucher Application',
            'res_model': 'voucher.cancel.reason.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('system_update_005.reinstate_voucher_form').id),
            'target': 'new',
        }