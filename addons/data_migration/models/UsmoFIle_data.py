from odoo import api, fields, models

class UsmoFIle(models.Model):
    _name = 'usmo.file'

    ContentType = fields.Char(string='Content Type')
    CreatedDT = fields.Char(string='Created DT')
    FileType = fields.Char(string='File Type')
    OriFileName = fields.Char(string='Ori File Name')
    RowGUID = fields.Char(string='Row GUID')
    Superseded = fields.Char(string='Superseded')
    SupersededBy = fields.Char(string='SupersededBy')
    SupersededDT = fields.Char(string='Superseded DT')
    SupersededNotes = fields.Char(string='SupersededNotes')
    Voucher = fields.Char(string='Voucher')
