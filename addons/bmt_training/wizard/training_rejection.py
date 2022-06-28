# -*- coding: utf-8 -*-

from odoo import models, fields


class TrainingRejection(models.TransientModel):
    _name = 'training.rejection'
    _description = "Training Rejection"

    comment = fields.Text(string="Comment")

    def me_button_reject(self):
        if self._context.get('active_model') == 'sales.pitch.training':
            training_id = self.env['sales.pitch.training'].browse(self._context.get('active_id'))
        elif self._context.get('active_model') == 'cooperative.governance.training':
            training_id = self.env['cooperative.governance.training'].browse(self._context.get('active_id'))
        elif self._context.get('active_model') == 'business.mgmt.training':
            training_id = self.env['business.mgmt.training'].browse(self._context.get('active_id'))   

        training_id.state = 'me_rejected'
        training_id.x_me_rejection = self.comment


    def button_reject(self):
        self.ensure_one()
        if self._context.get('active_model') == 'sales.pitch.training':
            training_id = self.env['sales.pitch.training'].browse(self._context.get('active_id'))
            mail_template = self.env.ref('bmt_training.sale_pitch_training_rejection_email_template')
        elif self._context.get('active_model') == 'cooperative.governance.training':
            training_id = self.env['cooperative.governance.training'].browse(self._context.get('active_id'))
            mail_template = self.env.ref('bmt_training.cooperative_governance_training_rejection_email_template')
        elif self._context.get('active_model') == 'business.mgmt.training':
            training_id = self.env['business.mgmt.training'].browse(self._context.get('active_id'))
            mail_template = self.env.ref('bmt_training.bmt_training_rejection_email_template')            
        else:
            training_id = ''
            mail_template = ''
        if training_id.state == 'coordinator_review':
            training_id.state = 'end_training'
            training_id.trainer_submitted_report = 'no'
            training_id.coordinator_approved = 'no'
            training_id.coordinator_rejected = 'yes'
            training_id.coordinator_rejection = self.comment
            if self._context.get('active_model') == 'sales.pitch.training' or self._context.get(
                    'active_model') == 'cooperative.governance.training':
                mail_template.send_mail(training_id.id, force_send=True,
                                        email_values={
                                            'email_from': self.env.user.login,
                                            'email_to': training_id.trainer_id.login
                                        })
            elif self._context.get('active_model') == 'business.mgmt.training':
                mail_template.send_mail(training_id.id, force_send=True,
                                        email_values={
                                            'email_from': self.env.user.login,
                                            'email_to': training_id.facilitator_id.login
                                        })
        elif training_id.state == 'bm_review':
            training_id.state = 'coordinator_review'
            training_id.bm_approved = 'no'
            training_id.bm_rejected = 'yes'
            training_id.branch_manager_rejection = self.comment
            training_id.coordinator_approved = False
            training_id.coordinator_rejected = False
            training_id.coordinator_rejection = False
            mail_template.send_mail(training_id.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': training_id.coordinator_review_id.login
                                    })
        elif training_id.state == 'ho_admin_review':
            training_id.state = 'bm_review'
            training_id.ho_admin_approved = 'no'
            training_id.ho_admin_rejected = 'yes'
            training_id.ho_admin_rejection = self.comment
            training_id.bm_approved = False
            training_id.bm_rejected = False
            training_id.branch_manager_rejection = False
            mail_template.send_mail(training_id.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': training_id.branch_manager_id.login
                                    })
        elif training_id.state == 'ho_manager_review':
            training_id.state = 'ho_admin_review'
            training_id.ho_manager_rejection = self.comment
            training_id.ho_admin_approved = False
            training_id.ho_admin_rejected = False
            training_id.ho_admin_rejection = False
            training_id.ho_manager_approved = 'no'
            training_id.ho_manager_rejected = 'yes'
            mail_template.send_mail(training_id.id, force_send=True,
                                    email_values={
                                        'email_from': self.env.user.login,
                                        'email_to': training_id.ho_admin_id.login
                                    })
