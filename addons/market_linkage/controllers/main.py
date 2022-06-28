from odoo import fields, http, tools, _
from odoo.http import request


class ProductsServices(http.Controller):

    @http.route(["/opportunities-mkl","/opportunities-mkl/page/<int:page>"], type='http', auth="public", website=True, csrf=False)
    def products_services(self, page=0, *args, **kwargs):
        if request.env.user.has_group('client_management.group_branch_beneficiary') \
                or request.env.user.has_group('client_management.group_partner_service_provider') \
                or request.env.user.has_group('mentorship.group_bao'):
            url = "/opportunities-mkl"
            opportunity_len = request.env['register.opportunity'].sudo().search([])
            opportunity_count = len(opportunity_len)
            ppg = 6
            pager = request.website.pager(url=url, total=opportunity_count, page=page, step=ppg)
            opportunity = request.env['register.opportunity'].sudo().search([], limit=ppg, offset=pager['offset'])
            oppo_list = []
            for oppo in opportunity:
                flag = True
                for oppo_app in oppo.opportunity_application_ids:
                    if oppo_app.user_id.id == request.env.user.id:
                        flag = False
                        break
                if flag == True:
                    oppo_list.append(oppo.id)
            final_opportunity = request.env['register.opportunity'].sudo().search([('id','in',oppo_list)], limit=ppg, offset=pager['offset'])
            return request.render("market_linkage.products_services_template", {'opportunity':final_opportunity, 'pager':pager})
        else:
            return request.render('mentorship.not_applicable_form', {})

    @http.route("/opportunity-enquiry-submit", type='http', auth="public", website=True, csrf=False)
    def opportunity_enquiry_submit(self , **post):
        opportunity = request.env['register.opportunity'].sudo().search([('id','=',post.get('id'))])
        flag = True
        if not request.env.user.id in opportunity.interested_bene_id.ids:
            user_id = request.env.user.id
            youth_enquiry_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', user_id)])
            opportunity.opportunity_application_ids = [(0,0, {'youth_enquiry_id':youth_enquiry_id,
                                            'opportunity_application_id':opportunity.id,'user_id':user_id})]
            opportunity.interested_bene_id = [(4, request.env.user.id)]
        else:
            flag = False
        return request.render("market_linkage.opportunity_thanks",{'flag':flag})

    @http.route("/register-mkl", type='http', auth="public", website=True, csrf=False)
    def register_mkl(self, **post):
        if request.env.user.has_group('client_management.group_branch_beneficiary') :
            beneficiary_id = request.env.user.id
            branch_id = request.env.user.branch_id.id
            province_ids = request.env['res.country.state'].sudo().search([('country_id.name', '=', 'South Africa')])
            enquiry_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', beneficiary_id)])
            metro_municipality_ids = request.env['res.metro.municipality'].sudo().search([])
            municipality_ids = request.env['res.municipality'].sudo().search([])
            branch_ids = request.env['res.branch'].sudo().search([])
            return request.render("market_linkage.register_mkl_template", {
                'beneficiary_id':beneficiary_id,
                'branch_id':branch_id,
                'enquiry':enquiry_id,
                'province_ids': province_ids,
                'metro_municipality_ids': metro_municipality_ids,
                'municipality_ids': municipality_ids,
                'branch_ids': branch_ids,
            })
        else:
            return request.render('mentorship.not_applicable_form', {})

    @http.route('/register-mkl/application/submit', type='http', auth='user', method='POST', csrf=True, website=True)
    def register_application_submit(self, *args, **kwargs):
        registration_bool =  True
        mkl_beneficiary_count = request.env['mkl.beneficiary'].search_count([('beneficiary_id','=',int(kwargs.get('beneficiary_id')))])
        if mkl_beneficiary_count > 0 :
            registration_bool = False
        else:
            application_id = request.env['mkl.beneficiary'].sudo().create({
                'title' : kwargs.get('title'),
                'branch_id' : kwargs.get('branch_id'),
                'beneficiary_id' : kwargs.get('beneficiary_id'),
                'oppo_type' : kwargs.get('oppo_type'),
                'description' : kwargs.get('description'),
                'business_name' : kwargs.get('business_name'),
                'registration_number' : kwargs.get('registration_number'),
                'contact_person' : kwargs.get('contact_person'),
                'contact_details' : kwargs.get('contact_details'),
            })
        return request.render('market_linkage.mkl_form_submitted', {'registration_bool':registration_bool})
