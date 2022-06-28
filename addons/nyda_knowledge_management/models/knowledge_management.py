# coding=utf-8
from odoo import api, fields, models, _


class KnowledgeManagement(models.Model):
    """ Main model for knowledge management. """
    _name = "knowledge.management"
    _description = "This model consist of basic structure and data regarding Knowledge Management"

    name = fields.Char('Name')
    description = fields.Text('Description')
    refrence_link = fields.Char('Reference Link')
    group_ids = fields.Many2many('res.groups', string='Groups')
    date = fields.Date('Date')
    document_ids = fields.One2many('knowledge.document', 'knowledge_id', string="Documents")
    state = fields.Selection([
        ('new', 'New'),
        ('review', 'Review'),
        ('publish', 'Publish')
    ], string='Knowledge Management Status', default='new')

    @api.multi
    def review_funcation(self):
        for rec in self:
            rec.write({
                'state': 'review',
            })
        return True

    @api.multi
    def publish_funcation(self):
        for rec in self:
            rec.write({
                'state': 'publish',
            })
        return True


class KnowledgeDocument(models.Model):
    """ User can add knowledge document to the risk. """
    _name = "knowledge.document"
    _description = "Attachments for Knowledge related documents."

    knowledge_id = fields.Many2one('knowledge.management', string="Knowledge")
    document_type = fields.Selection([
        ('image', 'Image'),
        ('doc', 'Doc'),
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('url', 'URL'),
        ('ppt', 'Presentation'),
        ('article', 'Article'),
        ('other', 'Other')
    ], string='Document Type', default='other')
    video_extension = fields.Char('Extension')
    attachment_id = fields.Many2one('ir.attachment', domain=[('res_model', '=', 'knowledge.management')])
    file_name = fields.Char('File Name', related="attachment_id.name")
    description = fields.Html("Description")
