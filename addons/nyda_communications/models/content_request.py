# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import  _
from datetime import date, datetime
from odoo.exceptions import UserError

class ContentRequest(models.Model):

     _name = 'content.request'
     _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
     _mail_post_access = 'read'
     _rec_name = 'serial_number'
     
     
     state = fields.Selection([('new', 'New'),('pending', 'Pending'), ('in_progress', 'In Progress'),
                                ('closed', ' Closed'),('delivered', ' Delivered')],string='Request Status', default='new',
                               group_expand='_expand_states', index=True)
     
     category_id = fields.Many2one('content.categories', string='Category')
     sub_category_id = fields.Many2one('content.sub.categories', string="Sub Category")     
     serial_number = fields.Char('Serial Number')
     requester  = fields.Many2one('hr.employee', string="Requester", default=lambda self: self.default_employee_id())
     requester_email = fields.Char(related='requester.work_email', string="Email")
     requester_branch = fields.Many2one(related='requester.branch_id', string='Branch')
     comms_specialist = fields.Many2one(related='requester_branch.communication_agent', string='Communication Specialist')
     comms_specialist_email = fields.Char(related='comms_specialist.email')
     deadline = fields.Datetime(string='Deadline')
     description = fields.Html('Request Description')
     color = fields.Integer(string='Color Index', default=4)
     active = fields.Boolean(default=True)

     @api.multi
     def default_employee_id(self):
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)])
        if employee:
            return employee.id
        
           
     @api.onchange('state')
     def onchange_state(self):
        if self.state == 'pending':
            self.color = 10
        if self.state == 'in_progress':
            self.color = 1
        if self.state == 'delivered':
            self.color = 4
        if self.state == 'closed':
            self.color = 3
     
     def _expand_states(self, states, domain, order):
         return [key for key, val in type(self).state.selection]
     
     
     def proceed_button(self):
        
        if self.comms_specialist_email:
            body = "<html>\
                        <body><p>Good Day " + str(self.comms_specialist.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Kindly note that content request  with Serial Number: " + str(self.serial_number) + "</p>\
                                <p>has been submitted and requires your attention </p>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.comms_specialist_email
                template = self.env['mail.mail'].create({
                    'subject': 'Content Request Created',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
        
        res = self.write({'state': 'pending'})    
        return res
             
     def state_in_progress(self):
         
        if self.requester_email:
            body = "<html>\
                        <body><p>Good Day " + str(self.requester.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Kindly note your content request  with Serial Number: " + str(self.serial_number) + "</p>\
                                <p>has been received and is currently in progress</p>\
                                 <p>You will be notified of any updates.</p>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA ERP</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.requester_email
                template = self.env['mail.mail'].create({
                    'subject': 'Content Request Update',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
      
        res = self.write({'state': 'in_progress'})    
        return res
    
     def completed_button(self):
         
        if self.requester_email:
            body = "<html>\
                        <body><p>Good Day " + str(self.requester.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Kindly note your content request  with Serial Number: " + str(self.serial_number) + "</p>\
                                <p>has been Completed</p>\
                                 <p>Kindly proceed to the ERP and click the received button to confirm that your request has been fulfilled.</p>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA ERP</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.requester_email
                template = self.env['mail.mail'].create({
                    'subject': 'Content Request Update',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
        res = self.write({'state': 'closed'})    
        return res
    
     def state_delivered(self):
         
         if self.comms_specialist_email:
            body = "<html>\
                        <body><p>Good Day " + str(self.comms_specialist.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Kindly that the receipt of the content with Serial Number: " + str(self.serial_number) + "</p>\
                                <p>has been confirmed by the requester</p>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA ERP</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.comms_specialist_email
                template = self.env['mail.mail'].create({
                    'subject': 'Content Request Confirmation',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
            res = self.write({'state': 'delivered'})    
            return res
    
     
     @api.model
     def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['serial_number'] = self.env['ir.sequence'].next_by_code('content.request')
        rec_obj = super(ContentRequest, self).create(values)
       
        return rec_obj