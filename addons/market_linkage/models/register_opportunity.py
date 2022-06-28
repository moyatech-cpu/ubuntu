# coding=utf-8
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class RegisterOpportunity(models.Model):
    _name = 'register.opportunity'
    _rec_name = 'title'

    title = fields.Char('Title')
    description = fields.Text('Description')
    oppo_type = fields.Selection([('service','Service'),('product','Product')],'Opportunity Type')
    branch_id = fields.Many2one('res.branch', string="Branch", default=lambda self: self.env.user.branch_id)
    task_ids = fields.One2many('opportunity.task','opportunity_task_id',Sting="Task")
    opportunity_application_ids = fields.One2many('opportunity.application','opportunity_application_id',Sting="Assigned Beneficiaries")
    attachment = fields.Binary('Attachment')
    file_name = fields.Char('File Name')
    match_count = fields.Integer(compute='_get_match_count',string="Match")
    is_assign_button = fields.Boolean("Is Assign",default=False)
    creator_id = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    interested_bene_id = fields.Many2many('res.users', string="Interested Beneficiary")
    current_user_id = fields.Many2one('res.users', string='Current User', default=lambda self: self.env.user)
    posted_date = fields.Date(string='Posted Date', default=fields.Date.context_today)
    closing_date = fields.Date(string='Contract end date')
    company = fields.Char('Company/Organization')
    reply_tile = fields.Text('Reply Tile with Opportunity')
    sector_id = fields.Many2one("mentor.sectors", string="Sectors")
    province_id = fields.Many2one('res.country.state', string="Province",
                                  domain="[('country_id.name', '=', 'South Africa')]")
    state = fields.Selection(
        [('new', 'New'),('not_match', 'Not match'),('match', 'Match'), ('linkage_report', 'Linkage Report'), ('project_closeout', 'Project Closeout'),
         ('complated', 'Completed')], 'States', default='new',copy=False)
    match_b_ids = fields.Many2many('res.users','reg_opportunity_res_users_1', string="Match Beneficiaries")
    match_op_ids = fields.Many2many('res.users', 'reg_opportunity_res_users_2',string="Match Opportunity Providers")
    linkage_report = fields.Binary('Linkage')
    linkage_file_name = fields.Char('Linkage File Name')
    signed_contrct_report = fields.Binary('Signed Contract/Invoice/Letter of Appointment')
    signed_contrct_file_name = fields.Char('Linkage File Name')
    beneficiary_ver_report = fields.Binary('Beneficiary Verification Form')
    beneficiary_ver_file_name = fields.Char('Linkage File Name')
    jobs_ver_report = fields.Binary('Jobs Verification Form')
    jobs_ver_name = fields.Char('Linkage File Name')
    monthly_report = fields.Binary('Monthly Report')
    monthly_file_name = fields.Char('Linkage File Name')
    project_closeout_report = fields.Binary('Project Closeout')
    project_closeout_file_name = fields.Char('Project Closeout File Name')



    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """ Override read_group to always display all states. """
        if groupby and groupby[0] == "state":
            # Default result structure
            state = [('new', 'New'),('not_match', 'Not match'),('match', 'Match'), ('linkage_report', 'Linkage Report'), ('project_closeout', 'Project Closeout'),
         ('complated', 'Completed')]
            read_group_all_states = [
                {'__context': {'group_by': groupby[1:]}, '__domain': domain + [('state', '=', state_value)],
                 'state': state_value, 'state_count': 0, } for state_value, state_name in state]
            # Get standard results
            read_group_res = super(RegisterOpportunity, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                                  orderby=orderby)
            # Update standard results with default results
            result = []
            for state_value, state_name in state:
                res = [x for x in read_group_res if x['state'] == state_value]
                if not res:
                    res = [x for x in read_group_all_states if x['state'] == state_value]
                res[0]['state'] = state_value
                result.append(res[0])
            return result
        else:
            return super(RegisterOpportunity, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                        orderby=orderby)


    @api.multi
    def req_service_provider_smart_button(self):
        req_service_providers = self.env['opportunity.match'].search([('register_oppo_id', '=', self.id)])
        action = self.env.ref('market_linkage.action_opportunity_match').read()[0]
        action['domain'] = [('register_oppo_id', '=', self.id)]
        if self.match_count == 1:
            action['views'] = [(self.env.ref('market_linkage.view_opportunity_match_form').id, 'form')]
            action['res_id'] = req_service_providers[0].id
        return action

    def _get_match_count(self):
        match_count = self.env['opportunity.match'].search_count([('register_oppo_id', '=', self.id)])
        self.match_count = match_count

    @api.model
    def create(self, vals):
        res = super(RegisterOpportunity, self).create(vals)
        if vals.get('title'):
            res.is_assign_button = True
        if self.env.user.has_group('client_management.group_partner_service_provider'):
            groups = self.env['res.groups'].search(
                [('id', '=', self.env.ref('mentorship.group_bao').id)])
            for user in groups.users:
                if user.branch_id == res.branch_id:
                    opportunity_provider_mail_template = self.env.ref(
                        'market_linkage.opportunity_provider_mail_template')
                    opportunity_provider_mail_template.with_context(u=user).send_mail(res.id, force_send=True)
        return res

    @api.multi
    def write(self, vals):
        if self.env.user.has_group('client_management.group_partner_service_provider'):
            if self.creator_id.id != self.env.user.id:
                raise UserError(_('You can\'t edit others Opportunity'))
        return super(RegisterOpportunity, self).write(vals)

    @api.multi
    def opportunity_req(self):
        if not self.env.user.id in self.interested_bene_id.ids:
            self.interested_bene_id = [(4, self.env.user.id)]
            groups = self.env['res.groups'].search(
                [('id', '=', self.env.ref('mentorship.group_bao').id)])
            beneficiary_confirm_opportunity_mail_template = self.env.ref(
                'market_linkage.beneficiary_confirm_opportunity_mail_template')
            beneficiary_confirm_opportunity_mail_template.with_context(u=self.env.user).send_mail(self.id, force_send=True)
            for user in groups.users:
                if user.branch_id == self.branch_id:
                    beneficiary_apply_opportunity_mail_template = self.env.ref(
                        'market_linkage.beneficiary_apply_opportunity_mail_template')
                    beneficiary_apply_opportunity_mail_template.with_context(u=user,b=self.env.user).send_mail(self.id, force_send=True)
        return

    @api.multi
    def matched(self):
        for rec in self:
            rec.write({
                'state': 'match',
            })
        return True
    
    @api.multi
    def match_req(self):
        for rec in self:
            rec.write({
                'state': 'not_match',
            })
        return True

    @api.multi
    def complated_funcation(self):
        for rec in self:
            rec.write({
                'state': 'complated',
            })
        return True


