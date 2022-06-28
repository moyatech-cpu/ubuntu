# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError

class VoucherSuppliers(models.TransientModel):
    _name = 'wiz.voucher.supplier'
    _description = 'Voucher Supplier Report'
    
    contract_state = fields.Selection([('ACTIVE','ACTIVE'),('EXPIRED','EXPIRED')],default='EXPIRED')
    vouchers_state = fields.Selection([('PENDING','PENDING'),('PAID','PAID'),('ALL','ALL')],default='PENDING')
    #end_date = fields.Date(string='End Date',required=True)
    province_id = fields.Many2one('res.country.state','Province')

    @api.multi
    def get_supplier_data(self):
        if self.province_id:
            if self.contract_state:
                if self.contract_state == 'ACTIVE':
                    mentees = self.env['res.partner'].sudo().search([('x_voucher_vendor','=',True),('contract_status','=',True),('state_id','=',self.province_id.id)])
                else:
                    mentees = self.env['res.partner'].sudo().search([('x_voucher_vendor','=',True),('contract_status','=',False),('state_id','=',self.province_id.id)])
            elif not self.contract_state:
                mentees = self.env['res.partner'].sudo().search([('x_voucher_vendor','=',True)])
        else:
            if self.contract_state:
                if self.contract_state == 'ACTIVE':
                    mentees = self.env['res.partner'].sudo().search([('x_voucher_vendor','=',True),('contract_status','=',True)])
                else:
                    mentees = self.env['res.partner'].sudo().search([('x_voucher_vendor','=',True),('contract_status','=',False)])
            elif not self.contract_state:
                mentees = self.env['res.partner'].sudo().search([('x_voucher_vendor','=',True)])
        
        for mentee in mentees:
            if self.vouchers_state == 'PENDING':
                vouchers = self.env['voucher.application'].sudo().search([('x_service_provider','=',mentee.id),('status','not in',('pending_payment','payment_completed'))])
            elif self.vouchers_state == 'PAID':
                vouchers = self.env['voucher.application'].sudo().search([('x_service_provider','=',mentee.id),('status','in',('pending_payment','payment_completed'))])
            else:
                vouchers = self.env['voucher.application'].sudo().search([('x_service_provider','=',mentee.id)])
        
        final_list = {'service_providers':mentees,
                      'vouchers':vouchers}
        return final_list
    
    def get_supplier_report(self):
        return self.env.ref('system_update_14.action_print_voucher_suppliers_report').report_action(self)
            
    '''contract_state = fields.Selection([('ACTIVE','ACTIVE'),('EXPIRED','EXPIRED')],default='EXPIRED')
    start_date = fields.Date(string='Start Date',required=True)
    end_date = fields.Date(string='End Date',required=True)
    province_id = fields.Many2one('res.country.state','Province')

    @api.multi
    def get_supplier_data(self):
        if self.province_id:
            if self.start_date and self.end_date and self.contract_state:
                if self.contract_state == 'ACTIVE':
                    mentees = self.env['res.partner'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date),('x_voucher_vendor','=',True),('contract_status','=',True),('state_id','=',self.province_id.id)])
                else:
                    mentees = self.env['res.partner'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date),('x_voucher_vendor','=',True),('contract_status','=',False),('state_id','=',self.province_id.id)])
            elif self.start_date and self.end_date and not self.contract_state:
                mentees = self.env['res.partner'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date),('x_voucher_vendor','=',True)])
        else:
            if self.start_date and self.end_date and self.contract_state:
                if self.contract_state == 'ACTIVE':
                    mentees = self.env['res.partner'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date),('x_voucher_vendor','=',True),('contract_status','=',True)])
                else:
                    mentees = self.env['res.partner'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date),('x_voucher_vendor','=',True),('contract_status','=',False)])
            elif self.start_date and self.end_date and not self.contract_state:
                mentees = self.env['res.partner'].sudo().search([('create_date','>=',self.start_date),('create_date','<=',self.end_date),('x_voucher_vendor','=',True)])
        
        for mentee in mentees:
            vouchers = self.env['voucher.application'].sudo().search([('x_service_provider','=',mentee.id)])
        final_list = {'service_providers':mentees,
                      'vouchers':vouchers}
        return final_list
    
    def get_supplier_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('system_update_14.action_print_voucher_suppliers_report').report_action(self)'''