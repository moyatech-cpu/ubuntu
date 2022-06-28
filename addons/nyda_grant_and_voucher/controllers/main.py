from odoo import fields, http, tools, _
from odoo.http import request
import json
import base64
import logging
from datetime import date, datetime
_logger = logging.getLogger(__name__)

class VoucherApplication(http.Controller):

    @http.route(["/voucher-application"], type='http', auth="user", website=True, csrf=False)
    def voucher_application(self, page=0, *args, **kwargs):
        if request.env.user.has_group('client_management.group_branch_beneficiary'):
            assessment_id = request.env['client.preassessment'].sudo().search([('client_id', '=', request.env.user.id)],
                                                                              limit=1, order='id desc')
            enquirys_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])
            # if not assessment_id:
            #     return request.render('nyda_grant_and_voucher.apply_for_pre_assessment', {
            #         'application_type': 'voucher'
            #     })
            existing_user = request.env['voucher.application'].search([('user_id', '=', request.env.user.id)])
            if existing_user:
                voucher_app_count = 0
                voucher_app_cancelled_decline = 0 #LM.Mahasha 29/09/2021-19:00
                voucher_id = ''
                for voucher_user in existing_user:
                    if voucher_user.status != 'decline' :
                        if voucher_user.status == 'payment_completed' or voucher_user.status == "send_payment_reciept" or voucher_user.status == 'pending_payment':
                            voucher_app_count += 1
                        else:
                            voucher_id = voucher_user
                    else:
                        voucher_id = voucher_user

                    if voucher_user.status == 'cancelled' or voucher_user.status == 'decline': #LM.Mahasha 29/09/2021-19:00
                            voucher_app_cancelled_decline += 1

                if voucher_app_count >= 4:
                    return request.render('nyda_grant_and_voucher.limit_reached_grant', {
                        'voucher_app_id': existing_user
                    })
                elif (voucher_app_cancelled_decline+voucher_app_count) != len(existing_user): #LM.Mahasha 29/09/2021-19:00
                    return request.render('nyda_grant_and_voucher.check_total_app', {
                        'voucher_app_id': voucher_id
                    })
            if enquirys_id and enquirys_id.state not in ['new', 'decline','cancelled']: #LM Mahasha 29/09/2021-16:15
                # return request.render('nyda_grant_and_voucher.not_recommended_yet', {
                #     'application_type': 'voucher'
                # })
                beneficiary_id = request.env.user.id
                branch_id = request.env.user.branch_id.id
                province_ids = request.env['res.country.state'].sudo().search(
                    [('country_id.name', '=', 'South Africa')])
                enquiry_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', beneficiary_id)])
                metro_municipality_ids = request.env['res.metro.municipality'].sudo().search([])
                municipality_ids = request.env['res.municipality'].sudo().search([])
                branch_ids = request.env['res.branch'].sudo().search([])
                business_start_reason_ids = request.env['business.start.reason'].sudo().search([])
                #L.M Mahasha correction of search model below 202
                #startup_business_sector_ids = request.env['business.sector'].sudo().search([])
                startup_business_sector_ids = request.env['mentor.sectors'].sudo().search([])
                startup_legal_entity_ids = request.env['legal.entity'].sudo().search([])
                business_start_monetary_ids = request.env['business.start.monetary'].sudo().search([])
                business_geographical_location_ids = request.env['business.geographical.location'].sudo().search([])
                business_operate_premises_ids = request.env['business.operate.premises'].sudo().search([])
                business_sector_ids = request.env['business.sector'].sudo().search([], order='name asc')
                business_development_assistance_ids = request.env['business.development.assistance'].sudo().search([])
                business_development_assistance_startup_ids = request.env[
                    'business.development.assistance'].sudo().search([])
                business_development_assistance_business_idea_ids = request.env[
                    'business.development.assistance'].sudo().search([])
                return request.render('nyda_grant_and_voucher.voucher_template', {
                    'beneficiary_id': beneficiary_id,
                    'branch_id': branch_id,
                    'enquiry': enquiry_id,
                    'province_ids': province_ids,
                    'metro_municipality_ids': metro_municipality_ids,
                    'municipality_ids': municipality_ids,
                    'branch_ids': branch_ids,
                    'assessment_id': assessment_id,
                    'business_start_reason_ids': business_start_reason_ids,
                    'startup_business_sector_ids': startup_business_sector_ids,
                    'startup_legal_entity_ids': startup_legal_entity_ids,
                    'business_start_monetary_ids': business_start_monetary_ids,
                    'business_geographical_location_ids': business_geographical_location_ids,
                    'business_operate_premises_ids': business_operate_premises_ids,
                    'business_sector_ids': business_sector_ids,
                    'business_development_assistance_ids': business_development_assistance_ids,
                    'business_development_assistance_startup_ids': business_development_assistance_startup_ids,
                    'business_development_assistance_business_idea_ids': business_development_assistance_business_idea_ids,
                })
            else:
                return request.render('mentorship.not_applicable_form', {})
        else:
            return request.render('mentorship.not_applicable_form', {})

    @http.route(["/grant-application"], type='http', auth="user", website=True, csrf=False)
    def grant_application(self, page=0, *args, **kwargs):
        if request.env.user.has_group('client_management.group_branch_beneficiary'):
            existing_user = request.env['grant.application'].search([('user_id', '=', request.env.user.id)])
            if existing_user:
                grant_app_count = 0
                grant_cancelled_rejected = 0 #LM Mahasha 29/09/2021-16:15
                grant_id = ''
                for grant_user in existing_user:
                    if grant_user.status == 'approved':
                        grant_app_count += 1
                    else:
                        grant_id = grant_user

                    if grant_user.status == 'cancelled' or grant_user.status == 'reject':  #LM Mahasha 29/09/2021-16:15
                        grant_cancelled_rejected += 1

                if grant_app_count >= 3:
                    return request.render('nyda_grant_and_voucher.limit_reached_grant', {
                        'grant_app_id': existing_user
                    })
                elif (grant_app_count+grant_cancelled_rejected) != len(existing_user): #LM Mahasha 29/09/2021-16:15
                    return request.render('nyda_grant_and_voucher.check_total_app', {
                        'grant_app_id': grant_id
                    })
            assessment_id = request.env['client.preassessment'].sudo().search([('client_id', '=', request.env.user.id)],
                                                                              limit=1, order='id desc')
            if not assessment_id:
                return request.render('nyda_grant_and_voucher.apply_for_pre_assessment', {
                    'application_type': 'grant'
                })
            if assessment_id and assessment_id.state != 'recommended':
                return request.render('nyda_grant_and_voucher.not_recommended_yet', {
                    'application_type': 'grant'
                })

            beneficiary_id = request.env.user.id
            branch_id = request.env.user.branch_id.id
            province_ids = request.env['res.country.state'].sudo().search([('country_id.name', '=', 'South Africa')])
            enquiry_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', beneficiary_id)])
            client_pre_assessment_id = request.env['client.preassessment'].sudo().search(
                [('client_id', '=', beneficiary_id)], limit=1, order='id desc')
            metro_municipality_ids = request.env['res.metro.municipality'].sudo().search([])
            municipality_ids = request.env['res.municipality'].sudo().search([])
            branch_ids = request.env['res.branch'].sudo().search([])
            business_start_reason_ids = request.env['business.start.reason'].sudo().search([])
            startup_business_sector_ids = request.env['mentor.sectors'].sudo().search([])
            startup_legal_entity_ids = request.env['legal.entity'].sudo().search([])
            return request.render('nyda_grant_and_voucher.grant_template', {
                'beneficiary_id': beneficiary_id,
                'branch_id': branch_id,
                'enquiry': enquiry_id,
                'client_pre_assessment': client_pre_assessment_id,
                'province_ids': province_ids,
                'metro_municipality_ids': metro_municipality_ids,
                'municipality_ids': municipality_ids,
                'branch_ids': branch_ids,
                'business_start_reason_ids': business_start_reason_ids,
                'startup_business_sector_ids': startup_business_sector_ids,
                'startup_legal_entity_ids': startup_legal_entity_ids,
            })
        else:
            return request.render('mentorship.not_applicable_form', {})

    @http.route(["/pre-assessment-application"], type='http', auth="user", website=True, csrf=False)
    def preassessment_application(self, page=0, *args, **kwargs):
        if request.env.user.has_group('client_management.group_branch_beneficiary'):
            enquiry_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])

            # branch = request.env['res.branch'].sudo().search([])
            if enquiry_id and enquiry_id.state not in ['new', 'decline']:
                province_ids = request.env['res.country.state'].sudo().search(
                    [('country_id.name', '=', 'South Africa')])
                metro_municipality_ids = request.env['res.metro.municipality'].sudo().search([])
                municipality_ids = request.env['res.municipality'].sudo().search([])
                branch_ids = request.env['res.branch'].sudo().search([])
                return request.render('nyda_grant_and_voucher.preassessment_template', {
                    'enquiry_id': enquiry_id,
                    'province_ids': province_ids,
                    'metro_municipality_ids': metro_municipality_ids,
                    'municipality_ids': municipality_ids,
                    'branch_ids': branch_ids,
                })
            else:
                return request.render('mentorship.not_applicable_form', {})
        else:
            return request.render('mentorship.not_applicable_form', {})

    @http.route("/pre-assessment-submit", type='http', auth="user", website=True, csrf=False)
    def pre_assessment_submit(self, **kw):
        supporting_document_ids = []
        supporting_docs = [value for key, value in kw.items() if 'supportingdoc' in key.lower()]
        if supporting_docs:
            for doc in supporting_docs:
                if doc:
                    supporting_document_ids.append((0, 0, {
                        'supporting_doc': base64.b64encode(doc.read()),
                        'supporting_doc_name': doc.filename
                    }))

        enquiry_id = request.env['youth.enquiry'].sudo().search([
            ('id', '=', int(kw.get('enquiry_id')))
        ], limit=1, order="id desc")
        assessment_id = request.env['client.preassessment'].sudo().search([('client_id', '=', request.env.user.id)],
                                                                              limit=1, order='id desc')
        if assessment_id and assessment_id.state == 'new':
                return request.render('nyda_grant_and_voucher.not_processed_yet', {
                    'application_type': 'grant'
                })
        grant_application_id = request.env['client.preassessment'].sudo().create({
            'branch_id': request.env.user.branch_id.id,
            'name': kw.get('name'),
            'surname': kw.get('surname'),
            'id_number': kw.get('sa_identity_number'),
            'home_telephone': kw.get('telephone'),
            'cell': kw.get('mobile'),
            'fax_number': kw.get('fax'),
            'email': kw.get('email'),
            'physical_address': kw.get('physical_address'),
            'postal_code': kw.get('physical_postal_code'),
            'geographic_location': kw.get('geographical_type'),
            'marital_status': kw.get('relationship'),
            'no_of_Children': kw.get('child_number'),
            'children_supporting': kw.get('child_number'),
            'board_member': kw.get('board_member'),
            'if_yes': kw.get('if_yes'),
            'highest_standard_passed': kw.get('grade'),
            'tertiary_education': kw.get('tertiary'),
            'specify_study': kw.get('fields'),
            'training_acquired': kw.get('training_acquired'),
            'currently_employed': kw.get('currently_employed'),
            'how_long': kw.get('for_how_long'),
            'technical_experience': kw.get('technical_experience'),
            # 'purpose_visit': kw.get('visit_to_nyda'),
            'benefited_from_nyda': kw.get('nyda_support_services'),
            'branch_name': kw.get('branch_name'),
            'branch_id.name': kw.get('branch_name'),
            'yes_specify': kw.get('please_specify'),
            'date_time': kw.get('date_time'),
            'assessed_to_be_requiring': kw.get('participate'),
            'no_indicate': kw.get('indicate_why'),
            'registered_business': kw.get('registered_business'),
            'reg_number': kw.get('reg_number'),
            'business_idea': kw.get('business_idea'),
            'own_business': kw.get('business_own'),
            'business_plan': kw.get('business_plan'),
            'start_a_business': kw.get('start_a_business'),
            'business_sector': kw.get('operating_business'),
            'type_of_business': kw.get('type_business'),
            'need_the_business': kw.get('seeks_business'),
            'potential_customers': kw.get('potential_customers'),
            'business_operate': kw.get('operate_customers'),
            'business_develop': kw.get('develop_customers'),
            'service_rendered': kw.get('service_be_rendered'),
            'funding': kw.get('require_business'),
            'management_skills': kw.get('start_the_business'),
            'technical_skills': kw.get('do_the_business'),
            'identified_potential_customers': kw.get('identified_potential'),
            'if_yes_ipc': kw.get('they'),
            'funds_to_invest': kw.get('invest_business'),
            'if_yes_fti': kw.get('much'),
            'any_equipment': kw.get('equipment_business'),
            'if_yes_ae': kw.get('them'),
            'start_the_business': kw.get('start_the_business'),
            'Indicate_the_business_sector': kw.get('is_operating_business'),
            'business': kw.get('business_types'),
            'seeks_to_satisfy': kw.get('business_satisfy'),
            'potential_customers_eb': kw.get('potential_customers'),
            'business_operating': kw.get('from_customers'),
            'service_business': kw.get('service_business'),
            'service_rendered_eb': kw.get('rendered_business'),
            'operation_business_eb': kw.get('operation'),
            'people_are_employed': kw.get('employed_business'),
            'annual_turnover': kw.get('turnover_business'),
            'business_you_want_to_start': kw.get('knowledge_business'),
            'training_you_received': kw.get('training_you_received'),
            # 'development_training': kw.get('attend_entrepreneurship'),
            'executive_summary': kw.get('executive_summary'),
            'company_overview': kw.get('company_overview'),
            'market_opportunity': kw.get('market_opportunity'),
            'market_opportunitys': kw.get('market_opportunitys'),
            'marketing_strategy': kw.get('marketing_strategy'),
            'competitive_advantage': kw.get('competitive_advantage'),
            'products_or_services': kw.get('products_or_services'),
            'management': kw.get('management'),
            'management_capability': kw.get('management_capability'),
            'financials': kw.get('financials'),
            'financial_understanding': kw.get('financial_understanding'),
            'operations': kw.get('operations'),
            'plan_composition': kw.get('plan_composition'),
            'provide_feedback': kw.get('feedback'),
            'strengths': kw.get('strengths'),
            'weaknesses': kw.get('weaknesses'),
            'suggestions': kw.get('suggestions'),
            'recommendation': kw.get('recommendation'),
            'client_id': enquiry_id.user_id.id,
            'supporting_document_ids': supporting_document_ids,
            'business_plan_document_name': kw.get('business_plan_document').filename if kw.get(
                'business_plan_document') else False,
            'business_plan_document': base64.b64encode(kw.get('business_plan_document').read()) if kw.get(
                'business_plan_document') else False,
        })

        return request.render("nyda_grant_and_voucher.pre_assessment_submitted")

    @http.route("/thank_you", type='http', website=True, csrf=False)
    def thank_you(self, **kw):
