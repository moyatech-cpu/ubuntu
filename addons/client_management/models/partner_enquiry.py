# coding=utf-8
import re
import datetime

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper


class PartnerEnquiry(models.Model):
    _name = 'partner.enquiry'
    _rec_name = 'partner_seq'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _mail_post_access = 'read'
    _order = "create_date DESC"

    active = fields.Boolean(default=True)
    partner_seq = fields.Char(required=True, copy=False,
                              default=lambda self: self.env['ir.sequence'].next_by_code('partner.enquiry.sequence'))
    entity_name = fields.Char('Entity Name')
    title = fields.Selection([('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr', 'Dr'), ('Prof', 'Prof')],
                             string="Title")
    state = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted for NYDA services'),
        ('decline', ' Decline'),
    ], string='Enquiry Status', default='new')
    company_reg_number = fields.Char('Company Register Number')
    name_entity_representative = fields.Char('Name of Entity Representative')
    surname = fields.Char('Surname')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('not_specify', 'Not Specify')], string="Gender")
    cell_phone_number = fields.Char('Cell Phone Number')
    alternative_number = fields.Char('Alternative Number')
    landline = fields.Char('Landline')
    job_title = fields.Char('Job Title')
    email = fields.Char('Email')
    enquire_type = fields.Selection(
        [('partner-with-us', 'Partner with us'), ('become-service-provider', 'Become a service provider'),
         ('donate', 'Donate'), ('other', 'Other')], string="Enquire_type")
    other_enquire_type = fields.Char('Other')
    geographic_location = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Reral area - Villages'),
         ('rural-area-farms', 'Rural area - Farms'), ('informa-settlement', 'Informa settlement')],
        string="Geographic Location")
    province = fields.Many2one('res.country.state', string="Province", domain="[('country_id.name', '=', 'South Africa')]")
    metro_municipality = fields.Many2one('res.metro.municipality', string="Metro Municipality")
    district = fields.Many2one('res.district', string="District")
    municipality = fields.Many2one('res.municipality', string="Municipality")
    nearest_branch = fields.Many2one('res.branch', string="Nearest Branch")
    physical_address = fields.Text('Physical address')
    your_question = fields.Text('Your Question')
    team_id = fields.Many2one('enquiry.team', string="Team")
    is_pending = fields.Boolean('Pending', default=False)
    user_id = fields.Many2one('res.users', string="User")

    #  Fields for Activity and other kanban details
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority", )
    color = fields.Integer(string='Color Index', default=4)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """ Override read_group to always display all states. """
        if groupby and groupby[0] == "state":
            # Default result structure
            states = [('new', 'New'), ('accepted', 'Accepted for NYDA services')]
            read_group_all_states = [
                {'__context': {'group_by': groupby[1:]}, '__domain': domain + [('state', '=', state_value)],
                 'state': state_value, 'state_count': 0, } for state_value, state_name in states]
            # Get standard results
            read_group_res = super(PartnerEnquiry, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                                    orderby=orderby)
            # Update standard results with default results
            result = []
            for state_value, state_name in states:
                res = [x for x in read_group_res if x['state'] == state_value]
                if not res:
                    res = [x for x in read_group_all_states if x['state'] == state_value]
                res[0]['state'] = state_value
                result.append(res[0])
            return result
        else:
            return super(PartnerEnquiry, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                          orderby=orderby)

    @api.model
    def create(self, vals):
        if self.search([('state', '!=', 'decline'), ('email', '=', vals.get('email'))]):
            raise UserError(_('You are already registered on our system. \nPlease login with your provided credentials.'))
        else:
            res = super(PartnerEnquiry, self).create(vals)
            #ts = TwilioSMSHelper()
            #ts.send_enquiry_sms({
            #    'message_from': '+13613362334',
            #    'message_to': '+27' + vals.get('cell_phone_number'),
            #    'message_text': "Thank you, We have received your enquiry. Use your ID no. when making a follow-up. \n Regards, \n Team NYDA."
            #})
            #user_ids = self.env['res.users'].search([('branch_id', '=', res.nearest_branch.id)])
            #for user in user_ids:
            #if user.has_group('client_management.group_branch_admin'):
            # Prevent Enquiry Email - Voucher Supplier Import
            #enquiry_email_template = self.env.ref('client_management.new_enquiry_partner_email_template')
            #enquiry_email_template.send_mail(res.id, force_send=True)

            return res

    @api.multi
    def write(self, vals):
        for rec in self:
            if vals and vals.get('state') == 'accepted':
                user = self.env['res.users'].sudo().with_context({'partner_user': True}).create({
                    'name': str(rec.name_entity_representative),
                    'login': rec.email,
                    'email': rec.email,
                    'phone': rec.cell_phone_number,
                    'mobile': rec.alternative_number,
                    'branch_id':rec.nearest_branch.id,
                    'groups_id': [(4, self.env.ref('base.group_portal').id),
                                  (4, self.env.ref('base.group_user').id),
                                  (4, self.env.ref('__export__.res_groups_178').id), # NYS Partner Permissions
                                  (4, self.env.ref('client_management.group_partner_service_provider').id)
                                  ],
                    'action_id': self.env.ref('website.action_website').id or False
                })
                if user:
                    user.sudo().with_context(create_user=True).action_reset_password()
                vals['color'] = 10
                rec.user_id = user
            if vals and vals.get('state') == 'decline':
                vals['color'] = 1
            if vals and vals.get('state') == 'new':
                vals['color'] = 4
        return super(PartnerEnquiry, self).write(vals)

    @api.onchange('state')
    def onchange_state(self):
        if self.state == 'accepted':
            self.color = 10
        if self.state == 'decline':
            self.color = 1
        if self.state == 'new':
            self.color = 4

    # validation for mobile field
    @api.onchange('cell_phone_number')
    def onchange_cell_phone_number(self):
        """ Phone validation for only digits and 10 length """
        if self.cell_phone_number:
            if self.cell_phone_number.isdigit():
                if len(self.cell_phone_number) != 10:
                    raise UserError(_('Number Must be 10 digits'))
            else:
                raise UserError(_("Phone number should only contain digits."))

    # validation for mobile field
    @api.onchange('alternative_number')
    def onchange_alternative_number(self):
        """ Alternative phone validation for only digits and 10 length """
        if self.alternative_number:
            if self.alternative_number.isdigit():
                if len(self.alternative_number) != 10:
                    raise UserError(_('Number Must be 10 digits'))
            else:
                raise UserError(_("Alternative Phone number should only contain digits."))

    @api.onchange('email')
    def onchange_email(self):
        """ Email validation """
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if self.email:
            if not re.search(regex, self.email):
                raise UserError(_("Please Enter valid email address."))

    @api.multi
    def decline_req(self):
        """ Decline enquiries """
        self.state = 'decline'
        self.is_pending = False
        return

    @api.multi
    def check_acceptance(self):
        """ Cron function to check for pending enquiries. """
        now = datetime.datetime.now()
        check_from = now - datetime.timedelta(hours=72)
        server_url = self.env['ir.config_parameter'].get_param('web.base.url', default='http://localhost:8069')
        form_view = self.env.ref('client_management.action_partner_enquiry')
        pending_mail_template = self.env.ref('client_management.pending_enquiry_partner_email_template')
        pending_enquiries = self.search(
            [('create_date', '<=', check_from.strftime(DEFAULT_SERVER_DATETIME_FORMAT)), ('state', '=', 'new')])
        if pending_enquiries:
            for pe in pending_enquiries:
                pe.sudo().write({
                    'is_pending': True,
                    'color': 11,
                })
                server_url = server_url + "/web?#id=%s&action_id=%s&model=youth.enquiry" % (pe.id, form_view.id)
                pending_mail_template.with_context(server_url=server_url).send_mail(pe.id, force_send=True)
        else:
            pass