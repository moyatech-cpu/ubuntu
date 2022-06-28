from odoo import api, fields, models

class UmsoVoucherReassign(models.Model):
    _name = 'umso.voucher.reassign'

    ID = fields.Char('ID')
    OriClientInvoice = fields.Char(string='Ori Client Invoice')
    OriExpiryDT = fields.Char(string='Ori Expiry DT')
    OriIssueDT = fields.Char(string='Ori Issue DT')
    OriIssuedBy = fields.Char(string='Ori Issued By')
    OriIssuedNotes = fields.Char(string='Ori Issued Notes')
    OriUsedBy = fields.Char(string='Ori Used By')
    OriVoucherNumber = fields.Char(string='Ori Voucher Number')
    ReassignDT = fields.Char(string='Reassign DT')
    RowGUID = fields.Char(string='Row GUID')
    UmsoVoucher = fields.Char(string='Umso Voucher')