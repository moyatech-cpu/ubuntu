# coding=utf-8
from odoo import api, fields, models, _

class OpportunityMatch(models.Model):
    _name = 'opportunity.match'
    _rec_name = 'title'

    title = fields.Char('Title')
    description = fields.Text('Description')
    states = fields.Selection([('new','New'),('linkage_report','Linkage Report'),('project_closeout','Project Closeout'),('complated','Completed')],'States',default='new')
    oppo_type = fields.Selection([('service','Service'),('service','Product')],'Opportunity Type')
    branch_id = fields.Many2one('res.branch', string="Nearest Branch", default=lambda self: self.env.user.branch_id)
    task_ids = fields.One2many('opportunity.task','opportunity_match_id',Sting="Task")
    attachment = fields.Binary('Attachment')
    file_name = fields.Char('File Name')
    oppo_provider_id = fields.Many2one('res.users', string='Opportunity Provider')
    beneficiary_id = fields.Many2one('res.users', string="Beneficiary")
    linkage_report = fields.Binary('Linkage')
    linkage_file_name = fields.Char('Linkage File Name')
    project_closeout_report = fields.Binary('Project Closeout')
    project_closeout_file_name = fields.Char('Project Closeout File Name')
    register_oppo_id = fields.Many2one('register.opportunity', string='Opportunity Id')

    @api.multi
    def linkage_funcation(self):
        for rec in self:
            rec.write({
                'state': 'linkage_report',
            })
        return True

    @api.multi
    def project_funcation(self):
        for rec in self:
            rec.write({
                'state': 'project_closeout',
            })
        return True

    @api.multi
    def complated_funcation(self):
        for rec in self:
            rec.write({
                'state': 'complated',
            })
        return True