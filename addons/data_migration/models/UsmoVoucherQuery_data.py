from odoo import api, fields, models

class UsmoVoucherQuery(models.Model):
    _name = 'usmo.voucher.query'

    Invoice = fields.Char(string='Invoice')
    InvoiceAmount = fields.Char(string='Invoice Amount')
    InvoiceNumber = fields.Char(string='Invoice Number')
    OriCompletedDT = fields.Char(string='Ori Completed DT')
    Product = fields.Char(string='Product')
    QueriedBy = fields.Char(string='Queried By')
    QueryDT = fields.Char(string='Query DT')
    QueryType = fields.Char(string='Query Type')
    Reason = fields.Char(string='Reason')
    RowGUID = fields.Char(string='Row GUID')
    VoucherID = fields.Char(string='Voucher ID')