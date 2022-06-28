# -*- coding: utf-8 -*-
import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import float_compare, float_is_zero

class AssetTransfer(models.Model):
    
    _name = 'asset.transfer'
    _inherit = ['mail.thread']
    _rec_name = 'serial_number'
    
    serial_number                       = fields.Char('Serial Number')
    asset_transfer_title                = fields.Char(string='Asset Transfer Title')
    asset_register                      = fields.Many2one('account.asset',string='Asset Register')
    asset_model                         = fields.Char(string='Asset Model',related="asset_register.model")
    asset_number                        = fields.Char(string='Asset Number',related="asset_register.asset_id")
    asset_serial_number                 = fields.Char(string='Asset Serial Number',related="asset_register.serial")
    state                               = fields.Selection([('new','New'),
                                                            ('1st_review','1st Review'),
                                                            ('2nd_review','2nd Review'),
                                                            ('completed','Completed'),
                                                            ('end','End')],'Status',group_expand='_expand_states', default='new')
    
    #default_user                        = fields.Many2one('res.users',default=lambda self: self.env.user and self.env.user.id or False,string="Dispatcher")
    asset_dispatcher                    = fields.Many2one('hr.employee',default=lambda self: self._get_employee_id()
                                                          ,string="Dispatcher")
    asset_dispatcher_branch             = fields.Many2one('res.branch',related='asset_dispatcher.branch_id', string="Dispatch Branch")
    
    asset_dispatcher_department         = fields.Many2one('hr.department',related="asset_dispatcher.department_id",string='Department')

    asset_recipient                     = fields.Many2one('hr.employee', string="Recipient")
    asset_recipient_department          = fields.Many2one('hr.department',related="asset_recipient.department_id", string="Recipient Department")
    asset_recipient_branch              = fields.Many2one('res.branch',related="asset_recipient.branch_id", string="Recipient Branch")
    
    asset_transfer_location             = fields.Char(string="Office No")
    asset_transfer_comments             = fields.Text(string="Asset Transfer Comments")
    asset_transfer_manager_comments     = fields.Text(string="Asset Transfer Manager Comments")
    asset_transfer_authority_comments   = fields.Text(string="Asset Transfer Authority Comments")
    color                               = fields.Integer(string='Color Index', default=4)
    
    first_review_user                   = fields.Many2one('res.users')
    second_review_user                  = fields.Many2one('res.users')
    first_reviewed_date                 = fields.Date('1st Review Date')
    second_reviewed_date                = fields.Date('2nd Review Date')
    
    def _get_employee_id(self):
    # assigning the related employee of the logged in user
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id
    
    def _expand_states(self, state, domain, order):
         return [key for key, val in type(self).state.selection]
    

    @api.onchange('asset_register')
    def onchange_asset_register(self):
        for rec in self:
            if self.asset_register:
                rec.asset_model          = rec.asset_register.model
                rec.asset_number         = rec.asset_register.asset_number 
                rec.asset_serial_number  = rec.asset_register.serial  
            
    @api.onchange('state')
    def onchange_state(self):
        if self.state == 'new':
            self.color = 10
        if self.state == '1st_review':
            self.color = 1
        if self.state == '2nd_review':
            self.color = 4
        if self.state == 'completed':
            self.color = 6
        if self.state == 'end':
            self.color = 3
    
    
    def asset_transfer_proceed_button(self):
        for records in self:
            
            records.write({
               'state' : '1st_review',
                })
    @api.multi
    def asset_transfer_1st_review_approve_button(self):
        for records in self:
            email_list = []
            body = "<html>\
            <body><b>Update Asset Transfer Request</b>\
            <table width='100%' height='100%' style='border:1px solid black;'>\
            <tr style='border:1px solid black;'>\
            <td style='border:1px solid black;'> Serial Number</td><td style='border:1px solid black;'>Title</td><td style='border:1px solid black;'>Dispatcher</td><td style='border:1px solid black;'>Department</td><td style='border:1px solid black;'>Receipient Branch</td><td style='border:1px solid black;'>Comment</td></tr>"
            for record_mail in self.env['res.users'].search(['|',('branch_id','=',rec.asset_dispatcher_branch.id),('branch_id','=',rec.asset_recipient_branch.id)]):
                if record_mail.email and (record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_asset_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_asset_officer') or 
                                          record_mail.has_group('nyda_risk_management.assets_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_asset_user') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_branch_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_cfo') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_regional_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_snr_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_snr_accountant') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_transfer_authority') or 
                                          record_mail.has_group('__export__.res_groups_371') or 
                                          record_mail.has_group('__export__.res_groups_373') or 
                                          record_mail.has_group('__export__.res_groups_374')):
                    email_list.append(str(record_mail.email))
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
            body += "<tr>"
            body += "<td style='border:1px solid black;'>"+records['serial_number']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_transfer_title']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_dispatcher']['name']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_dispatcher_department']['name']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_recipient_branch']['name']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_transfer_comments']+"</td>"
            body += "</table></body></html>"
            body += "<p><strong> Has been reviewed</strong></p><br/>\
                    <p>Thank You</p>"
            if email_list and mail_server_ids.smtp_user:
                email_to = ','.join(email_list)
                template = self.env['mail.mail'].create({
                    'subject': 'Asset Transfer - ' + records['serial_number'],
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
            template.write({'email_to': email_to})
            template.send()
        
            records.write({
                'state' : '2nd_review',
                'first_review_user': self.env.user.id,
                'first_reviewed_date': date.today()
                })
    @api.multi
    def asset_transfer_1st_review_reject_button(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Asset Transfer Reject Reason',
            'res_model': 'asset.transfer.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_asset_management.asset_transfer_line_mngr_reason_form').id),
            'target': 'new',
        }
        
    @api.multi
    def asset_transfer_2nd_review_approve_button(self):
        for records in self:
            email_list = []
            body = "<html>\
            <body><b>Update Asset Transfer Request</b>\
            <table width='100%' height='100%' style='border:1px solid black;'>\
            <tr style='border:1px solid black;'>\
            <td style='border:1px solid black;'> Serial Number</td><td style='border:1px solid black;'>Title</td><td style='border:1px solid black;'>Dispatcher</td><td style='border:1px solid black;'>Department</td><td style='border:1px solid black;'>Receipient Branch</td><td style='border:1px solid black;'>Comment</td></tr>"
            for record_mail in self.env['res.users'].search(['|',('branch_id','=',rec.asset_dispatcher_branch.id),('branch_id','=',rec.asset_recipient_branch.id)]):
                if record_mail.email and (record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_asset_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_asset_officer') or 
                                          record_mail.has_group('nyda_risk_management.assets_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_asset_user') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_branch_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_cfo') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_regional_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_snr_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_snr_accountant') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_transfer_authority') or 
                                          record_mail.has_group('__export__.res_groups_371') or 
                                          record_mail.has_group('__export__.res_groups_373') or 
                                          record_mail.has_group('__export__.res_groups_374')):
                    email_list.append(str(record_mail.email))
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
            body += "<tr>"
            body += "<td style='border:1px solid black;'>"+records['serial_number']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_transfer_title']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_dispatcher']['name']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_dispatcher_department']['name']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_recipient_branch']['name']+"</td>"
            body += "<td style='border:1px solid black;'>"+records['asset_transfer_comments']+"</td>"
            body += "</table></body></html>"
            body += "<p><strong> Has been reviewed and completed</strong></p><br/>\
                    <p>Thank You</p>"
            if email_list and mail_server_ids.smtp_user:
                email_to = ','.join(email_list)
                template = self.env['mail.mail'].create({
                    'subject': 'Asset Transfer - ' + records['serial_number'],
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
            template.write({'email_to': email_to})
            template.send()
        
            records.write({
                'state' : 'completed',
                'second_review_user': self.env.user.id,
                'second_reviewed_date': date.today()
                })
            #Set account.asset to match receipt details
            records.asset_register.location = records.asset_recipient_branch.id
            records.asset_register.office_details = records.asset_transfer_location
            records.asset_register.custodian = records.asset_recipient.id
    
    @api.multi
    def asset_transfer_2nd_review_reject_button(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Asset Transfer Reject Reason',
            'res_model': 'asset.transfer.reject.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_asset_management.asset_transfer_delegated_authority_reason_form').id),
            'target': 'new',
        }
    
    @api.model
    def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['serial_number'] = self.env['ir.sequence'].next_by_code('asset.transfer')
        rec_obj = super(AssetTransfer, self).create(values)
        for rec in rec_obj:
            email_list = []
            body = "<html>\
            <body><b>New Asset Transfer Request</b>\
            <table width='100%' height='100%' style='border:1px solid black;'>\
            <tr style='border:1px solid black;'>\
            <td style='border:1px solid black;'> Serial Number</td><td style='border:1px solid black;'>Title</td><td style='border:1px solid black;'>Dispatcher</td><td style='border:1px solid black;'>Department</td><td style='border:1px solid black;'>Receipient Branch</td><td style='border:1px solid black;'>Comment</td></tr>"
            for record_mail in self.env['res.users'].search(['|',('branch_id','=',rec.asset_dispatcher_branch.id),('branch_id','=',rec.asset_recipient_branch.id)]):
                if record_mail.email and (record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_asset_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_asset_officer') or 
                                          record_mail.has_group('nyda_risk_management.assets_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_asset_user') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_branch_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_cfo') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_regional_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_snr_manager') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_snr_accountant') or 
                                          record_mail.has_group('nyda_asset_management.nyda_asset_mngmnt_transfer_authority') or 
                                          record_mail.has_group('__export__.res_groups_371') or 
                                          record_mail.has_group('__export__.res_groups_373') or 
                                          record_mail.has_group('__export__.res_groups_374')):
                    email_list.append(str(record_mail.email))
        mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
        body += "<tr>"
        body += "<td style='border:1px solid black;'>"+rec['serial_number']+"</td>"
        body += "<td style='border:1px solid black;'>"+rec['asset_transfer_title']+"</td>"
        body += "<td style='border:1px solid black;'>"+rec['asset_dispatcher']['name']+"</td>"
        body += "<td style='border:1px solid black;'>"+rec['asset_dispatcher_department']['name']+"</td>"
        body += "<td style='border:1px solid black;'>"+rec['asset_recipient_branch']['name']+"</td>"
        body += "<td style='border:1px solid black;'>"+rec['asset_transfer_comments']+"</td>"
        body += "</table></body></html>"
        body += "<p><strong> Has been created for review </strong></p><br/>\
                <p>Thank You</p>"
        if email_list and mail_server_ids.smtp_user:
            email_to = ','.join(email_list)
            template = self.env['mail.mail'].create({
                'subject': 'Asset Transfer - ' + rec['serial_number'],
                'body_html': body,
                'email_from': self.env.user.email or '',
            })
            template.write({'email_to': email_to})
            template.send()
        
        return rec_obj