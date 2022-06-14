# coding=utf-8
import re
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper


class YouthEnquiry(models.Model):
    """ YouthInequiry Model structure """
    _name = 'youth.enquiry'
    _rec_name = 'youth_seq'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _mail_post_access = 'read'
    _order = 'create_date DESC'

    active = fields.Boolean(default=True)
    youth_seq = fields.Char(required=True, copy=False,
                            default=lambda self: self.env['ir.sequence'].next_by_code('youth.enquiry.sequence'))
    title = fields.Selection(
        [('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Dr', 'Dr'), ('Prof', 'Prof')], string="Title")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    name = fields.Char('Name')
    surname = fields.Char('Surname')
    state = fields.Selection([('new', 'New'), ('accepted', 'Accepted for NYDA services'), ('decline', ' Decline')],
                             string='Enquiry Status', default='new')
    id_number = fields.Char('ID Number')
    cell_phone_number = fields.Char('Cell Phone Number')
    alternative_number = fields.Char('Alternative Number')
    email = fields.Char('Email')
    population_group = fields.Selection(
        [('african', 'African'), ('asian', 'Asian'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Population Group")
    product_information_type = fields.Selection(
        [('voucher', 'Voucher Programme'), ('grant', 'Grant Programme'), ('jobs-opportunities', 'Job Opportunities'),
         ('training', 'Training'), ('mentorship', 'Mentorship Programme'),
         ('market-linkage', 'Market Linkage Programme'), ('nys', 'National Youth Services'),('thusano-fund', 'Thusano Fund')],
        string="Product Information Type")
    product_info_training = fields.Selection(
        [('job_preparedness', 'Job preparedness'), ('digital_skills', 'Digital skills'),
         ('bbbee', 'BBBEE and sales pitch training'), ('lst', 'Life skills training'),
         ('technical', 'Technical training'), ('bmt', 'Business Management Training')], 'Training')
    level_of_education = fields.Selection(
        [('below_8', 'Below Grade 8'), ('below_12', 'Below Matric/Grade 12'), ('grade_12', 'Matric/Grade 12'),
         ('scc', 'Short Course Certificate'), ('hc', 'Higher Certificate'), ('diploma', 'Diploma'),
         ('degree', 'Degree/Honours/Doctorate')], 'Level of Education')
    geographic_location = fields.Selection(
        [('urban', 'Urban'), ('peri-urban', 'Peri Urban'), ('rural-area-villages', 'Rural area - Villages'),
         ('rural-area-farms', 'Rural area - Farms'), ('informa-settlement', 'Informa settlement')],
        string="Geographic Location")
    province = fields.Many2one('res.country.state', string="Province",
                               domain="[('country_id.name', '=', 'South Africa')]")
    metro_municipality = fields.Many2one('res.metro.municipality', string="Metro Municipality")
    district = fields.Many2one('res.district', string="District")
    municipality = fields.Many2one('res.municipality', string="Municipality")
    nearest_branch = fields.Many2one('res.branch', string="Nearest Branch")
    physical_address = fields.Text('Physical address')
    your_question = fields.Text('Your Question')
    team_id = fields.Many2one('enquiry.team', string="Team")
    is_pending = fields.Boolean('Pending', default=False)
    user_id = fields.Many2one('res.users', string="User")
    sector_id = fields.Many2one("mentor.sectors", string="Sectors")

    #  Fields for Activity and other kanban details
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority", )
    color = fields.Integer(string='Color Index', default=4)

    #Additional fields to accomodate legacy imported data
    legacy_age = fields.Char(string="Legacy Age")
    legacy_dob = fields.Char(string="Legacy DOB")
    legacy_branch = fields.Char(string="Legacy Branch")
    legacy_create_date = fields.Char(string="Legacy Creation Date")
    legacy_product_information_type = fields.Char(string="Legacy Product Type")
    legacy_geographic_location = fields.Char(string="Legacy Geographic Location")

    # @api.multi
    # def name_get(self):
    #     """ Overriding name_get to show Name of Beneficiary instead of Sequence """
    #     res = []
    #     for rec in self:
    #         name_str = ''
    #         name_str += rec.name + " " + rec.surname + " ( " + rec.youth_seq + " )"
    #         res.append(name_str)
    #     return res

    @api.depends('name')
    def name_get(self):
        result = []
        # if self._context.get('participant'):
        for res in self:
            result.append((res.id, res.name))
        return result

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
            read_group_res = super(YouthEnquiry, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
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
            return super(YouthEnquiry, self).read_group\
                (domain, fields, groupby, offset=offset, limit=limit, orderby=orderby)

    @api.model
    def create(self, vals):
        if self.search([('id_number', '=', vals.get('id_number'))]):
            raise UserError(_('You are already registered on our system. \nPlease login with your provided credentials.'))
        else:
            res = super(YouthEnquiry, self).create(vals)
            #LM Mahasha 2022/03/07 07:50
            res.write({
                'state': 'accepted'})
            #enquiry_email_template = self.env.ref('client_management.new_enquiry_youth_email_template')
            #enquiry_email_template.send_mail(res.id, force_send=True)
            return res

    @api.multi
    def write(self, vals):
        for rec in self:
            if vals and vals.get('state') == 'accepted':
                user = self.env['res.users'].sudo().with_context({'youth_user': True}).create({
                    'name': rec.name + " " + rec.surname,
                    'login': rec.email,
                    'email': rec.email,
                    'branch_id': rec.nearest_branch.id,
                    'phone': rec.cell_phone_number,
                    'mobile': rec.alternative_number,
                    'groups_id': [(4, self.env.ref('base.group_portal').id),
                                  (4, self.env.ref('base.group_user').id),
                                  (4, self.env.ref('__export__.res_groups_177').id), # NYS Youth Permissions
                                  (4, self.env.ref('client_management.group_branch_beneficiary').id)
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
        return super(YouthEnquiry, self).write(vals)

    @api.onchange('state')
    def onchange_state(self):
        if self.state == 'accepted':
            self.color = 10
        if self.state == 'decline':
            self.color = 1
        if self.state == 'new':
            self.color = 4

    # SA Identity validation
    @api.onchange('id_number')
    def onchange_id_number(self):
        """ South African Identity number validation. """
        if self.id_number:
            try:
                if int(self.id_number[:2]) < 50:
                    date = "20" + self.id_number[:2] + "-" + self.id_number[2:4] + "-" + self.id_number[4:6]
                    b_date = datetime.strptime(date, '%Y-%m-%d')
                    temp_date = datetime.today().strftime('%Y-%m-%d')
                    current_date = datetime.strptime(temp_date, '%Y-%m-%d')
                    difference_in_years = relativedelta(current_date, b_date).years
                    if difference_in_years < 14 or difference_in_years > 35:
                        raise UserError(_('You are not on our age group'))
                else:
                    date = "19" + self.id_number[:2] + "-" + self.id_number[2:4] + "-" + self.id_number[4:6]
                    b_date = datetime.strptime(date, '%Y-%m-%d')
                    temp_date = datetime.today().strftime('%Y-%m-%d')
                    current_date = datetime.strptime(temp_date, '%Y-%m-%d')
                    difference_in_years = relativedelta(current_date, b_date).years
                    if difference_in_years < 14 or difference_in_years > 34:
                        raise UserError(_('You are not on our age group'))
            except Exception:
                raise UserError(_('You are not on our age group'))

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
        now = dt.datetime.now()
        check_from = now - dt.timedelta(hours=72)
        server_url = self.env['ir.config_parameter'].get_param('web.base.url', default='http://erp.nyda.gov.za')
        form_view = self.env.ref('client_management.action_youth_enquiry')
        pending_mail_template = self.env.ref('client_management.pending_enquiry_youth_email_template')
        pending_enquiries = self.search(
            [('create_date', '<=', check_from.strftime(DEFAULT_SERVER_DATETIME_FORMAT)), ('state', '=', 'new')])
        if pending_enquiries:
            for pe in pending_enquiries:
                pe.sudo().write({'is_pending': True, 'color': 11, })
                server_url = server_url + "/web?#id=%s&action_id=%s&model=youth.enquiry" % (pe.id, form_view.id)
                pending_mail_template.with_context(server_url=server_url).send_mail(pe.id, force_send=True)
        else:
            pass


class MentorSectors(models.Model):
    _name = 'mentor.sectors'

    name = fields.Char('Name')
