# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SMRejectContentPublishing(models.Model):
    _name = 'sm.reject.content.publish'
    _inherit = ['mail.thread']
    _rec_name = 'content_id'

    content_id = fields.Many2one('content.publishing', string='Content Reference')
    rejection_reason = fields.Text(string='Reason To Email')
    email_recipient = fields.Char(string='Email')
    
    @api.multi
    def submit_sm_reason(self):

        if self.email_recipient:
            body = "<html>\
                        <body><p>Content Reference" + str(self.content_id.serial_number) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Content Publishing Request with Serial Number: " + str(self.content_id.serial_number) + " has been rejected.</p>\
                                <p>with the reason stated below from the Senior Manager:.</p>\
                                <p>"+str(self.rejection_reason)+"</p><br></br>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.email_recipient
                template = self.env['mail.mail'].create({
                    'subject': 'Content Publishing Review Status',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
                
                
        content_data = self.env['content.publishing'].browse(self._context.get('active_id'))
        reject_content = content_data.write({
            'sm_reject_reason': self.rejection_reason,
            'state': 'new'
        })

        return True
    

class EDRejectContentPublishing(models.Model):
    _name = 'ed.reject.content.publish'
    _inherit = ['mail.thread']
    _rec_name = 'content_id'

    content_id = fields.Many2one('content.publishing', string='Content Reference')
    rejection_reason = fields.Text(string='Reason To Email')
    email_recipient = fields.Char(string='Email')
    
    @api.multi
    def submit_ed_reason(self):

        if self.email_recipient:
            body = "<html>\
                        <body><p>Content Reference" + str(self.content_id.serial_number) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Content Publishing Request with Serial Number: " + str(self.content_id.serial_number) + " has been rejected.</p>\
                                <p>with the reason stated below from the Executive Direcor:.</p>\
                                <p>"+str(self.rejection_reason)+"</p><br></br>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.email_recipient
                template = self.env['mail.mail'].create({
                    'subject': 'Content Publishing Review Status',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
                
                
        content_data = self.env['content.publishing'].browse(self._context.get('active_id'))
        content_data.write({
            'ed_reject_reason': self.rejection_reason,
            'state': 'sm_review'
        })

        return True


