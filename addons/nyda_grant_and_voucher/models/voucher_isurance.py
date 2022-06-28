# coding=utf-8
from odoo import api, fields, models
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT,\
    DEFAULT_SERVER_DATETIME_FORMAT


class VoucherIsurance(models.Model):
    """ Model to register all the appications for grant. """
    _name = 'voucher.isurance'
    _rec_name = 'applicant_name'

    serial_number = fields.Char('Serial #',default='New')
    start_date = fields.Date('Start Date', default=datetime.today())
    end_date = fields.Date('End Date')
    applicant_name = fields.Char('Applicant Name')
    applicant_email = fields.Char('Applicant Email')
    gender = fields.Selection([('female', 'Female'), ('male', 'Male')], string='Gender')
    mobile = fields.Char('Cell Phone Number')

    status = fields.Selection(
        [('active', 'Active'), ('decline', 'Declined')], default='active',
        string="status")

    service_provider = fields.Many2one('partner.enquiry', string="Service Provider")
    email = fields.Char('Email', related='service_provider.email')
    voucher_applicant_id = fields.Many2one('voucher.application', 'Voucher Number')
    company_reg_number = fields.Char('Company Register Number', related='service_provider.company_reg_number')
    job_title = fields.Char('Job Title', related='service_provider.job_title')
    cell_phone_number = fields.Char('Cell Phone Number', related='service_provider.cell_phone_number')
    nearest_branch = fields.Many2one('res.branch', string="Nearest Branch", related='service_provider.nearest_branch')
    voucher_isurance_objective = fields.Text("Support Service",related='voucher_applicant_id.voucher_isurance_objective')
    voucher_value_vat = fields.Float("Voucher value excl VAT",related='voucher_applicant_id.voucher_value_vat')

    @api.model
    def create(self, vals):
        if vals:
            vals['serial_number'] = self.env['ir.sequence'].next_by_code('voucher.isurance')
        res = super(VoucherIsurance, self).create(vals)
        return res

    @api.multi
    def cron_check_voucher_issuance(self):
        """ Check if  """
        voucher_issuance_applications = self.search([('status','=','active')])
        if voucher_issuance_applications:
            for voucher_issuance_application in voucher_issuance_applications:
                if voucher_issuance_application.start_date:
                    approval_letter_send_date = datetime.strptime(str(voucher_issuance_application.start_date), DEFAULT_SERVER_DATE_FORMAT).date()
                    diff_days = (date.today() - approval_letter_send_date).days
                    if diff_days > 30:
                        voucher_issuance_application.status = 'decline'
