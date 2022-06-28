# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime,date
from odoo.exceptions import UserError
from _ast import If

class SystemUpdate008(models.TransientModel):
    
    _inherit = 'voucher.status.report.bdo'
    
    region_id           = fields.Many2one('res.region', string='Region')
    regional_report     = fields.Boolean(string="Print Regional Report", default=False) 
    
    
    @api.onchange('regional_report')
    def onchange_branch(self):
        if self.regional_report:
            self.all_branch = False
            self.branch_id = False
    
    def get_voucher_data(self):
        voucher_list = []
        final_list = []
        branch = ''
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['res.users'].sudo().search([('branch_id', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['res.users'].sudo().search([('branch_id', '!=', False)])
            
        elif self.region_id and self.regional_report:
            users = self.env['res.users'].sudo().search([('branch_id.region_id', '=', self.region_id.id)])
        
        for uid in users:
            if self.region_id and self.regional_report:
                vouchers = self.env['voucher.application'].sudo().search([('application_date', '>=', sdate),
                            ('branch_id.region_id', '=', self.region_id.id),('application_date', '<=', edate)])
            else:
                vouchers = self.env['voucher.application'].sudo().search(
                [('bdo_name', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
                
        if self.report_type == 'num_voucher':
            val_type = 'number'
            for sv in voucher_list:
                if len(sv) == 1:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    if sv.status == 'recommended':
                        rec += 1
                    elif sv.status == 'approved':
                        app += 1
                    elif sv.status == 'decline':
                        dec += 1
                    elif sv.status == 'cancel':
                        can += 1
                    total_voucher = rec + app + dec + can
                    vdata = {'name':sv.bdo_name.name, 
                             'rec':rec,
                             'app':app,
                             'dec':dec,
                             'can':can,
                             'beneficiary_branch' : sv.branch_id.name,
                             'total': total_voucher}
                    final_list.append(vdata)
                elif len(sv) >= 2:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    name = ''
                    for voucher in sv:
                        name = voucher.bdo_name.name
                        if voucher.status == 'recommended':
                            rec += 1
                        elif voucher.status == 'approved':
                            app += 1
                        elif voucher.status == 'decline':
                            dec += 1
                        elif voucher.status == 'cancel':
                            can += 1
                    total_voucher = rec + app + dec + can
                    vdata = {'name': name, 'rec': rec, 'app': app,'beneficiary_branch' : sv.branch_id.name, 'dec': dec, 'can': can,'total': total_voucher}
                    final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            for sv in voucher_list:
                if len(sv) == 1:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    if sv.status == 'recommended':
                        rec += sv.x_voucher_value
                    elif sv.status == 'approved':
                        app += sv.x_voucher_value
                    elif sv.status == 'decline':
                        dec += sv.x_voucher_value
                    elif sv.status == 'cancel':
                        can += sv.x_voucher_value
                    total_voucher = rec + app + dec + can
                    vdata = {'name': sv.bdo_name.name, 'rec': rec, 'app': app, 'beneficiary_branch' : sv.branch_id.name,'dec': dec,
                             'can': can, 'total': total_voucher}
                    final_list.append(vdata)
                elif len(sv) >= 2:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    name = ''
                    for voucher in sv:
                        name = voucher.bdo_name.name
                        if voucher.status == 'recommended':
                            rec += voucher.x_voucher_value
                        elif voucher.status == 'approved':
                            app += voucher.x_voucher_value
                        elif voucher.status == 'decline':
                            dec += voucher.x_voucher_value
                        elif voucher.status == 'cancel':
                            can += voucher.x_voucher_value
                    total_voucher = rec + app + dec + can
                    vdata = {'name': name, 'rec': rec, 'app': app,'beneficiary_branch' : voucher.branch_id.name, 'dec': dec, 'can': can,
                             'total': total_voucher}
                    final_list.append(vdata)
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch, 
                'value_type': val_type,
                'report_type': dict(self._fields['report_type'].selection).get(self.report_type),
                'type': self.type, 
                'vouchers': final_list,
                'region' : self.region_id.name,
                }

    def get_client_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            # Inefficient
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
        
        elif self.region_id and self.region_id:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])
        
            for uid in users:
                
                if self.type == 'received_applications':
                    if self.x_bda:
                        
                        if self.region_id and self.regional_report:
                            vouchers = self.env['voucher.application'].sudo().search(
                            [('status', '=', 'new'), ('beneficiary_id', '=', uid.id),('branch_id.region_id', '=', self.region_id.id),
                            ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                        else:
                            vouchers = self.env['voucher.application'].sudo().search(
                            [('write_uid', '=', self.x_bda.id), ('status', '=', 'new'), ('beneficiary_id', '=', uid.id),
                            ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    else:
                        
                        if self.region_id and self.regional_report:
                            
                            vouchers = self.env['voucher.application'].sudo().search(
                            [('status', '=', 'new'), ('beneficiary_id', '=', uid.id),('branch_id.region_id', '=', self.region_id.id),
                            ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                            
                        else:
                            
                            vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'new'), ('beneficiary_id', '=', uid.id), 
                         ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                                                    
                if self.type == 'declined_applications':
                    if self.x_bda:
                        
                        if self.region_id and self.regional_report:
                            vouchers = self.env['voucher.application'].sudo().search(
                                [('status', '=', 'decline'),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate),('branch_id.region_id', '=', self.region_id.id),
                                  ('application_date', '<=', edate)])
                        else:
                            vouchers = self.env['voucher.application'].sudo().search(
                            [('write_uid', '=', self.x_bda.id), ('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),
                            ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                            
                    else:
                        
                        if self.region_id and self.regional_report:
                            
                            vouchers = self.env['voucher.application'].sudo().search(
                            [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),('branch_id.region_id', '=', self.region_id.id),
                            ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                            
                        else:
                            
                            vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id), 
                         ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                                        
                elif self.type == 'approved_applications':
                    if self.x_bda:
                        
                        if self.region_id and self.regional_report:
                            vouchers = self.env['voucher.application'].sudo().search(
                                    [('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), 
                                      ('branch_id.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                        else:
                            vouchers = self.env['voucher.application'].sudo().search(
                                    [('write_uid', '=', self.x_bda.id), ('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), 
                                    ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    else:
                        if self.region_id and self.regional_report:
                            vouchers = self.env['voucher.application'].sudo().search(
                                [('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                                   ('branch_id.region_id', '=', self.region_id.id), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                        else:
                             
                             vouchers = self.env['voucher.application'].sudo().search(
                                [('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                                    ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])                   
            
                elif self.type == 'status_client':
                    if self.x_bda:
                        if self.region_id and self.regional_report:
                            vouchers = self.env['voucher.application'].sudo().search(
                                [('status', 'in', ('voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), 
                                   ('branch_id.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                        else:
                            vouchers = self.env['voucher.application'].sudo().search(
                                [('write_uid', '=', self.x_bda.id), ('status', 'in', ('voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), 
                                   ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    else:
                        if self.region_id and self.regional_report:
                            vouchers = self.env['voucher.application'].sudo().search(
                                [('status', 'in', ('voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), 
                                   ('branch_id.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                        else:
                            vouchers = self.env['voucher.application'].sudo().search(
                                [('status', 'in', ('voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), 
                                    ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])                
                
            else:
                #Get all records between dates
                if self.x_bda:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('beneficiary_id', '=', uid.id),
                             ('branch_id.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                        
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('write_uid', '=', self.x_bda.id), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate),('branch_id.region_id', '=', self.region_id.id), ('application_date', '<=', edate)])
                    else:                    
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                        
        vouchers = self.env['voucher.application'].sudo().search(
                        [('application_date', '>=', sdate), ('application_date', '<=', edate)])
                                
        if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
                 
        for sv in voucher_list:
            rec_no += 1
            for voucher in sv:
                temp = ""
                try:
                    for service in voucher.x_recommended_service:
                        temp = service.name + "\n"+ temp
                except:
                    print("Invalid value")
                    
                vdata = {'rec_no': rec_no, 
                         'name': voucher.name, 
                         'surname': voucher.surname,
                         'serial_number': voucher.serial_number,
                         'service': voucher.business_development_assistance_ids,
                         'x_voucher_number': voucher.x_voucher_number,
                         'x_service_provider': voucher.x_service_provider.name,
                         'x_recommended_service': temp,
                         #'x_voucher_value': voucher.x_legacy_value,
                         'beneficiary_branch' : voucher.branch_id.name,
                         'x_voucher_value': voucher.x_voucher_value,
                         'gender': dict(voucher._fields['gender'].selection).get(voucher.gender),
                         'geographical_type': dict(voucher._fields['geographical_type'].selection).get(voucher.geographical_type),
                         'disability': dict(voucher._fields['disability'].selection).get(voucher.disability),
                         'population_group': dict(voucher._fields['population_group'].selection).get(voucher.population_group),
                         'status': dict(voucher._fields['status'].selection).get(voucher.status),
                         'application_date': voucher.application_date
                         }
                final_list.append(vdata)  
                total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,
                }
        
    def get_issuance_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')

        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
        
        elif self.region_id and self.region_id:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])

        for uid in users:

            if self.type == 'received_applications':
                if self.x_bda:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('nearest_branch.region_id', '=', self.region_id.id), ('status', '=', 'new'), ('beneficiary_id', '=', uid.id),
                             ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('write_uid', '=', self.x_bda.id), ('status', '=', 'new'), ('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                else:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', '=', 'new'), ('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id),
                             ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', '=', 'new'), ('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])

            if self.type == 'declined_applications':
                if self.x_bda:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', '=', 'decline'),('nearest_branch.region_id', '=', self.region_id.id), ('beneficiary_id', '=', uid.id),
                             ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('write_uid', '=', self.x_bda.id), ('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),
                             ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                else:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id),
                             ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),
                             ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])

            elif self.type == 'approved_applications':
                if self.x_bda:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                             ('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('write_uid', '=', self.x_bda.id), ('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                             ('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                        
                else:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                             ('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                             ('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])

            elif self.type == 'status_client':
                if self.x_bda:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', 'in', ('voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                             ('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('write_uid', '=', self.x_bda.id), ('status', 'in', ('voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                             ('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                        
                else:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', 'in', ('voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                             ('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('status', 'in', ('voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                             ('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                        

            else:
            #Get all records between dates
                if self.x_bda:
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id),('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('write_uid', '=', self.x_bda.id),
                             ('beneficiary_id', '=', uid.id), ('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                        
                else:
                #vouchers = self.env['voucher.application'].sudo().search(
                #    [('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    if self.region_id and self.regional_report:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('nearest_branch.region_id', '=', self.region_id.id),('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])
                    else:
                        vouchers = self.env['voucher.application'].sudo().search(
                            [('x_voucher_start_date', '>=', sdate), ('x_voucher_start_date', '<=', edate)])

            if len(vouchers) >= 1:
                    voucher_list.append(vouchers)

        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0

        for sv in voucher_list:
            rec_no += 1
            for voucher in sv:
                temp = ""
                try:
                    for service in voucher.x_recommended_service:
                        temp = service.name + "\n"+ temp
                except:
                    print("Invalid value")

                vdata = {'rec_no': rec_no,
                         'name': voucher.name,
                         'surname': voucher.surname,
                         'serial_number': voucher.serial_number,
                         'service': voucher.business_development_assistance_ids,
                         'x_voucher_number': voucher.x_voucher_number,
                         'x_service_provider': voucher.x_service_provider.name,
                         'x_recommended_service': temp,
                         #'x_voucher_value': voucher.x_legacy_value,
                         'beneficiary_branch' : voucher.branch_id.name,
                         'x_voucher_value': voucher.x_voucher_value,
                         'gender': dict(voucher._fields['gender'].selection).get(voucher.gender),
                         'geographical_type': dict(voucher._fields['geographical_type'].selection).get(voucher.geographical_type),
                         'disability': dict(voucher._fields['disability'].selection).get(voucher.disability),
                         'population_group': dict(voucher._fields['population_group'].selection).get(voucher.population_group),
                         'status': dict(voucher._fields['status'].selection).get(voucher.status),
                         'application_date': voucher.application_date
                         }
                final_list.append(vdata)
                total_voucher += voucher.x_voucher_value

        return {'start_date': self.start_date,
                'end_date': self.end_date,
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type),
                'vouchers': final_list,
                'total_voucher': total_voucher}

    def get_disabled_data(self):
        voucher_dict = {}
        final_list = []
        branch = ''
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        if self.branch_id:
            branch = self.branch_id.name
            dvouchers = self.env['voucher.application'].sudo().search(
                [('disability', '=', 'yes'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            ndvouchers = self.env['voucher.application'].sudo().search(
                [('disability', '=', 'no'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            if len(dvouchers) >= 1:
                voucher_dict.update({'dis': dvouchers})
            if len(ndvouchers) >= 1:
                voucher_dict.update({'ndis': ndvouchers})
        elif self.all_branch:
            branch = 'All Branch'
            dvouchers = self.env['voucher.application'].sudo().search(
                [('disability', '=', 'yes'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            ndvouchers = self.env['voucher.application'].sudo().search(
                [('disability', '=', 'no'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            if len(dvouchers) >= 1:
                voucher_dict.update({'dis': dvouchers})
            if len(ndvouchers) >= 1:
                voucher_dict.update({'ndis': ndvouchers})
                
        elif self.region_id and self.regional_report:
            dvouchers = self.env['voucher.application'].sudo().search(
                [('disability', '=', 'yes'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            ndvouchers = self.env['voucher.application'].sudo().search(
                [('disability', '=', 'no'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            if len(dvouchers) >= 1:
                voucher_dict.update({'dis': dvouchers})
            if len(ndvouchers) >= 1:
                voucher_dict.update({'ndis': ndvouchers})
        
        if self.report_type == 'num_voucher':
            val_type = 'number'
            if 'dis' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['dis']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Disabled', 'rec':rec,'app':app,'beneficiary_branch' : data.branch_id.name,'dec':dec,'can':can,'total': total_voucher}
                final_list.append(vdata)
            if 'ndis' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['ndis']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Not Disabled', 'rec':rec,'app':app,'beneficiary_branch' : data.branch_id.name,'dec':dec,'can':can,'total': total_voucher}
                final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            if 'dis' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['dis']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Disabled', 'rec': rec, 'app': app, 'beneficiary_branch' : data.branch_id.name, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'ndis' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['ndis']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Not Disabled', 'rec': rec, 'app': app,'beneficiary_branch' : data.branch_id.name, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch,'value_type': val_type,
                'type': dict(self._fields['report_type'].selection).get(self.report_type), 'vouchers': final_list ,
                'region' : self.region_id.name,}

    def get_gender_data(self):
        voucher_dict = {}
        final_list = []
        branch = ''
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        if self.branch_id:
            branch = self.branch_id.name
            fvouchers = self.env['voucher.application'].sudo().search(
                [('gender', '=', 'female'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            mvouchers = self.env['voucher.application'].sudo().search(
                [('gender', '=', 'male'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            if len(fvouchers) >= 1:
                voucher_dict.update({'female': fvouchers})
            if len(mvouchers) >= 1:
                voucher_dict.update({'male': mvouchers})
        elif self.all_branch:
            branch = 'All Branch'
            fvouchers = self.env['voucher.application'].sudo().search(
                [('gender', '=', 'female'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            mvouchers = self.env['voucher.application'].sudo().search(
                [('gender', '=', 'male'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            if len(fvouchers) >= 1:
                voucher_dict.update({'female': fvouchers})
            if len(mvouchers) >= 1:
                voucher_dict.update({'male': mvouchers})
                
        elif self.region_id and self.regional_report:
            fvouchers = self.env['voucher.application'].sudo().search(
                [('gender', '=', 'female'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            mvouchers = self.env['voucher.application'].sudo().search(
                [('gender', '=', 'male'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            if len(fvouchers) >= 1:
                voucher_dict.update({'female': fvouchers})
            if len(mvouchers) >= 1:
                voucher_dict.update({'male': mvouchers})
        
        
        if self.report_type == 'num_voucher':
            val_type = 'number'
            if 'female' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['female']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Female', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'male' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['male']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Male', 'rec': rec, 'app': app,'beneficiary_branch' : data.branch_id.name, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            if 'female' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['female']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Female', 'rec': rec, 'app': app,'beneficiary_branch' : data.branch_id.name, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'male' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['male']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Male', 'rec': rec, 'app': app,'beneficiary_branch' : data.branch_id.name, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch, 'value_type': val_type,
                'type': dict(self._fields['report_type'].selection).get(self.report_type), 'vouchers': final_list,
                'region' : self.region_id.name,}

    def get_branch_data(self):
        voucher_list = []
        final_list = []
        branch = ''
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        if self.all_branch:
            branch = 'All Branch'
            branch_list = self.env['res.branch'].sudo().search([])
        for bid in branch_list:
            vouchers = self.env['voucher.application'].sudo().search(
                [('branch_id', '=', bid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        if self.report_type == 'num_voucher':
            val_type = 'number'
            for sv in voucher_list:
                if len(sv) == 1:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    paid = 0
                    if sv.status == 'recommended':
                        rec += 1
                    elif sv.status == 'approved':
                        app += 1
                    elif sv.status == 'decline':
                        dec += 1
                    elif sv.status == 'cancel':
                        can += 1
                    elif sv.status == 'payment_completed':
                        paid += 1
                    total_voucher = rec + app + dec + can + paid
                    vdata = {'name': sv.branch_id.name, 'rec': rec, 'paid': paid, 'app': app,'beneficiary_branch' : sv.branch_id.name, 'dec': dec, 'can': can,
                             'total': total_voucher}
                    final_list.append(vdata)
                elif len(sv) >= 2:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    paid = 0
                    name = ''
                    for voucher in sv:
                        name = voucher.branch_id.name
                        if voucher.status == 'recommended':
                            rec += 1
                        elif voucher.status == 'approved':
                            app += 1
                        elif voucher.status == 'decline':
                            dec += 1
                        elif voucher.status == 'cancel':
                            can += 1
                        elif voucher.status == 'payment_completed':
                            paid += 1
                    total_voucher = rec + app + dec + can + paid
                    vdata = {'name': name, 'rec': rec, 'paid': paid, 'app': app, 'beneficiary_branch' : voucher.branch_id.name,'dec': dec, 'can': can,
                             'total': total_voucher}
                    final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            for sv in voucher_list:
                if len(sv) == 1:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    paid = 0
                    if sv.status == 'recommended':
                        rec += sv.voucher_value_vat
                    elif sv.status == 'approved':
                        app += sv.voucher_value_vat
                    elif sv.status == 'decline':
                        dec += sv.voucher_value_vat
                    elif sv.status == 'cancel':
                        can += sv.voucher_value_vat
                    total_voucher = rec + app + dec + can
                    vdata = {'name': sv.branch_id.name, 'rec': rec, 'paid': paid, 'app': app,'beneficiary_branch' : sv.branch_id.name, 'dec': dec,
                             'can': can, 'total': total_voucher}
                    final_list.append(vdata)
                elif len(sv) >= 2:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    paid = 0
                    name = ''
                    for voucher in sv:
                        name = voucher.branch_id.name
                        if voucher.status == 'recommended':
                            rec += voucher.voucher_value_vat
                        elif voucher.status == 'approved':
                            app += voucher.voucher_value_vat
                        elif voucher.status == 'decline':
                            dec += voucher.voucher_value_vat
                        elif voucher.status == 'cancel':
                            can += voucher.voucher_value_vat
                    total_voucher = rec + app + dec + can
                    vdata = {'name': name, 'rec': rec, 'app': app,'beneficiary_branch' : voucher.branch_id.name, 'paid': paid, 'dec': dec, 'can': can,
                             'total': total_voucher}
                    final_list.append(vdata)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch,'value_type': val_type,
                'type': dict(self._fields['report_type'].selection).get(self.report_type), 'vouchers': final_list}

    def get_branch_cons_data(self):
        voucher_list = []
        final_list = []
        branch = 'All Branch'
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        vouchers = self.env['voucher.application'].sudo().search(
            [('branch_id', '!=', False), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
        if len(vouchers) >= 1:
            voucher_list.append(vouchers)
        if self.report_type == 'num_voucher':
            val_type = 'number'
            for sv in voucher_list:
                if len(sv) >= 1:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    paid = 0
                    name = ''
                    for voucher in sv:
                        name = voucher.branch_id.name
                        if voucher.status == 'recommended':
                            rec += 1
                        elif voucher.status == 'approved':
                            app += 1
                        elif voucher.status == 'decline':
                            dec += 1
                        elif voucher.status == 'cancel':
                            can += 1
                        elif voucher.status == 'payment_completed':
                            paid += 1
                    total_voucher = rec + app + dec + can + paid
                    vdata = {'name': 'All Branch', 'rec': rec, 'paid': paid,'beneficiary_branch' : sv.branch_id.name, 'app': app, 'dec': dec, 'can': can,
                             'total': total_voucher}
                    final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            for sv in voucher_list:
                if len(sv) >= 1:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    paid = 0
                    for voucher in sv:
                        if voucher.status == 'recommended':
                            rec += voucher.voucher_value_vat
                        elif voucher.status == 'approved':
                            app += voucher.voucher_value_vat
                        elif voucher.status == 'decline':
                            dec += voucher.voucher_value_vat
                        elif voucher.status == 'cancel':
                            can += voucher.voucher_value_vat
                    total_voucher = rec + app + dec + can
                    vdata = {'name': 'All Branch', 'rec': rec,'beneficiary_branch' : sv.branch_id.name, 'app': app, 'paid': paid, 'dec': dec, 'can': can,
                             'total': total_voucher}
                    final_list.append(vdata)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch,'value_type': val_type,
                'type': dict(self._fields['report_type'].selection).get(self.report_type), 'vouchers': final_list}

    def get_race_data(self):
        voucher_dict = {}
        final_list = []
        branch = ''
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        if self.branch_id:
            branch = self.branch_id.name
            afr_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'african'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            white_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'white'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            asian_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'asian'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            indian_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'indian'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            col_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'coloured'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            if len(afr_vouchers) >= 1:
                voucher_dict.update({'african': afr_vouchers})
            if len(white_vouchers) >= 1:
                voucher_dict.update({'white': white_vouchers})
            if len(asian_vouchers) >= 1:
                voucher_dict.update({'asian': asian_vouchers})
            if len(indian_vouchers) >= 1:
                voucher_dict.update({'indian': indian_vouchers})
            if len(col_vouchers) >= 1:
                voucher_dict.update({'coloured': col_vouchers})
        elif self.all_branch:
            branch = 'All Branch'
            afr_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'african'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            white_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'white'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            asian_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'asian'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            indian_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'indian'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            col_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'coloured'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            if len(afr_vouchers) >= 1:
                voucher_dict.update({'african': afr_vouchers})
            if len(white_vouchers) >= 1:
                voucher_dict.update({'white': white_vouchers})
            if len(asian_vouchers) >= 1:
                voucher_dict.update({'asian': asian_vouchers})
            if len(indian_vouchers) >= 1:
                voucher_dict.update({'indian': indian_vouchers})
            if len(col_vouchers) >= 1:
                voucher_dict.update({'coloured': col_vouchers})
                
        elif self.region_id and self.regional_report:

            afr_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'african'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            white_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'white'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            asian_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'asian'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            indian_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'indian'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            col_vouchers = self.env['voucher.application'].sudo().search(
                [('population_group', '=', 'coloured'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            if len(afr_vouchers) >= 1:
                voucher_dict.update({'african': afr_vouchers})
            if len(white_vouchers) >= 1:
                voucher_dict.update({'white': white_vouchers})
            if len(asian_vouchers) >= 1:
                voucher_dict.update({'asian': asian_vouchers})
            if len(indian_vouchers) >= 1:
                voucher_dict.update({'indian': indian_vouchers})
            if len(col_vouchers) >= 1:
                voucher_dict.update({'coloured': col_vouchers})
        
        
        if self.report_type == 'num_voucher':
            val_type = 'number'
            if 'african' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['african']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'African', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'white' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['white']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'White', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'asian' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['asian']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Asian', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'indian' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['indian']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Indian', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'coloured' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['coloured']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Coloured', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            if 'african' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['african']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'African', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'white' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['white']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'White', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'asian' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['asian']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Asian', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'indian' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['indian']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Indian', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'coloured' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['coloured']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Coloured', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch, 'value_type': val_type,
                'type': dict(self._fields['report_type'].selection).get(self.report_type), 'vouchers': final_list,
                'region' : self.region_id.name,}

    def get_rural_urban_data(self):
        voucher_dict = {}
        final_list = []
        branch = ''
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        if self.branch_id:
            branch = self.branch_id.name
            rvouchers = self.env['voucher.application'].sudo().search(
                [('geographical_type', '=', 'urban'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            uvouchers = self.env['voucher.application'].sudo().search(
                [('geographical_type', '=', 'rural'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '=', self.branch_id.id)])
            if len(rvouchers) >= 1:
                voucher_dict.update({'rural': rvouchers})
            if len(uvouchers) >= 1:
                voucher_dict.update({'urban': uvouchers})
        elif self.all_branch:
            branch = 'All Branch'
            rvouchers = self.env['voucher.application'].sudo().search(
                [('geographical_type', '=', 'urban'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            uvouchers = self.env['voucher.application'].sudo().search(
                [('geographical_type', '=', 'rural'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id', '!=', False)])
            if len(rvouchers) >= 1:
                voucher_dict.update({'rural': rvouchers})
            if len(uvouchers) >= 1:
                voucher_dict.update({'urban': uvouchers})
                
        elif self.region_id and self.regional_report:

            rvouchers = self.env['voucher.application'].sudo().search(
                [('geographical_type', '=', 'urban'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            uvouchers = self.env['voucher.application'].sudo().search(
                [('geographical_type', '=', 'rural'), ('application_date', '>=', sdate), ('application_date', '<=', edate),
                 ('branch_id.region_id', '=', self.region_id.id)])
            if len(rvouchers) >= 1:
                voucher_dict.update({'rural': rvouchers})
            if len(uvouchers) >= 1:
                voucher_dict.update({'urban': uvouchers})        
        
        if self.report_type == 'num_voucher':
            val_type = 'number'
            if 'rural' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['rural']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Rural', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'urban' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['urban']:
                    if data.status == 'recommended':
                        rec += 1
                    elif data.status == 'approved':
                        app += 1
                    elif data.status == 'decline':
                        dec += 1
                    elif data.status == 'cancel':
                        can += 1
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Urban', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            if 'rural' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['rural']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Rural', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
            if 'urban' in voucher_dict:
                rec = 0
                app = 0
                dec = 0
                can = 0
                for data in voucher_dict['urban']:
                    if data.status == 'recommended':
                        rec += data.voucher_value_vat
                    elif data.status == 'approved':
                        app += data.voucher_value_vat
                    elif data.status == 'decline':
                        dec += data.voucher_value_vat
                    elif data.status == 'cancel':
                        can += data.voucher_value_vat
                total_voucher = rec + app + dec + can
                vdata = {'name': 'Urban', 'rec': rec, 'app': app, 'dec': dec, 'can': can, 'total': total_voucher}
                final_list.append(vdata)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch, 'value_type': val_type,
                'type': dict(self._fields['report_type'].selection).get(self.report_type), 'vouchers': final_list,
                'region' : self.region_id.name,}

    def get_sp_data(self):
        voucher_list = []
        final_list = []
        branch = ''
        val_type = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'),
                                  '%d-%m-%Y')
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['partner.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['partner.enquiry'].sudo().search([('nearest_branch', '!=', False)])
            
        elif self.region_id and self.regional_report:
            users = self.env['partner.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])
        
        for uid in users:
            if self.region_id and self.regional_report:
                vouchers = self.env['voucher.application'].sudo().search(
                    [('service_provider', '=', uid.id), ('application_date', '>=', sdate), 
                     ('branch_id.region_id', '=', self.region_id.id),('application_date', '<=', edate)])
            else:
                vouchers = self.env['voucher.application'].sudo().search(
                    [('service_provider', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        if self.report_type == 'num_voucher':
            val_type = 'number'
            for sv in voucher_list:
                if len(sv) == 1:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    if sv.status == 'recommended':
                        rec += 1
                    elif sv.status == 'approved':
                        app += 1
                    elif sv.status == 'decline':
                        dec += 1
                    elif sv.status == 'cancel':
                        can += 1
                    total_voucher = rec + app + dec + can
                    vdata = {'name':sv.service_provider.entity_name, 'rec':rec,'app':app,'dec':dec,'can':can,'total': total_voucher}
                    final_list.append(vdata)
                elif len(sv) >= 2:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    name = ''
                    for voucher in sv:
                        name = voucher.service_provider.entity_name
                        if voucher.status == 'recommended':
                            rec += 1
                        elif voucher.status == 'approved':
                            app += 1
                        elif voucher.status == 'decline':
                            dec += 1
                        elif voucher.status == 'cancel':
                            can += 1
                    total_voucher = rec + app + dec + can
                    vdata = {'name': name, 'rec': rec, 'app': app, 'dec': dec, 'can': can,'total': total_voucher}
                    final_list.append(vdata)
        elif self.report_type == 'voucher_values':
            val_type = 'amt'
            for sv in voucher_list:
                if len(sv) == 1:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    if sv.status == 'recommended':
                        rec += sv.voucher_value_vat
                    elif sv.status == 'approved':
                        app += sv.voucher_value_vat
                    elif sv.status == 'decline':
                        dec += sv.voucher_value_vat
                    elif sv.status == 'cancel':
                        can += sv.voucher_value_vat
                    total_voucher = rec + app + dec + can
                    vdata = {'name': sv.service_provider.entity_name, 'rec': rec, 'app': app, 'dec': dec,
                             'can': can, 'total': total_voucher}
                    final_list.append(vdata)
                elif len(sv) >= 2:
                    rec = 0
                    app = 0
                    dec = 0
                    can = 0
                    name = ''
                    for voucher in sv:
                        name = voucher.service_provider.entity_name
                        if voucher.status == 'recommended':
                            rec += voucher.voucher_value_vat
                        elif voucher.status == 'approved':
                            app += voucher.voucher_value_vat
                        elif voucher.status == 'decline':
                            dec += voucher.voucher_value_vat
                        elif voucher.status == 'cancel':
                            can += voucher.voucher_value_vat
                    total_voucher = rec + app + dec + can
                    vdata = {'name': name, 'rec': rec, 'app': app, 'dec': dec, 'can': can,
                             'total': total_voucher}
                    final_list.append(vdata)
        return {'start_date': self.start_date, 'end_date': self.end_date, 'branch': branch,'value_type': val_type,
                'type': dict(self._fields['report_type'].selection).get(self.report_type), 'vouchers': final_list,
                'region' : self.region_id.name,}

    def get_status_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            elif self.type == 'status_bdo':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_bdo').report_action(self)
            elif self.type == 'status_branch':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_branch').report_action(self)
            elif self.type == 'status_branch_cons':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_branch_cons').report_action(self)
            elif self.type == 'status_client':
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_issuance').report_action(self)            
            elif self.type == 'status_disable':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_disable').report_action(self)
            elif self.type == 'status_gender':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_gender').report_action(self)
            elif self.type == 'status_race':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_race').report_action(self)
            elif self.type == 'status_rural_urban':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_rural_urban').report_action(self)
            elif self.type == 'status_sp':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_sp').report_action(self)
            elif self.type == 'status_service':
                return self.env.ref('nyda_grant_and_voucher.action_report_status_service').report_action(self)
            elif self.type == 'received_applications':
                return self.env.ref('nyda_grant_and_voucher.action_application_received_report').report_action(self)
            elif self.type == 'approved_applications':
                return self.env.ref('nyda_grant_and_voucher.action_application_received_report').report_action(self)
            elif self.type == 'declined_applications':
                return self.env.ref('nyda_grant_and_voucher.action_application_received_report').report_action(self)
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_status_client_applications').report_action(self)                                


    def get_appointment_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
            
        elif self.region_id and self.regional_report:
            
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])
        
        
        for uid in users:
            
            if self.type == 'declined_applications':
                
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),
                         ('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    
            elif self.type == 'approved_applications':
                
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id), 
                         ('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', 'in', ('approved','voucher_isurance','work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id), 
                         ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            else:            
                vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '!=', 'new'), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
                 
        for sv in voucher_list:
            rec_no += 1
            for voucher in sv:
                vdata = {   'rec_no': rec_no,                    
                            'serial_number': voucher.serial_number,
                            'application_date': voucher.application_date,
                            'status': dict(voucher._fields['status'].selection).get(voucher.status),
                            'service': voucher.business_development_assistance_ids,
                            'beneficiary_branch' : voucher.branch_id.name,
                            'name': voucher.name,
                            'surname': voucher.surname,
                            'mobile': voucher.mobile,
                            'appointment_date': voucher.appointment_date,
                            'bdo_name': voucher.bdo_name.name
                         }
                final_list.append(vdata)  
                total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        

    def get_assessment_appointment_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_assessment_appointment_report').report_action(self)                                    


    def get_assessment_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''

        #self.start_date.strftime ('% Y-% m-% d% H:% m:% S')
     
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
            
        elif self.region_id and self.regional_report:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])
            
        for uid in users:
            if self.region_id and self.regional_report:
                vouchers = self.env['voucher.assessment'].sudo().search([('voucher_application_id.beneficiary_id', '=', uid.id),
                                                             ('voucher_application_id.branch_id.region_id', '=', self.region_id.id),('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date)])
            else:
                vouchers = self.env['voucher.assessment'].sudo().search([('voucher_application_id.beneficiary_id', '=', uid.id),
                                                             ('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date)])

        if len(vouchers) >= 1:
            voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
                 
        for sv in voucher_list:
            rec_no += 1
            for voucher in sv:
                vdata = {   'rec_no': rec_no,                    
                            'application_id': voucher.voucher_application_id.serial_number,
                            'beneficiary_branch' : voucher.voucher_application_id.branch_id.name,
                            'create_date': voucher.create_date,
                            'total': voucher.assessment_index_total
                         }
                final_list.append(vdata)  
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
    def get_assessment_conducted_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_assessment_conducted').report_action(self)                                    

    def get_voucher_issuance_multiple_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
        
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])    
            
        for uid in users:
            
            if self.type == 'declined_applications':
                
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search([('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),
                                ('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    
            elif self.type == 'approved_applications':
                
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search([('status', '=', 'approved'), ('beneficiary_id', '=', uid.id),
                    ('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                
                else:
                    vouchers = self.env['voucher.application'].sudo().search([('status', '=', 'approved'), ('beneficiary_id', '=', uid.id),
                                                                    ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            else:
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search([('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                                 ('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])

                else:
                    vouchers = self.env['voucher.application'].sudo().search([('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                            ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:
                
                #Get count of voucher applications per client
                applications_count=self.env['voucher.application'].search_count([('sa_identity_number','=',voucher.sa_identity_number)])
                
                #Only display beneficiaries with multiple voucher applications
                if applications_count > 1:
                    
                    applications=self.env['voucher.application'].search([('sa_identity_number','=',voucher.sa_identity_number)])
                    beneficiary_total = 0
                    
                    for va in applications:
                        beneficiary_total += va.x_voucher_value
                    
                    vdata = {'rec_no': rec_no,
                             'name': voucher.name, 
                             'surname': voucher.surname,
                             'sa_identity_number': voucher.sa_identity_number,
                             'mobile': voucher.mobile,
                             'beneficiary_branch' : voucher.branch_id.name,
                             'email': voucher.email,
                             'gender': voucher.gender,
                             'population_group': voucher.population_group,
                             'geographical_type': voucher.geographical_type,
                             'disability': voucher.disability,
                             'beneficiary_total': beneficiary_total,
                             }
                                        
                    '''
                    vdata = {'rec_no': rec_no,
                             'name': voucher.name, 
                             'surname': voucher.surname,
                             'serial_number': voucher.serial_number,
                             'sa_identity_number': voucher.sa_identity_number,
                             'x_voucher_number': voucher.x_voucher_number,
                             'x_service_provider': voucher.x_service_provider.name,
                             'x_recommended_service': voucher.x_recommended_service.name,
                             'x_voucher_value': voucher.x_voucher_value,
                             'gender': voucher.gender,
                             'geographical_type': voucher.geographical_type,
                             'disability': voucher.disability,
                             'population_group': voucher.population_group,
                             'application_date': voucher.application_date
                             }
                    '''
                    
                    final_list.append(vdata)  
                    total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
    def get_voucher_issuance_multiple_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_issuance_multiple_report').report_action(self) 
            
    def get_expired_vouchers_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
            
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])
            
        for uid in users:
            
            if self.type == 'declined_applications':
                
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id), ('x_voucher_end_date', '>', sdate),
                     ('nearest_branch.region_id', '=', self.region_id.id),('x_voucher_end_date', '<', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id), ('x_voucher_end_date', '>', sdate), ('x_voucher_end_date', '<', edate)])
                    
            elif self.type == 'approved_applications':
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'approved'), ('beneficiary_id', '=', uid.id), 
                         ('nearest_branch.region_id', '=', self.region_id.id),('x_voucher_end_date', '>', sdate), ('x_voucher_end_date', '<', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'approved'), ('beneficiary_id', '=', uid.id), ('x_voucher_end_date', '>', sdate), ('x_voucher_end_date', '<', edate)])
            else:
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                         ('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('x_voucher_end_date', '>', sdate), ('x_voucher_end_date', '<', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                         ('beneficiary_id', '=', uid.id), ('x_voucher_end_date', '>', sdate), ('x_voucher_end_date', '<', edate)])
                    
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:
                temp = ""
                try:
                    for service in voucher.x_recommended_service:
                        temp = service.name + "\n"+ temp
                except:
                    print("Invalid value")
                vdata = {'rec_no': rec_no,
                         'name': voucher.name, 
                         'surname': voucher.surname,
                         'serial_number': voucher.serial_number,
                         'sa_identity_number': voucher.sa_identity_number,
                         'x_voucher_number': voucher.x_voucher_number,
                         'beneficiary_branch' : voucher.branch_id.name,
                         'x_service_provider': voucher.x_service_provider.name,
                         'x_recommended_service': temp,
                         'x_voucher_value': voucher.x_voucher_value,
                         'voucher_end_date': voucher.x_voucher_end_date,
                         'gender': voucher.gender,
                         'geographical_type': voucher.geographical_type,
                         'disability': voucher.disability,
                         'population_group': voucher.population_group,
                         'application_date': voucher.application_date
                         }
                
                final_list.append(vdata)  
                total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
    def get_expired_vouchers_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_expired_report').report_action(self)             
            
    def get_reissued_vouchers_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
            
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])    
        
        for uid in users:
            
            if self.type == 'declined_applications':
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'decline'),('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('x_voucher_reissue_start_date', '>=', sdate), ('x_voucher_reissue_start_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id), ('x_voucher_reissue_start_date', '>=', sdate), ('x_voucher_reissue_start_date', '<=', edate)])
                    
            elif self.type == 'approved_applications':
                
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search([('status', '=', 'approved'), ('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id),
                                                                              ('x_voucher_reissue_start_date', '>=', sdate), ('x_voucher_reissue_start_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search([('status', '=', 'approved'), ('beneficiary_id', '=', uid.id),
                                                                              ('x_voucher_reissue_start_date', '>=', sdate), ('x_voucher_reissue_start_date', '<=', edate)])
            else:
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                         ('nearest_branch.region_id', '=', self.region_id.id),('x_voucher_reissue_start_date', '>=', sdate), ('x_voucher_reissue_start_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id), ('x_voucher_reissue_start_date', '>=', sdate), ('x_voucher_reissue_start_date', '<=', edate)])
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:
                temp = ""
                try:
                    for service in voucher.x_recommended_service:
                        temp = service.name + "\n"+ temp
                except:
                    print("Invalid value")
                vdata = {'rec_no': rec_no,
                         'name': voucher.name, 
                         'surname': voucher.surname,
                         'serial_number': voucher.serial_number,
                         'sa_identity_number': voucher.sa_identity_number,
                         'x_voucher_number': voucher.x_voucher_number,
                         'x_service_provider': voucher.x_service_provider.name,
                         'x_recommended_service': temp,
                         'x_voucher_value': voucher.x_voucher_value,
                         
                         'beneficiary_branch' : voucher.branch_id.name,
                         'x_voucher_reissue_start_date': voucher.x_voucher_reissue_start_date,
                         'x_voucher_reissue_end_date': voucher.x_voucher_reissue_end_date,
                         
                         'gender': voucher.gender,
                         'geographical_type': voucher.geographical_type,
                         'disability': voucher.disability,
                         'population_group': voucher.population_group,
                         'application_date': voucher.application_date
                         }
                
                final_list.append(vdata)  
                total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
    def get_reissued_vouchers_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_reissued_report').report_action(self)                         
            
    def get_beneficiaries_vouchers_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
            
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])
        
        for uid in users:
            
            if self.type == 'declined_applications':
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search([('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),
                                            ('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search([('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),
                                                                              ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    
            elif self.type == 'approved_applications':
                
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'approved'), ('beneficiary_id', '=', uid.id),
                         ('application_date', '>=', sdate),('nearest_branch.region_id', '=', self.region_id.id), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'approved'), ('beneficiary_id', '=', uid.id),
                         ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            else: 
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', 'in', ('voucher_isurance', 'work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                         ('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', 'in', ('voucher_isurance', 'work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                         ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:
                
                beneficiaries_list = []
                
                #Get count of voucher applications per client
                beneficiaries = self.env['business.ownership.status'].search([('voucher_application_id_business_ownership', '=', voucher.id)])
                
                for va in beneficiaries:
                
                    beneficiary_data = { 'rec_no': rec_no,
                                         'voucher_number': voucher.x_voucher_number,
                                         'name': va.name, 
                                         'contact_number': va.mobile,
                                         'population_group': va.population_group,
                                         'geographical_type': va.geographical_type,
                                         'beneficiary_branch' : voucher.branch_id.name,
                                         'disability': va.disability,
                                         'gender': va.gender,
                                         'ownership': va.ownership,
                                         'id_number': va.x_id_number,
                                         'position': va.position
                                         }
                    
                    beneficiaries_list.append(beneficiary_data)
                    
                voucher_data = {'rec_no': rec_no,
                                 'name': voucher.name,
                                 'surname': voucher.surname,
                                 'voucher_number': voucher.x_voucher_number,
                                 'sa_identity_number': voucher.sa_identity_number,
                                 'beneficiary_branch' : voucher.branch_id.name,
                                 'gender': voucher.gender,
                                 'geographical_type': voucher.geographical_type,
                                 'disability': voucher.disability,
                                 'population_group': voucher.population_group,
                                 'contact_number': voucher.mobile,
                                 'beneficiaries':beneficiaries_list
                                 }
                    
                final_list.append(voucher_data)                    
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
    def get_beneficiaries_vouchers_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_beneficiaries').report_action(self)                                     
            
    def get_jobs_created_data(self):
        voucher_list        = []
        final_list_before   = []
        final_list_after    = []
        branch              = ''
        val_type            = ''
        
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
        
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])    
        
        for uid in users:
            
            if self.type == 'declined_applications':
                
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'decline'),('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    
            elif self.type == 'approved_applications':
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'approved'),('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', 'approved'), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            else:
                    
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                     ('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                     ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:
                
                #Get count of voucher applications per client
                job_creation = self.env['job.creation.information'].search([('voucher_application_id', '=', voucher.id)])
                    
                for jc in job_creation:
                
                    before_data = {'rec_no': rec_no,
                                   'voucher_number': voucher.x_voucher_number,
                                   'before_funding_female': jc.before_funding_female,
                                   'before_funding_male': jc.before_funding_male,                             
                                   'before_funding_age_female': jc.before_funding_age_female,
                                   'beneficiary_branch' : voucher.branch_id.name,
                                   'before_funding_age_male': jc.before_funding_age_male,
                                   'before_funding_disabled_female': jc.before_funding_disabled_female,
                                   'before_funding_disabled_male': jc.before_funding_disabled_male,                                     
                                   }
                    
                    after_data = {'rec_no': rec_no,
                                  'voucher_number': voucher.x_voucher_number,
                                  'after_funding_female': jc.after_funding_female,
                                  'beneficiary_branch' : voucher.branch_id.name,
                                  'after_funding_male': jc.after_funding_male,                     
                                  'after_funding_age_female': jc.after_funding_age_female,
                                  'after_funding_age_male':   jc.after_funding_age_male,
                                  'after_funding_disabled_female': jc.after_funding_disabled_female,
                                  'after_funding_disabled_male': jc.after_funding_disabled_male,                                     
                                }                    
                    
                    final_list_before.append(before_data)
                    final_list_after.append(after_data)
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'final_list_before': final_list_before,
                'final_list_after': final_list_after,
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
    def get_jobs_created_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_jobs_created').report_action(self)                                                 
            
    def get_service_providers_data(self):
        partner_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        
        if self.x_province_id and self.x_service and self.branch_id:
            service_providers = self.env['res.partner'].sudo().search([('is_company', '=', True),
                                                                       ('state_id', '=', self.x_province_id.id),
                                                                       ('x_services', 'in', self.x_service.ids), 
                                                                       ('x_branch_id', '=', self.branch_id.id)])
        else:
            service_providers = self.env['res.partner'].sudo().search([('is_company', '=', True)])            
        
            
        if len(service_providers) >= 1:
            partner_list.append(service_providers)
        
        val_type        = 'amt'
        rec_no          = 0
        
        for partners in partner_list:
            rec_no += 1
            
            for partner in partners:
                vdata = {'rec_no': rec_no,
                         'name': partner.name, 
                         'mobile': partner.mobile,
                         'phone': partner.phone,
                         'partner_branch' : partner.state_id.name,
                         'email': partner.email,
                         'website': partner.website,
                         'services': partner.x_services,
                         }
                
                final_list.append(vdata)  
        temp = ""
        try:
            for service in self.x_service:
                temp = self.x_service.name + "\n"+ temp
        except:
            print("Invalid value")            
        return {
                'province': self.x_province_id.name,
                'service': temp,
                'branch': self.branch_id.name,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'partners': final_list
                }
        
    def get_service_providers_report(self):
        if self.x_service or self.branch_id or self.x_province_id:
            return self.env.ref('nyda_grant_and_voucher.action_report_voucher_service_providers').report_action(self)                                                                         
            
    def get_aftercare_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
        
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])    
        
        for uid in users:
            
            if self.type == 'declined_applications':
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'decline'), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    
            elif self.type == 'approved_applications':
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'approved'), ('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'approved'), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            else:
                if self.region_id and self.regional_report: 
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                     ('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                     ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:
                
                #Get count of voucher applications per client
                applications_count=self.env['voucher.application'].search_count([('sa_identity_number','=',voucher.sa_identity_number)])
                
                #Only display beneficiaries with multiple voucher applications
                if applications_count > 1:
                    
                    applications=self.env['voucher.application'].search([('sa_identity_number','=',voucher.sa_identity_number)])
                    beneficiary_total = 0
                    
                    for va in applications:
                        beneficiary_total += va.x_voucher_value
                    
                    vdata = {'rec_no': rec_no,
                             'name': voucher.name, 
                             'surname': voucher.surname,
                             'serial_number': voucher.serial_number,
                             'sa_identity_number': voucher.sa_identity_number,
                             'x_voucher_number': voucher.x_voucher_number,
                             'x_service_provider': voucher.x_service_provider.name,
                             'x_recommended_service': voucher.x_recommended_service.name,
                             'beneficiary_branch' : voucher.branch_id.name,
                             'x_voucher_value': voucher.x_voucher_value,
                             'gender': voucher.gender,
                             'geographical_type': voucher.geographical_type,
                             'disability': voucher.disability,
                             'population_group': voucher.population_group,
                             'application_date': voucher.application_date
                             }
                    
                    final_list.append(vdata)  
                    total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
    def get_aftercare_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_aftercare_report').report_action(self)

    def get_service_provider_query_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
            
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])    
        
        
        for uid in users:

            if self.x_service_provider:
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                     ('application_date', '>=', sdate),('nearest_branch.region_id', '=', self.region_id.id),('application_date', '<=', edate), ('x_service_provider', '=', self.x_service_provider.id)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                     ('application_date', '>=', sdate), ('application_date', '<=', edate), ('x_service_provider', '=', self.x_service_provider.id)])
            else:  
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                     ('beneficiary_id', '=', uid.id),('nearest_branch.region_id', '=', self.region_id.id),('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('work_plan', 'work_plan_submitted', 'submitted_product', 'client_review', 'nyda_review','bda_review', 'bdo_review', 'pc_review', 'branch_manager_review', 'ho_admin_review', 'qa_officer_review', 'ed_manager_review', 'nyda_head_office', 'send_payment_reciept', 'post_disbursement_done', 'pending_payment', 'payment_completed')),
                     ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:
                temp = ""
                try:
                    for service in voucher.x_recommended_service:
                        temp = service.name + "\n"+ temp
                except:
                    print("Invalid value")
                vdata = {'rec_no': rec_no,
                         'name': voucher.name, 
                         'surname': voucher.surname,
                         'serial_number': voucher.serial_number,
                         'sa_identity_number': voucher.sa_identity_number,                         
                         'x_voucher_number': voucher.x_voucher_number,
                         'x_service_provider': voucher.x_service_provider.name,
                         'beneficiary_branch' : voucher.branch_id.name,
                         'x_recommended_service': temp,
                         'client_approve_reject_description': voucher.client_approve_reject_description,
                         'x_bda_comments': voucher.x_bda_comments,
                         'application_date': voucher.application_date
                         }
                
                final_list.append(vdata)  
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list,
                'region' : self.region_id.name,
                }
        
    def get_service_provider_query_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_service_provider_query_report').report_action(self)                                                                                                                                                                                                   

    def get_redemptions_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
        
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])
        
        for uid in users:
            
            if self.x_voucher_status == 'Submitted':
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'ho_admin_review'),('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'ho_admin_review'), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    
            elif self.x_voucher_status == 'Approved':
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'pending_payment'),('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', 'pending_payment'), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                    
            elif self.x_voucher_status == 'Declined':
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('x_ed_manager_state', 'in', ('Query Invoice', 'Query Product')),('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate),
                     ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('x_ed_manager_state', 'in', ('Query Invoice', 'Query Product')), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate),
                     ('application_date', '<=', edate)])                
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:
                temp = ""
                try:
                    for service in voucher.x_recommended_service:
                        temp = service.name + "\n"+ temp
                except:
                    print("Invalid value")
                vdata = {'rec_no': rec_no,
                         'name': voucher.name, 
                         'surname': voucher.surname,
                         'serial_number': voucher.serial_number,
                         'sa_identity_number': voucher.sa_identity_number,
                         'x_voucher_number': voucher.x_voucher_number,
                         'x_service_provider': voucher.x_service_provider.name,
                         'beneficiary_branch' : voucher.branch_id.name,
                         'x_recommended_service': temp,
                         'x_voucher_value': voucher.x_voucher_value,
                         'gender': voucher.gender,
                         'geographical_type': voucher.geographical_type,
                         'disability': voucher.disability,
                         'population_group': voucher.population_group,
                         'application_date': voucher.application_date
                         }
                
                final_list.append(vdata)  
                total_voucher += voucher.x_voucher_value
        temp = ""
        try:
            for service in self.x_service:
                temp = self.x_service.name + "\n"+ temp
        except:
            print("Invalid value")              
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'service_provider': self.x_service_provider.name,
                'service': temp,
                'voucher_status': self.x_voucher_status,
                'beneficiary': self.x_voucher_beneficiary,
                'branch': self.branch_id,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name}
        
    def get_redemptions_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_redemptions').report_action(self)                  

    def get_service_providers_rating_data(self):
        assessment_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
        
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])
        
        for uid in users:
            
            if self.x_service_provider:
                
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('x_service_provider', '=', self.x_service_provider.id), ('beneficiary_id', '=', uid.id),
                     ('application_date', '>=', self.start_date),('nearest_branch.region_id', '=', self.region_id.id),('application_date', '<=', self.end_date)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('x_service_provider', '=', self.x_service_provider.id), ('beneficiary_id', '=', uid.id),
                     ('application_date', '>=', self.start_date), ('application_date', '<=', self.end_date)])
                
                for voucher in vouchers:
                    assessments = self.env['voucher.assessment'].sudo().search([('voucher_application_id', '=', voucher.id),('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date)])
                
                    if len(assessments) >= 1:
                        assessment_list.append(assessments)                    
            else:
                if self.region_id and self.regional_report:
                    
                    assessments = self.env['voucher.assessment'].sudo().search([('create_date', '>=', self.start_date),
                                ('voucher_application_id.nearest_branch.region_id', '=', self.region_id.id),('create_date', '<=', self.end_date)])
                    
                else:
                    
                     assessments = self.env['voucher.assessment'].sudo().search([('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date)])
        
                if len(assessments) >= 1:
                    assessment_list.append(assessments)
        
        val_type        = 'amt'
        rec_no          = 0
        total_ratings   = 0
        average_rating  = 0
        
        for sv in assessment_list:

            for assessment in sv:
                
                voucher_existence = self.env['voucher.application'].sudo().search_count([('id', '=', assessment.voucher_application_id.id)])
                
                if voucher_existence > 0:
                    rec_no += 1
                    
                    vdata = {   'rec_no': rec_no,
                                'voucher_application_id': assessment.voucher_application_id.name,
                                'voucher_number': assessment.voucher_application_id.x_voucher_number,
                                'service_provider': assessment.voucher_application_id.x_service_provider.name,
                                'x_waiting_period': assessment.x_waiting_period, 
                                'beneficiary_branch' : assessment.voucher_application_id.branch_id.name,
                                'x_sp_facilities': assessment.x_sp_facilities,
                                'x_sp_friendliness': assessment.x_sp_friendliness,
                                'x_sp_professionalism': assessment.x_sp_professionalism,
                                'x_overall_experience': assessment.x_overall_experience
                             }
                    
                    final_list.append(vdata)  
                    total_ratings += int(assessment.x_overall_experience)
        
        if rec_no > 0:
            average_rating = (total_ratings/rec_no)
            
        return {
                'start_date': self.start_date,
                'end_date': self.end_date,
                'service_provider': self.x_service_provider.name,
                'branch': self.branch_id.name,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'assessments': final_list,
                'average_rating': average_rating,
                'region' : self.region_id.name,
                }
        
    def get_service_providers_rating_report(self):
        if self.start_date and self.end_date:
            return self.env.ref('nyda_grant_and_voucher.action_report_voucher_client_service_ratings').report_action(self)                                                                         
        
    def get_voucher_payments_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
            
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])
            
        for uid in users:
            
            if self.x_service_provider:
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', ('payment_completed')), ('beneficiary_id', '=', uid.id),
                         ('application_date', '>=', sdate),('nearest_branch.region_id', '=', self.region_id.id), ('application_date', '<=', edate), ('x_service_provider', '=', self.x_service_provider.id)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                        [('status', '=', ('payment_completed')), ('beneficiary_id', '=', uid.id),
                         ('application_date', '>=', sdate), ('application_date', '<=', edate), ('x_service_provider', '=', self.x_service_provider.id)])
                    
            else:
                if self.region_id and self.regional_report: 
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', ('payment_completed')),('nearest_branch.region_id', '=', self.region_id.id),('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', '=', ('payment_completed')), ('beneficiary_id', '=', uid.id), ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:

                vdata = {   'rec_no': rec_no,
                            'x_voucher_number': voucher.x_voucher_number,
                            'x_voucher_value': voucher.x_voucher_value,
                            'service_provider': voucher.x_service_provider.name,
                            'beneficiary_branch' : voucher.branch_id.name,
                            'invoice_date': voucher.x_invoice_date,
                            'pc_approval_date': voucher.x_pc_approval_date,
                            'finance_submission_date': voucher.x_finance_submission_date,
                            'status': dict(voucher._fields['status'].selection).get(voucher.status),
                            'write_date': voucher.write_date
                        }
                
                final_list.append(vdata)  
                total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'service_provider': self.x_service_provider.name,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
    def get_voucher_payments_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_payments').report_action(self)
            
    def get_voucher_payment_tracking_report_data(self):
        voucher_list    = []
        final_list      = []
        branch          = ''
        val_type        = ''
        
        sdate = datetime.strptime(datetime.strftime(datetime.strptime(self.start_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        edate = datetime.strptime(datetime.strftime(datetime.strptime(self.end_date, '%Y-%m-%d'), '%d-%m-%Y'), '%d-%m-%Y')
        
        if self.branch_id:
            branch = self.branch_id.name
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '=', self.branch_id.id)])
        elif self.all_branch:
            branch = 'All Branch'
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch', '!=', False)])
        
        elif self.region_id and self.regional_report:
            users = self.env['youth.enquiry'].sudo().search([('nearest_branch.region_id', '=', self.region_id.id)])    
        
        for uid in users:
            
            if self.x_service_provider:
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('send_payment_reciept', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                     ('application_date', '>=', sdate),('nearest_branch.region_id', '=', self.region_id.id),('application_date', '<=', edate), ('x_service_provider', '=', self.x_service_provider.id)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('send_payment_reciept', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                     ('application_date', '>=', sdate),('application_date', '<=', edate), ('x_service_provider', '=', self.x_service_provider.id)])
                    
            else:
                if self.region_id and self.regional_report:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('send_payment_reciept', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                     ('application_date', '>=', sdate),('nearest_branch.region_id', '=', self.region_id.id),('application_date', '<=', edate)])
                else:
                    vouchers = self.env['voucher.application'].sudo().search(
                    [('status', 'in', ('send_payment_reciept', 'pending_payment', 'payment_completed')), ('beneficiary_id', '=', uid.id),
                     ('application_date', '>=', sdate), ('application_date', '<=', edate)])
            
            if len(vouchers) >= 1:
                voucher_list.append(vouchers)
        
        val_type        = 'amt'
        rec_no          = 0
        total_voucher   = 0
        
        for sv in voucher_list:
            rec_no += 1
            multi   = 0

            for voucher in sv:

                vdata = {   'rec_no': rec_no,
                            'x_voucher_number': voucher.x_voucher_number,
                            'x_voucher_value': voucher.x_voucher_value,
                            'service_provider': voucher.x_service_provider.name,
                            'invoice_date': voucher.x_invoice_date,
                            'beneficiary_branch' : voucher.branch_id.name,
                            'pc_approval_date': voucher.x_pc_approval_date,
                            'finance_submission_date': voucher.x_finance_submission_date,                            
                            'status': dict(voucher._fields['status'].selection).get(voucher.status),
                            'write_date': voucher.write_date
                        }
                
                final_list.append(vdata)  
                total_voucher += voucher.x_voucher_value
                    
        return {'start_date': self.start_date, 
                'end_date': self.end_date, 
                'branch': branch,
                'service_provider': self.x_service_provider.name,
                'value_type': val_type,
                'type': dict(self._fields['type'].selection).get(self.type), 
                'vouchers': final_list, 
                'total_voucher': total_voucher,
                'region' : self.region_id.name,}
        
    def get_voucher_payment_tracking_report(self):
        if self.start_date and self.end_date:
            converted_start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            converted_end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            if converted_start_date > converted_end_date:
                raise UserError(_("Start date cannot be greater than end date"))
            else:
                return self.env.ref('nyda_grant_and_voucher.action_report_voucher_payment_tracking').report_action(self)                            