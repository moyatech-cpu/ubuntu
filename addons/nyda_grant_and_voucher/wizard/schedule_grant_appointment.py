from odoo import models, fields, api

class ScheduleGrantAppointmentWizard(models.TransientModel):
    _name = 'schedule.grant.appointment'
    _description = 'Opens up a wizard for creating appointment and changes state'

    name = fields.Many2one('grant.application', string="Name", readonly=True)
    bdo_name = fields.Many2one('res.users', string="BDO Assigned")
    appointment_date = fields.Datetime(string="Appointment Date")
    appointment_location = fields.Text(string="Appointment Venue")

    @api.multi
    def create_appointment(self):
        active_id = self._context.get('active_id')
        vals = {
            'name': self.name.name,
            'bdo_name': self.bdo_name.id,
            'appointment_date': self.appointment_date,
            'appointment_location': self.appointment_location
        }
        if active_id:
            fetched_record = self.env['grant.application'].browse(active_id)
            fetched_record.user_name = vals['name']
            fetched_record.bdo_name = vals['bdo_name']
            fetched_record.appointment_date = vals['appointment_date']
            fetched_record.appointment_location = vals['appointment_location']
            fetched_record.status = 'inspected'
        # template_id = self.env.ref('nyda_grant_and_voucher.schedule_appointment_mail_template').id
        mail_template_id = self.env.ref('nyda_grant_and_voucher.grant_application_wizard_mail_template')
        mail_template_id_bdo = self.env.ref('nyda_grant_and_voucher.grant_application_wizard_mail_template_bdo')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).send_mail(active_id, force_send=True)
        if mail_template_id_bdo:
            mail_template_id_bdo.with_context(user=self.env.user).send_mail(active_id, force_send=True)
 
    @api.onchange('bdo_name')
    def onchange_bdo_name(self):
        users = self.env.ref("nyda_grant_and_voucher.group_grant_voucher_bdo").users.ids
        return {'domain': {'bdo_name': [('id', 'in', users)]}}
