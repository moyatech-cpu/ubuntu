# coding=utf-8
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
from lxml import etree

_logger = logging.getLogger(__name__)

class TenderCommittee(models.Model):
    """ Model for SCM Tender Committees """
    _name       = 'nyda.scm.tender.committee'
    #_inherit    = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    state               = fields.Selection([('new', 'New'),
                                            ('manager_review', 'Manager Review'), 
                                            ('ceo_review', 'CEO Review'),
                                            ('active', 'Active'),
                                            ('completed', 'Completed')],string='Status', default='new',
                                            group_expand='_expand_states', index=True)

    committee_type      = fields.Selection([('bsc', 'Bid Specificatiion Committee'),
                                            ('bec', 'Bid Evaluation Committee'), 
                                            ('bac', 'Bid Adjudication Committee')],string='Committee Type', default='new',
                                            group_expand='_expand_states', index=True)

    name                = fields.Char("Name", required=True, translate=True)
    start_date          = fields.Datetime(string='Start Date')
    end_date            = fields.Datetime(string='End Date')
    motivation          = fields.Text(string='Motivation')
    ceo_remarks         = fields.Text(string='CEO Remarks')
    committee_members   = fields.One2many('nyda.scm.tender.committee.members','committee_id',string='Committee Members')
    color               = fields.Integer(string='Color Index', default=4)
    active              = fields.Boolean(default=True)    
    
    @api.onchange('state')
    def onchange_state(self):
        if self.state == 'new':
            self.color = 10
        if self.state == 'manager_review':
            self.color = 1
        if self.state == 'ceo_review':
            self.color = 4
        if self.state == 'active':
            self.color = 3
        if self.state == 'completed':
            self.color = 4
                            
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]    
    
    @api.multi
    def import_csv(self):
        # this will get executed when you click the import button in your form
        return {}
                                                        
    def new_completed(self):
        res = self.write({'state': 'manager_review'})    
        return res

    def manager_approval(self):
        res = self.write({'state': 'ceo_review'})    
        return res

    def manager_reject(self):
        res = self.write({'state': 'new'})    
        return res

    def ceo_approval(self):
        res = self.write({'state': 'active'})    
        return res

    def ceo_reject(self):
        res = self.write({'state': 'manager_review'})    
        return res

    def completed(self):
        res = self.write({'state': 'completed'})    
        return res
    
class TenderBSCMember(models.Model):    
    _name = 'nyda.scm.tender.committee.members'
    
    committee_id    = fields.Many2one('nyda.scm.tender.committee',string='BSC Committee')
    member          = fields.Many2one('hr.employee',string='Member')
    role            = fields.Selection([('Member', 'Member'),
                                        ('Secretary', 'Secretary'),
                                        ('Chairperson', 'Chairperson')],string='Role')    
