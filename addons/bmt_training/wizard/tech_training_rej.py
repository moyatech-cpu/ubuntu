# -*- coding: utf-8 -*-

from odoo import models, fields


class TechTrainingRejection(models.TransientModel):
    _name = 'tech.training.rejection'
    _description = "Technical Training Rejection"

    comment = fields.Text(string="Comment")

    def button_reject(self):
        self.ensure_one()
        tech_training_id = self.env['technical.training'].browse(self._context.get('active_id'))
        mail_template = self.env.ref('bmt_training.technical_training_email_template')
        if tech_training_id.state == 'submit_sv_to_manager' and mail_template:
            tech_training_id.state = 'site_visit_reject'
            tech_training_id.site_visit_reject = self.comment
            mail_template.send_mail(tech_training_id.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': tech_training_id.nyda_specialist_id.login
                                    })
        elif tech_training_id.state == 'nyda_approve' and mail_template:
            tech_training_id.state = 'nyda_review'
            tech_training_id.prc_reject = self.comment
            mail_template.send_mail(tech_training_id.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': tech_training_id.nyda_specialist_id.login
                                    })
        elif tech_training_id.state == 'nyda_review' and mail_template:
            tech_training_id.state = 'nyda_reject'
            tech_training_id.nyda_reject = self.comment
            mail_template.send_mail(tech_training_id.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': tech_training_id.nyda_specialist_id.login
                                    })
        elif tech_training_id.state == 'submit_head_office' and mail_template:
            tech_training_id.state = 'placed_at_company'
            tech_training_id.ho_rejected = self.comment
            mail_template.send_mail(tech_training_id.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': tech_training_id.ho_admin_id.login
                                    })
        elif tech_training_id.state == 'pc_submit' and mail_template:
            tech_training_id.state = 'site_visit_approve'
            tech_training_id.prc_reject = self.comment
            mail_template.send_mail(tech_training_id.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': tech_training_id.trainer_id.login
                                    })

class UploadFile(models.TransientModel):
    _name = 'tech.training.upload'
    _description = "Technical Training Upload"

    upload_file = fields.Binary(string="Upload file")
    upload_file_name = fields.Char(string="File name")
    site_visit_file_ids = fields.Many2many('ir.attachment', string="Site Visit Reports")
    is_site_visit = fields.Boolean(string="Is Site Visit")

    def upload_files(self):
        self.ensure_one()
        tech_training_id = self.env['technical.training'].browse(self._context.get('active_id'))
        if tech_training_id.state in ['conducting_site_visit', 'site_visit_reject']:
            # tech_training_id.site_visit_report = self.upload_file
            # tech_training_id.site_visit_file_name = self.upload_file_name
            tech_training_id.site_visit_file_ids = False
            tech_training_id.site_visit_file_ids = self.site_visit_file_ids.ids
            tech_training_id.state = 'submit_sv_to_manager'
        elif tech_training_id.state in ['nyda_reject']:
            tech_training_id.project_closeout_report = self.upload_file
            tech_training_id.project_closeout_file_name = self.upload_file_name
            tech_training_id.state = 'pc_submit'
        elif tech_training_id.state in ['pc_submit','pc_reject','site_visit_approve']:
            tech_training_id.project_closeout_report = self.upload_file
            tech_training_id.project_closeout_file_name = self.upload_file_name
            tech_training_id.state = 'pc_submit'
