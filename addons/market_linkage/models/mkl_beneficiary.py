# coding=utf-8
from odoo import api, fields, models, _
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper
from odoo.exceptions import UserError

class MklBeneficiary(models.Model):
    _name = 'mkl.beneficiary'
    _rec_name = 'title'

    title = fields.Char('Title')
    description = fields.Text('Description')
    oppo_type = fields.Selection([('service', 'Service'), ('product', 'Product')], 'Opportunity Type')
    branch_id = fields.Many2one('res.branch', string="Nearest Branch", default=lambda self: self.env.user.branch_id)
    beneficiary_id = fields.Many2one('res.users', string='Beneficiary', default=lambda self: self.env.user)
    interested_oppo_pro_id = fields.Many2many('res.users', string="Interested Opportunity Provider")
    business_name = fields.Char('Business Name')
    registration_number = fields.Char('Registration Number')
    contact_person = fields.Char('Contact Person')
    contact_details = fields.Char('Contact Details')
    x_years_of_trade = fields.Char('Years of Trade')

    @api.multi
    def match_req(self):
        if not self.env.user.id in self.interested_oppo_pro_id.ids:
            self.interested_oppo_pro_id = [(4, self.env.user.id)]
            match_beneficiary_request_mail_template = self.env.ref(
                'market_linkage.match_beneficiary_request_mail_template')
            #match_beneficiary_request_mail_template.send_mail(self.id, force_send=True)
            '''
            if self.beneficiary_id.phone:
                ts = TwilioSMSHelper()
                ts.send_enquiry_sms({
                    'message_from': '+13613362334',
                    'message_to': '+27' + self.beneficiary_id.phone,
                    'message_text': "Opportunity Provider "+ self.env.user.name +" is interested on your request "+self.title +". \n Regards, \n Team NYDA."
                })
            '''
            groups = self.env['res.groups'].search(
                [('id', '=', self.env.ref('mentorship.group_bao').id)])
            for user in groups.users:
                if user.branch_id == self.branch_id:
                    match_boa_request_mail_template = self.env.ref(
                        'market_linkage.match_boa_request_mail_template')
                    match_boa_request_mail_template.with_context(u=user).send_mail(self.id, force_send=True)
        return

    @api.model
    def create(self, vals):
        res = super(MklBeneficiary, self).create(vals)
        '''
        beneficiary_create_mkl_record_beneficiary_template = self.env.ref(
            'market_linkage.beneficiary_create_mkl_record_beneficiary_template')
        #beneficiary_create_mkl_record_beneficiary_template.send_mail(res.id, force_send=True)
        groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('mentorship.group_bao').id)])
        if res.beneficiary_id.phone:
            ts = TwilioSMSHelper()
            ts.send_enquiry_sms({
                'message_from': '+13613362334',
                'message_to': '+27' + res.beneficiary_id.phone,
                'message_text': "You have successfully saved data"+ res.title +" in MKL database. \n Regards, \n Team NYDA."
            })
        for user in groups.users:
            if user.branch_id == res.branch_id:
                beneficiary_create_mkl_record_boa_template = self.env.ref(
                    'market_linkage.beneficiary_create_mkl_record_boa_template')
                beneficiary_create_mkl_record_boa_template.with_context(u=user).send_mail(res.id, force_send=True)
        '''
        return res


    @api.multi
    def write(self,vals):
        if self.env.user.has_group('client_management.group_branch_beneficiary'):
            if self.beneficiary_id.id != self.env.user.id:
                raise UserError(_('You can\'t edit others Data'))
        return super(MklBeneficiary,self).write(vals)

    def unlink(self):
        for res in self:
            if res.env.user.has_group('client_management.group_branch_beneficiary'):
                if res.beneficiary_id.id != res.env.user.id:
                    raise UserError(_('You cannot delete others Data'))
        return super(MklBeneficiary, self).unlink()