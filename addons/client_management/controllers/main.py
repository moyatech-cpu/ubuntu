from odoo import fields, http, tools, _
from odoo.http import request


class RegistrationFormController(http.Controller):
    """ Main controller for website -> backend mapping """

    @http.route("/register", type='http', auth="public", website=True, csrf=False)
    def registrationform(self, *args, **kwargs):
        return request.render("client_management.register_form", {})

    @http.route("/register-youth", type='http', auth="public", website=True, csrf=False)
    def registrationform_youth(self, *args, **kwargs):
        branches = request.env['res.branch'].sudo().search([])
        districts = request.env['res.district'].sudo().search([])
        municipalities = request.env['res.municipality'].sudo().search([])
        provinces = request.env['res.country.state'].sudo().search([('country_id.name', '=', 'South Africa')])
        metro_municipalities = request.env['res.metro.municipality'].sudo().search([])
        sectors = request.env['mentor.sectors'].sudo().search([])
        return request.render("client_management.register_form_youth",
                              {'branches': branches, 'districts': districts, 'municipalities': municipalities,
                               'provinces': provinces, 'metro_municipalities': metro_municipalities,
                               'sectors': sectors})

    @http.route("/register-partner", type='http', auth="public", website=True, csrf=False)
    def registrationform_partner(self, *args, **kwargs):
        branches = request.env['res.branch'].sudo().search([])
        districts = request.env['res.district'].sudo().search([])
        municipalities = request.env['res.municipality'].sudo().search([])
        provinces = request.env['res.country.state'].sudo().search([('country_id.name', '=', 'South Africa')])
        metro_municipalities = request.env['res.metro.municipality'].sudo().search([])
        return request.render("client_management.register_form_partner",
                              {'branches': branches, 'districts': districts, 'municipalities': municipalities,
                               'provinces': provinces, 'metro_municipalities': metro_municipalities})

    @http.route("/youth-enquiry-submit", type='http', auth="public", website=True, csrf=False)
    def youth_enquiry_submit(self, **kw):
        """ Route that creates backend record for enquiry """
        if request.env['youth.enquiry'].sudo().search(['|', ('id_number', '=', kw.get('id_number')),('email', '=', kw.get('email'))]):
            return request.render('client_management.duplicate_enquiry')
        else:
            request.env['youth.enquiry'].sudo().create(
                {'title': kw.get('select'), 'gender': kw.get('radio'), 'name': kw.get('name'),
                    'surname': kw.get('name1'), 'id_number': kw.get('id_number'),
                    'level_of_education': kw.get('level_of_education'), 'cell_phone_number': kw.get('cellphone'),
                    'alternative_number': kw.get('alterphone') or "", 'email': kw.get('email'),
                    'population_group': kw.get('select_population'),
                    'product_information_type': kw.get('select_info_type'),
                    'product_info_training': kw.get('product_info_training'), 'geographic_location': kw.get('geo_loc'),
                    'province': kw.get('province'), 'metro_municipality': kw.get('metro_municipality'),
                    'district': kw.get('district'), 'municipality': kw.get('municipality'),
                    'nearest_branch': kw.get('near_branch'), 'physical_address': kw.get('phy_address'),
                    'your_question': kw.get('question'), 'sector_id': kw.get('sector'), })
            return request.render("client_management.enquiry_thanks")

    @http.route("/partner-enquiry-submit", type='http', auth="public", website=True, csrf=False)
    def partner_enquiry_submit(self, **kw):
        """ Route that creates backend record for enquiry """
        if request.env['partner.enquiry'].sudo().search([('email', '=', kw.get('email'))]):
            return request.render('client_management.duplicate_enquiry')
        else:
            request.env['partner.enquiry'].sudo().create(
                {'title': kw.get('select'), 'entity_name': kw.get('entityname'),
                 'company_reg_number': kw.get('company_register_number'),
                 'name_entity_representative': kw.get('entity_representative'), 'surname': kw.get('name1'),
                 'gender': kw.get('radio'), 'cell_phone_number': kw.get('cellphone'),
                 'alternative_number': kw.get('alterphone'), 'landline': kw.get('landline'),
                 'job_title': kw.get('job_title'), 'email': kw.get('email'), 'enquire_type': kw.get('enquiry'),
                 'other_enquire_type': kw.get('other_enquire_type'), 'geographic_location': kw.get('geo_loc'),
                 'province': kw.get('province'), 'metro_municipality': kw.get('metro_municipality'),
                 'district': kw.get('district'), 'municipality': kw.get('municipality'),
                 'nearest_branch': kw.get('near_branch'), 'physical_address': kw.get('phy_address'),
                 'your_question': kw.get('question'), })
            return request.render("client_management.enquiry_thanks")

    @http.route(['/get_districts/<model("res.country.state"):state>'], type='json', auth="public", methods=['POST'],
                website=True)
    def get_districts(self, state, **kw):
        """ Ajax call to get districts """
        return dict(districts=[(dt.id, dt.name) for dt in
                               request.env['res.district'].sudo().search([('state_id', '=', state.id)])],
                    metro_municipality=[(dt.id, dt.name) for dt in request.env['res.metro.municipality'].sudo().search(
                        [('state_id', '=', state.id)])], branches=[(br.id, br.name) for br in
                                                                   request.env['res.branch'].sudo().search(
                                                                       [('state_id', '=', state.id)])], )

    @http.route(['/get_municipality/<model("res.district"):district>'], type='json', auth="public", methods=['POST'],
                website=True)
    def get_municipality(self, district, **kw):
        """ Ajax call to get municipalities """
        return dict(municipalities=[(mp.id, mp.name) for mp in
                                    request.env['res.municipality'].sudo().search([('district_id', '=', district.id)])])
