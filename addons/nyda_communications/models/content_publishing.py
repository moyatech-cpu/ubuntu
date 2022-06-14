# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import  _
from datetime import date, datetime
from odoo.exceptions import UserError

class ContentPublishing(models.Model):

     _name = 'content.publishing'
     _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
     _mail_post_access = 'read'
     _rec_name = 'serial_number'
     
     content_title = fields.Char('Content Title')
     sm_reject_reason = fields.Text(string='Senior Manager Content Reject Reason')
     ed_reject_reason = fields.Text(string='Executive Director Reject Reason')
     state = fields.Selection([('new', 'New'), ('sm_review', ' Senior Manager Review'),
                                ('ed_review', 'Exec. Director Review'),('approved', 'Approved'),
                                ('published', 'Published')],string='Content Status', default='new',
                               group_expand='_expand_states', index=True)
     
     serial_number = fields.Char('Serial Number')
     publisher  = fields.Many2one('hr.employee', string="Publisher", default=lambda self: self.default_employee_id())
     publisher_email = fields.Char(related='publisher.work_email', string="Email")
     publisher_branch = fields.Many2one(related='publisher.branch_id', string='Branch')
     comms_specialist = fields.Many2one(related='publisher_branch.communication_agent', string='Communication Specialist')
     comms_specialist_email = fields.Char(related='comms_specialist.email')
     content_deadline = fields.Datetime(string='Deadline')
     publisher_manager = fields.Many2one(related="publisher.parent_id", string="Publisher's Manager")
     exec_director = fields.Many2one(related="publisher.parent_id.parent_id", string="Executive Director")
     publisher_manager_work_email = fields.Char(related="publisher_manager.work_email", string="Email")
     exec_director_work_email_email = fields.Char(related="exec_director.work_email", string="Email")

          
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
        if self.state == 'new':
            self.color = 10
        if self.state == 'sm_review':
            self.color = 1
        if self.state == 'ed_review':
            self.color = 4
        if self.state == 'published':
            self.color = 6
        if self.state == 'approved':
            self.color = 3
        if self.state == 'forwarded':
            self.color = 2
     
     def _expand_states(self, states, domain, order):
         return [key for key, val in type(self).state.selection]
     
     
     
             
     #def foward_to_officer(self):
         
      #  if self.comms_specialist_email:
      #      body = "<html>\
      #                  <body><p>Good Day " + str(self.comms_specialist.name) + "</p>\
      #                  <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
      #      
      #      mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
 
     #       body += "<p>Kindly note that a content publish request with Serial Number: " + str(self.serial_number) + ".</p>\
      #                          <p>has been submitted and requires your attention :.</p>\
      #                          <p>Please contact the administration if you have any query.</p>\
      #                          <p>Regards, </p>\
       #                         <p>NYDA ERP</p>"

       #     body += "</body></html>"
        #    if mail_server_ids.smtp_user:
        #        email_to = self.comms_specialist_email
        #        template = self.env['mail.mail'].create({
        #            'subject': 'Approved Content Publish Request',
        #            'body_html': body,
        #            'email_from': self.env.user.email or '',
        #        })
        #        template.write({'email_to': email_to})
        #        template.send()
        
        #for rec in self:
        #     rec.write({'state': 'forwarded'})
    
    
     def submit_button(self):
         
        if self.publisher_manager_work_email:
            body = "<html>\
                        <body><p>Good Day " + str(self.publisher_manager.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Kindly note that a content publish request with Serial Number: " + str(self.serial_number) + "</p>\
                                <p>has been submitted and requires your attention</p>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA ERP</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.publisher_manager_work_email
                template = self.env['mail.mail'].create({
                    'subject': 'Content Publish Request Created',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
        
      
        res = self.write({'state': 'sm_review'})    
        return res   
     
     def approve_ed_review_button(self):
        
        if self.publisher:
            body = "<html>\
                        <body><p>Good Day " + str(self.publisher.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Kindly note that a your content publish request with Serial Number: " + str(self.serial_number) + "</p>\
                                <p>has been approved and requires your attention</p>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA ERP</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.publisher_email
                template = self.env['mail.mail'].create({
                    'subject': 'Content Publish Request Notification',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
                
        res = self.write({'state': 'approved'})    
        return res
        
        
     def approve_sm_review_button(self):
         
         if self.exec_director:
            body = "<html>\
                        <body><p>Good Day " + str(self.exec_director.name) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Kindly note that a content publish request with Serial Number: " + str(self.serial_number) + ".</p>\
                                <p>has been submitted and requires your attention.</p>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA ERP</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.exec_director_work_email_email
                template = self.env['mail.mail'].create({
                    'subject': 'Content Publish Request Notification',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
                
         for rec in self:
             rec.write({'state': 'ed_review'})
             
     def publish_button(self):
         
         for rec in self:
             rec.write({'state': 'published'})
             
     def reject_sm_review_button(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reject Content',
            'res_model': 'sm.reject.content.publish',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_communications.SM_reject_reason_content_publish_form').id),
            'target': 'new',
            'context': {'default_email_recipient':self.publisher_email,'default_content_id': self.id}
        }
             
     def reject_ed_review_button(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reject Content',
            'res_model': 'ed.reject.content.publish',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': (self.env.ref('nyda_communications.ED_reject_reason_content_publish_form').id),
            'target': 'new',
            'context': {'default_email_recipient':self.publisher_email,'default_content_id': self.id}
        }
     
     
     @api.model
     def create(self, values):
        """ Initially, injecting sequence to application that will be unique for all applications. """
        if values:
            values['serial_number'] = self.env['ir.sequence'].next_by_code('content.publishing')
        rec_obj = super(ContentPublishing, self).create(values)
       
        return rec_obj