from odoo import models, fields, api

class LetterSent(models.TransientModel):
    _name = 'letter.sent'
    _description = 'Opens up a wizard for sent letter'

    name = fields.Many2one('voucher.application', string="Name", readonly=True)
    bdo_name = fields.Many2one('res.users', string="BDO Assigned")
    appointment_date = fields.Date(string="Appointment Date")

    @api.multi
    def create_appointment(self):
        active_id = self.env.context.get('current_id')
        vals = {
            'name': self.name.name,
            'bdo_name': self.bdo_name.id,
            'appointment_date': self.appointment_date
        }
        if active_id:
            fetched_record = self.env['voucher.application'].browse(active_id)
            fetched_record.user_name = vals['name']
            fetched_record.bdo_name = vals['bdo_name']
            fetched_record.appointment_date = vals['appointment_date']
            fetched_record.status = 'appointment_drafted'
        mail_template_id = self.env.ref('nyda_grant_and_voucher.schedule_appointment_mail_template')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).send_mail(active_id, force_send=True)
        return True

    @api.multi
    def btn_sent_letter_req(self):
        voucher_application = self.env['sent_letter'].browse(self._context.get('active_id'))
        voucher_application.status = 'post_disbursement_done'
        voucher_application.post_disbursement = self.post_disbursement
        voucher_application.post_disbursement_name = self.post_disbursement_name
        return True

    @api.onchange('bdo_name')
    def onchange_bdo_name(self):
        users = self.env.ref("nyda_grant_and_voucher.group_grant_voucher_bdo").users.ids
        return {'domain': {'bdo_name': [('id', 'in', users)]}}
