# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class OpportunityProvider(models.Model):
    _name = 'opportunity.provider'
    _description = 'Opportunity Provider'

    name = fields.Char(string="Name")
    image = fields.Binary(string="Image", copy=False)
    company_no = fields.Char(string="Company No")
    tax_no = fields.Char(string="Tax No")
    vat = fields.Char(string="Vat")
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    town = fields.Char(string="Town")
    postal_code = fields.Char(string="Postal Code")
    province_id = fields.Many2one('res.country.state', string="Province")
    jobs_officer_id = fields.Many2one('res.users', string="Approved By Job Officer", copy=False)
    user_id = fields.Many2one('res.users', string="User", copy=False)
    branch_id = fields.Many2one('res.branch', string="Branch")
    state = fields.Selection([('new', 'New'), ('approved', 'Approved'), ('decline', 'Decline')], string="State",
                             default="new", copy=False)

    def dec_opp_provider(self):
        self.state = 'decline'

    def app_opp_provider(self):
        self.state = 'approved'
        if self.state== 'approved':
            user = self.env['res.users'].sudo().create({
                'name': self.name,
                'login': self.email,
                'email': self.email,
                'branch_id': self.branch_id.id,
                'phone': self.phone,
                'image': self.image,
                'mobile': self.mobile,
                'groups_id': [(4, self.env.ref('base.group_portal').id),
                              (4, self.env.ref('base.group_user').id),
                              (4, self.env.ref('job_opportunities.opportunity_provider').id)
                              ],
                # 'action_id': self.env.ref('website.action_website').id or False
            })
            if user:
                user.sudo().with_context(create_user=True).action_reset_password()
            self.user_id = user
            self.jobs_officer_id = self.env.user.id

    @api.constrains('company_no', 'phone', 'mobile','email')
    def check_number(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not self.company_no.isnumeric() or len(self.company_no) != 10:
            raise ValidationError(_('Please enter company number in digits and its length should be 10 !!'))
        # if not self.tax_no.isnumeric() or len(self.tax_no) != 10:
        #     raise ValidationError(_('Please enter tax number in digits and its length should be 10 !!'))
        # if not self.vat.isnumeric() or len(self.vat) != 10:
        #     raise ValidationError(_('Please enter vat in digits and its length should be 10 !!'))
        if not self.phone.isnumeric() or len(self.phone) != 10:
            raise ValidationError(_('Please enter phone number in digits and its length should be 10 !!'))
        if not self.mobile.isnumeric() or len(self.mobile) != 10:
            raise ValidationError(_('Please enter mobile number in digits and its length should be 10 !!'))
        if self.email:
            if not (re.search(regex, self.email)):
                raise ValidationError(_('Please enter valid email !!'))
        return True
