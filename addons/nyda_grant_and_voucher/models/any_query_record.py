# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AnyQueryRecord(models.Model):
    _name = 'any.query.record'
    _rec_name = 'query'

    query = fields.Text(string='Please Write Below If You Have Any Query')
    voucher_id = fields.Many2one('voucher.application', 'Voucher ID')
    status = fields.Selection(
        [('new', 'New'), ('assessment_report', 'Assessment Report'), ('appointment_drafted', 'Appointment Drafted'), ('recommended', 'Recommended'), (
            'approved', 'Approved'), ('voucher_isurance', 'Voucher Isurance'),
         ('work_plan_submitted', 'Work Plan Submitted'),
         ('submitted_product', 'Submitted Product'), ('client_review', 'Client Review'), ('nyda_review', 'NYDA Review'),
         ('nyda_head_office', 'NYDA Head Office Review'),
         ('send_payment_reciept', 'Send Payment Reciept'), ('post_disbursement_done', 'Post Disbursement Done'),
         ('link_mkl_database', 'Link MKL Database'), ('decline', 'Declined')],
         string="status")
