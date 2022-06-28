# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, SUPERUSER_ID
from datetime import datetime
from lxml import etree

class BMTCertificate(models.Model):
    _name = 'bmt.certificate'

    youth_id = fields.Many2one('youth.enquiry', string="Youth")
    bmt_id = fields.Many2one('business.mgmt.training', string="Business Management Training")
    bmt_training_certificate = fields.Binary(string="BMT Certificate")
    bmt_training_certificate_name = fields.Char(string="BMT Certificate Name")
    bmt_certi_upload_date = fields.Datetime(string="BMT Certificate Upload Date")
    certi_acceptance = fields.Boolean(string="Certificate Issuance Acceptance")
    training_type = fields.Selection(
        [('gyb', 'GYB - 3 days'), ('syb', 'SYB - 5 days'),
         ('iyb_one', 'IYB 1 - 5 days'),
         ('iyb_two', 'IYB 2 - 5 days'), ('syb_coops', 'SYB/Co-ops - 3 days')],
        string="Training course")

    @api.onchange('bmt_training_certificate')
    def onchange_certificate(self):
        if self.bmt_training_certificate:
            self.bmt_certi_upload_date = datetime.now()

class YouthEnquiry(models.Model):
    _inherit = 'youth.enquiry'

    # bmt_training_certificate = fields.Binary(string="BMT Certificate")
    # bmt_training_certificate_name = fields.Char(string="BMT Certificate Name")
    # bmt_certi_upload_date = fields.Datetime(string="BMT Certificate Upload Date")
    # certi_acceptance = fields.Boolean(string="Certificate Issuance Acceptance")
    bmt_certi_ids = fields.One2many('bmt.certificate', 'youth_id',string="BMT Certificate")
    coop_bmt_training_certificate = fields.Binary(string="Co-operative Gov. BMT Certificate")
    coop_bmt_training_certificate_name = fields.Char(string="Co-operative Gov. BMT Certificate Name")
    coop_bmt_certi_upload_date = fields.Datetime(string="Co-operative Gov. BMT Certificate Upload Date")
    coop_certi_acceptance = fields.Boolean(string="Co-operative Gov. Certificate Issuance Acceptance")
    # training_type = fields.Selection(
    #     [('gyb', 'GYB - 3 days'), ('syb', 'SYB - 5 days'),
    #      ('iyb_one', 'IYB 1 - 5 days'),
    #      ('iyb_two', 'IYB 2 - 5 days'), ('syb_coops', 'SYB/Co-ops - 3 days')],
    #     string="Training course")

    # @api.onchange('bmt_training_certificate')
    # def onchange_certificate(self):
    #     if self.bmt_training_certificate:
    #         self.bmt_certi_upload_date = datetime.now()

    @api.onchange('coop_bmt_training_certificate')
    def onchange_coop_certificate(self):
        if self.coop_bmt_training_certificate:
            self.coop_bmt_certi_upload_date = datetime.now()

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(YouthEnquiry, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type != 'search' and self.env.uid != SUPERUSER_ID:
            has_my_group = self.env.user.has_group('client_management.group_branch_beneficiary')
            if has_my_group:
                root = etree.fromstring(res['arch'])
                root.set('create', 'false')
                root.set('edit', 'false')
                res['arch'] = etree.tostring(root)
        return res
