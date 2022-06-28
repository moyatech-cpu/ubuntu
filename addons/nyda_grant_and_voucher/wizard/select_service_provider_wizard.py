from odoo import fields, models, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SelectServiceProviderWizard(models.TransientModel):
    _name = 'select.service.provider.wizard'
    _description = 'Opens wizard for applicant to select service provider'

    service_provider = fields.Many2one('partner.enquiry', string="Service Provider")
    company_reg_number = fields.Char('Company Register Number', related='service_provider.company_reg_number')
    job_title = fields.Char('Job Title', related='service_provider.job_title')
    cell_phone_number = fields.Char('Cell Phone Number', related='service_provider.cell_phone_number')
    email = fields.Char('Email', related='service_provider.email')
    nearest_branch = fields.Many2one('res.branch', string="Nearest Branch", related='service_provider.nearest_branch')
    #undefined fields
    x_service_provider = fields.Many2one('res.partner', string="Service Provider",domain=[('x_voucher_vendor', '=', True)])
    x_street_address = fields.Char("Street Address",related='x_service_provider.street')
    x_city = fields.Char("City", related='x_service_provider.city')
    x_phone = fields.Char("Phone", related='x_service_provider.phone')
    x_country_id = fields.Many2one('res.country', string="Country", related='x_service_provider.country_id')
    x_company_email = fields.Char("Email", related='x_service_provider.email')
    x_company_website = fields.Char("Company Website", related='x_service_provider.website',help="Website of Partner or Company")
    x_service_rating = fields.Selection([('0', 'None'),('1', 'Poor'),('2', 'Fair'),('3', 'Average'),('4', 'Good'),('5', 'Excellent')],"Service Rating", related='x_service_provider.service_rating',readonly=True)
    x_zip = fields.Char("Postal Code", relate='x_service_provider.zip')

    @api.multi
    def confirm_service_provider(self):
        if self.x_service_provider_1:
            active_id = self._context.get('active_id')
            voucher_id = self.env['voucher.application'].browse([active_id])

            voucher_isurance_obj = self.env['voucher.isurance']
            today = datetime.now()
            next_month = today + relativedelta(months=+1)

            print({
                'start_date': datetime.today() or False,
                'end_date': (datetime.today() + relativedelta(months=3)) or False,
                'applicant_name': voucher_id.name or False,
                'applicant_email': voucher_id.email or False,
                'gender': voucher_id.gender or False,
                'mobile': voucher_id.mobile or False,
                'status': 'active' or False,
                'service_provider': self.x_service_provider_1.id or False,
                'voucher_applicant_id': voucher_id.id or False
            })

            jeck = voucher_isurance_obj.create({
                                        'start_date': datetime.today() or False,
                                        'end_date': (datetime.today() + relativedelta(months=3)) or False,
                                        'applicant_name': voucher_id.name or False,
                                        'applicant_email': voucher_id.email or False,
                                        'gender': voucher_id.gender or False,
                                        'mobile': voucher_id.mobile or False,
                                        'status': 'active' or False,
                                        'x_service_provider': self.x_service_provider_1.id or False,
                                        'voucher_applicant_id': voucher_id.id or False
                                        })

            voucher_id.status = 'voucher_isurance'
            if voucher_id.status == 'voucher_isurance':
                voucher_id.x_service_provider	= self.x_service_provider_1.id
                voucher_id.x_voucher_issued		= jeck.id
        else:
            print("Select Provider FIRST")

# ------------------ONLY DISPLAY NAMES OF SERVICE PROVIDERS(SELECTION FIELD) FROM PARTNER.INQUIRY

    @api.onchange('service_provider')
    def onchange_service_provider(self):
        active_id = self._context.get('active_id')
        voucher_application_ids = self.env['voucher.application'].browse([active_id])
        print('----------voucher_application_ids->', voucher_application_ids)
        for app in voucher_application_ids:
            partner_model_records = self.env['partner.enquiry'].sudo().search([('enquire_type', '=', 'become-service-provider'),('state', '=', 'accepted'),
                                                                           (['partner_service_ids', 'in', app.business_development_assistance_ids.ids])])
            print('------->>>>>',partner_model_records)
            partner_model_records_ids = partner_model_records.ids

        return {'domain': {'service_provider': [('id', 'in', partner_model_records_ids)]}}

    @api.onchange('x_service_provider_1')
    def onchange_service_provider(self):
        active_id = self._context.get('active_id')
        voucher_application_ids = self.env['voucher.application'].browse([active_id])

        print('----------voucher_application_ids->', voucher_application_ids)
        for app in voucher_application_ids:
            partner_model_records = self.env['res.partner'].sudo().search([ (['x_services', 'in', app.x_recommended_service.ids]), (['state_id', '=', app.province_id.id]) ])
            print('------->>>>>',partner_model_records)
            partner_model_records_ids = partner_model_records.ids

        return {'domain': {'x_service_provider_1': [('id', 'in', partner_model_records_ids)]}}