# coding=utf-8

import datetime
from lxml import etree
from odoo import api, fields, models, _
from odoo.addons.sms_email.models.twilio_sms import TwilioSMSHelper
from odoo.tools import ustr
from odoo.exceptions import UserError


class MentorshipAgreement(models.Model):
    """ Created an agreement form between Mentor and Mentee. """
    _name = "mentorship.agreement"
    _description = "This model helps to create agreement between Mentor and Mentee."
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Char('Name')
    state = fields.Selection([('new', 'New'), ('mentee_signed', 'Signed by Mentee') , ('mentor_signed', 'Signed by Mentor'), ('accepted', 'Accepted'), ('declined', 'Declined')],
                             string="State", default='new')
    branch_id = fields.Many2one('res.branch', string="Branch")

    # Mentor Details
    mentor_id = fields.Many2one('mentor.application', string="Mentor")
    area_support_id = fields.Many2one('areas.support', string="Supported Area", related="mentor_id.area_support_id")
    business_name = fields.Char('Business Name', related="mentor_id.business_name")
    contact_number = fields.Char('Contact Number', related="mentor_id.preferred_contact_number")
    mentor_email = fields.Char('Email', related="mentor_id.email")

    # Mentee Details
    mentee_id = fields.Many2one('mentee.application', string="Mentee")
    mentee_identity = fields.Char('Identity Number', related="mentee_id.saiDentityNumber")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('not_specify', 'Not Specify')], string="Gender",
                              related="mentee_id.gender")
    populationGroup = fields.Selection(
        [('african', 'African'), ('asian', 'Asian'), ('coloured', 'Coloured'), ('indian', 'Indian'),
         ('white', 'White')], string="Population Group", related="mentee_id.populationGroup")
    typeOfLocation = fields.Selection([('rural', 'Rural'), ('urban', 'Urban'), ('peri_urban', 'Peri-urban'),
                                       ('informal_settlement', 'Informal Settlement')], string="Type of location",
                                      related="mentee_id.typeOfLocation")
    disabledPerson = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Are you a disabled person?',
                                      related="mentee_id.disabledPerson")
    mentee_email = fields.Char('Email', related="mentee_id.email")

    # General Details
    date_of_engagement = fields.Date('Date of Engagement')
    end_date_of_engagement = fields.Date('End Date of Engagement')
    bmp_ids = fields.One2many('business.monitoring.plan', 'agreement_id', 'Business Monitoring Plan')
    mentee_sign = fields.Binary('Mentee Signature')
    mentee_sign_date = fields.Date('Date')
    mentor_sign = fields.Binary('Mentor Signature')
    mentor_sign_date = fields.Date('Date')
    declined_by = fields.Many2one('res.users', string="Declined By")
    signed_by_mentee = fields.Boolean('Signed by Mentee', default=False)
    signed_by_mentor = fields.Boolean('Signed by Mentor', default=False)
    description = fields.Text("Description")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MentorshipAgreement, self).fields_view_get(view_id=view_id,
                                                               view_type=view_type,
                                                               toolbar=toolbar,
                                                               submenu=submenu)
        dom = etree.XML(res['arch'])
        domain = []
        mentee_id = self.env['mentee.application'].sudo().search([('branch_id', '=', self.branch_id),('is_assigned', '=', False),('areasSupport', 'in', self.area_support_id)])
        if mentee_id:
            domain.append(('id', 'in', mentee_id.ids))
        else:
            domain.append(('id', 'in', self.env['mentee.application'].sudo().search(
                [('is_assigned', '=', False)]).ids))

        for node in dom.xpath("//field[@name='mentee_id']"):
            node.set('domain', ustr(domain))
        res['arch'] = etree.tostring(dom)
        return res

    @api.model
    def create(self, values):
        """ Injecting sequence to agreement record for uniqueness. """
        if len(self.search([('mentor_id', '=', values.get('mentor_id'))])) > 5:
            raise UserError(_("This mentor already has 5 mentorship agreements created."))
        else:
            res = super(MentorshipAgreement, self).create(values)
            res.name = self.env['ir.sequence'].next_by_code('mentorship.agreement') or _('New')
            mentorship_agreemant_email_template = self.env.ref(
                'mentorship.mentorship_agreement_email_template')
            mentorship_agreemant_email_template.send_mail(res.id, force_send=True)
            #ts = TwilioSMSHelper()
            #ts.send_sms({
            #    'message_to': res.mentee_id.mobile,
            #    'message_text': """Hello, \n Your application for mentorship has been accepted. \nWe have assigned you to Mentor that is best match for your requirements.\n You can login to system to check details."""
            #})
            return res

    @api.multi
    def write(self, values):
        """ Changes when state is accepted. """
        res = super(MentorshipAgreement, self).write(values)
        for rec in self:
            # if rec.signed_by_mentee:

            if rec.state == 'accepted':
                rec.mentee_id.write({
                    'is_assigned': True,
                })
            #mail_template_id = self.env.ref('mentorship.mentor_application_signed_bao_mail_template')
            #bao_user_ids = self.env['res.users'].sudo().search([('branch_id', '=', rec.branch_id.id)])
            #for user in bao_user_ids:
            #    mail_template_id.with_context(mail_to=user.email or user.partner_id.mail).\
            #        send_mail(rec.id, force_send=True)
        return res

    # This function is not going to be executed as it is replaced by Wizard functionality. It is kept in case need in future.
    @api.multi
    def action_accepted_mentee(self):
        """ Auto Populate signature and date of mantee. """
        for rec in self:
            if rec.mentor_sign:
                rec.write({
                    'state': 'accepted',
                    'date_of_engagement': datetime.date.today()
                })
            # rec.mentee_sign = rec.mentee_id.signature
            rec.mentee_sign_date = datetime.date.today()
            rec.signed_by_mentee = True

    # This function is not going to be executed as it is replaced by Wizard functionality. It is kept in case need in future.
    @api.multi
    def action_accepted_mentor(self):
        """ Auto populate signature and date of mentor. """
        for rec in self:
            if rec.mentee_sign:
                rec.write({
                    'state': 'accepted',
                    'date_of_engagement': datetime.date.today()
                })
            # rec.mentor_sign = rec.mentor_id.signature
            rec.mentor_sign_date = datetime.date.today()
            rec.signed_by_mentor = True

    # This function will not be used as it has been replaced with wizard functionality. Kept for future requirements.
    @api.multi
    def action_decline(self):
        """ Decline mentroship matching """
        for rec in self:
            rec.declined_by = self.env.user.id
            rec.state = 'declined'


class BusinessMonitoringPlan(models.Model):
    """ Model to define business monitoring plans for mentorship for both mentor and mentee. """
    _name = "business.monitoring.plan"
    _description = "Define plan for mentorship along with its timeframe"

    agreement_id = fields.Many2one('mentorship.agreement', 'Agreement')
    business_needs = fields.Char('Mentee Business Needs')
    projected_time_frame = fields.Char('Projected Time Frame (Per Session)')
