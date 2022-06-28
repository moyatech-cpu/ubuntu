# coding=utf-8
from odoo import api, fields, models
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from odoo import http


class VoucherApplication(models.Model):
    """ Model to register all the appications for grant. """
    _inherit = 'voucher.application'

    x_total_approved_vouchers = fields.Integer("No of Vouchers received",compute='_calculate_total_vouchers',readonly=True,store=False)
    x_flag = fields.Text("Flag",readonly=True,store=False,compute="_check_flag")
    
    @api.depends('user_id')
    def _calculate_total_vouchers(self):
        for record in self:
            voucher_exists_ids = self.env['voucher.application'].sudo().search([('user_id', '=', record['user_id'].id),('status','in',('approved','send_payment_reciept','pending_payment','payment_completed','payment_released','recommended','voucher_isurance'))])
            tt_services = 0
            for voucher in voucher_exists_ids:
                tt_services += len(voucher.x_recommended_service)
                record['x_total_approved_vouchers'] = tt_services
    
    @api.depends('user_id')
    def _check_flag(self):
        for record in self:
            record['x_flag'] = ""
            if record['status'] == 'new':
                legacy_records = self.env['voucher.application'].sudo().search([('name', '=', record['name']),('surname', '=', record['surname']),('status','=','Legacy')])#,('x_dob','=',record['x_dob'])])
                if legacy_records:
                    record['x_flag'] = "Applicant has "+str(len(legacy_records))+" existing application(s) in legacy, kindly check services received manually."
            
    
    @api.multi
    def calculated_vouchers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Voucher Application',
            'res_model': 'voucher.application',
            'view_type': 'form',
            'view_mode': 'tree',
            'view_id': self.env.ref('nyda_grant_and_voucher.view_voucher_application_tree').id,
            'domain': [('user_id', '=', self.user_id.id),('status','in',('approved','send_payment_reciept','pending_payment','payment_completed','payment_released','recommended','voucher_isurance'))],
            'target': 'current',
        }
        


