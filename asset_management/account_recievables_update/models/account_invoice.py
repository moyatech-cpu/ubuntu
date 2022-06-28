# -*- coding: utf-8 -*-

import json
import re
import uuid
from functools import partial

from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode

from odoo import api, exceptions, fields, models, _
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

# mapping invoice type to journal type
TYPE2JOURNAL = {
    'out_invoice': 'sale',
    'in_invoice': 'purchase',
    'out_refund': 'sale',
    'in_refund': 'purchase',
}

# mapping invoice type to refund type
TYPE2REFUND = {
    'out_invoice': 'out_refund',        # Customer Invoice
    'in_invoice': 'in_refund',          # Vendor Bill
    'out_refund': 'out_invoice',        # Customer Credit Note
    'in_refund': 'in_invoice',          # Vendor Credit Note
}

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    state = fields.Selection([
            ('draft','Draft'),
            ('pending','Pending'),
            ('open', 'Open'),
            ('recon', 'Reconciled'),            
            ('post', 'Posted'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
             " * The 'Reconciled' status is set automatically when the invoice is reconciled with the client's statement. Its related journal entries are reconciled.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. .\n"
             " * The 'Cancelled' status is used when user cancel invoice.")
    
    
    @api.one
    def _get_outstanding_info_JSON(self):
        self.outstanding_credits_debits_widget = json.dumps(False)
        if self.state == 'open' or self.state == 'recon':
            domain = [('account_id', '=', self.account_id.id), ('partner_id', '=', self.env['res.partner']._find_accounting_partner(self.partner_id).id), ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0), ('amount_residual_currency', '!=', 0.0)]
            if self.type in ('out_invoice', 'in_refund'):
                domain.extend([('credit', '>', 0), ('debit', '=', 0)])
                type_payment = _('Outstanding credits')
            else:
                domain.extend([('credit', '=', 0), ('debit', '>', 0)])
                type_payment = _('Outstanding debits')
            info = {'title': '', 'outstanding': True, 'content': [], 'invoice_id': self.id}
            lines = self.env['account.move.line'].search(domain)
            currency_id = self.currency_id
            if len(lines) != 0:
                for line in lines:
                    # get the outstanding residual value in invoice currency
                    if line.currency_id and line.currency_id == self.currency_id:
                        amount_to_show = abs(line.amount_residual_currency)
                    else:
                        amount_to_show = line.company_id.currency_id.with_context(date=line.date).compute(abs(line.amount_residual), self.currency_id)
                    if float_is_zero(amount_to_show, precision_rounding=self.currency_id.rounding):
                        continue
                    info['content'].append({
                        'journal_name': line.ref or line.move_id.name,
                        'amount': amount_to_show,
                        'currency': currency_id.symbol,
                        'id': line.id,
                        'position': currency_id.position,
                        'digits': [69, self.currency_id.decimal_places],
                    })
                info['title'] = type_payment
                self.outstanding_credits_debits_widget = json.dumps(info)
                self.has_outstanding = True

    def open_payment_matching_screen(self):
        # Open reconciliation view for customers/suppliers
        action_context = {'partner_ids': [self.partner_id.id]}
        action_context.update({'mode': 'suppliers'})

        return {
            'type': 'ir.actions.client',
            'tag': 'manual_reconciliation_view',
            'context': action_context,
        }

    @api.multi
    def _get_printed_report_name(self):
        self.ensure_one()
        return  self.type == 'out_invoice' and self.state == 'draft' and _('Draft Invoice') or \
                self.type == 'out_invoice' and self.state in ('open','recon','paid') and _('Invoice - %s') % (self.number) or \
                self.type == 'out_refund' and self.state == 'draft' and _('Credit Note') or \
                self.type == 'out_refund' and _('Credit Note - %s') % (self.number) or \
                self.type == 'in_invoice' and self.state == 'draft' and _('Vendor Bill') or \
                self.type == 'in_invoice' and self.state in ('open','recon','paid') and _('Vendor Bill - %s') % (self.number) or \
                self.type == 'in_refund' and self.state == 'draft' and _('Vendor Credit Note') or \
                self.type == 'in_refund' and _('Vendor Credit Note - %s') % (self.number)

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        account_id = False
        payment_term_id = False
        fiscal_position = False
        bank_id = False
        warning = {}
        domain = {}
        company_id = self.company_id.id
        p = self.partner_id if not company_id else self.partner_id.with_context(force_company=company_id)
        type = self.type
        if p:
            rec_account = p.property_account_receivable_id
            pay_account = p.property_account_payable_id
            if not rec_account and not pay_account:
                action = self.env.ref('account.action_account_config')
                msg = _('Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
                raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))

            if type in ('out_invoice', 'out_refund'):
                account_id = rec_account.id
                payment_term_id = p.property_payment_term_id.id
            else:
                account_id = pay_account.id
                payment_term_id = p.property_supplier_payment_term_id.id

            delivery_partner_id = self.get_delivery_partner_id()
            fiscal_position = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id, delivery_id=delivery_partner_id)

            # If partner has no warning, check its company
            if p.invoice_warn == 'no-message' and p.parent_id:
                p = p.parent_id
            if p.invoice_warn != 'no-message':
                # Block if partner only has warning but parent company is blocked
                if p.invoice_warn != 'block' and p.parent_id and p.parent_id.invoice_warn == 'block':
                    p = p.parent_id
                warning = {
                    'title': _("Warning for %s") % p.name,
                    'message': p.invoice_warn_msg
                    }
                if p.invoice_warn == 'block':
                    self.partner_id = False

        self.account_id = account_id
        self.payment_term_id = payment_term_id
        self.date_due = False
        self.fiscal_position_id = fiscal_position

        if type in ('in_invoice', 'out_refund'):
            bank_ids = p.commercial_partner_id.bank_ids
            bank_id = bank_ids[0].id if bank_ids else False
            self.partner_bank_id = bank_id
            domain = {'partner_bank_id': [('id', 'in', bank_ids.ids)]}

        res = {}
        if warning:
            res['warning'] = warning
        if domain:
            res['domain'] = domain
        return res

    @api.multi
    def action_invoice_draft(self):
        #if self.filtered(lambda inv: inv.state != 'cancel'):
        #    raise UserError(_("Invoice must be cancelled in order to reset it to draft."))
        # go from canceled state to draft state
        self.write({'state': 'draft', 'date': False})
        
        # Delete former printed invoice
        try:
            report_invoice = self.env['ir.actions.report']._get_report_from_name('account.report_invoice')
        except IndexError:
            report_invoice = False
        if report_invoice and report_invoice.attachment:
            for invoice in self:
                with invoice.env.do_in_draft():
                    invoice.number, invoice.state = invoice.move_name, 'open'
                    attachment = self.env.ref('account.account_invoices').retrieve_attachment(invoice)
                if attachment:
                    attachment.unlink()
        return True
    
    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        
        #if to_open_invoices.filtered(lambda inv: inv.state != 'pending'):
        #    raise UserError(_("Invoice must be in draft state in order to validate it."))
        
        if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        to_open_invoices.invoice_validate()
        
        if self.type == 'out_refund':
            if self.move_id:
                number = str(self.move_id.name)
                self.move_id.name = number.replace("INV", "CRN")
        
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoice has been successfully moved to open status."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }
    
    @api.multi
    def action_invoice_proceed(self):
        # PR MOHAPI 14/10/2020
        self.write({'state': 'pending'})
        
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoice has been successfully moved to pending status."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }

    @api.multi
    def action_invoice_post(self):
        # PR MOHAPI 12/11/2022
        self.write({'state': 'post'})
    
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoice has been successfully posted."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }
        
    @api.multi
    def action_invoice_recon(self):
        # PR MOHAPI 12/11/2020
        self.write({'state': 'recon'})
    
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoice has been successfully reconciled."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }
    
    @api.multi
    def action_invoice_paid(self):
        # lots of duplicate calls to action_invoice_paid, so we remove those already paid
        to_pay_invoices = self.filtered(lambda inv: inv.state != 'paid')
        if to_pay_invoices.filtered(lambda inv: inv.state != 'recon'):
            raise UserError(_('Invoice must be reconciled in order to set it to register payment.'))
        if to_pay_invoices.filtered(lambda inv: not inv.reconciled):
            raise UserError(_('You cannot pay an invoice which is partially paid. You need to reconcile payment entries first.'))
        return to_pay_invoices.write({'state': 'paid'})

    @api.multi
    def action_invoice_re_open(self):
        if self.filtered(lambda inv: inv.state != 'paid'):
            raise UserError(_('Invoice must be paid in order to set it to register payment.'))
        self.write({'state': 'open'})
        
        view = self.env.ref('sh_message.sh_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        context['message'] = "  Invoice has been successfully moved to open status."
        return{
                'name':'Success',
                'type':'ir.actions.act_window',
                'view_type':'form',
                'view_mode':'form',
                'res_model':'sh.message.wizard',
                'views':[(view.id, 'form')],
                'view_id':view.id,
                'target':'new',
                'context':context,
        }    











































