import logging
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime,date,timedelta
from lxml import etree
from odoo.exceptions import ValidationError
from odoo.tools.misc import ustr

_logger = logging.getLogger(__name__)

class ScheduleAppointmentWizard(models.TransientModel):
    _name = 'schedule.appointment.wizard'
    _description = 'Opens up a wizard for creating appointment and changes state'

    name = fields.Many2one('voucher.application', string="Serial no.", readonly=True)
    bdo_name = fields.Many2one('res.users', string="BDO Assigned", domain=lambda self: [
        ("groups_id", "=", self.env.ref("nyda_grant_and_voucher.group_grant_voucher_bdo").id)])
    appointment_date = fields.Datetime(string="Appointment Date")
    x_location = fields.Text(string="Location")
    
    @api.constrains('appointment_date')
    @api.one
    def _check_appointment(self):
        current_date = (datetime.today()).strftime("%Y-%m-%d %H:%M:%S")
        c_date = datetime.strptime(current_date,"%Y-%m-%d %H:%M:%S").date()
        d_date = datetime.strptime(self.appointment_date,"%Y-%m-%d %H:%M:%S").date()
        
        #Dont allow current date to be greater than chosen date
        if c_date > d_date:
            raise ValidationError("Please choose a meeting date in the future.") 
        
    @api.multi
    def create_appointment(self):
        active_id = self.env.context.get('current_id')
        vals = {
            'name': self.name.name,
            'bdo_name': self.bdo_name.id,
            'appointment_date': self.appointment_date,
            'x_location': self.x_location
        }
        if active_id:
            fetched_record = self.env['voucher.application'].browse(active_id)
            fetched_record.user_name = vals['name']
            fetched_record.bdo_name = vals['bdo_name']
            fetched_record.appointment_date = vals['appointment_date']
            fetched_record.x_location = vals['x_location']
            fetched_record.status = 'appointment_drafted'
        mail_template_id = self.env.ref('nyda_grant_and_voucher.schedule_appointment_mail_template')
        if mail_template_id:
            mail_template_id.with_context(user=self.env.user).send_mail(active_id, force_send=True)
        return True

    # @api.onchange('bdo_name')
    # def onchange_bdo_name(self):
    #     users = self.env.ref("nyda_grant_and_voucher.group_grant_voucher_bdo").users.ids
    #     return {'domain': {'bdo_name': [('id', 'in', users)]}}
