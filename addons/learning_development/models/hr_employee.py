# hr.view_employee_form
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    surname = fields.Char(string="Surname")
    emp_number = fields.Char(string="Employment Number")
    branch_id = fields.Many2one('res.branch', string="Branch")
    previous_qualification = fields.Text(string="Previous Obtained Qualifications(studies)")
    app_identity_number = fields.Char(string="Applicant's Identity Number")
    province_id = fields.Many2one('res.country.state', string="Province")
    physical_address = fields.Text(string="Physical Address")

    @api.model
    def create(self, vals):
        if vals:
            vals['app_identity_number'] = self.env['ir.sequence'].sudo().next_by_code('application.identity.number')
        res = super(HrEmployee, self).create(vals)
        return res

    @api.onchange('user_id')
    def onchange_user(self):
        self.branch_id = self.user_id.branch_id.id

    @api.constrains('emp_number')
    @api.one
    def _check_number(self):
        emp_num = self.emp_number
        is_emp_number = emp_num.isnumeric()
        if is_emp_number == False:
            raise ValidationError(_("Employment Number must be in digits"))
        else:
            if emp_num and int(emp_num) <= 0:
                raise ValidationError(_('Employment Number should not be zero.'))
