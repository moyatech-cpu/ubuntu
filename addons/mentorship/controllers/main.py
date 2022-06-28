# coding=utf-8
import json
import base64
from odoo import fields, http, tools, _
from odoo.http import request


class MentorshipRegistrationController(http.Controller):
    """ Controller to register Mentorship applications from beneficiary and service provider. """

    @http.route('/mentorship/about', type="http", auth='public', website=True, csrf=False)
    def mentorship_about(self, *args, **kwargs):
        """ Route to display description about mentorship programme. """
        return request.render('mentorship.mentorship_description', {})

    @http.route(["/mentorship/application/mentee",
                 "/mentorship/application/mentor"], type='http', auth="user", website=True, csrf=False)
    def mentorship_application(self, *args, **kwargs):
        """ Route for users to apply for mentorship programme. """
        branch_ids = request.env['res.branch'].sudo().search([])
        municipality_ids = request.env['res.municipality'].sudo().search([])
        metro_municipality_ids = request.env['res.metro.municipality'].sudo().search([])
        province_ids = request.env['res.country.state'].sudo().search([('country_id.name', '=', 'South Africa')])
        district_ids = request.env['res.district'].sudo().search([])
        business_type_ids = request.env['mentor.business.types'].sudo().search([])
        sector_ids = request.env['mentor.sectors'].sudo().search([])
        supported_area_ids = request.env['areas.support'].sudo().search([])
        legal_entity_ids = request.env['legal.entity'].sudo().search([])
        mentoring_support_ids = request.env['mentoring.support'].sudo().search([])
        user_id = request.env.user
        enquiry_id = False
        is_mentee = False
        is_mentor = False
        if request.env.user.has_group('client_management.group_branch_beneficiary')\
                or request.env.user.has_group('client_management.group_partner_service_provider'):
            if request.env.user.has_group('client_management.group_branch_beneficiary'):
                is_mentee = request.env.user.has_group('client_management.group_branch_beneficiary')
                enquiry_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', user_id.id)])
            else:
                is_mentor = request.env.user.has_group('client_management.group_partner_service_provider')
                enquiry_id = request.env['partner.enquiry'].sudo().search([('user_id', '=', user_id.id)])

            return request.render('mentorship.mentorship_application_form', {
                'is_mentee': is_mentee,
                'is_mentor': is_mentor,
                'enquiry': enquiry_id,
                'branch_id': branch_ids,
                'municipality_ids': municipality_ids,
                'metro_municipality_ids': metro_municipality_ids,
                'province_ids': province_ids,
                'district_ids': district_ids,
                'business_type_ids': business_type_ids,
                'sector_ids': sector_ids,
                'supported_area_ids': supported_area_ids,
                'legal_entity_ids': legal_entity_ids,
                'mentoring_support_ids': mentoring_support_ids,
            })
        else:
            return request.render('mentorship.not_applicable_form', {})

    @http.route('/mentorship/application/submit', type='http', auth='user', method='POST', csrf=True, website=True)
    def mentorship_application_submit(self, *args, **kwargs):
        """ Creates records from form to backend objects. """
        application_id = False
        fmt_data = json.loads(kwargs.get('formatted_data'))
        import pprint
        print (pprint.pformat(kwargs))
        user_id = request.env.user
        fmt_data['user_id'] = user_id.id
        if fmt_data.get('application_type') == 'mentor_application':
            supporting_document_ids = []
            supporting_docs = [value for key, value in kwargs.items() if 'supportingdoc' in key.lower()]
            if supporting_docs:
                for doc in supporting_docs:
                    supporting_document_ids.append((0, 0, {'supporting_doc': base64.b64encode(doc.read()),
                                                           'supporting_doc_name': doc.filename
                                                           }))
            signature = False
            if kwargs.get('signature'):
                signature = base64.b64encode(kwargs.get('signature').read())
            fmt_data['signature'] = signature
            fmt_data['attachment_cv'] = base64.b64encode(kwargs.get('attachment_cv').read())
            fmt_data['doc_refrence_1'] = base64.b64encode(kwargs.get('doc_refrence_1').read())
            fmt_data['doc_refrence_2'] = base64.b64encode(kwargs.get('doc_refrence_2').read())
            fmt_data['sector'] = [(6, 0, fmt_data.get('sector'))]
            fmt_data['business_type'] = [(6, 0, fmt_data.get('business_type'))]
            fmt_data['name'] = fmt_data.get('first_name')
            fmt_data['mobile_phone_number'] = fmt_data.get('work_phone_number')
            fmt_data['work_phone_number'] = fmt_data.get('mobile')
            fmt_data['supporting_document_ids'] = supporting_document_ids
            if fmt_data.get('business_type_other1'):
                fmt_data['bool_other_1'] = True
            if fmt_data.get('business_type_other2'):
                fmt_data['bool_other_2'] = True
            if fmt_data.get('business_type_other3'):
                fmt_data['bool_other_3'] = True
            fmt_data.pop('formatted_data')
            fmt_data.pop('first_name')
            fmt_data.pop('mobile')
            fmt_data.pop('application_type')
            fmt_data.pop('company_reg_number')
            fmt_data.pop('csrf_token')
            application_id = request.env['mentor.application'].sudo().create(fmt_data)
        if fmt_data.get('application_type') == 'mentee_application':
            attm = False
            motivation_ids = []
            skillsTraining_ids = []
            if fmt_data.get('skillsTraining_ids'):
                for training in fmt_data.get('skillsTraining_ids'):
                    skillsTraining_ids.append((0, 0, training))
            if fmt_data.get('motivation_ids'):
                for i in fmt_data.get('motivation_ids'):
                    motivation_ids.append((0, 0, i))
            if kwargs.get('attachment_id'):
                attm = kwargs.get('attachment_id')
                encoded_string = base64.b64encode(kwargs.get('attachment_id').read())
                fmt_data['attachment_id'] = encoded_string
                fmt_data['attachment_name'] = attm.filename
            signature = False
            if kwargs.get('signature'):
                signature = base64.b64encode(kwargs.get('signature').read())
            fmt_data['signature'] = signature
            fmt_data['motivation_ids'] = motivation_ids
            fmt_data['areasSupport'] = [(6, 0, fmt_data.get('areasSupport'))]
            fmt_data['sector'] = [(6, 0, fmt_data.get('sector'))]
            fmt_data['mentoringSupport'] = [(6, 0, fmt_data.get('mentoringSupport'))]
            fmt_data['slegalEntity'] = [(6, 0, fmt_data.get('slegalEntity'))]
            fmt_data['legalEntity'] = [(6, 0, fmt_data.get('legalEntity'))]
            fmt_data['skillsTraining_ids'] = skillsTraining_ids
            # fmt_data['physical_state_id'] = kwargs.get('province')
            fmt_data['firstName'] = kwargs.get('first_name')
            fmt_data['slegalEntityBool'] = True if fmt_data['slegalEntityChar'] else False
            fmt_data['legalEntityBool'] = True if fmt_data['legalEntityChar'] else False
            # fmt_data.pop('province')
            fmt_data.pop('application_type')
            fmt_data.pop('course')
            fmt_data.pop('csrf_token')
            # fmt_data.pop('district')
            fmt_data.pop('duration')
            fmt_data.pop('first_name')
            fmt_data.pop('formatted_data')
            fmt_data.pop('institutionOrganisation')
            # fmt_data.pop('institutionOrganization')
            # fmt_data.pop('metro_municipality')
            fmt_data.pop('motivationText')
            # fmt_data.pop('municipality')
            fmt_data.pop('title')
            application_id = request.env['mentee.application'].sudo().create(fmt_data)

        return request.render('mentorship.form_submitted', {})
