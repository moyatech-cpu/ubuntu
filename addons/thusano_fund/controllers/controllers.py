# -*- coding: utf-8 -*-
from odoo import fields, http, tools, _
from odoo.http import request
import json
import base64

class ThusanoFund(http.Controller):
    
    @http.route(['/form'], type='http', auth='user', website=True, csrf=False)
    def application_form(self, page=0, *args, **kw):
        
        applicant_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])
        partner_id = request.env['partner.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])
        
        if applicant_id:
                
             return request.render('thusano_fund.temp_thusano_form', {
                 'applicant': applicant_id,
                 })
        elif partner_id:
            
            return request.render('thusano_fund.ngo_npo_thusano_form', {
                 'partner': partner_id,
                 })
        else :
             return request.render('thusano_fund.not_applicable_form')
         
    @http.route(['/form/submit'],type='http', auth='user', website=True, csrf=False)
    def submit_form(self, **post):
        
        if post.get('empl_sector') == "government":
            return request.render("thusano_fund.government_sector_error")
            
        applicant_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])
        partner_id = request.env['partner.enquiry'].sudo().search([('user_id', '=', request.env.user.id)])
        
        
        if post.get('npo_ngo_reg_docs'):
            npo_ngo_reg_docs = post.get('npo_ngo_reg_docs').filename
            post['npo_ngo_reg_docs'] = base64.b64encode(post.get('npo_ngo_reg_docs').read())
        else:
            letter_stating_financial_need = False
            
        if post.get('npo_invoice'):
            npo_invoice = post.get('npo_invoice').filename
            post['npo_invoice'] = base64.b64encode(post.get('npo_invoice').read())
        else:
            letter_stating_financial_need = False
            
        if post.get('tax_exemption_docs'):
            tax_exemption_docs = post.get('tax_exemption_docs').filename
            post['tax_exemption_docs'] = base64.b64encode(post.get('tax_exemption_docs').read())
        else:
            letter_stating_financial_need = False
            
        if post.get('proposal_w_budget'):
            proposal_w_budget = post.get('proposal_w_budget').filename
            post['proposal_w_budget'] = base64.b64encode(post.get('proposal_w_budget').read())
        else:
            letter_stating_financial_need = False
            
        if post.get('letter_stating_financial_need'):
            letter_stating_financial_need = post.get('letter_stating_financial_need').filename
            post['letter_stating_financial_need'] = base64.b64encode(post.get('letter_stating_financial_need').read())
        else:
            letter_stating_financial_need = False
            
        if post.get('academic_record_acceptance_letter'):
            academic_record_acceptance_letter = post.get('academic_record_acceptance_letter').filename
            post['academic_record_acceptance_letter'] = base64.b64encode(post.get('academic_record_acceptance_letter').read())

        else:
            academic_record_acceptance_letter = False
        if post.get('certified_identity_document_applicant'):
            certified_identity_document_applicant = post.get('certified_identity_document_applicant').filename
            post['certified_identity_document_applicant'] = base64.b64encode(post.get('certified_identity_document_applicant').read())
        else:
            certified_identity_document_applicant = False

        if post.get('income_proof'):
            income_proof = post.get('income_proof').filename
            post['income_proof'] = base64.b64encode(post.get('income_proof').read())
        else:
            income_proof = False
        if post.get('affidavit'):
            affidavit = post.get('affidavit').filename
            post['affidavit'] = base64.b64encode(post.get('affidavit').read())

        else:
            affidavit = False
        
        if post.get('institution_invoice_quotation'):
            institution_invoice_quotation = post.get('institution_invoice_quotation').filename
            post['institution_invoice_quotation'] = base64.b64encode(
                post.get('institution_invoice_quotation').read())

        else:
            institution_invoice_quotation = False

        
        thusano_fund_application_id = request.env['thusano.fund'].create({
            'name': post.get('name'),
            'surname' : post.get('surname'),
            'gender' : post.get('gender'),
            'cell_phone_number': post.get('cellphone'),
            'alternative_number' : post.get('alterphone'),
            'partner_job_title': post.get('partner_job_title'),
            'reg_fees': post.get('reg_fees'),
            'email': post.get('email'),
            'reg_fees': post.get('reg_fees'),
            'outstanding_fees': post.get('outstanding_fees'),
            'ngo_ngo_funding': post.get('npo_ngo_number'),
            'second_parent_name' : post.get('second_parent_name'),
            'parent_id_number' : post.get('parent_id_number'),
            'short_courses_technical_training': post.get('short_courses_technical_training'),
            'other_related_funding': post.get(''),
            'gross_income': post.get('gross_income'),
            'has_sponsor': post.get('has_sponsor'),
            'employment_status': post.get('employment_status'),
            'parent_name': post.get('parent_name'),
            'parent_id_number': post.get('parent_id_number'),
            'sponsor_name': post.get('sponsor_name'),
            'self_support_statement': post.get('self_support_statement'),
            'motivation_statement': post.get('motivation_statement'),
            'empl_sector':post.get('empl_sector'),
            'user_type': post.get('user_type'),
            'postal_address': post.get('postal_address'),
            'physical_address': post.get('physical_address'),
            'id_number': post.get('id_number'),
            'npo_invoice': post.get('npo_invoice'),
            'appl_amount': post.get('appl_amount'),
            'tax_exemption_docs': post.get('tax_exemption_docs'),
            'proposal_w_budget': post.get('proposal_w_budget'),
            'npo_ngo_reg_docs': post.get('npo_ngo_reg_docs'),
            'certified_identity_document_applicant': post.get('certified_identity_document_applicant'),
            'letter_stating_financial_need': post.get('letter_stating_financial_need'),
            'academic_record_acceptance_letter': post.get('academic_record_acceptance_letter'),
            'income_proof': post.get('income_proof'),
            'affidavit': post.get('affidavit'),
            'institution_invoice_quotation': post.get('institution_invoice_quotation'),
        })
        
        if thusano_fund_application_id:
            
            if applicant_id:
                mail_template_id = request.env.ref('thusano_fund.thusano_website_submit_mail_template')
                if mail_template_id:
                    user_id = request.env['youth.enquiry'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
                    user_email = user_id.email
                    mail_template_id.with_context(user=request.env.user, c_email=user_email).send_mail(
                    thusano_fund_application_id.id, force_send=True)
            elif partner_id:
                mail_template_id = request.env.ref('thusano_fund.thusano_website_submit_mail_template')
                if mail_template_id:
                    user_id = request.env['partner.enquiry'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
                    user_email = user_id.email
                    mail_template_id.with_context(user=request.env.user, c_email=user_email).send_mail(
                    thusano_fund_application_id.id, force_send=True)
        return request.render("thusano_fund.thusano_form_submit_success")