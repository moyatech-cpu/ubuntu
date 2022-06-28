from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class VoucherSupportingDocuments(models.TransientModel):
    _name = 'reissue.voucher'
    _description = 'Voucher Reissuance Wizard'

    # linkage_report = fields.Binary('Linkage Report')
    # file_name = fields.Char('File Name')
    reissued_voucher_supporting_doc = fields.Binary('Voucher Issuance Supporting Document')
    reissued_voucher_supporting_doc_file_name = fields.Char('Voucher Issuance Supporting Document File Name')
    start_date = fields.Date("Re-issue Start Date",default=datetime.today())
    # linkage_report_ids = fields.One2many('linkage.report',Sting="Linkage Report")

    @api.multi
    def voucher_resupporting_documents_seq(self):  #modified lines 23,34-38
        voucher_id = self.env['voucher.application'].browse(self._context.get('active_id'))
        
        voucher_id.x_voucher_reissue_start_date = self.start_date or False
        voucher_id.x_voucher_reissue_end_date = (datetime.strptime(self.start_date, '%Y-%m-%d').date() + relativedelta(months=3)) or False
        
        voucher_id.reissued_voucher_supporting_doc = self.reissued_voucher_supporting_doc
        voucher_id.reissued_voucher_supporting_doc_file_name = self.reissued_voucher_supporting_doc_file_name
        voucher_id.status = 'work_plan'
        voucher_id.x_reissue_voucher_reason = self.x_reissue_voucher_reason
        voucher_id.x_voucher_number = self.env['ir.sequence'].next_by_code('voucher.isurance')
        print('---------\n\n\n', voucher_id.x_voucher_number)
        mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_issued_sp')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)
        return True
    

class VoucherSupportingDocuments(models.Model):
    _inherit = 'voucher.application'
    
    reissued_voucher_supporting_doc = fields.Binary('Voucher Re-Issuance (V8)')
    reissued_voucher_supporting_doc_file_name = fields.Char('Voucher Re-Issuance File Name')
    voucher_issuance_supporting_document = fields.Binary('Voucher Issuance (V8)')
    voucher_issuance_supporting_document_file_name = fields.Char('Voucher Issuance File Name')
    
    @api.multi
    def reissue_voucher(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Voucher Re-issuance',
            'res_model': 'reissue.voucher',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'current_id': self.id}
        }

class VoucherSupportingDocuments(models.TransientModel):
    _inherit = 'voucher.supporting.documents'

    @api.multi
    def voucher_supporting_documents_seq(self):  #modified lines 23,34-38
        voucher_id = self.env['voucher.application'].browse(self._context.get('active_id'))
        
        voucher_id.voucher_issuance_supporting_document = self.x_voucher_supporting_documents
        voucher_id.voucher_issuance_supporting_document_file_name = self.x_voucher_supporting_documents_file_name
        voucher_id.status = 'work_plan'
        voucher_id.x_voucher_number = self.env['ir.sequence'].next_by_code('voucher.isurance')
        print('---------\n\n\n', voucher_id.x_voucher_number)
        mail_template_id = self.env.ref('nyda_grant_and_voucher.voucher_issued_sp')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).sudo().send_mail(voucher_id.id, force_send=True)
        return True



