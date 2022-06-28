# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError


class MentorApplication(models.Model):
    _name = 'mentor.application'
    _rec_name = 'name'
    _description = 'Mentor Application Form'

    @api.multi
    def _compute_active_agreements(self):
        for rec in self:
            rec.active_agreements = len(self.env['mentorship.agreement'].sudo().search(
                [('mentor_id', '=', rec.id)])) or 0

    state = fields.Selection([
        ('new', 'New'),
        ('recommended', 'Recommended'),
        ('bgarg_review', 'BGARG Review'),
        ('accepted', 'Accepted'),
        ('reject', 'Rejected'),
    ], string='Application Status', default='new')
    reject_reason = fields.Text('Reason for Reject')
    title = fields.Selection(
        [('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs'), ('Dr', 'Dr'), ('Prof', 'Prof'), ('Sir', 'Sir')],
        string="Title")
    surname = fields.Char('Surname')
    name = fields.Char('Name')
    date_of_birth = fields.Date("Date of Birth")
    street_address = fields.Text('Street address')
    postal_address = fields.Text('Postal address')
    city = fields.Char('City/Village')
    municipality = fields.Many2one('res.municipality', string="Municipality")
    province = fields.Many2one('res.country.state', string="Province", domain="[('country_id.name', '=', 'South Africa')]")
    email = fields.Char('Email')
    work_phone_number = fields.Char('Work Phone Number')
    mobile_phone_number = fields.Char('Mobile Phone Number')
    preferred_contact_number = fields.Char('Preferred Contact Number')
    business_name = fields.Char('Business Name')
    qualification_obtained = fields.Char('Qualification Obtained')
    company = fields.Char('Company/Institution')
    occupation = fields.Selection(
        [('professional', 'Professional'), ('business', 'Business'), ('owner', 'Owner'), ('employee', 'Employee')],
        string="Occupation")
    no_year_experience_bussiness = fields.Float('No. of years of experience in business')
    criminal_record = fields.Char('Criminal Record')
    no_year_as_mentor = fields.Float('No. of years involved as a mentor')
    institute_name_as_mentor = fields.Char('Institutions Name – involved as a mentor')
    explain_experience = fields.Text('Explain your experience in mentoring')
    doc_refrence_1 = fields.Binary(string='Upload Refrence 1')
    doc_refrence_2 = fields.Binary(string='Upload Refrence 2')

    bussiness_skill = fields.Text('Provide details of the Business Skills that you must support the NYDA – VBMP:')
    short_profile_explaining = fields.Text(
        'Please provide a short profile explaining the mentoring that your provided to young entrepreneurs/ or would \
         like to provide to young people and the value it added to their businesses/ or will intend to have.')
    ideal_profile_of_mentee = fields.Text('Give your ideal profile of the mentee you would like to be matched or \
                                     paired with.')
    benefit_mentor = fields.Text('State what you hope to benefit from the programme as a Mentor')

    sector = fields.Many2many("mentor.sectors", string="Sectors")
    business_type = fields.Many2many("mentor.business.types", string="Business Types")
    business_type_other1 = fields.Char('Other1')
    business_type_other2 = fields.Char('Other2')
    business_type_other3 = fields.Char('Other3')
    bool_other_1 = fields.Boolean("Bool Other1")
    bool_other_2 = fields.Boolean("Bool Other1")
    bool_other_3 = fields.Boolean("Bool Other1")
    nyda_branch_1 = fields.Many2one('res.branch',string="NYDA Branch1")
    nyda_branch_2 = fields.Many2one('res.branch',string="NYDA Branch2")
    nyda_branch_3 = fields.Many2one('res.branch',string="NYDA Branch3")
    nyda_branch_4 = fields.Many2one('res.branch',string="NYDA Branch4")
    signature = fields.Binary(string='SIGNATURE')
    dateTime_application = fields.Date(string='Date', default=date.today())
    attachment_cv = fields.Binary(string='Your CV')
    user_id = fields.Many2one('res.users', string='User ID')
    branch_id = fields.Many2one('res.branch', string="Nearest Branch")
    supporting_document_ids = fields.One2many('supporting.documents', 'mentor_application_id', string="Supporting Documents")
    recommendation_char = fields.Text("Recommendation")

    # For matching with mentee
    area_support_id = fields.Many2one('areas.support', string="Supported Area")
    active_agreements = fields.Integer('Active Agreements', compute='_compute_active_agreements')
    bgarg_minutes = fields.Binary('BGARG Minutes')
    signed_agreement = fields.Binary('Mentor Signed Agreement')

    # report function
    @api.multi
    def _get_business_type_value(self):
        res = []
        vals = {}
        for rec in self.business_type:
            if rec:
                if rec.name == 'Agriculture':
                    vals.update({'Agriculture': True})
                if rec.name == 'Pottery and Glassware':
                    vals.update({'Pottery_and_Glassware': True})
                if rec.name == 'Arts and Entertainment':
                    vals.update({'Arts_and_Entertainment': True})
                if rec.name == 'Restaurant and Fast Foods' :
                    vals.update({'Restaurant_and_Fast_Foods': True})
                if rec.name == 'Building and Construction' :
                    vals.update({'Building_and_Construction': True})
                if rec.name == 'Textiles and Soft Furnishing':
                    vals.update({'Textiles_and_Soft_Furnishing': True})
                if rec.name == 'Business Services':
                    vals.update({'Business_Services': True})
                if rec.name == 'Timber and Wood':
                    vals.update({'Timber_and_Wood': True})
                if rec.name == 'Chemical and Pharmaceutical' :
                    vals.update({'Chemical_and_Pharmaceutical': True})
                if rec.name == 'Tourism and Hospitality' :
                    vals.update({'Tourism_and_Hospitality': True})

                if rec.name == 'Electrical and Electronics':
                    vals.update({'Electrical_and_Electronics': True})
                if rec.name == 'Vehicle Repairs and Parts':
                    vals.update({'Vehicle_Repairs_and_Parts': True})
                if rec.name == 'Fashion and Clothing':
                    vals.update({'Fashion_and_Clothing': True})
                if rec.name == 'Water':
                    vals.update({'Water': True})
                if rec.name == 'Food and Beverages':
                    vals.update({'Food_and_Beverages': True})
                if rec.name == 'Other1':
                    vals.update({'Other1': True})
                if rec.name == 'Information Technology':
                    vals.update({'Information_Technology': True})
                if rec.name == 'Other2':
                    vals.update({'Other2': True})
                if rec.name == 'Paper and Printing':
                    vals.update({'Paper_and_Printing': True})
                if rec.name == 'Other3':
                    vals.update({'Other3': True})
        if not vals.get('Agriculture'):
            vals.update({'Agriculture': False})
        if not vals.get('Pottery_and_Glassware'):
            vals.update({'Pottery_and_Glassware': False})
        if not vals.get('Arts_and_Entertainment'):
            vals.update({'Arts_and_Entertainment': False})
        if not vals.get('Restaurant_and_Fast_Foods'):
            vals.update({'Restaurant_and_Fast_Foods': False})
        if not vals.get('Building_and_Construction'):
            vals.update({'Building_and_Construction': False})
        if not vals.get('Textiles_and_Soft_Furnishing'):
            vals.update({'Textiles_and_Soft_Furnishing': False})
        if not vals.get('Business_Services'):
            vals.update({'Business_Services': False})
        if not vals.get('Timber_and_Wood'):
            vals.update({'Timber_and_Wood': False})
        if not vals.get('Chemical_and_Pharmaceutical'):
            vals.update({'Chemical_and_Pharmaceutical': False})
        if not vals.get('Tourism_and_Hospitality'):
            vals.update({'Tourism_and_Hospitality': False})

        if not vals.get('Electrical_and_Electronics'):
            vals.update({'Electrical_and_Electronics': False})
        if not vals.get('Vehicle_Repairs_and_Parts'):
            vals.update({'Vehicle_Repairs_and_Parts': False})
        if not vals.get('Fashion_and_Clothing'):
            vals.update({'Fashion_and_Clothing': False})
        if not vals.get('Water'):
            vals.update({'Water': False})
        if not vals.get('Food_and_Beverages'):
            vals.update({'Food_and_Beverages': False})
        if not vals.get('Other1'):
            vals.update({'Other1': False})
        if not vals.get('Information_Technology'):
            vals.update({'Information_Technology': False})
        if not vals.get('Other2'):
            vals.update({'Other2': False})
        if not vals.get('Paper_and_Printing'):
            vals.update({'Paper_and_Printing': False})
        if not vals.get('Other3'):
            vals.update({'Other3': False})
        res.append(vals)
        return res

    # report function
    @api.multi
    def _get_sector_value(self):
        res = []
        vals = {}
        for rec in self.sector:
            if rec:
                if rec.name == 'Retail / Wholesale':
                    vals.update({'Retail_Wholesale': True})
                if rec.name == 'Service':
                    vals.update({'Service': True})
                if rec.name == 'Manufacturing':
                    vals.update({'Manufacturing': True})
                if rec.name == 'Franchising' :
                    vals.update({'Franchising': True})

        if not vals.get('Retail_Wholesale'):
            vals.update({'Retail_Wholesale': False})
        if not vals.get('Service'):
            vals.update({'Service': False})
        if not vals.get('Manufacturing'):
            vals.update({'Manufacturing': False})
        if not vals.get('Franchising'):
            vals.update({'Franchising': False})
        res.append(vals)
        return res

    @api.model
    def default_get(self, fields):
        result = super(MentorApplication, self).default_get(fields)
        user = self.env['partner.enquiry'].sudo().search([('email', '=', self.env.user.login)], limit=1, order="id desc")
        result.update({
            'title': user.title,
            'company': user.entity_name,
            'name': user.name_entity_representative,
            'surname': user.surname,
            'email': user.email,
            'work_phone_number': user.cell_phone_number,
            'mobile_phone_number': user.alternative_number,
            'preferred_contact_number': user.landline,
            'business_name': user.job_title,
            'municipality': user.municipality.id,
            'province': user.province.id,
            'street_address': user.physical_address,
            'branch_id': user.nearest_branch.id,
        })
        return result


    @api.onchange('business_type')
    def onchange_business_type(self):
        temp_bool_1 = False
        temp_bool_2 = False
        temp_bool_3 = False
        for res in self.business_type:
            if res.name == 'Other1':
                temp_bool_1 = True
            if res.name == 'Other2':
                temp_bool_2 = True
            if res.name == 'Other3':
                temp_bool_3 = True
        if temp_bool_1:
            self.bool_other_1 = True
        else:
            self.bool_other_1 = False
        if temp_bool_2:
            self.bool_other_2 = True
        else:
            self.bool_other_2 = False
        if temp_bool_3:
            self.bool_other_3 = True
        else:
            self.bool_other_3 = False

    @api.onchange('email')
    def onchange_email(self):
        """ Email validation """
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if self.email:
            if not re.search(regex, self.email):
                raise UserError(_("Please Enter valid email address."))

    @api.multi
    def acceptedFuncation(self):
        for rec in self:
            mail_template_id = self.env.ref('mentorship.mentor_application_accept_mail_template')
            if mail_template_id:
                mail_template_id.with_context(mail_from=self.env.user.partner_id.email). \
                    send_mail(rec.id, force_send=True)
            rec.write({
                'state': 'accepted',
            })
        return True

    @api.multi
    def recommend_to_nyda(self):
        for rec in self:
            mail_template_id = self.env.ref('mentorship.mentor_application_recommended_mail_template')
            if mail_template_id:
                mail_template_id.with_context(mail_from=self.env.user.partner_id.email). \
                    send_mail(rec.id, force_send=True)
            rec.write({
                'state': 'recommended'
            })

    # This function will not be called as it is replaced by Wizard functionality.
    @api.multi
    def rejectedFuncation(self):
        for rec in self:
            rec.write({
                'state': 'reject',
            })
        return True

    @api.multi
    def action_suggested_mentee(self):
        """ Suggested Mentee Applications. """
        mentee_apps = self.env['mentee.application'].search([('branch_id', '=', self.branch_id.id),('areasSupport', 'in', self.area_support_id.id)])
        action = self.env.ref('mentorship.action_mentee_application').read()[0]
        if len(mentee_apps) > 1:
            action['domain'] = [('id', 'in', mentee_apps.ids)]
        elif len(mentee_apps) == 1:
            action['views'] = [(self.env.ref('mentorship.view_mentee_application_form').id, 'form')]
            action['res_id'] = mentee_apps.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_process_application(self):
        return {
            'name': "Mentorship Agreement",
            'res_model': 'mentorship.agreement',
            'type': 'ir.actions.act_window',
            'context': {'default_mentor_id': self.id, 'default_branch_id': self.branch_id.id},
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("mentorship.view_mentorship_agreement_form").id,
            'target': 'current'
        }

# class MentorSectors(models.Model):
#     _name = 'mentor.sectors'
#
#     name = fields.Char('Name')


class MentorBusinessTypes(models.Model):
    _name = 'mentor.business.types'

    name = fields.Char('Name')


class SupportingDocuments(models.Model):
    """ Supporting Documents model to allow user upload supporting documents to application. """
    _name = "supporting.documents"
    _description = "Allows User to attach supporting documents along with application."

    mentor_application_id = fields.Many2one('mentor.application', string="Mentor Application")
    supporting_doc = fields.Binary('Supporting Document')
    supporting_doc_name = fields.Char('Supporting Document')




