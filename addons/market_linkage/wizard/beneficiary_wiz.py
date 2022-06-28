from odoo import api, fields, models
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper

class BeneficiaryWiz(models.TransientModel):
    _name = 'beneficiary.wiz'
    _description = 'Assign Beneficiary'

    def _default_oppo_provider(self):
        branch_users = self.env['register.opportunity'].browse(self._context.get('active_id'))
        groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('client_management.group_partner_service_provider').id)])
        group_users = groups.mapped("users").ids
        # ('branch_id', '=', branch_users.branch_id.id)
        return [('id', 'in', group_users)]

    def _default_beneficiary(self):
        user = self.env['register.opportunity'].browse(self._context.get('active_id'))
        groups = self.env['res.groups'].search(
            [('id', '=', self.env.ref('client_management.group_branch_beneficiary').id)])
        group_users = groups.mapped("users").ids
        return [('id', '=', group_users)]

    oppo_provider_id = fields.Many2one('res.users', string="Opportunity Provider", domain=lambda self: self._default_oppo_provider())
    beneficiary_id = fields.Many2one('res.users', string="Beneficiary", domain=lambda self: self._default_beneficiary())
    applied_on = fields.Selection([
        ('nearest_branch', 'Nearest Branch'),
        ('province', 'Province'),
        ('sector', 'Sector')], "Search On",
        default='nearest_branch', required=True)
    branch_id = fields.Many2one('res.branch', string="Nearest Branch")
    province_id = fields.Many2one('res.country.state', string="Province",
                                  domain="[('country_id.name', '=', 'South Africa')]")
    sector_id = fields.Many2one("mentor.sectors", string="Sectors")

    @api.onchange('branch_id')
    def onchange_branch_id(self):
        if self.branch_id:
            user_id = self.env['res.users'].sudo().search([('branch_id','=',self.branch_id.id)])
            user_ids = user_id.filtered(lambda user: user.has_group('client_management.group_branch_beneficiary') )
            application_ids = self.env['mkl.beneficiary'].sudo().search([])
            application_user_ids = application_ids.mapped("beneficiary_id")
            return {'domain': {'beneficiary_id': [('id', 'in', user_ids.ids),('id','in',application_user_ids.ids)]}, }

    @api.onchange('province_id')
    def onchange_province_id(self):
        if self.province_id:
            enquiry_ids = self.env['youth.enquiry'].sudo().search([('province', '=', self.province_id.id)])
            group_users = enquiry_ids.mapped("user_id")
            user_ids = group_users.filtered(lambda user: user.has_group('client_management.group_branch_beneficiary'))
            application_ids = self.env['mkl.beneficiary'].sudo().search([])
            application_user_ids = application_ids.mapped("beneficiary_id")
            return {'domain': {'beneficiary_id': [('id', 'in', user_ids.ids),('id','in',application_user_ids.ids)]}, }

    @api.onchange('sector_id')
    def onchange_sector_id(self):
        if self.sector_id:
            enquiry_ids = self.env['youth.enquiry'].sudo().search([('sector_id', '=', self.sector_id.id)])
            group_users = enquiry_ids.mapped("user_id")
            application_ids = self.env['mkl.beneficiary'].sudo().search([])
            application_user_ids = application_ids.mapped("beneficiary_id")
            user_ids = group_users.filtered(lambda user: user.has_group('client_management.group_branch_beneficiary'))
            return {'domain': {'beneficiary_id': [('id', 'in', user_ids.ids),('id','in',application_user_ids.ids)]}, }

    @api.multi
    def assign_beneficiary(self):
        user = self.env['register.opportunity'].browse(self._context.get('active_id'))
        if user.state == 'not_match':
            user.state = 'match'
        user.match_b_ids = [(4, self.beneficiary_id.id)]
        user.match_op_ids = [(4, self.oppo_provider_id.id)]
        # match_opportunity = self.env['opportunity.match'].create({
        #     'title' : user.title ,
        #     'description' : user.description ,
        #     'oppo_type' : user.oppo_type ,
        #     'branch_id' : user.branch_id.id ,
        #     'task_ids' : [(6, 0, user.task_ids.ids)] ,
        #     'attachment' : user.attachment ,
        #     'file_name' : user.file_name ,
        #     'oppo_provider_id' : self.oppo_provider_id.id ,
        #     'beneficiary_id' : self.beneficiary_id.id ,
        #     'register_oppo_id' : user.id
        # })
        # boa_assign_service_provider_to_beneficiary_email_template = self.env.ref(
        #     'market_linkage.boa_assign_service_provider_to_beneficiary_email_template')
        # boa_assign_service_provider_to_beneficiary_email_template.send_mail(match_opportunity.id, force_send=True)
        # boa_assign_beneficiary_to_service_provider_email_template = self.env.ref(
        #     'market_linkage.boa_assign_beneficiary_to_service_provider_email_template')
        # boa_assign_beneficiary_to_service_provider_email_template.send_mail(match_opportunity.id, force_send=True)
        # ts = TwilioSMSHelper()
        # if self.oppo_provider_id.phone:
        #     ts.send_enquiry_sms({
        #         'message_from': '+13613362334',
        #         'message_to': '+27' + self.oppo_provider_id.phone,
        #         'message_text': "Opportunity " + user.title + " has been match and assign Beneficiary." + self.beneficiary_id.name + " \n Regards, \n Team NYDA."
        #     })
        # if self.beneficiary_id.phone:
        #     ts.send_enquiry_sms({
        #         'message_from': '+13613362334',
        #         'message_to': '+27' + self.beneficiary_id.phone,
        #         'message_text': "You have match Opportunity Provider for Opportunity "+ user.title +".  \n Regards, \n Team NYDA."
        #     })
        return True