class PdddTrainingParticipants(models.Model):
    _inherit = 'training.attendance'

    @api.multi
    def do_confirm(self):
        """ Confermation Done """
        self.state = 'confirm'
        for records in self:
            email_list = []
            body = "<html>\
                <body><b>Trainee Confirmed</b>\
                <br/>\
                <table width='100%' height='100%' style='border:1px solid black;'>\
                <tr style='border:1px solid black;'>\
                <td style='border:1px solid black;'> Title </td><td style='border:1px solid black;'>Trainer</td><td style='border:1px solid black;'>Branch</td><td style='border:1px solid black;'>Venue</td><td style='border:1px solid black;'>Start Date</td><td style='border:1px solid black;'>End Date</td></tr>"
            email_list.append(str(records['participant_id']['email']))
                
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
            body += "<tr>"
            if records['sp_training_id'] and records['sp_training_id']['trainer_id'] and records['sp_training_id']['branch_id'] and records['sp_training_id']['venue'] and records['sp_training_id']['start_date'] and records['sp_training_id']['end_date']:
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['trainer_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['branch_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['venue']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['start_date']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['end_date']+"</td>"
                body += "</table></body></html>"
            
                body += "<p><strong> The training above has been scheduled and confirmed for you to attend.</strong></p><br/>\
                    <p>Thank You</p>"
                #_logger.info(body)
                if email_list and mail_server_ids.smtp_user:
                    email_to = ','.join(email_list)
                    template = self.env['mail.mail'].create({
                        'subject': 'Training - ' + records['sp_training_id']['name'],
                        'body_html': body,
                        'email_from': self.env.user.email or '',
                    })
                template.write({'email_to': email_to})
                template.send()
            elif records['sp_training_id_2'] and records['sp_training_id_2']['trainer_id'] and records['sp_training_id_2']['branch_id'] and records['sp_training_id_2']['venue'] and records['sp_training_id_2']['start_date'] and records['sp_training_id_2']['end_date']:
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['trainer_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['branch_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['venue']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['start_date']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['end_date']+"</td>"
                body += "</table></body></html>"
            
                body += "<p><strong> The training above has been scheduled and confirmed for you to attend.</strong></p><br/>\
                    <p>Thank You</p>"
                #_logger.info(body)
                if email_list and mail_server_ids.smtp_user:
                    email_to = ','.join(email_list)
                    template = self.env['mail.mail'].create({
                        'subject': 'Training - ' + records['sp_training_id_2']['name'],
                        'body_html': body,
                        'email_from': self.env.user.email or '',
                    })
                template.write({'email_to': email_to})
                template.send()
            elif records['sp_training_id_3'] and records['sp_training_id_3']['trainer_id'] and records['sp_training_id_3']['branch_id'] and records['sp_training_id_3']['venue'] and records['sp_training_id_3']['start_date'] and records['sp_training_id_3']['end_date']:
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['trainer_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['branch_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['venue']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['start_date']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['end_date']+"</td>"
                body += "</table></body></html>"
            
                body += "<p><strong> The training above has been scheduled and confirmed for you to attend.</strong></p><br/>\
                    <p>Thank You</p>"
                #_logger.info(body)
                if email_list and mail_server_ids.smtp_user:
                    email_to = ','.join(email_list)
                    template = self.env['mail.mail'].create({
                        'subject': 'Training - ' + records['sp_training_id_3']['name'],
                        'body_html': body,
                        'email_from': self.env.user.email or '',
                    })
                template.write({'email_to': email_to})
                template.send()
        return

    @api.multi
    def do_reject(self):
        """ Reject Done """
        self.state = 'reject'
        for records in self:
            email_list = []
            body = "<html>\
                <body><b>Trainee Reject</b>\
                <br/>\
                <table width='100%' height='100%' style='border:1px solid black;'>\
                <tr style='border:1px solid black;'>\
                <td style='border:1px solid black;'> Title </td><td style='border:1px solid black;'>Trainer</td><td style='border:1px solid black;'>Branch</td><td style='border:1px solid black;'>Venue</td><td style='border:1px solid black;'>Start Date</td><td style='border:1px solid black;'>End Date</td></tr>"
            email_list.append(str(records['participant_id']['email']))
                
            mail_server_ids = self.env['ir.mail_server'].search([], limit=1)
            body += "<tr>"
            if records['sp_training_id'] and records['sp_training_id']['trainer_id'] and records['sp_training_id']['branch_id'] and records['sp_training_id']['venue'] and records['sp_training_id']['start_date'] and records['sp_training_id']['end_date']:
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['trainer_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['branch_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['venue']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['start_date']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id']['end_date']+"</td>"
                body += "</table></body></html>"
            
                body += "<p><strong> You have been reject to the training details above</strong></p><br/>\
                    <p>Thank You</p>"
                _logger.info(body)
                if email_list and mail_server_ids.smtp_user:
                    email_to = ','.join(email_list)
                    template = self.env['mail.mail'].create({
                        'subject': 'Training - ' + records['sp_training_id']['name'],
                        'body_html': body,
                        'email_from': self.env.user.email or '',
                    })
                template.write({'email_to': email_to})
                template.send()
            elif records['sp_training_id_2'] and records['sp_training_id_2']['trainer_id'] and records['sp_training_id_2']['branch_id'] and records['sp_training_id_2']['venue'] and records['sp_training_id_2']['start_date'] and records['sp_training_id_2']['end_date']:
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['trainer_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['branch_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['venue']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['start_date']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_2']['end_date']+"</td>"
                body += "</table></body></html>"
            
                body += "<p><strong> You have been reject to the training details above</strong></p><br/>\
                    <p>Thank You</p>"
                #_logger.info(body)
                if email_list and mail_server_ids.smtp_user:
                    email_to = ','.join(email_list)
                    template = self.env['mail.mail'].create({
                        'subject': 'Training - ' + records['sp_training_id_2']['name'],
                        'body_html': body,
                        'email_from': self.env.user.email or '',
                    })
                template.write({'email_to': email_to})
                template.send()
            elif records['sp_training_id_3'] and records['sp_training_id_3']['trainer_id'] and records['sp_training_id_3']['branch_id'] and records['sp_training_id_3']['venue'] and records['sp_training_id_3']['start_date'] and records['sp_training_id_3']['end_date']:
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['trainer_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['branch_id']['name']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['venue']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['start_date']+"</td>"
                body += "<td style='border:1px solid black;'>"+records['sp_training_id_3']['end_date']+"</td>"
                body += "</table></body></html>"
            
                body += "<p><strong> You have been reject to the training details above</strong></p><br/>\
                    <p>Thank You</p>"
                #_logger.info(body)
                if email_list and mail_server_ids.smtp_user:
                    email_to = ','.join(email_list)
                    template = self.env['mail.mail'].create({
                        'subject': 'Training - ' + records['sp_training_id_3']['name'],
                        'body_html': body,
                        'email_from': self.env.user.email or '',
                    })
                template.write({'email_to': email_to})
                template.send()
        return
