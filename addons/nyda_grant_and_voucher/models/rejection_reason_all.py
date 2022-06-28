# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class RejectionReasonAll(models.Model):
    _name = 'rejection.reason.all'
    _rec_name = 'voucher_id'

    voucher_id = fields.Many2one('voucher.application', 'Voucher ID')
    rejection_reason = fields.Text(string='Please Write Below Your Rejection Reason')
    # current_user_id = fields.Many2one('', string='User By')
    # groups_id = fields.Many2many('res.groups', string='Groups', related='current_user_id.groups_id')
    status = fields.Selection(
        [('new', 'New'), ('assessment_report', 'Assessment Report'), ('appointment_drafted', 'Appointment Drafted'), ('recommended', 'Recommended'), (
            'approved', 'Approved'), ('voucher_isurance', 'Voucher Isurance'),
         ('work_plan_submitted', 'Work Plan Submitted'),
         ('submitted_product', 'Submitted Product'), ('client_review', 'Client Review'), ('nyda_review', 'NYDA Review'),
         ('nyda_head_office', 'NYDA Head Office Review'),
         ('send_payment_reciept', 'Send Payment Reciept'), ('post_disbursement_done', 'Post Disbursement Done'),
         ('link_mkl_database', 'Link MKL Database'), ('decline', 'Declined')],
         string="status")





