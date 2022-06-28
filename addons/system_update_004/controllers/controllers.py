# -*- coding: utf-8 -*-
"""from odoo import http

class Test(http.Controller):
    
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
                voucher_id = ''
                for voucher_user in existing_user:
                    if voucher_user.status != 'decline' :
                        if voucher_user.status == 'approved' or voucher_user.status == 'payment_completed' or voucher_user.status == "payment_released":
                            voucher_app_count += 1
                        else:
                            voucher_id = voucher_user
                if voucher_app_count > 4:
                    return request.render('nyda_grant_and_voucher.limit_reached_grant', {
                        'voucher_app_id': existing_user
                    })
                elif voucher_app_count != len(existing_user):
                    return request.render('nyda_grant_and_voucher.check_total_app', {
                        'voucher_app_id': voucher_id
                    })
            if enquirys_id and enquirys_id.state not in ['new', 'decline']:
                # return request.render('nyda_grant_and_voucher.not_recommended_yet', {
                #     'application_type': 'voucher'
                # })
                beneficiary_id = request.env.user.id
                branch_id = request.env.user.branch_id.id
                #x_total_approved_vouchers = equest.env.user.x_total_approved_vouchers
                province_ids = request.env['res.country.state'].sudo().search(
                    [('country_id.name', '=', 'South Africa')])
                enquiry_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', beneficiary_id)])
                metro_municipality_ids = request.env['res.metro.municipality'].sudo().search([])
                municipality_ids = request.env['res.municipality'].sudo().search([])
                branch_ids = request.env['res.branch'].sudo().search([])
                business_start_reason_ids = request.env['business.start.reason'].sudo().search([])
                startup_business_sector_ids = request.env['business.sector'].sudo().search([])
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
                    #'total_vouchers_recieved': x_total_approved_vouchers,
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
        
        
        # --------------------------------------------------------
        #grant-voucher.js
        #979: <h4 t-att-value="total_vouchers_recieved"></h4>
        """
