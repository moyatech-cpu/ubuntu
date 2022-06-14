# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ThusanoRejectReason(models.Model):
    _name = 'thusano.reject.reason'
    _inherit = ['mail.thread']
    _rec_name = 'applicaiton_id'

    applicant_name = fields.Char(string="Applicant Name")
    applicaiton_id = fields.Many2one('thusano.fund', 'Rejection Application Ref')
    rejection_reason = fields.Text(string='Reason To Email Applicant')
    email_recipient = fields.Char(string='Email')
    
    @api.multi
    def submit_reason(self):

        if self.email_recipient:
            body = "<html>\
                        <body><p>Thusano Fund Application " + str(self.applicaiton_id.serial_number) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Application for " + str(self.applicant_name) + " with Serial Number: " + str(self.applicaiton_id.serial_number) + " has been rejected.</p>\
                                <p>with the reason stated below :.</p>\
                                <p>"+str(self.rejection_reason)+"</p><br></br>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.email_recipient
                template = self.env['mail.mail'].create({
                    'subject': 'Thusano Fund Application Outcome',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()