class OpportunityTask(models.Model):
    _name = 'opportunity.task'
    _rec_name = 'name'

    name = fields.Char('Name')
    description = fields.Char('Description')
    date = fields.Date('Date')
    opportunity_task_id = fields.Many2one('register.opportunity',string='Opportunity')
    opportunity_match_id = fields.Many2one('opportunity.match',string='Opportunity Match')


class OpportunityApplication(models.Model):
    _name = 'opportunity.application'
    _rec_name = 'name'

    state = fields.Selection(
        [('new', 'New'), ('not_match', 'Not match'), ('match', 'Match')], 'States', default='new', copy=False)
    youth_enquiry_id = fields.Many2one('youth.enquiry',string='Youth Id')
    mkl_beneficiary_id = fields.Many2one('mkl.beneficiary',string='Mkl Database')
    name = fields.Char('Name',related='youth_enquiry_id.name')
    id_number = fields.Char('ID Number',related='youth_enquiry_id.id_number')
    cell_phone_number = fields.Char('Cell Phone Number',related='youth_enquiry_id.cell_phone_number')
    email = fields.Char('Email',related='youth_enquiry_id.email')
    branch_id = fields.Many2one('res.branch',related='youth_enquiry_id.nearest_branch',string='Branch')
    user_id = fields.Many2one('res.users',string='User Id')
    opportunity_application_id = fields.Many2one('register.opportunity',string='Opportunity')
    business_name = fields.Char('Business Name')
    registration_number = fields.Char('Registration Number')
    contact_person = fields.Char('Contact Person')
    contact_details = fields.Text('Contact Details')

    @api.onchange('mkl_beneficiary_id')
    def onchange_mkl_beneficiary_id(self):
        if self.mkl_beneficiary_id:
            self.business_name = self.mkl_beneficiary_id.business_name
            self.registration_number = self.mkl_beneficiary_id.registration_number
            self.contact_person = self.mkl_beneficiary_id.contact_person
            self.contact_details = self.mkl_beneficiary_id.contact_details
            self.user_id =  self.mkl_beneficiary_id.beneficiary_id.id
            enquiry_id = self.env['youth.enquiry'].sudo().search([('user_id', '=', self.mkl_beneficiary_id.beneficiary_id.id)])[0]
            self.youth_enquiry_id = enquiry_id.id

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """ Override read_group to always display all states. """
        if groupby and groupby[0] == "state":
            # Default result structure
            state = [('new', 'New'), ('not_match', 'Not match'), ('match', 'Match')]
            read_group_all_states = [
                {'__context': {'group_by': groupby[1:]}, '__domain': domain + [('state', '=', state_value)],
                 'state': state_value, 'state_count': 0, } for state_value, state_name in state]
            # Get standard results
            read_group_res = super(OpportunityApplication, self).read_group(domain, fields, groupby, offset=offset,
                                                                         limit=limit,
                                                                         orderby=orderby)
            # Update standard results with default results
            result = []
            for state_value, state_name in state:
                res = [x for x in read_group_res if x['state'] == state_value]
                if not res:
                    res = [x for x in read_group_all_states if x['state'] == state_value]
                res[0]['state'] = state_value
                result.append(res[0])
            return result
        else:
            return super(OpportunityApplication, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                               orderby=orderby)

    @api.multi
    def action_match_beneficiary(self):
        match_beneficiary_request_mail_template = self.env.ref('market_linkage.beneficiary_match_opportunity')
        match_beneficiary_request_mail_template.send_mail(self.id, force_send=True)
        if self.cell_phone_number:
            ts = TwilioSMSHelper()
            ts.send_enquiry_sms({'message_from': '+13613362334',
                                 'message_to': '+27' + self.cell_phone_number,
                                 'message_text': "Opportunity Provider "+ self.env.user.name +" is interested on your request "+self.mkl_beneficiary_id.title +". \n Regards, \n Team NYDA."})
            groups = self.env['res.groups'].search([('id', '=', self.env.ref('mentorship.group_bao').id)])
            for user in groups.users:
                if user.branch_id == self.branch_id:
                    match_boa_request_mail_template = self.env.ref('market_linkage.match_boa_request_mail_template_alt')
                    match_boa_request_mail_template.with_context(u=user).send_mail(self.id, force_send=True)

        for rec in self:
            rec.write({
                'state': 'match',
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.multi
    def action_not_match_beneficiary(self):
        for rec in self:
            rec.write({
                'state': 'not_match',
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
