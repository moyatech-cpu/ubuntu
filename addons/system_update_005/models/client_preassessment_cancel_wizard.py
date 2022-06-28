from odoo import api, fields, models

class ClientPreassessmentCancelWizard(models.TransientModel):
    _name = 'client.preassessment.cancel.wizard'

    assessment_id = fields.Many2one('client.preassessment', string="Pre Assessment")
    reinstate_assessment_reason = fields.Text(string='Reason To Reinstate')
    cancel_assessment_reason = fields.Text(string='Reason To Cancel')
    rejection_reason = fields.Text(string='Reason To Email Applicant')
    
    @api.multi
    def cancel_assessment(self):
        assessment = self.env['client.preassessment'].browse(self._context.get('active_id'))
        cancel_assess = assessment.write({
            'cancel_assessment_reason': self.cancel_assessment_reason,
            'current_state': assessment.state,
            'cancel_state': 'cancelled'
        })
        
    @api.multi
    def reinstate_assessment(self):
        assessment = self.env['client.preassessment'].browse(self._context.get('active_id'))
        reinstate_assess = assessment.write({
            'reinstate_assessment_reason': self.reinstate_assessment_reason,
            'state': assessment.current_state,
            'cancel_state': False
        })
            
    
    
    @api.multi
    def submit_reason(self):

        if self.email_recipient:
            body = "<html>\
                        <body><p>Pre Assessment Application " + str(self.assessment_id.client_ref_no) + "</p>\
                        <div style='font-family: Lucida Grande, Ubuntu, Arial, Verdana, sans-serif; font-size: 12px; color: rgb(34, 34, 34); background-color: #FFF;'>"
            
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)

            body += "<p>Application for " + str(self.assessment_id.name) + " with Reference Number: " + str(self.assessment_id.client_ref_no) + " has been rejected.</p>\
                                <p>with the reason stated below :.</p>\
                                <p>"+str(self.rejection_reason)+"</p><br></br>\
                                <p>Please contact the administration if you have any query.</p>\
                                <p>Regards, </p>\
                                <p>NYDA</p>"

            body += "</body></html>"
            if mail_server_ids.smtp_user:
                email_to = self.assessment_id.email
                template = self.env['mail.mail'].create({
                    'subject': 'Pre Assessment Application Outcome',
                    'body_html': body,
                    'email_from': self.env.user.email or '',
                })
                template.write({'email_to': email_to})
                template.send()
 
        assessment_application = self.env['client.preassessment'].browse(self._context.get('active_id'))
        update_state = assessment_application.write({
            'outcome_of_the_assessment': 'rejection',
            'state': False
        })      