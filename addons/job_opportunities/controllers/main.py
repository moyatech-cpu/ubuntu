# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64


class JobDatabase(http.Controller):
    @http.route('/job_opportunities/job_opportunities/', auth='public')
    def index(self, **kw):
        pass

    @http.route('/career', type='http', auth="public", website=True)
    def career(self, **kw):
        job_users = request.env['jobs.database'].search([('user_id', '=', request.env.user.id)])
        if not job_users:
            return http.request.render('job_opportunities.jobs_registration', {})
        jobs_data = request.env['opportunities'].search([('active', '=', True)])
        degree = request.env['degree'].search([])
        return http.request.render('job_opportunities.career_form',
                                   {'jobs': jobs_data, 'degree': degree})

    @http.route('/opp_pro_reg', type='http', auth="user", website=True)
    def opp_pro_reg(self, **kw):
        sp_users = request.env['res.users'].sudo().search(
            [('groups_id', '=', request.env.ref('client_management.group_partner_service_provider').id)]).ids
        opp_provider = request.env['opportunity.provider'].sudo().search([('user_id', '=', request.env.user.id)])
        if not request.env.user.id in sp_users:
            return http.request.render('job_opportunities.sp_applicable_form', {})
        elif opp_provider:
            return http.request.render('job_opportunities.regd_opp_pro', {})
        else:
            user = request.env['res.users'].search([('id', '=', request.env.user.id)])
            branch = request.env['res.branch'].search([])
            province = request.env['res.country.state'].sudo().search([('country_id.name', '=', 'South Africa')])
            return http.request.render('job_opportunities.register_form_sp',
                                       {'user': user, 'branch': branch, 'provinces': province})

    @http.route('/opp_reg_done', type='http', auth="user", website=True, csrf=False)
    def opp_reg_done(self, **kwargs):
        print ("\n\n\n kwargs ",kwargs)
        opp_provider = request.env['opportunity.provider'].sudo().create({
            'user_id': request.env.user.id,
            'name': kwargs.get('name'),
            'company_no': kwargs.get('comp_no'),
            'phone': kwargs.get('cellphone'),
            'mobile': kwargs.get('mobile'),
            'tax_no': kwargs.get('tax_num'),
            'vat': kwargs.get('vat_num'),
            'email': kwargs.get('email'),
            'branch_id': kwargs.get('user_branch'),
            'street': kwargs.get('street'),
            'street2': kwargs.get('street2'),
            'town': kwargs.get('town'),
            'province_id': kwargs.get('province'),
            'postal_code': kwargs.get('pcode')
        })
        if opp_provider:
            return http.request.render('job_opportunities.thank_you_opp_pro',{})

    @http.route('/register_job', type='http', auth="public", website=True)
    def register_job(self, **kw):
        benificiary = request.env['youth.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])
        jobs_db = request.env['jobs.database'].sudo().search([('user_id', '=', request.env.user.id)])
        if not benificiary.id:
            return http.request.render('job_opportunities.jd_not_applicable_form', {})
        elif jobs_db:
            return http.request.render('job_opportunities.alraedy_reg_form', {})
        else:
            province = request.env['res.country.state'].sudo().search([('country_id.name', '=', 'South Africa')])
            branch = request.env['res.branch'].sudo().search([])
            mun = request.env['res.municipality'].sudo().search([])
            job = request.env['hr.job'].sudo().search([])
            district = request.env['res.district'].sudo().search([])
            # if request.env.ref('client_management.group_branch_beneficiary').id in request.env.user.groups_id.ids:
            #     benificiary = request.env['youth.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])
            # else:
            #     benificiary = request.env['youth.enquiry']
            return http.request.render('job_opportunities.register_form_jobs_db',
                                       {'provinces': province, 'branches': branch, 'municipality': mun, 'job': job,
                                        'ben': benificiary, 'district': district})

    @http.route(['/position/<model("opportunities"):post>'], type='http', auth="public", website=True)
    def position(self, post, search='', **kwargs):
        youth = request.env['youth.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])
        if not youth:
            return http.request.render('job_opportunities.jobs_registration', {})
        degree = request.env['degree'].sudo().search([])
        return http.request.render('job_opportunities.jobs_description_template',
                                   {'data': post, 'ben': request.env.user, 'degree': degree,
                                    'user': request.env.user.id, 'youth': youth})

    @http.route(['/register_application'], type='http', auth="public", website=True, csrf=False)
    def register_application(self, **kwargs):
        youth = request.env['youth.enquiry'].search([('id', '=', int(kwargs.get('yid')))])
        user = request.env['res.users'].search([('id', '=', int(kwargs.get('uid')))])
        job = request.env['opportunities'].search([('id', '=', int(kwargs.get('jid')))])
        if kwargs.get('yid'):
            application = request.env['application'].sudo().create({
                'name': youth.name + "'s Application",
                'applicant_name': youth.name,
                'contact_id': youth.id,
                'applied_user_id': user.id,
                'email': kwargs.get('email'),
                'phone': kwargs.get('cellphone'),
                'degree_id': int(kwargs.get('degree')),
                'opportunity_id': job.id,
                'official_responsible_id': job.official_responsible_id.id,
                'referred_by': kwargs.get('ref_by'),
                'resume_name': kwargs.get('resume').filename,
                'resume': base64.b64encode(kwargs.get('resume').read())
            })
            if application:
                email_template = request.env.ref('job_opportunities.job_app_email_template')
                if email_template:
                    email_template.send_mail(application.id, force_send=True)
        return http.request.render('job_opportunities.app_thanks_form')

    @http.route(["/job_reg"], type='http', auth="public", website=True, csrf=False)
    def register_job_db(self, **kwargs):
        youth_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])
        if len(kwargs) != 0:
            jobs_db = request.env['jobs.database'].sudo().create({
                'title': kwargs.get('title'),
                'name': kwargs.get('name'),
                'surname': kwargs.get('surname'),
                'id_no': kwargs.get('id_number'),
                'gender': kwargs.get('gender'),
                'disability': kwargs.get('disability'),
                'home_language': kwargs.get('select_lang_type'),
                'employment_status': kwargs.get('emp_status'),
                'location': kwargs.get('geo_loc'),
                'cell_phone': int(kwargs.get('cellphone')),
                'alt_number': int(kwargs.get('alterphone')),
                'email': kwargs.get('email'),
                'population_group': kwargs.get('select_population'),
                'highest_education': kwargs.get('level_of_education'),
                'drivers_license': kwargs.get('license_status'),
                'license_code': kwargs.get('license_code'),
                'marital_status': kwargs.get('marital_status'),
                'occupation': kwargs.get('occupation'),
                'scholar_level': kwargs.get('scholar_level'),
                'completed_job_preparedeness': kwargs.get('nyda_status'),
                'branch_id': int(kwargs.get('ben_branch')),
                'municipality_id': int(kwargs.get('municipality')),
                'district': kwargs.get('district'),
                'street': kwargs.get('street'),
                'street2': kwargs.get('street2'),
                'town': kwargs.get('town'),
                'province_id': kwargs.get('province'),
                'postal_code': int(kwargs.get('pcode')),
                'user_id': request.env.user.id,
                'youth_enquiry_id': request.env['youth.enquiry'].sudo().search(
                    [('user_id', '=', request.env.user.id)]).id,
                'is_matric_certificate': kwargs.get('matric_certi'),
                'is_teritory_higher_education': kwargs.get('ter_high_edu'),
            })
            if jobs_db:
                if kwargs.get('matric_certi') == 'yes':
                    jobs_db.matric_Result_ids.create({
                        'subject': kwargs.get('subject'),
                        'level_grade': kwargs.get('level'),
                        'symbol': kwargs.get('symbol'),
                        'jobs_database_id': jobs_db.id,
                        'certificate': base64.b64encode(kwargs.get('attachment_matric').read()),
                        'certificate_name': kwargs.get('attachment_matric').filename
                    })
                if kwargs.get('ter_high_edu') == 'yes':
                    jobs_db.teritory_higher_education_ids.create({
                        'name': kwargs.get('teritory_name'),
                        'major_subjects': kwargs.get('major_subjects'),
                        'teritory_year_completed': kwargs.get('year_completed_date'),
                        'qualification_obtained': kwargs.get('qualification'),
                        'attachment': base64.b64encode(kwargs.get('attachment').read()),
                        'attachment_name': kwargs.get('attachment').filename,
                        'jobs_database_id': jobs_db.id
                    })
                jobs_db.computer_skills_ids.create({
                    'x_qualification': kwargs.get('comp_qual'),
                    'ms_word': kwargs.get('ms_word'),
                    'excel': kwargs.get('excel'),
                    'database_system': kwargs.get('db_system'),
                    'graphic_design': kwargs.get('graphic_design'),
                    'int_mo': kwargs.get('int_mo'),
                    'accounts': kwargs.get('acc'),
                    'quali_att_name': kwargs.get('comp_qual_att').filename,
                    'quali_att': base64.b64encode(kwargs.get('comp_qual_att').read()),
                    'jobs_database_id': jobs_db.id
                })
                jobs_db.organisations_ids.create({
                    'name_of_organisation': kwargs.get('organisation_name'),
                    'start_date': kwargs.get('org_start_date'),
                    'end_date': kwargs.get('org_end_date'),
                    'position_held_id': kwargs.get('pos_held'),
                    'reason_for_leaving': kwargs.get('reason_for_leaving'),
                    'jobs_database_id': jobs_db.id
                })
                jobs_db.referees_ids.create({
                    'organisation': kwargs.get('ref_organisation_name'),
                    'job_title_id': kwargs.get('ref_job_pos'),
                    'telephone': kwargs.get('ref_telephone'),
                    'mobile': kwargs.get('ref_mobile'),
                    'jobs_database_id': jobs_db.id
                })
        return http.request.render('job_opportunities.thanks_form', {})
