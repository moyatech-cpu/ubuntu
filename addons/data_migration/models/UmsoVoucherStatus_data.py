from odoo import api, fields, models

class UmsoVoucherStatus(models.Model):
    _name = 'umso.voucher.status'

    ID = fields.Char(string='ID')
    Description = fields.Char(string='Description')
    Status = fields.Char(string='Status')
