from odoo import api, fields, models
from odoo.exceptions import UserError #added

class AttendanceReport(models.TransientModel):
    _name = 'attendance.register'
    _description = 'Attendance Register'

    # linkage_report = fields.Binary('Linkage Report')
    # file_name = fields.Char('File Name')
    attendance_register_file = fields.Binary('Attendance Register')
    attendance_register_name = fields.Char('Attendance Register File Name')
    # linkage_report_ids = fields.One2many('linkage.report',Sting="Linkage Report")

    @api.multi
    def attendance_reg_req(self):  #modified lines 23,34-38
        user = self.env['voucher.application'].browse(self._context.get('active_id'))
        
        # user.linkage_file_name =  self.file_name
        # user.linkage_report = self.linkage_report
        user.x_attendance_register = self.attendance_register_file
        user.x_attendance_register_name = self.attendance_register_name
        return True