#        return request.render("nyda_grant_and_voucher.grant_form_submitted", {'grant_application_id': ''})
        return request.render("nyda_grant_and_voucher.voucher_form_submitted",
                              {'voucher_application_id': ''})

    @http.route("/grant-application-submit", type='http', auth="user", website=True, csrf=False)
    def grant_application_submit(self, **kw):
        # existing_business and entrepreneurial_training radio button
        if 'existing_business' not in kw.keys():
            existing_business_status = False
        else:
            existing_business_status = eval(kw.get('existing_business'))

        if 'entrepreneurial_training' not in kw.keys():
            entrepreneurial_training_status = False
        else:
            entrepreneurial_training_status = eval(kw.get('entrepreneurial_training'))

        # supporting documents
        # if kw.get('identity_document_2'):
        #     identity_document_2_name = kw.get('identity_document_2').filename
        #     kw['identity_document_2'] = base64.b64encode(kw.get('identity_document_2').read())
        # else:
        #     identity_document_2_name = False
        # if kw.get('identity_document_3'):
        #     identity_document_3_name = kw.get('identity_document_3').filename
        #     kw['identity_document_3'] = base64.b64encode(kw.get('identity_document_3').read())
        # else:
        #     identity_document_3_name = False
        # if kw.get('proof_of_residence'):
        #     proof_of_residence_name = kw.get('proof_of_residence').filename
        #     kw['proof_of_residence'] = base64.b64encode(kw.get('proof_of_residence').read())
        # else:
        #     proof_of_residence_name = False

        #UPDATE START L.M Mahasha 08/10 22:28
        if kw.get('proof_of_residence'):
            proof_of_residence_name = kw.get('proof_of_residence').filename
            kw['proof_of_residence'] = base64.b64encode(kw.get('proof_of_residence').read())
        else:
            proof_of_residence_name = False

        if kw.get('curriculum_vitae'):
            curriculum_vitae_name = kw.get('curriculum_vitae').filename
            kw['curriculum_vitae'] = base64.b64encode(kw.get('curriculum_vitae').read())
        else:
            curriculum_vitae_name = False

        if kw.get('supplier_bank_details'):
            supplier_bank_details_name = kw.get('supplier_bank_details').filename
            kw['supplier_bank_details'] = base64.b64encode(kw.get('supplier_bank_details').read())
        else:
            supplier_bank_details_name = False

        if kw.get('six_month_personal_bs'):
            six_month_personal_bs_name = kw.get('six_month_personal_bs').filename
            kw['six_month_personal_bs'] = base64.b64encode(kw.get('six_month_personal_bs').read())
        else:
            six_month_personal_bs_name = False

        if kw.get('six_month_business_bs'):
            six_month_business_bs_name = kw.get('six_month_business_bs').filename
            kw['six_month_business_bs'] = base64.b64encode(kw.get('six_month_business_bs').read())
        else:
            six_month_business_bs_name = False

        if kw.get('certificate_qualification'):
            certificate_qualification_name = kw.get('certificate_qualification').filename
            kw['certificate_qualification'] = base64.b64encode(kw.get('certificate_qualification').read())
        else:
            certificate_qualification_name = False

        if kw.get('six_twentyfour_bs'):
            six_twentyfour_bs_name = kw.get('six_twentyfour_bs').filename
            kw['six_twentyfour_bs'] = base64.b64encode(kw.get('six_twentyfour_bs').read())
        else:
            six_twentyfour_bs_name = False
        #LM.Mahasha Update Oct 14 16:21
        #if kw.get('management_accounts'):
        #    management_accountsname = kw.get('management_accounts').filename
        #    kw['management_accounts'] = base64.b64encode(kw.get('management_accounts').read())
        #else:
        #    management_accounts_name = False

        if kw.get('buisness_asset_reg'):
            buisness_asset_reg_name = kw.get('buisness_asset_reg').filename
            kw['buisness_asset_reg'] = base64.b64encode(kw.get('buisness_asset_reg').read())
        else:
            buisness_asset_reg_name = False

        if kw.get('tax_certificate'):
            tax_certificate_name = kw.get('tax_certificate').filename
            kw['tax_certificate'] = base64.b64encode(kw.get('tax_certificate').read())
        else:
            tax_certificate_name = False
        #UPDATE END L.M Mahasha 08/10 22:28

        if kw.get('formal_business_plan'):
            formal_business_plan_name = kw.get('formal_business_plan').filename
            kw['formal_business_plan'] = base64.b64encode(kw.get('formal_business_plan').read())
        else:
            formal_business_plan_name = False
        if kw.get('certified_identity_document_applicant'):
            certified_identity_document_applicant_name = kw.get('certified_identity_document_applicant').filename
            kw['certified_identity_document_applicant'] = base64.b64encode(
                kw.get('certified_identity_document_applicant').read())

        else:
            certified_identity_document_applicant_name = False
        if kw.get('proof_of_business_registration'):
            proof_of_business_registration_name = kw.get('proof_of_business_registration').filename
            kw['proof_of_business_registration'] = base64.b64encode(kw.get('proof_of_business_registration').read())
        else:
            proof_of_business_registration_name = False

        if kw.get('business_bank_account'):
            business_bank_account_name = kw.get('business_bank_account').filename
            kw['business_bank_account'] = base64.b64encode(kw.get('business_bank_account').read())
        else:
            business_bank_account_name = False
        if kw.get('financial_statement_signed_accountant'):
            financial_statement_signed_accountant_name = kw.get('financial_statement_signed_accountant').filename
            kw['financial_statement_signed_accountant'] = base64.b64encode(
                kw.get('financial_statement_signed_accountant').read())

        else:
            financial_statement_signed_accountant_name = False

        if kw.get('one_year_management_account'):
            one_year_management_account_name = kw.get('one_year_management_account').filename
            kw['one_year_management_account'] = base64.b64encode(
                kw.get('one_year_management_account').read())

        else:
            one_year_management_account_name = False

        if kw.get('additional_permanent_job_creation'):
            additional_permanent_job_creation_name = kw.get('additional_permanent_job_creation').filename
            kw['additional_permanent_job_creation'] = base64.b64encode(
                kw.get('additional_permanent_job_creation').read())
        else:
            additional_permanent_job_creation_name = False
        if kw.get('requires_skills_operate_business'):
            requires_skills_operate_business_name = kw.get('requires_skills_operate_business').filename
            kw['requires_skills_operate_business'] = base64.b64encode(kw.get('requires_skills_operate_business').read())

        else:
            requires_skills_operate_business_name = False

        if kw.get('market_letters_off_take_contracts'):
            market_letters_off_take_contracts_name = kw.get('market_letters_off_take_contracts').filename
            kw['market_letters_off_take_contracts'] = base64.b64encode(
                kw.get('market_letters_off_take_contracts').read())
        else:
            market_letters_off_take_contracts_name = False
        if kw.get('business_operational_years_document'):
            business_operational_years_document_name = kw.get('business_operational_years_document').filename
            kw['business_operational_years_document'] = base64.b64encode(
                kw.get('business_operational_years_document').read())
        else:
            business_operational_years_document_name = False
        if kw.get('valid_tax_clearance_certificate'):
            valid_tax_clearance_certificate_name = kw.get('valid_tax_clearance_certificate').filename
            kw['valid_tax_clearance_certificate'] = base64.b64encode(kw.get('valid_tax_clearance_certificate').read())
        else:
            valid_tax_clearance_certificate_name = False
        if kw.get('breakdown_of_funds'):
            breakdown_of_funds_name = kw.get('breakdown_of_funds').filename
            kw['breakdown_of_funds'] = base64.b64encode(kw.get('breakdown_of_funds').read())
        else:
            breakdown_of_funds_name = False
        if kw.get('usage_of_working_capital'):
            usage_of_working_capital_name = kw.get('usage_of_working_capital').filename
            kw['usage_of_working_capital'] = base64.b64encode(kw.get('usage_of_working_capital').read())
        else:
            usage_of_working_capital_name = False
        if kw.get('nyda_business_plan_template_document'):
            nyda_business_plan_template_document_name = kw.get('nyda_business_plan_template_document').filename
            kw['nyda_business_plan_template_document'] = base64.b64encode(
                kw.get('nyda_business_plan_template_document').read())
        else:
            nyda_business_plan_template_document_name = False
        if kw.get('provide_management_accounts'):
            provide_management_accounts_name = kw.get('provide_management_accounts').filename
            kw['provide_management_accounts'] = base64.b64encode(kw.get('provide_management_accounts').read())
        else:
            provide_management_accounts_name = False
        if kw.get('other_doc'):
            other_doc_name = kw.get('other_doc').filename
            kw['other_doc'] = base64.b64encode(kw.get('other_doc').read())
        else:
            other_doc_name = False

        # if kw.get('current_employees'):
        #     current_employees_name = kw.get('current_employees').filename
        #     kw['current_employees'] = base64.b64encode(kw.get('current_employees').read())
        # else:
        #     current_employees_name = False
        # if kw.get('bank_statement'):
        #     bank_statement_name = kw.get('bank_statement').filename
        #     kw['bank_statement'] = base64.b64encode(kw.get('bank_statement').read())
        # else:
        #     bank_statement_name = False
        # if kw.get('business_plan_grant'):
        #     business_plan_grant_name = kw.get('business_plan_grant').filename
        #     kw['business_plan_grant'] = base64.b64encode(kw.get('business_plan_grant').read())
        # else:
        #     business_plan_grant_name = False
        # if kw.get('quotations_grant'):
        #     quotations_grant_name = kw.get('quotations_grant').filename
        #     kw['quotations_grant'] = base64.b64encode(kw.get('quotations_grant').read())
        # else:
        #     quotations_grant_name = False

        fmt_data = json.loads(kw.get('form_data'))
        job_creation_info = []
        for job in fmt_data.get('job_creation_ids'):
            job_creation_info.append((0, 0, job))

        grant_amount_utilization_info = []
        for job in fmt_data.get('grant_amount_utilization'):
            grant_amount_utilization_info.append((0, 0, job))

        grant_business_income_info = []
        for job in fmt_data.get('grant_business_income_ids'):
            grant_business_income_info.append((0, 0, job))

        grant_personal_income_info = []
        for job in fmt_data.get('grant_personal_income_ids'):
            grant_personal_income_info.append((0, 0, job))

        grant_business_expenses_info = []
        for job in fmt_data.get('grant_business_expenses_ids'):
            grant_business_expenses_info.append((0, 0, job))

        grant_personal_expenses_info = []
        for job in fmt_data.get('grant_personal_expenses_ids'):
            grant_personal_expenses_info.append((0, 0, job))

        other_expenses__info = []
        for job in fmt_data.get('other_expenses_ids'):
            other_expenses__info.append((0, 0, job))

        
        log_info = {
            'datetime: ':str(datetime.now()),
            'name: ':kw.get('name'),
            'surname: ' : kw.get('surname'),
            'sa_identity_number: ' :kw.get('sa_identity_number'),
            'gender: ' : kw.get('gender'),
            'population_group: ' : kw.get('population_group'),
            'home_language: ' : kw.get('home_language'),
            'disability: ' : kw.get('disability'),
            'telephone: ' : kw.get('telephone'),
            'mobile: ' :  kw.get('mobile'),
            'email: ' :  kw.get('email'),
            'fax: ' :  kw.get('fax'),
            'physical_address: ': kw.get('physical_address'),
            'physical_postal_code: ':kw.get('physical_postal_code'),
            'postal_address: ': kw.get('postal_address'),
            'postal_code: ' :  kw.get('postal_code'),
            'province_id: ' :kw.get('province_id'),
            'geographical_type: ' : kw.get('geographical_type'),
            'formal_qualification: ' : kw.get('formal_qualification'),
            'trainings_attended: ' : kw.get('trainings_attended'),
            'next_of_kin: ' : kw.get('next_of_kin'),
            'relative_physical_address: ' :  kw.get('relative_physical_address'),
            'relative_mobile: ' :  kw.get('relative_mobile'),
            'relationship: ' : kw.get('relationship'),
            'job_creation_info_ids: ' : job_creation_info,
            'grant_amount_utilization: ' :  grant_amount_utilization_info,
            'grant_business_income_ids: ' :  grant_business_income_info,
            'grant_personal_income_ids: ' :  grant_personal_income_info,
            'grant_business_expenses_ids: ' :  grant_business_expenses_info,
            'grant_personal_expenses_ids: ' :  grant_personal_expenses_info,
            'other_expenses_ids: ' : other_expenses__info,
            'existing_business: ' :  existing_business_status,
            'entrepreneurial_training: ' : entrepreneurial_training_status,
            'business_start_reason_ids: ' : [(6, 0, fmt_data.get('business_start_reason_ids'))],
            'startup_business_sector_ids: ' :  [(6, 0, fmt_data.get('startup_business_sector_ids'))],
            'startup_legal_entity_ids: ':  [(6, 0, fmt_data.get('startup_legal_entity_ids'))],
            'grant_business_sector_ids: ' :  [(6, 0, fmt_data.get('grant_business_sector_ids'))],
            'grant_legal_entity_ids: ' : [(6, 0, fmt_data.get('grant_legal_entity_ids'))],
            'business_start_reason_char: ' :  kw.get('business_start_reason_char'),
            'business_goals: ' : kw.get('business_goals'),
            'business_experience: ' : kw.get('business_experience'),
            'expertise_in_business: ' : kw.get('expertise_in_business'),
            'startup_business_name: ' :  kw.get('startup_business_name'),
            'startup_business_type: ' : kw.get('startup_business_type'),
            'startup_business_sector_char: ' : kw.get('startup_business_sector_char'),
            'startup_legal_entity_char: ' :  kw.get('startup_legal_entity_char'),
            'certified_identity_document_applicant: ' : 'file-text',
            'nyda_business_plan_template_document: ' :  'file-text',
            'usage_of_working_capital: ' : 'file-text',
            'business_bank_account: ' : 'file-text',
            'proof_of_business_registration: ' : 'file-text',
            'requires_skills_operate_business: ' : 'file-text',
            'additional_permanent_job_creation: ' : 'file-text',
            'formal_business_plan: ' : 'file-text',
            'provide_management_accounts: ' : 'file-text',
            'market_letters_off_take_contracts: ' :  'file-text',
            'business_operational_years_document: ' : 'file-text',
            'valid_tax_clearance_certificate: ' : 'file-text',
            'breakdown_of_funds: ' : kw.get('breakdown_of_funds'),
            'financial_statement_signed_accountant: ' : 'file-text',
            'one_year_management_account: ' : 'file-text',
            'other_doc: ' : 'file-text',
            'certified_identity_document_applicant_name: ' : certified_identity_document_applicant_name,
            'nyda_business_plan_template_document_name: ' : nyda_business_plan_template_document_name,
            'usage_of_working_capital_name: ' : usage_of_working_capital_name,
            'business_bank_account_name: ' : business_bank_account_name,
            'proof_of_business_registration_name: ' : proof_of_business_registration_name,
            'requires_skills_operate_business_name: ' : requires_skills_operate_business_name,
            'additional_permanent_job_creation_name: ' : additional_permanent_job_creation_name,
            'formal_business_plan_name: ' : formal_business_plan_name,
            'provide_management_accounts_name: ' :  provide_management_accounts_name,
            'market_letters_off_take_contracts_name: ' : market_letters_off_take_contracts_name,
            'business_operational_years_document_name: ' : business_operational_years_document_name,
            'valid_tax_clearance_certificate_name: ' : valid_tax_clearance_certificate_name,
            'breakdown_of_funds_name: ' : breakdown_of_funds_name,
            'financial_statement_signed_accountant_name: ' : financial_statement_signed_accountant_name,
            'one_year_management_account_name: ' : one_year_management_account_name,
            'other_doc_name: ' : other_doc_name,
            'grant_business_name: ' : kw.get('grant_business_name'),
            'grant_business_type: ' : kw.get('grant_business_type'),
            'grant_business_sector_char: ' : kw.get('grant_business_sector_char'),
            'grant_legal_entity_char: ' : kw.get('grant_legal_entity_char'),
            'grant_amount_required: ' : kw.get('grant_amount_required'),
            'grant_business_income_other: ' : kw.get('grant_business_income_other'),
            'grant_business_income_other_rupees: ' : kw.get('grant_business_income_other_rupees'),
            'grant_personal_income_other: ' : kw.get('grant_personal_income_other'),
            'grant_personal_income_other_rupees: ' : kw.get('grant_personal_income_other_rupees'),
            'grant_business_expenses_other: ' : kw.get('grant_business_expenses_other'),
            'grant_business_expenses_other_rupees: ' : kw.get('grant_business_expenses_other_rupees'),
            'grant_personal_expenses_other: ' : kw.get('grant_personal_expenses_other'),
            'grant_personal_expenses_other_rupees: ' : kw.get('grant_personal_expenses_other_rupees'),
            'beneficiary_id: ' : kw.get('beneficiary_id'),
            # 'grant_business_registration': kw.get(
            #     'grant_business_registration'),
            #UPDATE START L.M Mahasha 08/10 22:33
            'proof_of_residence_name: ' : proof_of_residence_name,
            'curriculum_vitae_name: ' : curriculum_vitae_name,
            #'business_bank_account_name': business_bank_account_name,
            #'supplier_quotations_name': supplier_quotations_name,
            'supplier_bank_details_name: ' : supplier_bank_details_name,
            'six_month_personal_bs_name: ' : six_month_personal_bs_name,
            'six_month_business_bs_name: ' : six_month_business_bs_name,
            'certificate_qualification_name: ' : certificate_qualification_name,
            'six_twentyfour_bs_name: ': six_twentyfour_bs_name,
            
            #LM.Mahasha Update Oct 14 16:21
            #'management_accounts_name': management_accounts_name,
            'buisness_asset_reg_name: ' :  buisness_asset_reg_name,
            'tax_certificate_name: ' : tax_certificate_name,

            'proof_of_residence: ' : 'file-text',
            'curriculum_vitae: ' : 'file-text',
            #'business_bank_account': business_bank_account,
            #'supplier_quotations': kw.get('supplier_quotations'),
            'supplier_bank_details: ' : 'file-text',
            'six_month_personal_bs: ' : 'file-text',
            'six_month_business_bs: ' : 'file-text',
            'certificate_qualification: ' : 'file-text',
            'six_twentyfour_bs: ' : 'file-text',
            
            #LM.Mahasha Update Oct 14 16:21
            #'management_accounts': kw.get('management_accounts'),
            'buisness_asset_reg: ' :  'file-text',
            'tax_certificate: ' : 'file-text',
            #UPDATE END L.M Mahasha 08/10 22:33

            'grant_business_registration_number: ': kw.get('grant_business_registration_number'),
            'grant_threshold: ': kw.get('grant_threshold'),

            'x_no_loan_funding_debt: ' : kw.get('x_no_loan_funding_debt'),
            'x_no_sme_loan_funding: ' : kw.get('x_no_sme_loan_funding'),
            'x_loan_not_written_off: ' : kw.get('x_loan_not_written_off')
            }
        
        _logger.info(str(log_info))    
        


        grant_application_id = request.env['grant.application'].sudo().create({
            'name': kw.get('name'),
            'surname': kw.get('surname'),
            'sa_identity_number': kw.get('sa_identity_number'),
            'gender': kw.get('gender'),
            'population_group': kw.get('population_group'),
            'home_language': kw.get('home_language'),
            'disability': kw.get('disability'),
            'telephone': kw.get('telephone'),
            'mobile': kw.get('mobile'),
            'email': kw.get('email'),
            'fax': kw.get('fax'),
            'physical_address': kw.get('physical_address'),
            'physical_postal_code': kw.get('physical_postal_code'),
            'postal_address': kw.get('postal_address'),
            'postal_code': kw.get('postal_code'),
            'province_id': kw.get('province_id'),
            'geographical_type': kw.get('geographical_type'),
            'formal_qualification': kw.get('formal_qualification'),
            'trainings_attended': kw.get('trainings_attended'),
            'next_of_kin': kw.get('next_of_kin'),
            'relative_physical_address': kw.get('relative_physical_address'),
            'relative_mobile': kw.get('relative_mobile'),
            'relationship': kw.get('relationship'),
            'job_creation_info_ids': job_creation_info,
            'grant_amount_utilization': grant_amount_utilization_info,
            'grant_business_income_ids': grant_business_income_info,
            'grant_personal_income_ids': grant_personal_income_info,
            'grant_business_expenses_ids': grant_business_expenses_info,
            'grant_personal_expenses_ids': grant_personal_expenses_info,
            'other_expenses_ids': other_expenses__info,
            'existing_business': existing_business_status,
            'entrepreneurial_training': entrepreneurial_training_status,
            'business_start_reason_ids': [(6, 0, fmt_data.get('business_start_reason_ids'))],
            'startup_business_sector_ids': [(6, 0, fmt_data.get('startup_business_sector_ids'))],
            'startup_legal_entity_ids': [(6, 0, fmt_data.get('startup_legal_entity_ids'))],
            'grant_business_sector_ids': [(6, 0, fmt_data.get('grant_business_sector_ids'))],
            'grant_legal_entity_ids': [(6, 0, fmt_data.get('grant_legal_entity_ids'))],
            'business_start_reason_char': kw.get('business_start_reason_char'),
            'business_goals': kw.get('business_goals'),
            'business_experience': kw.get('business_experience'),
            'expertise_in_business': kw.get('expertise_in_business'),
            'startup_business_name': kw.get('startup_business_name'),
            'startup_business_type': kw.get('startup_business_type'),
            'startup_business_sector_char': kw.get('startup_business_sector_char'),
            'startup_legal_entity_char': kw.get('startup_legal_entity_char'),
            'certified_identity_document_applicant': kw.get('certified_identity_document_applicant'),
            'nyda_business_plan_template_document': kw.get('nyda_business_plan_template_document'),
            'usage_of_working_capital': kw.get('usage_of_working_capital'),
            'business_bank_account': kw.get('business_bank_account'),
            'proof_of_business_registration': kw.get('proof_of_business_registration'),
            'requires_skills_operate_business': kw.get('requires_skills_operate_business'),
            'additional_permanent_job_creation': kw.get('additional_permanent_job_creation'),
            'formal_business_plan': kw.get('formal_business_plan'),
            'provide_management_accounts': kw.get('provide_management_accounts'),
            'market_letters_off_take_contracts': kw.get('market_letters_off_take_contracts'),
            'business_operational_years_document': kw.get('business_operational_years_document'),
            'valid_tax_clearance_certificate': kw.get('valid_tax_clearance_certificate'),
            'breakdown_of_funds': kw.get('breakdown_of_funds'),
            'financial_statement_signed_accountant': kw.get('financial_statement_signed_accountant'),
            'one_year_management_account': kw.get('one_year_management_account'),
            'other_doc': kw.get('other_doc'),
            'certified_identity_document_applicant_name': certified_identity_document_applicant_name,
            'nyda_business_plan_template_document_name': nyda_business_plan_template_document_name,
            'usage_of_working_capital_name': usage_of_working_capital_name,
            'business_bank_account_name': business_bank_account_name,
            'proof_of_business_registration_name': proof_of_business_registration_name,
            'requires_skills_operate_business_name': requires_skills_operate_business_name,
            'additional_permanent_job_creation_name': additional_permanent_job_creation_name,
            'formal_business_plan_name': formal_business_plan_name,
            'provide_management_accounts_name': provide_management_accounts_name,
            'market_letters_off_take_contracts_name': market_letters_off_take_contracts_name,
            'business_operational_years_document_name': business_operational_years_document_name,
            'valid_tax_clearance_certificate_name': valid_tax_clearance_certificate_name,
            'breakdown_of_funds_name': breakdown_of_funds_name,
            'financial_statement_signed_accountant_name': financial_statement_signed_accountant_name,
            'one_year_management_account_name': one_year_management_account_name,
            'other_doc_name': other_doc_name,
            'grant_business_name': kw.get('grant_business_name'),
            'grant_business_type': kw.get('grant_business_type'),
            'grant_business_sector_char': kw.get('grant_business_sector_char'),
            'grant_legal_entity_char': kw.get('grant_legal_entity_char'),
            'grant_amount_required': kw.get('grant_amount_required'),
            'grant_business_income_other': kw.get('grant_business_income_other'),
            'grant_business_income_other_rupees': kw.get('grant_business_income_other_rupees'),
            'grant_personal_income_other': kw.get('grant_personal_income_other'),
            'grant_personal_income_other_rupees': kw.get('grant_personal_income_other_rupees'),
            'grant_business_expenses_other': kw.get('grant_business_expenses_other'),
            'grant_business_expenses_other_rupees': kw.get('grant_business_expenses_other_rupees'),
            'grant_personal_expenses_other': kw.get('grant_personal_expenses_other'),
            'grant_personal_expenses_other_rupees': kw.get('grant_personal_expenses_other_rupees'),
            'beneficiary_id': kw.get('beneficiary_id'),
            # 'grant_business_registration': kw.get(
            #     'grant_business_registration'),
            #UPDATE START L.M Mahasha 08/10 22:33
            'proof_of_residence_name': proof_of_residence_name,
            'curriculum_vitae_name': curriculum_vitae_name,
            #'business_bank_account_name': business_bank_account_name,
            #'supplier_quotations_name': supplier_quotations_name,
            'supplier_bank_details_name': supplier_bank_details_name,
            'six_month_personal_bs_name': six_month_personal_bs_name,
            'six_month_business_bs_name': six_month_business_bs_name,
            'certificate_qualification_name': certificate_qualification_name,
            'six_twentyfour_bs_name': six_twentyfour_bs_name,
            
            #LM.Mahasha Update Oct 14 16:21
            #'management_accounts_name': management_accounts_name,
            'buisness_asset_reg_name': buisness_asset_reg_name,
            'tax_certificate_name': tax_certificate_name,

            'proof_of_residence': kw.get('proof_of_residence'),
            'curriculum_vitae': kw.get('curriculum_vitae'),
            #'business_bank_account': business_bank_account,
            #'supplier_quotations': kw.get('supplier_quotations'),
            'supplier_bank_details': kw.get('supplier_bank_details'),
            'six_month_personal_bs': kw.get('six_month_personal_bs'),
            'six_month_business_bs': kw.get('six_month_business_bs'),
            'certificate_qualification': kw.get('proof_of_residence'),
            'six_twentyfour_bs': kw.get('six_twentyfour_bs'),
            
            #LM.Mahasha Update Oct 14 16:21
            #'management_accounts': kw.get('management_accounts'),
            'buisness_asset_reg': kw.get('buisness_asset_reg'),
            'tax_certificate': kw.get('tax_certificate'),
            #UPDATE END L.M Mahasha 08/10 22:33

            'grant_business_registration_number': kw.get('grant_business_registration_number'),
            'grant_threshold': kw.get('grant_threshold'),

            'x_no_loan_funding_debt': kw.get('x_no_loan_funding_debt'),
            'x_no_sme_loan_funding': kw.get('x_no_sme_loan_funding'),
            'x_loan_not_written_off': kw.get('x_loan_not_written_off'),

        })

        if grant_application_id:
            mail_template_id = request.env.ref('nyda_grant_and_voucher.grant_website_submit_mail_template')
            if mail_template_id:
                company_id = request.env['res.company'].search([], limit=1)
                company_email = company_id.email
                mail_template_id.with_context(user=request.env.user, c_email=company_email).send_mail(
                    grant_application_id.id, force_send=True)
            #UPDATE
            attached_files = request.httprequest.files.getlist('x_supplier_quotations_ids')

            for attachment in attached_files:
                file = attachment.read()
                attachment_id = request.env['ir.attachment'].create({
                    'name': attachment.filename,
                    'datas_fname': attachment.filename,
                    'type': 'binary',
                    'datas': base64.b64encode(file),
                    'res_model': 'grant.application',
                    'res_id': grant_application_id.id
                })
                grant_application_id.update({
                    'x_supplier_quotations_ids': [(4, attachment_id.id)],
                })
            #END

        # 'identity_document_1': kw.get(
        #     'identity_document_1'),
        # 'identity_document_2': kw.get(
        #     'identity_document_2'),
        # 'identity_document_3': kw.get(
        #     'identity_document_3'),
        # 'proof_of_residence': kw.get(
        #     'proof_of_residence'),
        # 'company_registration': kw.get(
        #     'company_registration'),
        # 'company_profile': kw.get(
        #     'company_profile'),
        # 'current_employees': kw.get(
        #     'current_employees'),
        # 'bank_statement': kw.get(
        #     'bank_statement'),
        # 'business_plan_grant': kw.get(
        #     'business_plan_grant'),
        # 'quotations_grant': kw.get(
        #     'quotations_grant'),

        # 'identity_document_1_name': identity_document_1_name,
        # 'identity_document_2_name': identity_document_2_name,
        # 'identity_document_3_name': identity_document_3_name,
        # 'proof_of_residence_name': proof_of_residence_name,
        # 'company_registration_name': company_registration_name,
        # 'company_profile_name': company_profile_name,
        # 'current_employees_name': current_employees_name,
        # 'bank_statement_name': bank_statement_name,
        # 'business_plan_grant_name': business_plan_grant_name,
        # 'quotations_grant_name': quotations_grant_name,
        #return request.render("nyda_grant_and_voucher.grant_form_submitted",
        #                      {'grant_application_id': grant_application_id})
        return request.render("nyda_grant_and_voucher.voucher_form_submitted",
                              {'voucher_application_id': grant_application_id})

    @http.route("/voucher-application-submit", type='http', auth="user", website=True, csrf=False)
    def voucher_application_submit(self, **kw):
        print('-------->>>>--\n\n', kw)
        # existing_business and entrepreneurial_training radio button
        voucher_exists_id = request.env['voucher.application'].sudo().search([('user_id', '=', request.env.user.id)], limit=1, order='id desc')
        if voucher_exists_id and not(voucher_exists_id.status == 'completed' or voucher_exists_id.status == 'decline' or voucher_exists_id.status == 'payment_completed' or voucher_exists_id.status == 'pending_payment' or voucher_exists_id.status == 'payment_released' or voucher_exists_id.status == 'send_payment_reciept' or voucher_exists_id.status == 'cancelled'): #L.M Mahasha 26/09/2021-16:22
            return request.render('nyda_grant_and_voucher.voucher_application_exists', {'application_type': 'voucher'})
        if 'existing_business' not in kw.keys():
            existing_business_status = False
        else:
            existing_business_status = eval(kw.get('existing_business'))

        if 'business_idea' not in kw.keys():
            business_idea_status = False
        else:
            business_idea_status = eval(kw.get('business_idea'))

        if 'no_business' not in kw.keys():
            no_business_status = False
        else:
            no_business_status = eval(kw.get('existing_business'))

        if 'entrepreneurial_training' not in kw.keys():
            entrepreneurial_training_status = False
        else:
            entrepreneurial_training_status = eval(kw.get('entrepreneurial_training'))

        if 'separate_bank_account' not in kw.keys():
            separate_bank_account_status = False
        else:
            separate_bank_account_status = eval(kw.get('separate_bank_account'))

        if 'previous_work_on_industry' not in kw.keys():
            previous_work_on_industry_status = False
        else:
            previous_work_on_industry_status = eval(kw.get('previous_work_on_industry'))

        if 'able_invest_resource' not in kw.keys():
            able_invest_resource_status = False
        else:
            able_invest_resource_status = eval(kw.get('able_invest_resource'))

        # supporting documents
        if kw.get('identity_document_1'):
            identity_document_1_name = kw.get('identity_document_1').filename
            kw['identity_document_1'] = base64.b64encode(kw.get('identity_document_1').read())
        else:
           identity_document_1_name = False
        # if kw.get('proof_of_residence'):
        #     proof_of_residence_name = kw.get('proof_of_residence').filename
        #     kw['proof_of_residence'] = base64.b64encode(kw.get('proof_of_residence').read())
        # else:
        #     proof_of_residence_name = False
        if kw.get('company_registration'):
            company_registration_name = kw.get('company_registration').filename
            kw['company_registration'] = base64.b64encode(kw.get('company_registration').read())
        else:
            company_registration_name = False
        if kw.get('company_profile'):
            company_profile_name = kw.get('company_profile').filename
            kw['company_profile'] = base64.b64encode(kw.get('company_profile').read())
        else:
            company_profile_name = False
        #x_bmt_certificate
        if kw.get('current_employees'):
            current_employees_name = kw.get('current_employees').filename
            kw['current_employees'] = base64.b64encode(kw.get('current_employees').read())
        else:
            current_employees_name = False
        
        if kw.get('x_bmt_certificate'):
            x_bmt_certificate_name = kw.get('x_bmt_certificate').filename
            kw['x_bmt_certificate'] = base64.b64encode(kw.get('x_bmt_certificate').read())
        else:
            x_bmt_certificate_name = False
        # if kw.get('bank_statement'):
        #     bank_statement_name = kw.get('bank_statement').filename
        #     kw['bank_statement'] = base64.b64encode(kw.get('bank_statement').read())
        # else:
        #     bank_statement_name = False
        # if kw.get('business_plan_grant'):
        #     business_plan_grant_name = kw.get('business_plan_grant').filename
        #     kw['business_plan_grant'] = base64.b64encode(kw.get('business_plan_grant').read())
        # else:
        #     business_plan_grant_name = False
        # if kw.get('quotations_grant'):
        #     quotations_grant_name = kw.get('quotations_grant').filename
        #     kw['quotations_grant'] = base64.b64encode(kw.get('quotations_grant').read())
        # else:
        #     quotations_grant_name = False
        if kw.get('other_doc'):
            other_doc_name = kw.get('other_doc').filename
            kw['other_doc'] = base64.b64encode(kw.get('other_doc').read())
        else:
            other_doc_name = False

        fmt_data = json.loads(kw.get('form_data'))
        job_creation_info = []
        for job in fmt_data.get('job_creation_ids'):
            job_creation_info.append((0, 0, job))

        ownership_status_info = []
        for job in fmt_data.get('ownership_status_ids'):
            ownership_status_info.append((0, 0, job))

        business_ownership_status_info = []
        for job in fmt_data.get('business_ownership_status_ids'):
            business_ownership_status_info.append((0, 0, job))

        log_info = {
            'name': kw.get('name'),
            'surname': kw.get('surname'),
            'sa_identity_number': kw.get('sa_identity_number'),
            'gender': kw.get('gender'),
            'population_group': kw.get('population_group'),
            'home_language': kw.get('home_language'),
            'disability': kw.get('disability'),
            'telephone': kw.get('telephone'),
            'mobile': kw.get('mobile'),
            'email': kw.get('email'),
            'fax': kw.get('fax'),
            'physical_address': kw.get('physical_address'),
            'physical_postal_code': kw.get('physical_postal_code'),
            'postal_address': kw.get('postal_address'),
            'postal_code': kw.get('postal_code'),
            'province_id': kw.get('province_id'),
            'geographical_type': kw.get('geographical_type'),
            'formal_qualification': kw.get('formal_qualification'),
            'trainings_attended': kw.get('trainings_attended'),
            'next_of_kin': kw.get('next_of_kin'),
            'relative_physical_address': kw.get('relative_physical_address'),
            'relative_mobile': kw.get('relative_mobile'),
            'relationship': kw.get('relationship'),
            'existing_business': existing_business_status,
            'business_idea': business_idea_status,
            'no_business': no_business_status,
            'entrepreneurial_training': entrepreneurial_training_status,
            'separate_bank_account': separate_bank_account_status,
            'previous_work_on_industry': previous_work_on_industry_status,
            'able_invest_resource': able_invest_resource_status,
            'job_creation_info_ids': job_creation_info,
            'ownership_status_ids': ownership_status_info,
            'business_ownership_status_ids': business_ownership_status_info,
            'business_start_reason_ids': [(6, 0,fmt_data.get('business_start_reason_ids'))],
            'existing_business_start_reason_ids': [(6, 0, fmt_data.get('existing_business_start_reason_ids'))],
            'startup_business_start_reason_ids': [(6, 0, fmt_data.get('startup_business_start_reason_ids'))],
            'x_existing_business_sector_id': [(6,0,fmt_data.get('existing_business_sector_ids'))],
            'existing_legal_entity_ids': [(6, 0,fmt_data.get('existing_legal_entity_ids'))],
            'business_start_reason_char': kw.get('business_start_reason_char'),
            'startup_business_start_reason_char': kw.get('startup_business_start_reason_char'),
            'business_goals': kw.get('business_goals'),
            'business_experience': kw.get('business_experience'),
            'expertise_in_business': kw.get('expertise_in_business'),
            'startup_business_name': kw.get('startup_business_name'),
            'startup_business_type': kw.get('startup_business_type'),
            'identity_document_1_name': identity_document_1_name,
            'identity_document_1': kw.get('identity_document_1'),
            # 'identity_document_2': kw.get('identity_document_2'),
            # 'identity_document_3': kw.get('identity_document_3'),
            # 'proof_of_residence': kw.get(
            #     'proof_of_residence'),
            'company_registration': kw.get('company_registration'),
            'company_profile': kw.get('company_profile'),
            'current_employees': kw.get('current_employees'),
            # 'bank_statement': kw.get(
            #     'bank_statement'),
            # 'business_plan_grant': kw.get(
            #     'business_plan_grant'),
            # 'quotations_grant': kw.get(
            #     'quotations_grant'),
            'other_doc': kw.get('other_doc'),

            # 'identity_document_2_name': identity_document_2_name,
            # 'identity_document_3_name': identity_document_3_name,
            # 'proof_of_residence_name': proof_of_residence_name,
            'company_registration_name': company_registration_name,
            'company_profile_name': company_profile_name,
            'current_employees_name': current_employees_name,
            # 'bank_statement_name': bank_statement_name,
            # 'business_plan_grant_name': business_plan_grant_name,
            # 'quotations_grant_name': quotations_grant_name,
            'other_doc_name': other_doc_name,
            'startup_business_sector_ids': [(6, 0,
                fmt_data.get('startup_business_sector_ids'))],
            'startup_legal_entity_ids': [(6, 0,fmt_data.get('startup_legal_entity_ids'))],
            'business_development_assistance_ids':
                [(6, 0, fmt_data.get('business_development_assistance_ids'))],
            # 'business_development_assistance_startup_ids': [
            #     (6, 0, fmt_data.get('business_development_assistance_startup_ids'))],
            # 'business_development_assistance_business_idea_ids': [
            #     (6, 0, fmt_data.get('business_development_assistance_business_idea_ids'))],
            'startup_business_sector_char': kw.get('startup_business_sector_char'),
            'startup_legal_entity_char': kw.get('startup_legal_entity_char'),
            'startup_idea_description_type_of_business':
                kw.get('startup_idea_description_type_of_business'),
            'startup_idea_description_business_need_satisfy':
                kw.get('startup_idea_description_business_need_satisfy'),
            'startup_idea_description_potential_customers':
                kw.get('startup_idea_description_potential_customers'),
            'startup_idea_description_operate_business':
                kw.get('startup_idea_description_operate_business'),
            'startup_idea_description_operate_product_servivces':
                kw.get('startup_idea_description_operate_product_servivces'),
            'management_skills_start_business': kw.get('management_skills_start_business'),
            'technical_skills_start_business': kw.get('technical_skills_start_business'),
            'identified_potential_customers': kw.get('identified_potential_customers'),
            'know_competitors': kw.get('know_competitors'),
            'money_to_cover_startup': kw.get('money_to_cover_startup'),
            'money_to_cover_operating': kw.get('money_to_cover_operating'),
            'required_equipments_and_machine': kw.get('required_equipments_and_machine'),
            'existing_business_name': kw.get('existing_business_name'),
            'existing_business_type': kw.get('existing_business_type'),
            'existing_idea_description_type_of_business':
                kw.get('existing_idea_description_type_of_business'),
            'existing_idea_description_business_need_satisfy':
                kw.get('existing_idea_description_business_need_satisfy'),
            'existing_idea_description_potential_customers':
                kw.get('existing_idea_description_potential_customers'),
            'existing_idea_description_operate_business':
                kw.get('existing_idea_description_operate_business'),
            'existing_idea_description_operate_product_servivces':
                kw.get('existing_idea_description_operate_product_servivces'),
            'business_running_time': kw.get('business_running_time'),
            'count_employees': kw.get('count_employees'),
            'change_in_emp_count': kw.get('change_in_emp_count'),
            'estimate_annual_turnover': kw.get('estimate_annual_turnover'),
            'change_in_turnover': kw.get('change_in_turnover'),
            'business_start_method': kw.get('business_start_method'),
            'business_premise': kw.get('business_premise'),
            'business_area_description': kw.get('business_area_description'),
            'growth_business_sector': kw.get('growth_business_sector'),
            'business_comply_industry': kw.get('business_comply_industry'),
            'startup_involvement': kw.get('startup_involvement'),
            'business_management_experiance': kw.get('business_management_experiance'),
            'future_business_goals': kw.get('future_business_goals'),
            'business_assistance_improvements': kw.get('business_assistance_improvements'),
            'change_in_emp_reason': kw.get('change_in_emp_reason'),
            'change_in_turnover_reason': kw.get('change_in_turnover_reason'),
            'business_operate_premises_char': kw.get('business_operate_premises_char'),
            'existing_business_sector_char': kw.get('existing_business_sector_char'),
            'existing_legal_entity_char': kw.get('existing_legal_entity_char'),
            'existing_business_start_reason_char': kw.get('existing_business_start_reason_char'),
            'business_start_monetary_id': kw.get('business_start_monetary_id'),
            'business_operate_premises_id': kw.get('business_operate_premises_id'),
            'business_geographical_location_id': kw.get('business_geographical_location_id'),
            'business_sector_id': kw.get('business_sector_id'),
            'beneficiary_id': kw.get('beneficiary_id'),
            'business_development_assistance': kw.get('business_development_assistance'),
            #'check_box_transfer_field': kw.get('check_box_transfer_field'),
            'expected_turn_over_hidden_value': kw.get('expected_turn_over_hidden_value'),
            'total_status_ownership_percent': kw.get('total_status_ownership_percent'),
            'total_business_ownership_percent': kw.get('total_business_ownership_percent')
            }
        
        _logger.info(str(log_info))    


        voucher_application_id = request.env['voucher.application'].sudo().create({
            'name': kw.get('name'),
            'surname': kw.get('surname'),
            'sa_identity_number': kw.get('sa_identity_number'),
            'gender': kw.get('gender'),
            'population_group': kw.get('population_group'),
            'home_language': kw.get('home_language'),
            'disability': kw.get('disability'),
            'telephone': kw.get('telephone'),
            'mobile': kw.get('mobile'),
            'email': kw.get('email'),
            'fax': kw.get('fax'),
            'physical_address': kw.get('physical_address'),
            'physical_postal_code': kw.get('physical_postal_code'),
            'postal_address': kw.get('postal_address'),
            'postal_code': kw.get('postal_code'),
            'province_id': kw.get('province_id'),
            'geographical_type': kw.get('geographical_type'),
            'formal_qualification': kw.get('formal_qualification'),
            'trainings_attended': kw.get('trainings_attended'),
            'next_of_kin': kw.get('next_of_kin'),
            'relative_physical_address': kw.get('relative_physical_address'),
            'relative_mobile': kw.get('relative_mobile'),
            'relationship': kw.get('relationship'),
            'existing_business': existing_business_status,
            'business_idea': business_idea_status,
            'no_business': no_business_status,
            'entrepreneurial_training': entrepreneurial_training_status,
            'separate_bank_account': separate_bank_account_status,
            'previous_work_on_industry': previous_work_on_industry_status,
            'able_invest_resource': able_invest_resource_status,
            'job_creation_info_ids': job_creation_info,
            'ownership_status_ids': ownership_status_info,
            'business_ownership_status_ids': business_ownership_status_info,
            'business_start_reason_ids': [(6, 0,fmt_data.get('business_start_reason_ids'))],
            'existing_business_start_reason_ids': [(6, 0, fmt_data.get('existing_business_start_reason_ids'))],
            'startup_business_start_reason_ids': [(6, 0, fmt_data.get('startup_business_start_reason_ids'))],
            'existing_business_sector_ids': [(6,0,fmt_data.get('existing_business_sector_ids'))],
            'existing_legal_entity_ids': [(6, 0,fmt_data.get('existing_legal_entity_ids'))],
            'business_start_reason_char': kw.get('business_start_reason_char'),
            'startup_business_start_reason_char': kw.get('startup_business_start_reason_char'),
            'business_goals': kw.get('business_goals'),
            'business_experience': kw.get('business_experience'),
            'expertise_in_business': kw.get('expertise_in_business'),
            'startup_business_name': kw.get('startup_business_name'),
            'startup_business_type': kw.get('startup_business_type'),
            'identity_document_1_name': identity_document_1_name,
            'identity_document_1': kw.get('identity_document_1'),
            # 'identity_document_2': kw.get('identity_document_2'),
            # 'identity_document_3': kw.get('identity_document_3'),
            # 'proof_of_residence': kw.get(x_bmt_certificate
            #     'proof_of_residence'),
            'company_registration': kw.get('company_registration'),
            'company_profile': kw.get('company_profile'),
            'current_employees': kw.get('current_employees'),
            'x_bmt_certificate': kw.get('x_bmt_certificate'),
            # 'bank_statement': kw.get(
            #     'bank_statement'),
            # 'business_plan_grant': kw.get(
            #     'business_plan_grant'),
            # 'quotations_grant': kw.get(
            #     'quotations_grant'),
            'other_doc': kw.get('other_doc'),

            # 'identity_document_2_name': identity_document_2_name,
            # 'identity_document_3_name': identity_document_3_name,
            # 'proof_of_residence_name': proof_of_residence_name,
            'company_registration_name': company_registration_name,
            'company_profile_name': company_profile_name,
            'current_employees_name': current_employees_name,
            'x_bmt_certificate_name': x_bmt_certificate_name,
            # 'bank_statement_name': bank_statement_name,
            # 'business_plan_grant_name': business_plan_grant_name,
            # 'quotations_grant_name': quotations_grant_name,
            'other_doc_name': other_doc_name,
            'startup_business_sector_ids': [(6, 0,
                fmt_data.get('startup_business_sector_ids'))],
            'startup_legal_entity_ids': [(6, 0,fmt_data.get('startup_legal_entity_ids'))],
            'business_development_assistance_ids':
                [(6, 0, fmt_data.get('business_development_assistance_ids'))],
            # 'business_development_assistance_startup_ids': [
            #     (6, 0, fmt_data.get('business_development_assistance_startup_ids'))],
            # 'business_development_assistance_business_idea_ids': [
            #     (6, 0, fmt_data.get('business_development_assistance_business_idea_ids'))],
            'startup_business_sector_char': kw.get('startup_business_sector_char'),
            'startup_legal_entity_char': kw.get('startup_legal_entity_char'),
            'startup_idea_description_type_of_business':
                kw.get('startup_idea_description_type_of_business'),
            'startup_idea_description_business_need_satisfy':
                kw.get('startup_idea_description_business_need_satisfy'),
            'startup_idea_description_potential_customers':
                kw.get('startup_idea_description_potential_customers'),
            'startup_idea_description_operate_business':
                kw.get('startup_idea_description_operate_business'),
            'startup_idea_description_operate_product_servivces':
                kw.get('startup_idea_description_operate_product_servivces'),
            'management_skills_start_business': kw.get('management_skills_start_business'),
            'technical_skills_start_business': kw.get('technical_skills_start_business'),
            'identified_potential_customers': kw.get('identified_potential_customers'),
            'know_competitors': kw.get('know_competitors'),
            'money_to_cover_startup': kw.get('money_to_cover_startup'),
            'money_to_cover_operating': kw.get('money_to_cover_operating'),
            'required_equipments_and_machine': kw.get('required_equipments_and_machine'),
            'existing_business_name': kw.get('existing_business_name'),
            'existing_business_type': kw.get('existing_business_type'),
            'existing_idea_description_type_of_business':
                kw.get('existing_idea_description_type_of_business'),
            'existing_idea_description_business_need_satisfy':
                kw.get('existing_idea_description_business_need_satisfy'),
            'existing_idea_description_potential_customers':
                kw.get('existing_idea_description_potential_customers'),
            'existing_idea_description_operate_business':
                kw.get('existing_idea_description_operate_business'),
            'existing_idea_description_operate_product_servivces':
                kw.get('existing_idea_description_operate_product_servivces'),
            'business_running_time': kw.get('business_running_time'),
            'count_employees': kw.get('count_employees'),
            'change_in_emp_count': kw.get('change_in_emp_count'),
            'estimate_annual_turnover': kw.get('estimate_annual_turnover'),
            'change_in_turnover': kw.get('change_in_turnover'),
            'business_start_method': kw.get('business_start_method'),
            'business_premise': kw.get('business_premise'),
            'business_area_description': kw.get('business_area_description'),
            'growth_business_sector': kw.get('growth_business_sector'),
            'business_comply_industry': kw.get('business_comply_industry'),
            'startup_involvement': kw.get('startup_involvement'),
            'business_management_experiance': kw.get('business_management_experiance'),
            'future_business_goals': kw.get('future_business_goals'),
            'business_assistance_improvements': kw.get('business_assistance_improvements'),
            'change_in_emp_reason': kw.get('change_in_emp_reason'),
            'change_in_turnover_reason': kw.get('change_in_turnover_reason'),
            'business_operate_premises_char': kw.get('business_operate_premises_char'),
            'existing_business_sector_char': kw.get('existing_business_sector_char'),
            'existing_legal_entity_char': kw.get('existing_legal_entity_char'),
            'existing_business_start_reason_char': kw.get('existing_business_start_reason_char'),
            'business_start_monetary_id': kw.get('business_start_monetary_id'),
            'business_operate_premises_id': kw.get('business_operate_premises_id'),
            'business_geographical_location_id': kw.get('business_geographical_location_id'),
            'business_sector_id': kw.get('business_sector_id'),
            'beneficiary_id': kw.get('beneficiary_id'),
            'business_development_assistance': kw.get('business_development_assistance'),
            #'check_box_transfer_field': kw.get('check_box_transfer_field'),
            'expected_turn_over_hidden_value': kw.get('expected_turn_over_hidden_value'),
            'total_status_ownership_percent': kw.get('total_status_ownership_percent'),
            'total_business_ownership_percent': kw.get('total_business_ownership_percent')
        })

        print('--------->>>>>>>\n\n\n', voucher_application_id)
        return request.render("nyda_grant_and_voucher.voucher_form_submitted",
                              {'voucher_application_id': voucher_application_id})